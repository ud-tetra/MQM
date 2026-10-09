#!/usr/bin/env python3
import json
from fractions import Fraction
import sympy as sp

lA,lS,m,mu,rho,nu,A,H,Q=sp.symbols('ell_A ell_S m mu rho nu A H Q')
Pclean=(1-lA)**4
Punsafe=(1-lA*(1-m))**4-(1-lA)**4
Pdet=1-(1-lA*(1-m))**4
Prep=4*lA*(1-m)*(1-lA)**3*(1-lS)*(1-mu)*(1-rho)*(1-nu)

# Composition under A+H+Q=1.
Safe=A*Pclean
Unsafe=A*Punsafe
Hold=H+A*Pdet
Quar=Q
Restored=(A+H)*Prep
assert sp.expand(Safe+Unsafe+Hold+Quar).subs(Q,1-A-H)==1

# First-order in active loss only.
u1=sp.series(Punsafe,lA,0,2).removeO()
d1=sp.series(Pdet,lA,0,2).removeO()
c1=sp.series(Pclean,lA,0,2).removeO()

# NDSSR-only optimistic partial channel stress, controller ideal A=1,H=Q=0.
subs={lA:sp.Rational(1,100),lS:sp.Rational(1,100),m:0,mu:0,rho:0,nu:0,A:1,H:0,Q:0}
stress={
 "SAFE_ACCEPT":sp.N(Safe.subs(subs),16),
 "UNSAFE_ACCEPT_POSSIBLE":sp.N(Unsafe.subs(subs),16),
 "HOLD":sp.N(Hold.subs(subs),16),
 "QUARANTINE":sp.N(Quar.subs(subs),16),
 "RESTORED_HOLD_SUBSET":sp.N(Restored.subs(subs),16)
}

out={
 "version":"0.1",
 "status":"EXACT_2PV_D5_CHANNEL_STATE_COMPOSITION",
 "physical_promotion":0,
 "channel_probabilities":{
   "P_clean_active":str(sp.factor(Pclean)),
   "P_unsafe_no_detected":str(sp.factor(Punsafe)),
   "P_detected_any":str(sp.factor(Pdet)),
   "P_repaired_single":str(sp.factor(Prep))
 },
 "first_order_active_loss":{
   "P_clean_active":str(c1),
   "P_unsafe_no_detected":str(u1),
   "P_detected_any":str(d1)
 },
 "combined":{
   "SAFE_ACCEPT":"A*(1-ell_A)^4",
   "UNSAFE_ACCEPT_POSSIBLE":"A*((1-ell_A*(1-m))^4-(1-ell_A)^4)",
   "HOLD":"H + A*(1-(1-ell_A*(1-m))^4)",
   "QUARANTINE":"Q",
   "RESTORED_HOLD_SUBSET":"(A+H)*4*ell_A*(1-m)*(1-ell_A)^3*(1-ell_S)*(1-mu)*(1-rho)*(1-nu)"
 },
 "state_transition_notes":{
   "spare_only_loss":"current safe ACCEPT remains allowed when all four active channel ancillas survive; mark next state DEGRADED_NO_SPARE",
   "successful_single_replacement":"current attempt is HOLD; fresh retry begins from restored four-active configuration",
   "missed_active_loss":"can produce UNSAFE_ACCEPT_POSSIBLE only when no detected active loss triggers HOLD and the frozen 2+PV controller would otherwise ACCEPT",
   "data_loss":"frozen 2+PV QUARANTINE remains dominant"
 },
 "NDSSR_only_optimistic_stress":{
   "assumptions":"A=1,H=Q=0; ell_A=ell_S=0.01; m=mu=rho=nu=0",
   **{k:float(v) for k,v in stress.items()}
 },
 "scope":"symbolic state-machine composition; channel independence from the frozen 2+PV controller is an explicit benchmark assumption"
}
print(json.dumps(out,indent=2,sort_keys=True))
