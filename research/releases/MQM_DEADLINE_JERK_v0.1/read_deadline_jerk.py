import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
import json,hashlib,time,argparse
import numpy as np
P=Path(__file__).resolve().parent;pr=json.loads((P/'PROTOCOL.json').read_text());ap=argparse.ArgumentParser();ap.add_argument('--checkpoint',required=True);args=ap.parse_args();checkpoint=Path(args.checkpoint)
assert hashlib.sha256(checkpoint.read_bytes()).hexdigest()==pr['source_checkpoint_sha256']
ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
M=192;H,H1,n=ns['models'](M);data=np.load(checkpoint);W=data['W'];u=data['u'];assert W.shape==(19299,192)
def pair(A,B):
 out=np.zeros((8,8),complex);out[5:8,5:8]=(A[:3]*n)@B[:3].conj().T
 X=A[3:3+4*M].reshape(4,M,M);Y=B[3:3+4*M].reshape(4,M,M)
 out[:4,:4]=np.einsum('ajk,bjk,k->ab',X,Y.conj(),n)
 out[4,4]=np.sum(A[3+4*M:]*B[3+4*M:].conj()*n)
 return out
start=time.monotonic();A=H@W;B=H@A;C=H@B
hot=1j*(pair(C,W)-3*pair(B,A)+3*pair(A,B)-pair(W,C))
a=H1@u;b=H1@a;c=H1@b
cold=np.zeros((8,8),complex)
cold[:4,:4]=1j*(np.outer(c[:4],u[:4].conj())-3*np.outer(b[:4],a[:4].conj())+3*np.outer(a[:4],b[:4].conj())-np.outer(u[:4],c[:4].conj()))
cold[4,4]=(1j*(np.vdot(u[4:],c[4:])-3*np.vdot(a[4:],b[4:])+3*np.vdot(b[4:],a[4:])-np.vdot(c[4:],u[4:]))).real
J=hot-n.sum()*cold
# Separate source-state derivative: finite hot trace through reduced source K and bath commutators is checked on small models in audit_jerk.py.
out={'status':'SIMULATED binary64 readout; acceptance requires rational error enclosure','M':M,'checkpoint_sha256':pr['source_checkpoint_sha256'],'readout':'direct covariance-weighted third-commutator dyads;8 total coefficient magnitude','jerk_real':J.real.tolist(),'jerk_imag':J.imag.tolist(),'half_trace_diagnostic':float(abs(np.linalg.eigvalsh(J)).sum()/2),'hermiticity_diagnostic':float(np.linalg.norm(J-J.conj().T)),'cold_population_third_diagnostic':float(cold[:4,:4].trace().real),'seconds':time.monotonic()-start}
(P/'results/DEADLINE_JERK_OUTPUT.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k not in ['jerk_real','jerk_imag']})
