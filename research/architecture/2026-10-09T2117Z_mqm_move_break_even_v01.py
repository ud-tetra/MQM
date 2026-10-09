#!/usr/bin/env python3
import json, math
from fractions import Fraction

A0v=Fraction(23,63)
K2v=Fraction(78,1265)
A0d=Fraction(1,3)
K2d=Fraction(413,6325)
Cv=0.9570935821134408
T2=12700.0

eta=(math.sqrt(float(A0v))-math.sqrt(float(A0d)))/(math.sqrt(float(K2d))-math.sqrt(float(K2v)))
tau_concurrent=12.2/(6-4)
tau_serial=12.2/(42-16)
ell_star=1-Cv**(1/(42-16))
tau_concurrent_diag=(12.2-T2*math.log(Cv))/(6-4)
tau_serial_diag=(12.2-T2*math.log(Cv))/(42-16)

out={
 "version":"0.1",
 "status":"DERIVED_TYPED_MOVE_BREAK_EVEN_SURFACES",
 "physical_promotion":0,
 "ideal_Magnus":{
   "v128":{"A0":"23/63","K2":"78/1265"},
   "D6":{"A0":"1/3","K2":"413/6325"},
   "eta_cross":eta,
   "ruling":"D6 has lower zeroth-order residual; v128 has lower K2. Under the frozen diagnostic D6 is lower for eta<eta_cross and v128 for eta>eta_cross."
 },
 "timing":{
   "concurrent_move_epoch":{
     "equations":["t_v=12.2+4 tau_M","t_D6=6 tau_M"],
     "break_even_tau_us":tau_concurrent,
     "ruling":"D6 is faster below 6.1 us per concurrent transport epoch; v128 is faster above it."
   },
   "serial_role_move":{
     "equations":["t_v=12.2+16 tau_r","t_D6=42 tau_r"],
     "break_even_tau_us":tau_serial,
     "ruling":"D6 is faster below this per-role move duration; v128 is faster above it."
   }
 },
 "loss":{
   "move_only":{
     "equations":["S_v=(1-ell_M)^16","S_D6=(1-ell_M)^42"],
     "ruling":"v128 has strictly higher move-only survival for every 0<ell_M<1."
   },
   "with_v128_local_control_product_diagnostic":{
     "C_v":Cv,
     "equations":["S_v=C_v(1-ell_M)^16","S_D6=(1-ell_M)^42"],
     "break_even_ell_M":ell_star,
     "break_even_percent_per_moved_role":100*ell_star,
     "ruling":"Below the break-even loss, D6 has the higher product diagnostic; above it, v128 does."
   }
 },
 "T2star_product_diagnostic":{
   "T2star_us":T2,
   "concurrent_move_break_even_tau_us":tau_concurrent_diag,
   "serial_role_break_even_tau_us":tau_serial_diag,
   "typed_warning":"includes v128 local-control exposure product and exponential T2* diagnostic; not a calibrated success probability"
 },
 "scope":"typed architecture break-even surfaces with MOVE parameters left symbolic; not hardware prediction"
}
print(json.dumps(out,indent=2,sort_keys=True))
