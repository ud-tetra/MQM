import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import json,sys
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.linalg import expm_multiply
from fractions import Fraction as F
P=Path(__file__).resolve().parent
ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
rows=[]
for M in [4,8,192]:
 _,H,_=ns['models'](M);d=M+4;seed=np.zeros(d);seed[0]=1;Proj=np.diag(np.r_[np.ones(4),np.zeros(M)])
 v1=H@seed;v2=H@v1
 assert np.array_equal(v1,np.eye(d)[1]);assert np.array_equal(v2,np.eye(d)[0]+np.eye(d)[2])
 E,V=eigh(H);C1=H@Proj-Proj@H;C2=H@C1-C1@H
 for t in [16-2**-11,16.,16+2**-11]:
  a=V@(np.exp(-1j*E*t)*(V.T@seed));b=expm_multiply(-1j*H*t,seed)
  err=np.linalg.norm(a-b);assert err<2**-32
  z=-1j*H@b;zz=-H@(H@b);q=float(np.vdot(b[:4],b[:4]).real)
  qp=float(2*np.vdot(b[:4],z[:4]).real);qpp=float(2*np.vdot(z[:4],z[:4]).real+2*np.vdot(b[:4],zz[:4]).real)
  comm1=float((1j*np.vdot(b,C1@b)).real);comm2=float(-np.vdot(b,C2@b).real)
  assert abs(qp-comm1)<2**-32 and abs(qpp-comm2)<2**-32
  assert abs(qp)<=2*np.sqrt(q)+2**-32 and abs(qpp)<=2+2*np.sqrt(2*q)+2**-32
  rows.append(dict(M=M,time=t,vector_discrepancy=err,q=q,q_prime=qp,q_second=qpp,derivative_discrepancy=abs(qp-comm1),curvature_discrepancy=abs(qpp-comm2)))
# Independent cross-multiplied integer acceptance and report-ceiling audit.
r=json.loads((P/'results/FLOW_CERTIFICATE.json').read_text());audit=[]
for row in r['rows']:
 num,den=map(int,row['total'].split('/'));passed=num*65536<den;assert passed==row['pass_amplitude']
 audit.append(dict(k=row['k'],target_pass=passed,positive_integer_margin=den-num*65536))
selected=next(z for z in audit if z['target_pass']);assert selected['k']==11
num,den=map(int,next(z for z in r['rows'] if z['k']==11)['total'].split('/'));assert num*2**23<127*den
out=dict(status='SIMULATED separate routes plus EXACT integer audit',controls=rows,integer_audit=audit,external_independent_review=False,physical_promotion=0)
(P/'results/FLOW_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(controls=len(rows),moment_checks=6,max_vector_discrepancy=max(z['vector_discrepancy'] for z in rows),max_derivative_discrepancy=max(z['derivative_discrepancy'] for z in rows),max_curvature_discrepancy=max(z['curvature_discrepancy'] for z in rows),integer_decisions=len(audit))))
