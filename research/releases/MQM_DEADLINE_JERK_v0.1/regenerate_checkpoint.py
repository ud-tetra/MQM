import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import json,time,hashlib
import numpy as np
P=Path(__file__).resolve().parent;ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
M=192;H,H1,n=ns['models'](M);assert max(np.diff(H.indptr))<=196
V=np.zeros((H.shape[0],M));V[3+np.arange(M),np.arange(M)]=1
R=V;I=np.zeros_like(V);start=time.monotonic()
for step in range(128):
 ar=R.copy();ai=I.copy();tr=R.copy();ti=I.copy()
 for k in range(1,49):
  nr=(H@ti)/(8*k);ni=-(H@tr)/(8*k);ar+=nr;ai+=ni;tr,ti=nr,ni
 R,I=ar,ai
 if (step+1)%16==0:print('hot steps',step+1,flush=True)
W=R+1j*I;seed=np.zeros((M+4,1));seed[0]=1;R=seed;I=np.zeros_like(seed)
for step in range(128):
 ar=R.copy();ai=I.copy();tr=R.copy();ti=I.copy()
 for k in range(1,49):
  nr=(H1@ti)/(8*k);ni=-(H1@tr)/(8*k);ar+=nr;ai+=ni;tr,ti=nr,ni
 R,I=ar,ai
u=(R+1j*I)[:,0]
# Polarization uses retained positive dyads to reconstruct cross terms.
def curvature(K,W,n,M):
 A=K@W;B=K@A
 return 2*ns['retained'](A,n,M)-(ns['retained'](W+B,n,M)-ns['retained'](W-B,n,M))/2
hot=curvature(H,W,n,M);a=H1@u;b=H1@a
cold=np.zeros((8,8),complex);cold[:4,:4]=2*np.outer(a[:4],a[:4].conj())-np.outer(b[:4],u[:4].conj())-np.outer(u[:4],b[:4].conj());cold[4,4]=2*np.vdot(a[4:],a[4:]).real-2*np.vdot(u[4:],b[4:]).real
C=hot-n.sum()*cold
np.savez_compressed(P/'results/POINT_CHECKPOINT.npz',W=W,u=u)
out={'status':'BINARY64 returned entries; require directed error ledger','M':M,'steps':128,'degree':48,'curvature_real':C.real.tolist(),'curvature_imag':C.imag.tolist(),'half_trace_diagnostic':float(abs(np.linalg.eigvalsh(C)).sum()/2),'cold_population_curvature_diagnostic':float(cold[:4,:4].trace().real),'seconds':time.monotonic()-start,'checkpoint_sha256':hashlib.sha256((P/'results/POINT_CHECKPOINT.npz').read_bytes()).hexdigest()}
(P/'results/POINT_OUTPUT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if not k.endswith('_real') and not k.endswith('_imag')},indent=2),flush=True)
