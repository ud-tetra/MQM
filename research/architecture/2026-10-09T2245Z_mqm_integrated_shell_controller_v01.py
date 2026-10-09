#!/usr/bin/env python3
import json, math
from collections import deque

Cv=0.9570935821134408

def choose_motion(cal):
    if cal is None:
        return "SOURCE_BLOCKED"
    tv=12.2+4*cal["tau_v"]
    td=6*cal["tau_D6"]
    sv=Cv*(1-cal["ell_v"])**16
    sd=(1-cal["ell_D6"])**42
    time_pref="V128" if tv<td else "D6" if td<tv else "TIE"
    loss_pref="V128" if sv>sd else "D6" if sd>sv else "TIE"
    if time_pref==loss_pref and time_pref in ("V128","D6"):
        return time_pref
    if time_pref=="TIE" and loss_pref in ("V128","D6"):
        return loss_pref
    if loss_pref=="TIE" and time_pref in ("V128","D6"):
        return time_pref
    return "CONFIG_REVIEW"

stress={
 "D6_AUTO":{"tau_v":5.0,"tau_D6":1.0,"ell_v":0.001,"ell_D6":0.001},
 "V128_AUTO":{"tau_v":2.0,"tau_D6":4.0,"ell_v":0.005,"ell_D6":0.005},
 "CONFLICT_REVIEW":{"tau_v":2.0,"tau_D6":4.0,"ell_v":0.0001,"ell_D6":0.0001},
 "MISSING":None
}
assert choose_motion(stress["D6_AUTO"])=="D6"
assert choose_motion(stress["V128_AUTO"])=="V128"
assert choose_motion(stress["CONFLICT_REVIEW"])=="CONFIG_REVIEW"
assert choose_motion(stress["MISSING"])=="SOURCE_BLOCKED"

receipt_modes=["K4_ONLY","S4_ONLY","K4_PLUS_S4"]

def transitions(state,mode):
    if state=="SOURCE_BLOCKED":
        return []
    if state=="CONFIG_REVIEW":
        return [("manual_choose","READY")]
    if state=="READY":
        return [("start_fresh","RUN_2PV")]
    if state=="RUN_2PV":
        return [
          ("clean_accept","ACCEPT"),
          ("controller_hold","HOLD"),
          ("controller_quarantine","QUARANTINE"),
          ("data_or_hub_loss","QUARANTINE"),
          ("two_plus_channel_loss","HOLD"),
          ("one_channel_loss_no_spare","HOLD"),
          ("one_channel_loss_spare_ok","REPAIRING"),
          ("spare_only_loss","DEGRADED_NO_SPARE")
        ]
    if state=="DEGRADED_NO_SPARE":
        return [
          ("clean_accept","ACCEPT"),
          ("controller_hold","HOLD"),
          ("data_or_hub_loss","QUARANTINE"),
          ("channel_loss","HOLD")
        ]
    if state=="REPAIRING":
        nxt="RECEIPT_K4" if mode in ("K4_ONLY","K4_PLUS_S4") else "RECEIPT_S4"
        return [("repair_fail","HOLD"),("repair_success",nxt)]
    if state=="RECEIPT_K4":
        nxt="RECEIPT_S4" if mode=="K4_PLUS_S4" else "RETRY_READY"
        return [("receipt_fail","HOLD"),("receipt_pass",nxt)]
    if state=="RECEIPT_S4":
        return [("receipt_fail","HOLD"),("receipt_pass","RETRY_READY")]
    if state=="RETRY_READY":
        return [("start_fresh_retry","RUN_2PV")]
    return []

def check_mode(mode):
    # history flags: repaired, k4pass, s4pass, fresh_generation
    start=("READY",False,False,False,0)
    Q=deque([(start,[])])
    seen={start}
    accepting_paths=[]
    reachable=set()
    violations=[]
    while Q:
        node,path=Q.popleft()
        st,rep,k4,s4,gen=node
        reachable.add(st)
        for ev,nst in transitions(st,mode):
            nrep,nk4,ns4,ng=rep,k4,s4,gen
            if st=="READY" and ev=="start_fresh":
                nrep=nk4=ns4=False; ng+=1
            if st=="RUN_2PV" and ev=="one_channel_loss_spare_ok":
                nrep=True; nk4=ns4=False
            if st=="RECEIPT_K4" and ev=="receipt_pass":
                nk4=True
            if st=="RECEIPT_S4" and ev=="receipt_pass":
                ns4=True
            if st=="RETRY_READY" and ev=="start_fresh_retry":
                # verify required receipt path before opening a fresh attempt
                if mode=="K4_ONLY" and not nk4: violations.append("retry_without_K4")
                if mode=="S4_ONLY" and not ns4: violations.append("retry_without_S4")
                if mode=="K4_PLUS_S4" and not (nk4 and ns4): violations.append("retry_without_both")
                nrep=nk4=ns4=False; ng+=1
            if nst=="ACCEPT":
                # ACCEPT only from active attempt states, never from repair/receipt/retry directly.
                if st not in ("RUN_2PV","DEGRADED_NO_SPARE"):
                    violations.append("accept_from_illegal_state")
                if rep:
                    violations.append("accept_before_fresh_retry")
                accepting_paths.append(path+[(st,ev,nst)])
            if ev=="data_or_hub_loss" and nst!="QUARANTINE":
                violations.append("data_loss_not_quarantine")
            if ev=="two_plus_channel_loss" and nst!="HOLD":
                violations.append("multi_channel_loss_not_hold")
            if st=="REPAIRING" and nst in ("ACCEPT","RETRY_READY"):
                violations.append("repair_jump")
            nxt=(nst,nrep,nk4,ns4,ng)
            if nst not in ("ACCEPT","HOLD","QUARANTINE") and nxt not in seen and ng<3:
                seen.add(nxt);Q.append((nxt,path+[(st,ev,nst)]))
    assert not violations,violations
    return {
      "reachable_states":sorted(reachable),
      "reachable_nonterminal_state_count":len(seen),
      "accepting_path_count_sampled":len(accepting_paths),
      "violations":violations,
      "invariants_pass":True
    }

results={m:check_mode(m) for m in receipt_modes}
out={
 "version":"0.1",
 "status":"EXACT_INTEGRATED_SHELL_CONTROLLER_MODEL_CHECK",
 "physical_promotion":0,
 "configuration_decisions":{k:choose_motion(v) for k,v in stress.items()},
 "spare_policy_decisions":{"homogeneous":"UNIFORM","known_heterogeneous":"ASYMMETRIC"},
 "receipt_mode_checks":results,
 "state_machine":{
   "repair_path":"RUN_2PV -> REPAIRING -> receipt gate(s) -> RETRY_READY -> fresh RUN_2PV",
   "accept_rule":"ACCEPT only from RUN_2PV or DEGRADED_NO_SPARE on a current clean attempt",
   "data_loss_rule":"QUARANTINE",
   "multi_channel_loss_rule":"HOLD",
   "missing_calibration_rule":"SOURCE_BLOCKED",
   "metric_conflict_rule":"CONFIG_REVIEW"
 },
 "latent_risk":"UNSAFE_ACCEPT_POSSIBLE from missed channel loss remains analytic, not an observable controller state",
 "claim_boundary":"finite-state implementation correctness only; not fault-tolerance or hardware validation"
}
print(json.dumps(out,indent=2,sort_keys=True))
