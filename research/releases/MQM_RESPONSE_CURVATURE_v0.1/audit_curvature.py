import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import itertools,json,math
import numpy as np
from fractions import Fraction as F
from scipy.linalg import eigh
P=Path(__file__).resolve().parent;ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
rng=np.random.default_rng(1711);rows=[]
for M in [4,8]:
 _,H1,n=ns['models'](M);freq=H1.diagonal()[4:];c=H1[3,4:];charges=[1,1,1,1,0,2,2,2];bs=[]
 for a,q in enumerate(charges):
  for modes in itertools.combinations_with_replacement(range(M),2-q):bs.append((a,tuple(modes.count(j) for j in range(M))))
 lut={v:i for i,v in enumerate(bs)};H=np.zeros((len(bs),len(bs)));B=np.zeros_like(H)
 for j,(a,f) in enumerate(bs):
  H[j,j]=B[j,j]=np.dot(freq,f)
  for u,v,z in [(0,1,1),(1,2,1),(2,3,math.sqrt(4*math.sqrt(2))),(5,6,1),(6,7,1)]:
   if a==u and (v,f) in lut:k=lut[(v,f)];H[j,k]=H[k,j]=z
  for hi,lo in [(3,4),(5,0),(6,1),(7,2)]:
   if a==hi:
    for site in range(M):
     ff=list(f);ff[site]+=1
     if (lo,tuple(ff)) in lut:k=lut[(lo,tuple(ff))];H[j,k]=H[k,j]=c[site]*math.sqrt(1+f[site])
 def trace(X):
  out=np.zeros((8,8),complex)
  for j,(a,f) in enumerate(bs):
   for k,(b,g) in enumerate(bs):
    if f==g:out[a,b]+=X[j,k]
  return out
 comm=lambda A,X:A@X-X@A
 K=H-B;C=comm(K,B);assert np.linalg.norm(K,2)<14;assert np.linalg.norm(C,2)<256/3
 discrepancies=[]
 for sample in range(3):
  v=rng.normal(size=len(bs))+1j*rng.normal(size=len(bs));v/=np.linalg.norm(v);X=np.outer(v,v.conj())
  full=trace(comm(H,comm(H,X)));reduced=trace(comm(K,comm(K,X))+comm(C,X));err=float(np.linalg.norm(full-reduced));assert err<2**-32;discrepancies.append(err)
 # Actual thermal response: dense double commutator versus propagated dyad curvature.
 rho0=np.zeros_like(H)
 for site in range(M):f=tuple(int(k==site) for k in range(M));rho0[lut[(0,f)],lut[(0,f)]]=n[site]
 E,V=eigh(H);U=(V*np.exp(-16j*E))@V.T;rho=U@rho0@U.conj().T
 full=-trace(comm(H,comm(H,rho)));hv=H@U;hhv=H@hv
 vector=trace(2*hv@rho0@hv.conj().T-hhv@rho0@U.conj().T-U@rho0@hhv.conj().T)
 err=float(np.linalg.norm(full-vector));assert err<2**-32
 rows.append({'M':M,'occupation_dimension':len(bs),'mixed_commutator_norm':float(np.linalg.norm(C,2)),'local_generator_norm':float(np.linalg.norm(K,2)),'Jacobi_discrepancies':discrepancies,'thermal_curvature_route_discrepancy':err,'quadrature_second_moment_discrepancy':float(abs(np.dot(c*c,freq*freq)-128/math.pi*256/3))})
cert=json.loads((P/'results/TRANSPORT_CERTIFICATE.json').read_text());checks=[]
for r in cert['rows']:
 x=F(r['total']);passed=x.numerator*65536<x.denominator;assert passed==r['pass'];checks.append({'k':r['k'],'pass':passed})
assert next(r for r in checks if r['pass'])['k']==6
x=F(next(r['total'] for r in cert['rows'] if r['k']==6));assert x.numerator*2**23<119*x.denominator
out={'status':'SIMULATED separate curvature routes / EXACT integer decisions','rows':rows,'integer_decisions':checks,'external_independent_review':False,'physical_promotion':0};(P/'results/CURVATURE_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
