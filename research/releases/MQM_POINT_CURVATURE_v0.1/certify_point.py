from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import json,sys
sys.set_int_max_str_digits(30000)
P=Path(__file__).resolve().parent
par=json.loads((P/'inputs/PARAMETER_INTERVALS.json').read_text());raw=json.loads((P/'inputs/LAUNCH_OUTPUT.json').read_text());out=json.loads((P/'results/POINT_OUTPUT.json').read_text())
def root(q):
 s=2**80;n=isqrt(q.numerator*s*s//q.denominator)
 if F(n*n,s*s)<q:n+=1
 return F(n,s)
a=[[F(v) for v in z] for z in raw['real']];b=[[F(v) for v in z] for z in raw['imag']]
N=[root(sum(a[i][j]**2+b[i][j]**2 for i in range(4))) for j in range(3)]
qp=2*sum(a[i][0]*b[i][1]-b[i][0]*a[i][1] for i in range(4))
qpp=2*sum(a[i][1]**2+b[i][1]**2-a[i][0]*a[i][2]-b[i][0]*b[i][2] for i in range(4))
step=32*F(1,2**43)*3**8+F(8**49,factorial(49))/(1-F(8,50))+F(1,2**800)
dh=F(par['Hamiltonian_Q2_error_upper'])+F(1,2**40);finite_e=16*dh+256*step
U=F(16)+F(1,8);x=4*U;R=x**192/factorial(192)/(1-x/193)
e=finite_e+84*U*R;e2=F(3,2)*e
slope=abs(qp)+2*(e*N[1]+e*N[0]+e*e);assert slope<F(1,2**16)
cold_curv=abs(qpp)+2*(2*N[1]*e+e*e)+2*(e*N[2]+e2*N[0]+e*e2);assert cold_curv<F(1,2**14)
nu=F(par['occupation_trace_upper']);dn=F(par['occupation_l1_error_upper'])
Craw=sum(abs(F(v)) for key in ['curvature_real','curvature_imag'] for row in out[key] for v in row)/2
# half trace-norm curvature superoperator: ||ad_H^2|| <=4h^2.
gamma=F(1,2**25)/(1-F(1,2**25))
readout=32*gamma*nu*4*(64+dh)**2*(1+finite_e)**2+16*F(1,2**43)*nu*(64+dh)**2*(1+finite_e)**2
assert readout<F(1,2**20)
Cerr=nu*(4*64**2*(2*finite_e+finite_e**2)+4*dh*(128+dh)*(1+finite_e)**2)+4*64**2*dn+F(1,2**20)
thermal_curv=Craw+Cerr;assert thermal_curv<F(1,2**13)
# Exact reduced third commutator: adK^3+2adC adK+adK adC+adD.
# K<14,C<256/3,D<4096/3 from flat-band fourth moment and pi>3.
third=nu*(8*14**3+12*14*F(256,3)+2*F(4096,3))
assert 8*14**3+12*14*F(256,3)+2*F(4096,3)==F(117056,3)
V=F(64,31457265);vac=336*U**3*V*R
y=8*U+F(25,16);r=F(1,2**21);G2=F(128,3)
eta=4*G2*r/(1-r)*y**384/factorial(384)/(1-y/385)+2*G2*r**9/(1-r);cov=2*U**2*eta
E0=F(3,2**18)+F(1,2**128);A=F(7,2048);x16=F(12433696189517,58512905602490430);rows=[]
for k in range(3,25):
 w=F(1,2**k);s1=N[1]+e;s2=N[2]+e2;h3=F(13,4)
 b0=A+s1*w+s2*w*w/2+h3*w**3/6
 b1=s1+s2*w+h3*w*w/2;b2=s2+h3*w
 cold_third=6*b1*b2+2*b0*h3
 dq=F(1,2**16)*w+F(1,2**14)*w*w/2+cold_third*w**3/6
 dv=F(1,2**20)*w+F(1,2**13)*w*w/2+third*w**3/6
 xu=x16+6*V*(16*w+w*w/2);assert xu<1;higher=xu*xu/(2*(1-xu));assert higher<F(1,2**25)
 total=E0+dq+F(3,2**26)+dv+vac+cov+higher
 rows.append({'k':k,'halfwidth':str(w),'cold_variation':str(dq),'thermal_variation':str(dv),'cold_third_bound':str(cold_third),'total':str(total),'pass':total<F(1,2**16),'decimal_diagnostic':float(total)})
chosen=next(z for z in rows if z['pass']);assert chosen['k']==5
# Engineering display enclosure selected after evaluation, not acceptance.
assert F(chosen['total'])<F(123,2**23)<F(1,2**16)
result={'status':'DERIVED conditional point-curvature window','cold_deadline_curvature_upper':str(cold_curv),'cold_display':'2^-14','thermal_deadline_curvature_upper':str(thermal_curv),'thermal_display':'2^-13','thermal_third_upper':str(third),'thermal_third_coefficient':'117056/3 times nu_U','fresh_uniform_response_comparison':str(vac),'fresh_uniform_covariance_comparison':str(cov),'horizon':str(U),'window':'16 +/-2^-5 model time units','uniform_error_upper':'123/2^23<2^-16','halfwidth_gain_vs_parent':2,'relative_halfwidth':'2^-9','physical_promotion':0,'external_review':'OPEN','thermal_continuum_derivative_transfer':'OPEN; value comparison only','rows':rows}
(P/'results/POINT_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print('cold curvature',float(cold_curv),'thermal curvature',float(thermal_curv),'third',float(third));print('window',chosen['halfwidth'],'total',chosen['decimal_diagnostic'])
