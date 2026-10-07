from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import json
P=Path(__file__).resolve().parent
raw=json.loads((P/'results/LAUNCH_OUTPUT.json').read_text());par=json.loads((P/'inputs/PARAMETER_INTERVALS.json').read_text())
# Rational upper square root on a fixed dyadic grid; exact integer decision.
def sqrt_up(z,b=80):
 assert z>=0
 s=1<<b;n=isqrt(z.numerator*s*s//z.denominator)
 if F(n*n,s*s)<z:n+=1
 assert F(n*n,s*s)>=z
 return F(n,s)
a=[[F(v) for v in row] for row in raw['real']];b=[[F(v) for v in row] for row in raw['imag']]
q=[sum(a[i][j]**2+b[i][j]**2 for i in range(4)) for j in range(3)]
norm=[sqrt_up(z) for z in q]
qp=2*sum(a[i][0]*b[i][1]-b[i][0]*a[i][1] for i in range(4))
# Inherited conservative Q2 envelope is also valid for the Q1 generator.
gamma=F(1,2**43);step=32*gamma*3**8+F(8**49,factorial(49))/(1-F(8,50))+F(1,2**800)
roundoff=256*step
U=F(16)+F(1,64);x=4*U
R=x**192/factorial(192)/(1-x/193);transfer=84*U*R
err=16*F(par['Hamiltonian_Q2_error_upper'])+roundoff+transfer
errors=[err,err,F(3,2)*err] # exact two-entry curvature seed has norm sqrt2<3/2
slope=abs(qp)+2*(errors[0]*norm[1]+errors[1]*norm[0]+errors[0]*errors[1])
# Report ceiling chosen after evaluation; acceptance is the frozen target.
assert slope<F(1,2**16)
slope_cap=F(1,2**16)
V=F(64,31457265);vac=336*U**3*V*R;assert vac<F(1,2**30)
y=8*U+F(25,16);r=F(1,2**21);G2=F(128,3)
eta=4*G2*r/(1-r)*y**384/factorial(384)/(1-y/385)+2*G2*r**9/(1-r)
cov=2*U**2*eta;assert cov<F(1,2**56)
E0=F(3,2**18)+F(1,2**128);a0=F(7,2048);assert E0<a0*a0
x16=F(12433696189517,58512905602490430);rows=[]
for k in range(6,25):
 w=F(1,2**k)
 # Native time variation uses conserved H p1 and H(p0+p2) launch norms.
 # sqrt2<3/2; ||2p1+lambda p3||=sqrt(4+4sqrt2)<13/4.
 curvature=2*(norm[1]+errors[1]+F(3,2)*w)**2+2*(a0+w)*(norm[2]+errors[2]+F(13,4)*w)
 dq=slope_cap*w+curvature*w*w/2
 xu=x16+6*V*(16*w+w*w/2);higher=xu*xu/(2*(1-xu));assert higher<F(1,2**25)
 total=E0+dq+F(3,2**26)+F(1,2**20)*w+w*w/8+F(1,2**30)+F(1,2**56)+higher
 rows.append({'k':k,'halfwidth':str(w),'cold_variation':str(dq),'curvature_bound':str(curvature),'total':str(total),'pass':total<F(1,2**16),'decimal_diagnostic':float(total)})
chosen=next(z for z in rows if z['pass']);assert chosen['k']==8
assert F(chosen['total'])<F(115,2**23)<F(1,2**16)
out={'status':'DERIVED conditional','launch_norm_upper':list(map(str,norm)),'native_squared_norm_exact':list(map(str,q)),'raw_slope_exact':str(qp),'slope_upper':str(slope),'slope_display_upper':'2^-16','launch_error_upper':str(err),'roundoff_upper':str(roundoff),'continuum_launch_transfer_upper':str(transfer),'uniform_response_transfer':str(vac),'uniform_covariance_transfer':str(cov),'horizon':str(U),'window':'16 +/- 2^-8 model time units','relative_halfwidth':'2^-12','uniform_error_upper':'115/2^23 < 2^-16','gain_vs_parent':8,'gain_vs_initial_window':256,'rows':rows,'external_review':'OPEN','physical_promotion':0}
(P/'results/TRANSPORT_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k in ['status','window','uniform_error_upper','gain_vs_parent','physical_promotion']}));print('slope',float(slope),'error',float(err),'total',chosen['decimal_diagnostic'],'curvature',float(F(chosen['curvature_bound'])))
