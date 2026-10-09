#!/usr/bin/env python3
import json, math
from fractions import Fraction

phi=(1+math.sqrt(5))/2
adj=2.0
nextn=1+math.sqrt(5)
# Spare A4 relative to active A0..A3 on a 5-cycle:
# two active slots adjacent to spare, two at separation 2.
move_distances=[adj,adj,nextn,nextn]
avg=sum(move_distances)/4
assert abs(avg-(3+math.sqrt(5))/2)<1e-12

def probs(ea,es,m,mu,rho,nu):
    r=(1-m)*(1-mu)*(1-rho)*(1-nu)
    p4=(1-ea)**4+4*ea*(1-ea)**3*(1-es)*r
    unsafe=1-(1-ea*m)**4
    hold=1-p4-unsafe
    return p4,unsafe,hold,r

stress=probs(0.01,0.01,0,0,0,0)
baseline=(1-0.01)**4
assert abs(stress[0]-0.9990198504)<1e-12
assert stress[1]==0
assert abs(stress[2]-(1-stress[0]))<1e-12

# Raw channel-slot assignments: choose spare slot and biject four channel labels to remaining slots.
raw_assignments=5*math.factorial(4)

out={
 "version":"0.1",
 "status":"EXACT_D5_CUT_CHANNEL_REPLACEMENT",
 "physical_promotion":0,
 "mapping":{
   "cut_channels":[[8,4],[8,5],[8,6],[8,7]],
   "active_slots":["A0","A1","A2","A3"],
   "spare_slot":"A4",
   "raw_equivalent_label_assignments":raw_assignments
 },
 "replacement_geometry":{
   "spare_to_active_distance_classes":{"2":2,"1+sqrt(5)":2},
   "mean_distance_exact":"(3+sqrt(5))/2",
   "mean_distance":avg,
   "max_distance_exact":"1+sqrt(5)",
   "max_distance":nextn
 },
 "symbolic":{
   "r":"(1-m)(1-mu)(1-rho)(1-nu)",
   "P_four_active":"(1-ell_A)^4 + 4 ell_A (1-ell_A)^3 (1-ell_S) r",
   "P_unsafe":"1-(1-ell_A m)^4",
   "P_HOLD":"1-P_four_active-P_unsafe"
 },
 "ideal_detector_replacement":{
   "corrects":"any single active-channel ancilla loss when the spare survives the epoch",
   "detects_fail_closed":"two or more active losses, or one active loss with unavailable spare",
   "does_not_correct":"data/hub qubit loss"
 },
 "NDSSR_only_stress":{
   "ell_A":0.01,"ell_S":0.01,"m":0,"mu":0,"rho":0,"nu":0,
   "four_active_probability":stress[0],
   "unsafe_probability":stress[1],
   "hold_probability":stress[2],
   "no_spare_four_active_probability":baseline,
   "absolute_availability_gain":stress[0]-baseline,
   "relative_failure_reduction":1-(1-stress[0])/(1-baseline),
   "typed_warning":"optimistic partial-channel stress; MOVE/reset/detector errors are set ideal and the 1% loss is specifically NDSSR-associated"
 },
 "scope":"ancilla/coupler replacement layer only; not QEC distance, threshold, or hardware validation"
}
print(json.dumps(out,indent=2,sort_keys=True))
