import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import json,math
import numpy as np
from numpy.polynomial.legendre import leggauss,legvander
P=Path(__file__).resolve().parent
protocol={'status':'Frozen before supplementary diagnostic evaluation','feature_modes':[8,16],'feature_orders':[0,1,2],'feature_times':['0','1/4','1/2'],'embedding_horizon':'1/2','numeric_reference_modes':192,'covariance_modes':[16,32],'covariance_orders':[0,1,2,3],'covariance_times':['0','1/4','1/2'],'floating_tolerance':'2^-30; diagnostic only','noncommuting_ODE_cases':4,'seed':521,'interpretation':'Small-reference implementation controls; not independent continuum or device validation'}
(P/'CONTROL_PROTOCOL.json').write_text(json.dumps(protocol,indent=2)+'\n')
def tail(n,x):return x**n/math.factorial(n)/(1-x/(n+1))
B=16.;G=math.sqrt(128/math.pi);x,w=leggauss(192);refdelta=B*x;refroot=np.sqrt(w/2);features=[]
for M in [8,16]:
 y,v=leggauss(M);delta=B*y;root=np.sqrt(v/2);Q=legvander(y,M-1)*np.sqrt(2*np.arange(M)+1);E=root[:,None]*Q
 Eref=refroot[:,None]*legvander(x,M-1)*np.sqrt(2*np.arange(M)+1)
 Wc=np.exp(-.25j*refdelta)[:,None]*(Eref@E.T)*np.exp(.25j*delta)[None,:]
 for t in [0,.25,.5]:
  for r in [0,1,2]:
   native=(-1j*refdelta)**r*np.exp(-1j*refdelta*t)*G*refroot;finite=(-1j*delta)**r*np.exp(-1j*delta*t)*G*root
   err=float(np.linalg.norm(native-Wc@finite));bound=4*7*B**r*tail(M-r,2)
   assert err<bound+2**-30
   features.append({'M':M,'r':r,'t':t,'discrepancy':err,'ideal_feature_majorant_diagnostic':bound})
V=64/31457265;r0=2**-21;cov=[];nref=1/np.expm1((5/16)*(64+refdelta));G2=128/3
for M in [16,32]:
 y,v=leggauss(M);delta=B*y;n=1/np.expm1((5/16)*(64+delta))
 for t in [0,.25,.5]:
  for r in range(4):
   a=(128/math.pi)*np.sum((w/2)*nref*(-1j*refdelta)**r*np.exp(-1j*refdelta*t));b=(128/math.pi)*np.sum((v/2)*n*(-1j*delta)**r*np.exp(-1j*delta*t))
   eta=B**r*(4*G2*r0/(1-r0)*tail(2*M-r,21)+2*G2*r0**9/(1-r0));err=float(abs(a-b));assert err<eta+2**-30
   cov.append({'M':M,'r':r,'t':t,'discrepancy':err,'ideal_covariance_majorant_diagnostic':eta})
# Exact rational ODE coefficients independently reconstruct noncommuting propagator derivatives.
rng=np.random.default_rng(521);identities=[]
def skew():
 A=np.array([[F(int(v),8) for v in row] for row in rng.integers(-4,5,size=(3,3))],dtype=object)
 return A-A.T
for case in range(4):
 B0=skew();B1=skew();B2=skew();I=np.eye(3,dtype=int).astype(object);coeff=[I]
 for n in range(3):
  z=np.zeros((3,3),dtype=object)
  for k,C in enumerate([B0,B1,B2/2]):
   if k<=n:z+=C@coeff[n-k]
  coeff.append(z/F(n+1))
 expected=[B0,B1+B0@B0,B2+2*B1@B0+B0@B1+B0@B0@B0]
 for j in range(1,4):assert np.array_equal(factorial(j)*coeff[j],expected[j-1])
 identities.append({'case':case,'exact_derivative_orders':[1,2,3],'noncommuting':bool(np.any(B0@B1!=B1@B0))})
out={'status':'SIMULATED feature/covariance controls and EXACT rational ODE identities','feature_checks':len(features),'feature_rows':features,'covariance_checks':len(cov),'covariance_rows':cov,'exact_ODE_checks':12,'exact_ODE_rows':identities,'numeric_reference_not_continuum_certificate':True,'physical_promotion':0,'external_review':'OPEN'}
(P/'results/FEATURE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print({'feature_checks':len(features),'covariance_checks':len(cov),'exact_ODE_checks':12,'max_feature_discrepancy':max(x['discrepancy'] for x in features),'max_covariance_discrepancy':max(x['discrepancy'] for x in cov)})
