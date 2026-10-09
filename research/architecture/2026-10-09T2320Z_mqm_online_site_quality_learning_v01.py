#!/usr/bin/env python3
import itertools,json,math

alpha=0.05
K=15
T=5
nmin=100
base_stream=[
 {"window":0,"active_trials":[1000]*5,"active_failures":[30]*5,"spare_trials":[200]*5,"spare_failures":[1]*5,"check_trials":[1000]*5,"check_failures":[2]*5},
 {"window":1,"active_trials":[1000]*5,"active_failures":[10,20,30,45,60],"spare_trials":[200]*5,"spare_failures":[1]*5,"check_trials":[1000]*5,"check_failures":[2]*5},
 {"window":2,"active_trials":[10000]*5,"active_failures":[100,200,300,400,500],"spare_trials":[10000]*5,"spare_failures":[50]*5,"check_trials":[10000]*5,"check_failures":[20]*5}
]

counts=[]
for n0 in range(6):
  for n1 in range(6-n0):
    for n2 in range(6-n0-n1):
      for n3 in range(6-n0-n1-n2):
        counts.append((n0,n1,n2,n3,5-n0-n1-n2-n3))

def ucb(f,n):
    if n<nmin: return None
    return min(1.0,f/n+math.sqrt(math.log(2*K/alpha)/(2*n)))

def optimize(ea,es,rc):
    best=None
    for c in counts:
        vals=[(1-ea[i])**(T-c[i])*(1-es[i])**c[i]*(1-rc[i])**T for i in range(5)]
        key=(min(vals),-sum(abs(c[i]-1) for i in range(5)),tuple(-x for x in c))
        if best is None or key>best[0]:
            best=(key,c,vals)
    return best[1],best[2]

cum={k:[0]*5 for k in ["active_trials","active_failures","spare_trials","spare_failures","check_trials","check_failures"]}
rows=[]
for w in base_stream:
    for k in cum:
        cum[k]=[cum[k][i]+w[k][i] for i in range(5)]
    ea=[ucb(cum["active_failures"][i],cum["active_trials"][i]) for i in range(5)]
    es=[ucb(cum["spare_failures"][i],cum["spare_trials"][i]) for i in range(5)]
    rc=[ucb(cum["check_failures"][i],cum["check_trials"][i]) for i in range(5)]
    if any(x is None for x in ea+es+rc):
        rows.append({"window":w["window"],"policy":"SOURCE_BLOCKED"})
        continue
    c,vals=optimize(ea,es,rc)
    label="UNIFORM" if c==(1,1,1,1,1) else "ASYMMETRIC"
    rows.append({
      "window":w["window"],
      "policy":label,
      "spare_counts":list(c),
      "active_loss_ucb":ea,
      "spare_loss_ucb":es,
      "check_failure_ucb":rc,
      "worst_conservative_site_survival":min(vals),
      "site_survivals":vals
    })

# Safety thresholds remain immutable; only schedule is updated.
out={
 "version":"0.1",
 "status":"EXACT_ONLINE_SITE_QUALITY_CONTROLLER_REPLAY",
 "physical_promotion":0,
 "estimator":{"type":"Hoeffding_UCB","alpha":alpha,"family_size":K,"minimum_trials":nmin},
 "updates":rows,
 "immutable_safety_rules":[
   "ACCEPT criteria unchanged",
   "HOLD/QUARANTINE transitions unchanged",
   "receipt unsafe targets unchanged",
   "MOVE decision thresholds unchanged"
 ],
 "adapted_object":"five-epoch spare-frequency schedule only",
 "observations":{
   "early_uncertainty":"conservative spare-channel bounds can delay asymmetric allocation even when point estimates differ",
   "calibration_rich_window":"when confidence intervals tighten, schedule is allowed to shift without changing safety criteria"
 },
 "claim_boundary":"synthetic online-learning behavior only; no hardware convergence/performance claim"
}
print(json.dumps(out,indent=2,sort_keys=True))
