import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
from fractions import Fraction as F
import json,math
import numpy as np
from scipy.linalg import eigh
from scipy.sparse.linalg import expm_multiply
P=Path(__file__).resolve().parent;ns={'__file__':str(P/'inputs/response_model.py')};exec((P/'inputs/response_model.py').read_text(),ns)
rows=[];comm=lambda H,X:H@X-X@H
for M in [4,8]:
 H,H1,n=ns['models'](M);A=H.toarray();delta=H1.diagonal()[4:];rho=np.zeros_like(A);gauge_errors=[];hot=0
 for j in range(M):
  v=np.zeros(len(A));v[3+j]=1;K=A-delta[j]*np.eye(len(A));p=[v]
  for r in range(4):p.append(K@p[-1])
  bound=np.linalg.norm(p[4])+4*np.linalg.norm(p[3])*np.linalg.norm(p[1])+3*np.linalg.norm(p[2])**2
  X=np.outer(v,v);Y=X.copy()
  for r in range(4):X=comm(A,X);Y=comm(K,Y)
  er=float(np.linalg.norm(X-Y));assert er<2**-22;gauge_errors.append(er)
  actual=abs(np.linalg.eigvalsh(X)).sum()/2;assert actual<=bound+2**-22
  hot+=n[j]*bound;rho[3+j,3+j]=n[j]
 coldseed=np.zeros(M+4);coldseed[0]=1;s3=H1@(H1@(H1@coldseed));s3b=np.zeros_like(coldseed);s3b[1]=2;s3b[3]=H1[2,3];assert np.linalg.norm(s3-s3b)<2**-40
 s4=H1@s3;formula=4+(2+H1[2,3]**2)**2+H1[2,3]**2*sum(H1[3,4:]**2);assert abs(np.vdot(s4,s4).real-formula)<2**-36;assert formula<324
 vals,Q=eigh(A);U=(Q*np.exp(-16j*vals))@Q.T;rhoT=U@rho@U.conj().T;X=rhoT
 for k in range(4):X=comm(A,X)
 warm_actual=abs(np.linalg.eigvalsh(X)).sum()/2;assert warm_actual<=hot+2**-32
 psi=expm_multiply(-16j*H1,coldseed);p1=expm_multiply(-16j*H1,H1@coldseed);p2=expm_multiply(-16j*H1,H1@(H1@coldseed));p3=expm_multiply(-16j*H1,s3)
 q3=-2*np.vdot(psi[:4],p3[:4]).imag+6*np.vdot(p1[:4],p2[:4]).imag
 rho1=np.outer(psi,psi.conj());D=rho1
 for k in range(3):D=comm(H1,D)
 actual3=(1j*D[:4,:4].trace()).real;assert abs(q3-actual3)<2**-30
 rows.append({'M':M,'gauged_launch_checks':M,'max_gauge_discrepancy':max(gauge_errors),'warm_fourth_trace_at16':float(warm_actual),'warm_launch_triangle_bound':float(hot),'cold_source_fourth_squared_norm':float(formula),'cold_third_scalar_discrepancy':float(abs(q3-actual3))})
cert=json.loads((P/'results/LAUNCH_FOURTH_CERTIFICATE.json').read_text());decisions=[]
for x in cert['rows']:
 v=F(x['total']);passed=v.numerator*65536<v.denominator;assert passed==x['pass'];decisions.append({'k':x['k'],'pass':passed})
assert next(x['k'] for x in decisions if x['pass'])==4
chosen=F(next(x['total'] for x in cert['rows'] if x['k']==4));assert chosen.numerator*2**23<115*chosen.denominator
j=json.loads((P/'results/CONTINUUM_JET_CERTIFICATE.json').read_text());comparisons=[]
for row in j['rows']:
 eps=list(map(F,row['kernel_half_trace_by_order']));U=F(129,8);v=6*eps[1]+7*U*eps[2]+U*U*eps[3]/2
 assert str(v)==row['uniform_third_transfer_upper'];passed=v.numerator*4096<v.denominator;assert passed==row['auxiliary_pass'];comparisons.append({'M':row['M'],'auxiliary_pass':passed})
assert F(j['rows'][1]['uniform_third_transfer_upper'])<F(1,2**118)
assert F(j['rows'][0]['uniform_third_transfer_upper'])<F(7,64)
out={'status':'SIMULATED finite routes / EXACT rational decision audit','small_model_rows':rows,'launch_gauge_checks':12,'native_source_identity_checks':4,'cold_third_route_checks':2,'warm_time16_bound_checks':2,'rational_decisions':decisions,'continuum_integer_comparisons':comparisons,'M256_comparison_display':'<2^-118','M192_comparison_display':'<7/64, auxiliary target not cleared','external_review':'OPEN','physical_promotion':0}
(P/'results/LAUNCH_FOURTH_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
