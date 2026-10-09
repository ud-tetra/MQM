#!/usr/bin/env python3
import json
from fractions import Fraction

def metrics(p6,p12,mode):
    z6=(1-p6)**6
    u6=4*p6**3*(1-p6)**3 + 3*p6**4*(1-p6)**2
    z12=(1-p12)**12
    u12=6*p12**4*(1-p12)**8 + 16*p12**6*(1-p12)**6 + 9*p12**8*(1-p12)**4
    if mode=="K4_ONLY":
        return z6,u6,1-z6-u6,6,1
    if mode=="S4_ONLY":
        return z12,u12,1-z12-u12,12,1
    safe=z6*z12
    unsafe=(z6+u6)*(z12+u12)-safe
    hold=1-(z6+u6)*(z12+u12)
    return safe,unsafe,hold,18,2

def dominates(a,b):
    # maximize safe; minimize unsafe,bits,layers
    no_worse=a["safe"]>=b["safe"] and a["unsafe"]<=b["unsafe"] and a["bits"]<=b["bits"] and a["layers"]<=b["layers"]
    strict=a["safe"]>b["safe"] or a["unsafe"]<b["unsafe"] or a["bits"]<b["bits"] or a["layers"]<b["layers"]
    return no_worse and strict

def clean(x):
    if isinstance(x,Fraction): return {"exact":f"{x.numerator}/{x.denominator}","value":float(x)}
    return x

modes=["K4_ONLY","S4_ONLY","K4_PLUS_S4"]
equal=[Fraction(1,10000),Fraction(1,1000),Fraction(1,100),Fraction(1,20)]
agrid=[Fraction(1,1000),Fraction(1,100)]
rows=[]
for p in equal:
    cand=[]
    for mode in modes:
        s,u,h,b,l=metrics(p,p,mode)
        cand.append({"mode":mode,"safe":s,"unsafe":u,"hold":h,"bits":b,"layers":l})
    front=[x["mode"] for x in cand if not any(dominates(y,x) for y in cand if y is not x)]
    rows.append({"family":"equal_iid","p":str(p),"pareto":front,
                 "metrics":{x["mode"]:{k:clean(v) for k,v in x.items() if k!="mode"} for x in cand}})
agrid_rows=[]
for p6 in agrid:
  for p12 in agrid:
    cand=[]
    for mode in modes:
      s,u,h,b,l=metrics(p6,p12,mode)
      cand.append({"mode":mode,"safe":s,"unsafe":u,"hold":h,"bits":b,"layers":l})
    front=[x["mode"] for x in cand if not any(dominates(y,x) for y in cand if y is not x)]
    agrid_rows.append({"p6":str(p6),"p12":str(p12),"pareto":front,
      "metrics":{x["mode"]:{k:clean(v) for k,v in x.items() if k!="mode"} for x in cand}})

# Detect any equal-iid case where combined survives Pareto.
combined_equal=[r["p"] for r in rows if "K4_PLUS_S4" in r["pareto"]]
out={
 "version":"0.1",
 "status":"EXACT_RECEIPT_DEPTH_YIELD_BENCHMARK",
 "physical_promotion":0,
 "equal_iid_results":rows,
 "asymmetric_grid_results":agrid_rows,
 "summary":{
   "combined_on_equal_iid_pareto":combined_equal,
   "semantic_warning":"K4 and S4 validate different typed receipt objects. Bit-model dominance cannot erase semantic coverage.",
   "selection_rule":"Use the shallowest gate that meets the declared receipt object and unsafe-pass target; do not add K4+S4 merely for lower depth/yield metrics."
 },
 "leading_order":{
   "K4_ONLY_unsafe":"4 p6^3 + O(p6^4)",
   "S4_ONLY_unsafe":"6 p12^4 + O(p12^5)",
   "K4_PLUS_S4_unsafe":"4 p6^3 + 6 p12^4 + higher/cross terms"
 }
}
print(json.dumps(out,indent=2,sort_keys=True))
