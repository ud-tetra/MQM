from pathlib import Path
from fractions import Fraction as F
from math import factorial
import json
P=Path(__file__).resolve().parent;U=F(129,8);B=F(16);V=F(64,31457265);r=F(1,2**21);G2=F(128,3)
def tail(n,x):
 assert x<n+1
 return x**n/factorial(n)/(1-x/(n+1))
def multiply(a,b):
 c=[F(0)]*4
 for i in range(4):
  for j in range(4-i):c[i+j]+=a[i]*b[j]
 return c
def power(a,n):
 x=[F(1),F(0),F(0),F(0)]
 for i in range(n):x=multiply(x,a)
 return x
rows=[]
for M in [192,256]:
 d=[84*B**j*tail(M-j,4*U) for j in range(3)]
 a0=F(14);a1=21*B;a2=21*B*B
 u=[F(1),a0,a0*a0+a1,a0**3+3*a0*a1+a2]
 D0=U*d[0]
 e=[D0,d[0]+a0*D0,d[1]+2*a0*d[0]+u[2]*D0,d[2]+3*a0*d[1]+3*(a1+a0*a0)*d[0]+u[3]*D0]
 # At most2 endpoint derivatives per segment and3 segments per ket.
 Ps=[2**j*u[j]/factorial(j) for j in range(4)];Es=[2**j*e[j]/factorial(j) for j in range(4)]
 Cs=[B**j/factorial(j) for j in range(4)];y=8*U+F(25,16)
 eta=[B**j*(4*G2*r/(1-r)*tail(2*M-j,y)+2*G2*r**9/(1-r)) for j in range(4)]
 Eta=[eta[j]/factorial(j) for j in range(4)]
 vac=multiply(multiply(Cs,Es),power(Ps,5));cov=multiply(Eta,power(Ps,6))
 eps=[4*factorial(j)*(6*V*vac[j]+cov[j]) for j in range(4)]
 debit=6*eps[1]+7*U*eps[2]+U*U/2*eps[3]
 # Named7 slots are bounded by total derivative order.
 slots={name:str(eps[order]) for name,order in [('t',1),('s',1),('u',1),('tt',2),('ts',2),('ss',2),('ttt',3)]}
 rows.append({'M':M,'scope':'Ideal source reference; not directed finite propagation at256','feature_generator_errors':[str(x) for x in d],'propagator_derivative_errors':[str(x) for x in e],'covariance_derivative_errors':[str(x) for x in eta],'kernel_half_trace_by_order':[str(x) for x in eps],'seven_slots':slots,'uniform_third_transfer_upper':str(debit),'auxiliary_target':'2^-12 model-time^-3','auxiliary_pass':debit<F(1,2**12),'decimal_diagnostic':float(debit)})
assert rows[0]['auxiliary_pass'] is False and rows[1]['auxiliary_pass'] is True
out={'status':'DERIVED conditional seven-slot continuum derivative comparison; exact rational budgets','horizon':'129/8','eight_source_dyads':True,'native_insertions_norm':1,'propagator_segments_per_ket_max':3,'endpoint_derivative_factor_per_order':'2^r','formula':'epsilon_r=4r![z^r](6V C(z)E(z)P(z)^5+Eta(z)P(z)^6);delta3<=6epsilon1+7Uepsilon2+U^2epsilon3/2','current192_tight_derivative_certificate':'OPEN: conservative comparison exceeds frozen auxiliary budget','prospective256_derivative_comparison':'Conditional pass; finite256 response/parameter/propagation certificate OPEN','physical_promotion':0,'external_review':'OPEN','rows':rows}
(P/'results/CONTINUUM_JET_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print([{k:x[k] for k in ['M','auxiliary_pass','decimal_diagnostic']} for x in rows])
