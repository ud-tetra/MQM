#!/usr/bin/env python3
import json
from fractions import Fraction

def eval_probs(p6,p12):
    z6=(1-p6)**6
    u6=4*p6**3*(1-p6)**3 + 3*p6**4*(1-p6)**2
    d6=1-z6-u6
    z12=(1-p12)**12
    u12=6*p12**4*(1-p12)**8 + 16*p12**6*(1-p12)**6 + 9*p12**8*(1-p12)**4
    d12=1-z12-u12
    safe=z6*z12
    unsafe=(z6+u6)*(z12+u12)-safe
    hold=1-(z6+u6)*(z12+u12)
    return z6,u6,d6,z12,u12,d12,safe,unsafe,hold

p=Fraction(1,100)
vals=eval_probs(p,p)
names=["Z6","U6","D6","Z12","U12","D12","P_receipt_safe","P_receipt_unsafe_pass","P_receipt_hold"]
stress={k:{"exact":f"{v.numerator}/{v.denominator}","value":float(v)} for k,v in zip(names,vals)}

# Leading orders.
out={
 "version":"0.1",
 "status":"EXACT_D5_S4_RETRY_RECEIPT_GATE",
 "physical_promotion":0,
 "codes":{
   "K4":{"parameters":"[6,3,3]","nonzero_weight_spectrum":{"3":4,"4":3}},
   "S4":{"parameters":"[12,5,4]","nonzero_weight_spectrum":{"4":6,"6":16,"8":9}}
 },
 "exact":{
   "Z6":"(1-p6)^6",
   "U6":"4*p6^3*(1-p6)^3 + 3*p6^4*(1-p6)^2",
   "D6":"1-Z6-U6",
   "Z12":"(1-p12)^12",
   "U12":"6*p12^4*(1-p12)^8 + 16*p12^6*(1-p12)^6 + 9*p12^8*(1-p12)^4",
   "D12":"1-Z12-U12",
   "P_receipt_safe":"Z6*Z12",
   "P_receipt_unsafe_pass":"(Z6+U6)*(Z12+U12)-Z6*Z12",
   "P_receipt_hold":"1-(Z6+U6)*(Z12+U12)"
 },
 "leading_order":{
   "U6":"4*p6^3 + O(p6^4)",
   "U12":"6*p12^4 + O(p12^5)",
   "combined_unsafe":"4*p6^3 + 6*p12^4 + higher/cross terms"
 },
 "one_percent_iid_receipt_stress":stress,
 "retry_state_machine":[
   "RESTORED_HOLD",
   "fresh K4 receipt acquisition",
   "fresh S4 comparison acquisition",
   "RETRY_READY only if both syndromes are zero",
   "otherwise HOLD_RECEIPT",
   "fresh 2+PV attempt begins only after the receipt gate"
 ],
 "claim_boundary":"receipt-bit verification only; independent-layer iid stress is not a quantum logical-error model"
}
print(json.dumps(out,indent=2,sort_keys=True))
