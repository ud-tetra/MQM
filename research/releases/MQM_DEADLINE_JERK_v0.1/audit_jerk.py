import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import itertools,json,math
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.linalg import expm_multiply
P=Path(__file__).resolve().parent;model=P/'inputs/response_model.py';ns={'__file__':str(model)};exec(model.read_text(),ns)
rows=[];rng=np.random.default_rng(419)
for M in [4,8]:
 H,H1,n=ns['models'](M);freq=H1.diagonal()[4:];c=H1[3,4:];charge=[1,1,1,1,0,2,2,2];bs=[]
 for a,q in enumerate(charge):
  for modes in itertools.combinations_with_replacement(range(M),2-q):bs.append((a,tuple(modes.count(j) for j in range(M))))
 lut={v:i for i,v in enumerate(bs)};K=np.zeros((len(bs),len(bs)));Hb=np.zeros_like(K);Hs=np.zeros_like(K)
 for j,(a,f) in enumerate(bs):
  K[j,j]=Hb[j,j]=np.dot(freq,f)
  for u,v,z in [(0,1,1),(1,2,1),(2,3,math.sqrt(4*math.sqrt(2))),(5,6,1),(6,7,1)]:
   if a==u and (v,f) in lut:
    k=lut[(v,f)];K[j,k]=K[k,j]=Hs[j,k]=Hs[k,j]=z
  for hi,lo in [(3,4),(5,0),(6,1),(7,2)]:
   if a==hi:
    for site in range(M):
     ff=list(f);ff[site]+=1
     if (lo,tuple(ff)) in lut:
      k=lut[(lo,tuple(ff))];K[j,k]=K[k,j]=c[site]*math.sqrt(1+f[site])
 def trace(X):
  R=np.zeros((8,8),complex)
  for j,(a,f) in enumerate(bs):
   for k,(b,g) in enumerate(bs):
    if f==g:R[a,b]+=X[j,k]
  return R
 local=K-Hb;C=local@Hb-Hb@local;D=C@Hb-Hb@C;E3=D@Hb-Hb@D
 comm=lambda A,X:A@X-X@A
 third_errors=[]
 for sample in range(3):
  v=rng.normal(size=len(bs))+1j*rng.normal(size=len(bs));v/=np.linalg.norm(v);rho=np.outer(v,v.conj())
  full=trace(comm(K,comm(K,comm(K,comm(K,rho)))))
  reduced=trace(comm(local,comm(local,comm(local,comm(local,rho))))+3*comm(C,comm(local,comm(local,rho)))+2*comm(local,comm(C,comm(local,rho)))+comm(local,comm(local,comm(C,rho)))+3*comm(D,comm(local,rho))+comm(local,comm(D,rho))+3*comm(C,comm(C,rho))+comm(E3,rho))
  error=float(np.linalg.norm(full-reduced));assert error<2**-22;third_errors.append(error)
 vals,E=eigh(K);U=(E*np.exp(-16j*vals))@E.T;rho0=np.zeros_like(K)
 for j in range(M):f=tuple(int(k==j) for k in range(M));rho0[lut[(0,f)],lut[(0,f)]]=n[j]
 rho=U@rho0@U.conj().T;curvature=1j*trace(comm(K,comm(K,comm(K,rho))))
 H2=K@K
 H3=K@H2;vectors=1j*trace(H3@rho-3*H2@rho@K+3*K@rho@H2-rho@H3)
 err=float(np.linalg.norm(curvature-vectors));assert err<2**-32
 seed=np.zeros(M+4);seed[0]=1;psi=expm_multiply(-16j*H1,seed)
 s1=expm_multiply(-16j*H1,H1@seed);s2=expm_multiply(-16j*H1,(H1@H1)@seed)
 qp=2*np.vdot(psi[:4],-1j*s1[:4]).real
 qpp=2*np.vdot(s1[:4],s1[:4]).real-2*np.vdot(psi[:4],s2[:4]).real
 Pnative=np.diag(np.r_[np.ones(4),np.zeros(M)])
 double=H1@(H1@Pnative-Pnative@H1)-(H1@Pnative-Pnative@H1)@H1
 qpp_comm=-np.vdot(psi,double@psi).real;assert abs(qpp-qpp_comm)<2**-32
 exch=K-Hb-Hs;G=float(np.linalg.norm(c));en=float(np.max(abs(np.linalg.eigvalsh(exch))));assert en<=math.sqrt(2)*G+1e-12
 assert np.linalg.norm(E3,2)<16384
 rows.append({'M':M,'three_mixed_norm':float(np.linalg.norm(E3,2)),'fourth_commutator_discrepancies':third_errors,'third_dyad_discrepancy':err,'cold_deadline_curvature':float(qpp),'cold_commutator_discrepancy':float(abs(qpp-qpp_comm)),'local_norm':float(np.linalg.norm(local,2)),'mixed_norm':float(np.linalg.norm(C,2)),'twice_mixed_norm':float(np.linalg.norm(D,2))})
# Separate exact word recurrence: R_(n+1)=R_n A+[R_n,B].
from collections import defaultdict
R={('A',):1};derivative={'A':'C','C':'D','D':'E'}
for order in range(2,5):
 T=defaultdict(int)
 for word,coefficient in R.items():
  T[word+('A',)]+=coefficient
  for j,label in enumerate(word):T[word[:j]+(derivative[label],)+word[j+1:]]+=coefficient
 R=dict(T)
assert R=={('A','A','A','A'):1,('C','A','A'):3,('A','C','A'):2,('A','A','C'):1,('D','A'):3,('A','D'):1,('C','C'):3,('E',):1}
from fractions import Fraction as F
cert=json.loads((P/'results/JERK_CERTIFICATE.json').read_text());checks=[]
for row in cert['rows']:
 x=F(row['total']);passed=x.numerator*65536<x.denominator;assert passed==row['pass'];checks.append({'k':row['k'],'pass':passed})
assert next(v for v in checks if v['pass'])['k']==5
x=F(next(v['total'] for v in cert['rows'] if v['k']==5));assert x.numerator*2**23<111*x.denominator
out={'status':'SIMULATED same-agent separate routes / EXACT word recurrence and integer audit','rows':rows,'retained_fourth_words':{' '.join(k):v for k,v in R.items()},'integer_decisions':checks,'thermal_continuum_derivative_transfer':'OPEN','external_review':'OPEN','physical_promotion':0}
(P/'results/JERK_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
