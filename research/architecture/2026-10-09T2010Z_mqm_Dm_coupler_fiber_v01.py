#!/usr/bin/env python3
import json, math

rows=[]
for m in range(3,9):
    R=1/math.sin(math.pi/m)
    c=math.sqrt(1+R*R)
    k=max(2,c)/min(2,c)
    rows.append({
      "m":m,
      "ring_radius":R,
      "terminal_to_slot":c,
      "terminal_asymmetry":0.0,
      "kappa":k,
      "slots":m,
      "spares_after_four_active":max(m-4,0)
    })

# Exact monotonicity: c_m strictly increases with integer m>=3 because sin(pi/m) strictly decreases.
# Therefore global integer kappa minimum is either side of c_m=2; compare m=5 and m=6.
k5=next(x["kappa"] for x in rows if x["m"]==5)
k6=next(x["kappa"] for x in rows if x["m"]==6)
assert k5<k6
# Verify broadly.
allrows=[]
for m in range(3,65):
    R=1/math.sin(math.pi/m); c=math.sqrt(1+R*R); k=max(2,c)/min(2,c)
    allrows.append((k,m))
assert min(allrows)[1]==5

# Pareto: minimize kappa, maximize slots, maximize spares.
def dom(a,b):
    no_worse=a["kappa"]<=b["kappa"] and a["slots"]>=b["slots"] and a["spares_after_four_active"]>=b["spares_after_four_active"]
    strict=a["kappa"]<b["kappa"] or a["slots"]>b["slots"] or a["spares_after_four_active"]>b["spares_after_four_active"]
    return no_worse and strict
front=[x for x in rows if not any(dom(y,x) for y in rows if y is not x)]

out={
 "version":"0.1",
 "status":"EXACT_DM_COUPLER_FIBER_BENCHMARK",
 "physical_promotion":0,
 "family":{
   "terminal_distance":2,
   "adjacent_slot_distance":2,
   "terminal_to_slot":"sqrt(1+csc(pi/m)^2)",
   "terminal_asymmetry":"0 for every slot and every m"
 },
 "rows":rows,
 "unique_global_integer_distortion_minimum":{
   "m":5,
   "kappa_exact":"2/sqrt(3+2/sqrt(5))",
   "kappa":k5,
   "relative_edge_spread_percent":100*(k5-1),
   "slots":5,
   "spares_after_four_active":1
 },
 "D6_reference":{
   "m":6,
   "kappa_exact":"sqrt(5)/2",
   "kappa":k6,
   "relative_edge_spread_percent":100*(k6-1),
   "slots":6,
   "spares_after_four_active":2
 },
 "pareto_m":[x["m"] for x in front],
 "interpretation":"D5 uniquely minimizes the multiscale edge mismatch, while larger m retain more redundant slots at increasing geometric distortion.",
 "scope":"geometric coupler/ancilla fiber only; no source-bound hardware coupling or loss advantage"
}
print(json.dumps(out,indent=2,sort_keys=True))
