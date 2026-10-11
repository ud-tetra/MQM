from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import json,sys
sys.set_int_max_str_digits(30000)
P=Path(__file__).resolve().parent
par=json.loads((P/'inputs/PARAMETER_INTERVALS.json').read_text());raw=json.loads((P/'inputs/LAUNCH_OUTPUT.json').read_text());out=json.loads((P/'inputs/DEADLINE_JERK_OUTPUT.json').read_text());launch=json.loads((P/'results/LAUNCH_MOMENTS_OUTPUT.json').read_text())
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
Jraw=sum(abs(F(v)) for key in ['jerk_real','jerk_imag'] for row in out[key] for v in row)/2
# Third commutator norm <=8h^3; parameter perturbation uses a^3-b^3 factorization.
gamma=F(1,2**25)/(1-F(1,2**25));h=F(64)
readout=32*gamma*nu*8*(h+dh)**3*(1+finite_e)**2+16*F(1,2**43)*nu*(h+dh)**3*(1+finite_e)**2
assert readout<F(1,2**12)
Jerr=nu*(8*h**3*(2*finite_e+finite_e**2)+8*dh*((h+dh)**2+h*(h+dh)+h*h)*(1+finite_e)**2)+8*h**3*dn+F(1,2**12)
thermal_jerk=Jraw+Jerr;assert thermal_jerk<F(1,2**6)
# Gauge invariance ad(H-delta_j I)^4=adH^4 on each launch.
gnorm=F(1,2**37)/(1-F(1,2**37));power_error=[]
for rpower in range(1,5):
 bound=rpower*(2*dh)*(80+2*dh)**(rpower-1)+((1+F(1,2**43))**rpower-1)*(80+2*dh)**rpower
 power_error.append(bound)
hot_norms=[[root((F(v)+F(1,2**800))/(1-gnorm))+power_error[r] for v in launch['hot_power_squared_norms'][r]] for r in range(4)]
combo=[hot_norms[3][j]+4*hot_norms[2][j]*hot_norms[0][j]+3*hot_norms[1][j]**2 for j in range(192)]
hot_fourth=sum(F(n)*v for n,v in zip(launch['occupation'],combo))+dn*max(combo)
fourth=hot_fourth+F(151,4)*nu
c=[F(v) for v in launch['cold_third_live_real']];d=[F(v) for v in launch['cold_third_live_imag']]
N3=root(sum(v*v+z*z for v,z in zip(c,d)));e3=F(13,4)*e+2*dh+F(1,2**40)
q3=-2*sum(a[i][0]*d[i]-b[i][0]*c[i] for i in range(4))+6*sum(a[i][1]*b[i][2]-b[i][1]*a[i][2] for i in range(4))
cold_third_point=abs(q3)+2*(e*N3+e3*N[0]+e*e3)+6*(e*N[2]+e2*N[1]+e*e2)
V=F(64,31457265);vac=336*U**3*V*R
y=8*U+F(25,16);r=F(1,2**21);G2=F(128,3)
eta=4*G2*r/(1-r)*y**384/factorial(384)/(1-y/385)+2*G2*r**9/(1-r);cov=2*U**2*eta
E0=F(3,2**18)+F(1,2**128);A=F(7,2048);x16=F(12433696189517,58512905602490430);rows=[]
for k in range(3,25):
 w=F(1,2**k);s1=N[1]+e;s2=N[2]+e2;s3=N3+e3;h4=F(18)
 b0=A+s1*w+s2*w*w/2+s3*w**3/6+h4*w**4/24
 b1=s1+s2*w+s3*w*w/2+h4*w**3/6;b2=s2+s3*w+h4*w*w/2;b3=s3+h4*w
 cold_fourth=2*b0*h4+8*b1*b3+6*b2*b2
 dq=F(1,2**16)*w+F(1,2**14)*w*w/2+cold_third_point*w**3/6+cold_fourth*w**4/24
 dv=F(1,2**20)*w+F(1,2**13)*w*w/2+F(1,2**6)*w**3/6+fourth*w**4/24
 xu=x16+6*V*(16*w+w*w/2);assert xu<1;higher=xu*xu/(2*(1-xu));assert higher<F(1,2**25)
 total=E0+dq+F(3,2**26)+dv+vac+cov+higher
 rows.append({'k':k,'halfwidth':str(w),'cold_variation':str(dq),'thermal_variation':str(dv),'cold_fourth_bound':str(cold_fourth),'total':str(total),'pass':total<F(1,2**16),'decimal_diagnostic':float(total)})
chosen=next(z for z in rows if z['pass'])
# Reporting enclosure rounded upward after evaluation; frozen target unchanged.
v=F(chosen['total']);display=(v.numerator*2**23+v.denominator-1)//v.denominator
assert v<F(display,2**23)<F(1,2**16)
parent=json.loads((P/'inputs/JERK_CERTIFICATE.json').read_text());prior=F(next(z['total'] for z in parent['rows'] if z['k']==5))
new_same=F(next(z['total'] for z in rows if z['k']==5));assert new_same<prior
result={'status':'DERIVED conditional launch-local fourth remainder and cold third derivative','hot_fourth_upper':str(hot_fourth),'thermal_fourth_upper':str(fourth),'cold_third_point_upper':str(cold_third_point),'cold_seed_error':str(e3),'native_third_launch_norm_upper':str(N3+e3),'source_fourth_launch_norm':'<18','finite_thermal_deadline_third_display':'2^-6 inherited conditional','horizon':str(U),'selected_halfwidth':chosen['halfwidth'],'selected_k':chosen['k'],'uniform_error_upper':str(display)+'/2^23<2^-16','decimal_diagnostic':float(v),'parent_total_at2^-5':str(prior),'new_total_at2^-5':str(new_same),'halfwidth_gain_vs_parent':2**(5-chosen['k']),'thermal_continuum_derivative_transfer':'OPEN atM192: computed seven-slot comparison too coarse; idealM256 comparison separately passes','external_review':'OPEN','physical_promotion':0,'rows':rows}
(P/'results/LAUNCH_FOURTH_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print('cold third',float(cold_third_point),'fourth',float(fourth),'display',display,'halfwidth',chosen['halfwidth'],'total',float(v))
