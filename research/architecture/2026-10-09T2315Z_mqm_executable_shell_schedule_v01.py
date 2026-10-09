#!/usr/bin/env python3
import json
from collections import deque

ROUND={"CZ":39,"GR":40,"RZ_address_requests":346,"RESET_site_requests":14,"NDSSR_site_requests":14}

def receipt_chain(mode):
    if mode=="K4_ONLY": return ["RECEIPT_K4"]
    if mode=="S4_ONLY": return ["RECEIPT_S4"]
    return ["RECEIPT_K4","RECEIPT_S4"]

def build_schedule(motion,spares,receipt_mode):
    if motion not in ("D6","V128"): raise ValueError("motion")
    if len(spares)!=5: raise ValueError("spares")
    chain=receipt_chain(receipt_mode)
    events=[
      {"id":"cfg","family":"CONFIG","state_in":"READY","state_out":"READY","payload":{"motion_mode":motion,"receipt_mode":receipt_mode}},
      {"id":"spare","family":"SPARE_ASSIGN","state_in":"READY","state_out":"READY","payload":{"five_epoch_spare_schedule":spares}},
      {"id":"motion","family":"MOVE","state_in":"READY","state_out":"READY","payload":{"mode":motion,"duration":"SOURCE_BOUND"}},
      {"id":"a1","family":"2PV_ACQUIRE","state_in":"READY","state_out":"RUN_2PV","payload":{"round":1,"native_counts":ROUND}},
      {"id":"a2","family":"2PV_ACQUIRE","state_in":"RUN_2PV","state_out":"RUN_2PV","payload":{"round":2,"native_counts":ROUND}},
      {"id":"cmp","family":"2PV_COMPARE","state_in":"RUN_2PV","branches":{
         "equal_zero":"ACCEPT",
         "equal_nonzero":"RECOVERY",
         "mismatch":"HOLD",
         "data_or_hub_loss":"QUARANTINE",
         "one_channel_loss_spare_ok":"REPAIRING",
         "one_channel_loss_no_spare":"HOLD",
         "two_plus_channel_loss":"HOLD"
      }},
      {"id":"rec","family":"RECOVERY","state_in":"RECOVERY","state_out":"VERIFY","payload":{"decoder":"frozen ideal-center recovery"}},
      {"id":"verify","family":"2PV_VERIFY","state_in":"VERIFY","branches":{"zero":"ACCEPT","nonzero":"HOLD","loss":"QUARANTINE"},"payload":{"native_counts":ROUND}},
      {"id":"repair_move","family":"REPAIR_MOVE","state_in":"REPAIRING","branches":{"success":"RESET_PREP","failure":"HOLD"}},
      {"id":"reset","family":"RESET_PREP","state_in":"RESET_PREP","branches":{"success":chain[0],"failure":"HOLD"}}
    ]
    if receipt_mode in ("K4_ONLY","K4_PLUS_S4"):
      nxt="RECEIPT_S4" if receipt_mode=="K4_PLUS_S4" else "RETRY_READY"
      events.append({"id":"rk4","family":"RECEIPT_K4","state_in":"RECEIPT_K4","branches":{"pass":nxt,"fail":"HOLD"},"payload":{"bits":6,"code":"[6,3,3]"}})
    if receipt_mode in ("S4_ONLY","K4_PLUS_S4"):
      events.append({"id":"rs4","family":"RECEIPT_S4","state_in":"RECEIPT_S4","branches":{"pass":"RETRY_READY","fail":"HOLD"},"payload":{"bits":12,"code":"[12,5,4]"}})
    events.append({"id":"retry","family":"STATE","state_in":"RETRY_READY","state_out":"READY","payload":{"action":"increment_attempt_id_and_start_fresh_2PV"}})
    return events

def transition(state,event,receipt_mode):
    # Abstract model checker over state/event labels.
    if state=="READY":
      if event=="start": return "RUN_2PV"
      return None
    if state=="RUN_2PV":
      return {
       "equal_zero":"ACCEPT","equal_nonzero":"RECOVERY","mismatch":"HOLD",
       "data_loss":"QUARANTINE","one_loss_spare":"REPAIRING",
       "one_loss_no_spare":"HOLD","two_plus_loss":"HOLD"
      }.get(event)
    if state=="RECOVERY":
      return "VERIFY" if event=="recover" else None
    if state=="VERIFY":
      return {"zero":"ACCEPT","nonzero":"HOLD","loss":"QUARANTINE"}.get(event)
    if state=="REPAIRING":
      return "RESET_PREP" if event=="repair_success" else "HOLD" if event=="repair_fail" else None
    if state=="RESET_PREP":
      if event=="reset_fail": return "HOLD"
      if event=="reset_success":
        return "RECEIPT_K4" if receipt_mode in ("K4_ONLY","K4_PLUS_S4") else "RECEIPT_S4"
    if state=="RECEIPT_K4":
      if event=="fail": return "HOLD"
      if event=="pass": return "RECEIPT_S4" if receipt_mode=="K4_PLUS_S4" else "RETRY_READY"
    if state=="RECEIPT_S4":
      return {"pass":"RETRY_READY","fail":"HOLD"}.get(event)
    if state=="RETRY_READY":
      return "RUN_2PV" if event=="fresh_retry" else None
    return None

def model_check(mode):
    eventsets={
      "READY":["start"],
      "RUN_2PV":["equal_zero","equal_nonzero","mismatch","data_loss","one_loss_spare","one_loss_no_spare","two_plus_loss"],
      "RECOVERY":["recover"],
      "VERIFY":["zero","nonzero","loss"],
      "REPAIRING":["repair_success","repair_fail"],
      "RESET_PREP":["reset_success","reset_fail"],
      "RECEIPT_K4":["pass","fail"],
      "RECEIPT_S4":["pass","fail"],
      "RETRY_READY":["fresh_retry"]
    }
    # Track whether current attempt is fresh-after-repair and receipt-certified.
    start=("READY",False,False,False,0)
    q=deque([start]); seen={start}; violations=[]; accepts=0
    while q:
      st,repaired,k4,s4,attempt=q.popleft()
      for ev in eventsets.get(st,[]):
        ns=transition(st,ev,mode)
        if ns is None: continue
        nr,nk,ns4,na=repaired,k4,s4,attempt
        if st=="READY" and ev=="start": na+=1; nr=nk=ns4=False
        if st=="RUN_2PV" and ev=="one_loss_spare": nr=True; nk=ns4=False
        if st=="RECEIPT_K4" and ev=="pass": nk=True
        if st=="RECEIPT_S4" and ev=="pass": ns4=True
        if st=="RETRY_READY" and ev=="fresh_retry":
          if mode=="K4_ONLY" and not nk: violations.append("retry_without_K4")
          if mode=="S4_ONLY" and not ns4: violations.append("retry_without_S4")
          if mode=="K4_PLUS_S4" and not(nk and ns4): violations.append("retry_without_both")
          na+=1; nr=nk=ns4=False
        if ns=="ACCEPT":
          accepts+=1
          if st not in ("RUN_2PV","VERIFY"): violations.append("illegal_accept_origin")
          if nr: violations.append("accept_before_fresh_retry")
        if st in ("REPAIRING","RESET_PREP","RECEIPT_K4","RECEIPT_S4","RETRY_READY") and ns=="ACCEPT":
          violations.append("repair_path_jump_accept")
        node=(ns,nr,nk,ns4,na)
        if ns not in ("ACCEPT","HOLD","QUARANTINE") and na<3 and node not in seen:
          seen.add(node);q.append(node)
    assert not violations,violations
    return {"invariants_pass":True,"violations":[],"state_instances":len(seen),"accept_transitions_examined":accepts}

examples={
 "D6_UNIFORM_K4":build_schedule("D6",[0,1,2,3,4],"K4_ONLY"),
 "V128_ASYMMETRIC_S4":build_schedule("V128",[3,3,4,4,4],"S4_ONLY"),
 "V128_ASYMMETRIC_BOTH":build_schedule("V128",[3,3,4,4,4],"K4_PLUS_S4")
}
checks={m:model_check(m) for m in ("K4_ONLY","S4_ONLY","K4_PLUS_S4")}
out={
 "version":"0.1",
 "status":"EXACT_EXECUTABLE_ABSTRACT_SHELL_SCHEDULE",
 "physical_promotion":0,
 "native_round_reference_counts":ROUND,
 "examples":examples,
 "model_checks":checks,
 "machine_semantics":{
   "schedule_is":"branching executable abstract event graph",
   "unknown_durations":"MOVE and backend-native timing remain source-bound",
   "fresh_retry":"RETRY_READY increments attempt identity and executes a new two-acquisition 2+PV attempt"
 },
 "claim_boundary":"abstract executable schedule/model-check only; not a hardware-timed executable"
}
print(json.dumps(out,indent=2,sort_keys=True))
