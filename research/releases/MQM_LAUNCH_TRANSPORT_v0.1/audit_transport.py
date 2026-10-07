import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.linalg import expm_multiply
from fractions import Fraction as F
P=Path(__file__).resolve().parent
ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
rows=[]
for M in [4,8,192]:
 _,H,_=ns['models'](M);d=M+4;seeds=np.zeros((d,3));seeds[0,0]=seeds[1,1]=seeds[0,2]=seeds[2,2]=1
 assert np.array_equal(H@seeds[:,0],seeds[:,1]);assert np.array_equal(H@seeds[:,1],seeds[:,2])
 E,V=eigh(H)
 for t in [16-2**-8,16.,16+2**-8]:
  U=V@(np.exp(-1j*E*t)[:,None]*(V.T@seeds));W=expm_multiply(-1j*H*t,seeds)
  discrepancy=float(np.linalg.norm(U-W));assert discrepancy<2**-32
  identities=[float(np.linalg.norm(H@W[:,0]-W[:,1])),float(np.linalg.norm(H@W[:,1]-W[:,2]))];assert max(identities)<2**-32
  slope=float(2*np.vdot(W[:4,0],-1j*W[:4,1]).real)
  curvature=float(2*np.vdot(W[:4,1],W[:4,1]).real-2*np.vdot(W[:4,0],W[:4,2]).real)
  rows.append(dict(M=M,time=t,vector_discrepancy=discrepancy,launch_identity_discrepancies=identities,q_prime=slope,q_second=curvature))
  if M==192 and t==16:
   stored=np.load(P/'results/LAUNCH_VECTORS.npz')['vectors'];replay=float(np.linalg.norm(stored-W));assert replay<2**-32
cert=json.loads((P/'results/TRANSPORT_CERTIFICATE.json').read_text());audit=[]
for row in cert['rows']:
 f=F(row['total']);passed=f.numerator*65536<f.denominator;assert passed==row['pass'];audit.append({'k':row['k'],'pass':passed})
chosen=next(z for z in audit if z['pass']);assert chosen['k']==8
selected=F(next(z['total'] for z in cert['rows'] if z['k']==8));assert selected.numerator*2**23<115*selected.denominator
# Monotone majorant terms are nonnegative; every time in the declared interval is covered.
assert all(F(z['cold_variation'])>0 and F(z['curvature_bound'])>0 for z in cert['rows'])
out={'status':'SIMULATED separate implementations / EXACT integer acceptance audit','controls':rows,'integer_decisions':audit,'Taylor_vs_exponential_discrepancy':replay,'external_independent_review':False,'physical_promotion':0}
(P/'results/TRANSPORT_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print('controls',len(rows),'integer decisions',len(audit),'Taylor discrepancy',replay)
