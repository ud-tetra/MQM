#!/usr/bin/env python3
import json
from fractions import Fraction

# Exact symbolic formulas are emitted as strings; no third-party CAS dependency.
# Frozen definitions:
# q=1-ell_A, d=ell_A(1-m), u=ell_A m
# Pclean=q^4
# Punsafe=(q+u)^4-q^4 = (1-ell_A(1-m))^4-(1-ell_A)^4
# Pdet=1-(q+u)^4
# Prep=4*d*q^3*(1-ell_S)*(1-mu)*(1-rho)*(1-nu)

l=Fraction(1,100)
q=1-l
safe=q**4
unsafe=Fraction(0,1)
hold=1-safe
restored=4*l*q**3*q
spare_only=safe*l

out={
 "version":"0.1a",
 "status":"EXACT_2PV_D5_CHANNEL_STATE_COMPOSITION",
 "physical_promotion":0,
 "channel_probabilities":{
   "P_clean_active":"(1-ell_A)^4",
   "P_unsafe_no_detected":"(1-ell_A*(1-m))^4-(1-ell_A)^4",
   "P_detected_any":"1-(1-ell_A*(1-m))^4",
   "P_repaired_single":"4*ell_A*(1-m)*(1-ell_A)^3*(1-ell_S)*(1-mu)*(1-rho)*(1-nu)"
 },
 "first_order_active_loss":{
   "P_clean_active":"1-4*ell_A+O(ell_A^2)",
   "P_unsafe_no_detected":"4*ell_A*m+O(ell_A^2)",
   "P_detected_any":"4*ell_A*(1-m)+O(ell_A^2)"
 },
 "combined":{
   "SAFE_ACCEPT":"A*(1-ell_A)^4",
   "UNSAFE_ACCEPT_POSSIBLE":"A*((1-ell_A*(1-m))^4-(1-ell_A)^4)",
   "HOLD":"H + A*(1-(1-ell_A*(1-m))^4)",
   "QUARANTINE":"Q",
   "RESTORED_HOLD_SUBSET":"(A+H)*4*ell_A*(1-m)*(1-ell_A)^3*(1-ell_S)*(1-mu)*(1-rho)*(1-nu)"
 },
 "normalization":"SAFE_ACCEPT+UNSAFE_ACCEPT_POSSIBLE+HOLD+QUARANTINE=1 when A+H+Q=1",
 "state_transition_notes":{
   "spare_only_loss":"current safe ACCEPT remains allowed when all four active channel ancillas survive; mark next state DEGRADED_NO_SPARE",
   "successful_single_replacement":"current attempt is HOLD; fresh retry begins from restored four-active configuration",
   "missed_active_loss":"can produce UNSAFE_ACCEPT_POSSIBLE only when no detected active loss triggers HOLD and the frozen 2+PV controller would otherwise ACCEPT",
   "data_loss":"frozen 2+PV QUARANTINE remains dominant"
 },
 "NDSSR_only_optimistic_stress":{
   "assumptions":"A=1,H=Q=0; ell_A=ell_S=0.01; m=mu=rho=nu=0",
   "SAFE_ACCEPT":float(safe),
   "UNSAFE_ACCEPT_POSSIBLE":float(unsafe),
   "HOLD":float(hold),
   "QUARANTINE":0.0,
   "RESTORED_HOLD_SUBSET":float(restored),
   "SAFE_ACCEPT_DEGRADED_NO_SPARE":float(spare_only)
 },
 "scope":"symbolic state-machine composition; channel independence from the frozen 2+PV controller is an explicit benchmark assumption"
}
print(json.dumps(out,indent=2,sort_keys=True))
