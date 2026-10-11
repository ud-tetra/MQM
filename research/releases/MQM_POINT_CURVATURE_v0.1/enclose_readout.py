import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json
import numpy as np
P=Path(__file__).resolve().parent;ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
M=192;H,H1,n=ns['models'](M);data=np.load(P/'results/POINT_CHECKPOINT.npz');W=data['W'];u=data['u']
def pair(A,B):
 out=np.zeros((8,8),complex);out[5:8,5:8]=(A[:3]*n)@B[:3].conj().T
 X=A[3:3+4*M].reshape(4,M,M);Y=B[3:3+4*M].reshape(4,M,M)
 out[:4,:4]=np.einsum('ajk,bjk,k->ab',X,Y.conj(),n)
 out[4,4]=np.sum(A[3+4*M:]*B[3+4*M:].conj()*n)
 return out
A=H@W;B=H@A;hot=2*pair(A,A)-pair(B,W)-pair(W,B)
a=H1@u;b=H1@a;cold=np.zeros((8,8),complex);cold[:4,:4]=2*np.outer(a[:4],a[:4].conj())-np.outer(b[:4],u[:4].conj())-np.outer(u[:4],b[:4].conj());cold[4,4]=2*np.vdot(a[4:],a[4:]).real-2*np.vdot(u[4:],b[4:]).real
C=hot-n.sum()*cold;f=P/'results/POINT_OUTPUT.json';old=json.loads(f.read_text());polar=np.array(old['curvature_real'])+1j*np.array(old['curvature_imag']);err=float(np.linalg.norm(C-polar));assert err<2**-32
(P/'results/POINT_OUTPUT_POLARIZATION.json').write_text(json.dumps(old,indent=2)+'\n')
old.update(curvature_real=C.real.tolist(),curvature_imag=C.imag.tolist(),half_trace_diagnostic=float(abs(np.linalg.eigvalsh(C)).sum()/2),direct_vs_polarization_discrepancy=err,certified_readout_route='direct weighted bilinear dyads; conservative268435456 operation budget; round-to-nearest model')
f.write_text(json.dumps(old,indent=2)+'\n');print('direct vs polarization',err)
