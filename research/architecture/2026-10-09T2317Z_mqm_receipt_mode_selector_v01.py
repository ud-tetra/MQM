#!/usr/bin/env python3
import json
from fractions import Fraction

def F(s):
    if isinstance(s,Fraction): return s
    a,b=s.split("/")
    return Fraction(int(a),int(b))

def probs(p6,p12,mode):
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

admissible={
 "K4":["K4_ONLY","K4_PLUS_S4"],
 "S4":["S4_ONLY","K4_PLUS_S4"],
 "BOTH":["K4_PLUS_S4"],
 "GENERIC":["K4_ONLY","S4_ONLY","K4_PLUS_S4"]
}

def select(p6,p12,req,target):
    rows=[]
    for mode in admissible[req]:
        safe,unsafe,hold,bits,layers=probs(p6,p12,mode)
        if unsafe<=target:
            rows.append((layers,bits,hold,-safe,mode,safe,unsafe))
    if not rows:
        return {"decision":"HOLD_CONFIG","reason":"no semantically admissible receipt mode meets frozen unsafe target"}
    rows.sort()
    _,bits,hold,_,mode,safe,unsafe=rows[0]
    return {
      "decision":mode,
      "safe":{"exact":f"{safe.numerator}/{safe.denominator}","value":float(safe)},
      "unsafe":{"exact":f"{unsafe.numerator}/{unsafe.denominator}","value":float(unsafe)},
      "hold":{"exact":f"{hold.numerator}/{hold.denominator}","value":float(hold)},
      "bits":bits,
      "layers":1 if mode!="K4_PLUS_S4" else 2
    }

tests=[
 {"name":"generic_1pct_strict","p6":"1/100","p12":"1/100","req":"GENERIC","target":"1/1000000"},
 {"name":"k4_1pct","p6":"1/100","p12":"1/100","req":"K4","target":"1/100000"},
 {"name":"generic_asym_bad_s4","p6":"1/1000","p12":"1/100","req":"GENERIC","target":"1/1000000"},
 {"name":"both_asym","p6":"1/100","p12":"1/1000","req":"BOTH","target":"1/100000"}
]
results={}
for t in tests:
    results[t["name"]]=select(F(t["p6"]),F(t["p12"]),t["req"],F(t["target"]))

assert results["generic_1pct_strict"]["decision"]=="S4_ONLY"
assert results["k4_1pct"]["decision"]=="K4_ONLY"
assert results["generic_asym_bad_s4"]["decision"]=="K4_ONLY"
assert results["both_asym"]["decision"]=="K4_PLUS_S4"

out={
 "version":"0.1",
 "status":"EXACT_RECEIPT_MODE_SELECTOR",
 "physical_promotion":0,
 "selection_rule":"semantic coverage first; then unsafe target; then minimize layers, bits, HOLD",
 "tests":results,
 "policy":{
   "K4":"never substitute S4_ONLY for the K4 receipt object",
   "S4":"never substitute K4_ONLY for the S4 receipt object",
   "BOTH":"requires K4_PLUS_S4 regardless of generic bit-model Pareto result",
   "GENERIC":"choose among all modes by the frozen unsafe/cost rule"
 },
 "claim_boundary":"selector implementation correctness under exact receipt-bit formulas only"
}
print(json.dumps(out,indent=2,sort_keys=True))
