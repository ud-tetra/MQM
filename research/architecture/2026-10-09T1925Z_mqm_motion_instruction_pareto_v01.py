#!/usr/bin/env python3
from fractions import Fraction
import json

carriers={
 "A4":{"cells":4,"interfaces":6,"receipt_distance":3},
 "D6":{"cells":6,"interfaces":6,"receipt_distance":2},
 "S4":{"cells":24,"interfaces":12,"receipt_distance":4}
}

identity={
 "I":{"a0":Fraction(1,1),"k2":Fraction(0,1),"exposure":0,"word_length":0},
 "a":{"a0":Fraction(65,84),"k2":Fraction(127,6325),"exposure":6,"word_length":1},
 "b":{"a0":Fraction(55,126),"k2":Fraction(15616,170775),"exposure":72,"word_length":1},
 "ab":{"a0":Fraction(41,84),"k2":Fraction(933,6325),"exposure":72,"word_length":2},
 "zb":{"a0":Fraction(3,7),"k2":Fraction(31679,170775),"exposure":108,"word_length":2}
}
swap={
 "c":{"cost":12,"word_length":1,"h":1},
 "dcd":{"cost":14,"word_length":3,"h":2},
 "bc":{"cost":24,"word_length":2,"h":3},
 "bdcd":{"cost":26,"word_length":4,"h":6}
}
cycle3={
 "d":{"cost":12,"word_length":1,"h":1},
 "ad":{"cost":15,"word_length":2,"h":2},
 "abd":{"cost":21,"word_length":3,"h":4}
}

def pareto(rows, keys_min, key_max=None):
    def dom(a,b):
        le=all(a[k]<=b[k] for k in keys_min)
        lt=any(a[k]<b[k] for k in keys_min)
        if key_max:
            le=le and a[key_max]>=b[key_max]
            lt=lt or a[key_max]>b[key_max]
        return le and lt
    return [r for r in rows if not any(dom(q,r) for q in rows if q is not r)]

rows=[]
for m,x in identity.items():
  for c,y in carriers.items():
    rows.append({"motion":m,"carrier":c,
      "zeroth_residual":x["a0"],"second_order":x["k2"],
      "exposure":x["exposure"],"word_length":x["word_length"],
      "cells":y["cells"],"interfaces":y["interfaces"],"receipt_distance":y["receipt_distance"]})
ifront=pareto(rows,["zeroth_residual","second_order","exposure","word_length","cells","interfaces"],"receipt_distance")

def nonid_front(lib):
  rows=[]
  for m,x in lib.items():
    for c,y in carriers.items():
      rows.append({"motion":m,"carrier":c,"exposure":x["cost"],"word_length":x["word_length"],"h":x["h"],
        "cells":y["cells"],"interfaces":y["interfaces"],"receipt_distance":y["receipt_distance"]})
  return pareto(rows,["exposure","word_length","h","cells","interfaces"],"receipt_distance")

sfront=nonid_front(swap)
cfront=nonid_front(cycle3)

def fmt(v):
  if isinstance(v,Fraction): return f"{v.numerator}/{v.denominator}"
  return v
def clean(rows):
  return [{k:fmt(v) for k,v in r.items()} for r in rows]

# Dominance diagnostics independent of carrier.
assert all(r["motion"]!="ab" for r in ifront)
assert set(r["motion"] for r in ifront)=={"I","a","b","zb"}
assert set(r["carrier"] for r in ifront)=={"A4","S4"}
assert set(r["motion"] for r in sfront)=={"c"}
assert set(r["motion"] for r in cfront)=={"d"}
assert set(r["carrier"] for r in sfront)=={"A4","S4"}
assert set(r["carrier"] for r in cfront)=={"A4","S4"}

out={
 "version":"0.1",
 "status":"EXACT_PHASE_A_MOTION_INSTRUCTION_PARETO",
 "physical_promotion":0,
 "identity_pareto":clean(ifront),
 "logical_XZ_transposition_pareto":clean(sfront),
 "logical_3cycle_pareto":clean(cfront),
 "dominance":{
   "identity_ab":"dominated by b: b has lower zeroth residual, lower second-order metric, equal exposure, and shorter word",
   "D6_carrier":"dominated by A4 on current Pareto carrier metrics: more cells, equal interface count, lower receipt distance",
   "S4_carrier":"not dominated by A4 because receipt distance 4 trades against 24 cells and 12 interfaces",
   "nonidentity_hidden_cycles":"h>1 short-word representatives are dominated by h=1 representatives under the frozen nonidentity objectives"
 },
 "instruction_set_candidate":{
   "logical_identity_choices":["I","a","b","zb"],
   "canonical_XZ_transposition":"c",
   "canonical_logical_3cycle":"d",
   "default_low_overhead_carrier":"A4",
   "high_receipt_redundancy_carrier":"S4",
   "D6_role":"retain as cyclic addressing/transport specialist outside this Pareto objective set"
 },
 "scope":"Phase A frozen short-word candidate library only; not a global optimum over all 1152 transitions and not a hardware ranking"
}
print(json.dumps(out,indent=2,sort_keys=True))
