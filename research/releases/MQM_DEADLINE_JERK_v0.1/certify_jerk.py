from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import json,sys
sys.set_int_max_str_digits(30000)
P=Path(__file__).resolve().parent
par=json.loads((P/'inputs/PARAMETER_INTERVALS.json').read_text());raw=json.loads((P/'inputs/LAUNCH_OUTPUT.json').read_text());out=json.loads((P/'results/DEADLINE_JERK_OUTPUT.json').read_text())
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
# R4=A^4+3CA^2+2ACA+A^2C+3DA+AD+3C^2+E.
# K<14,C<256/3,D<4096/3,E<16384; E=[D,H_B].
fourth_coeff=16*14**4+48*F(256,3)*14**2+16*F(4096,3)*14+12*F(256,3)**2+2*16384
assert fourth_coeff==1843456==2**8*19*379
fourth=nu*fourth_coeff
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
 dv=F(1,2**20)*w+F(1,2**13)*w*w/2+F(1,2**6)*w**3/6+fourth*w**4/24
 xu=x16+6*V*(16*w+w*w/2);assert xu<1;higher=xu*xu/(2*(1-xu));assert higher<F(1,2**25)
 total=E0+dq+F(3,2**26)+dv+vac+cov+higher
 rows.append({'k':k,'halfwidth':str(w),'cold_variation':str(dq),'thermal_variation':str(dv),'cold_third_bound':str(cold_third),'total':str(total),'pass':total<F(1,2**16),'decimal_diagnostic':float(total)})
chosen=next(z for z in rows if z['pass']);assert chosen['k']==5
# Reporting enclosure rounded upward after evaluation; frozen target unchanged.
v=F(chosen['total']);display=(v.numerator*2**23+v.denominator-1)//v.denominator
assert v<F(display,2**23)<F(1,2**16)
parent=json.loads((P/'inputs/PARENT_CERTIFICATE.json').read_text());prior=F(next(z['total'] for z in parent['rows'] if z['k']==chosen['k']))
assert v<prior
result={'status':'DERIVED conditional finite deadline third derivative and fourth remainder','deadline_jerk_upper':str(thermal_jerk),'deadline_jerk_display':'2^-6','readout_allowance_upper':str(readout),'fourth_upper':str(fourth),'fourth_coefficient':1843456,'fourth_coefficient_factorization':'2^8*19*379','horizon':str(U),'selected_halfwidth':chosen['halfwidth'],'window':'16 +/-2^-5 model time units','uniform_error_upper':str(display)+'/2^23<2^-16','decimal_diagnostic':float(v),'parent_total':str(prior),'ceiling_reduction_at_parent_halfwidth':str(prior-v),'halfwidth_gain_vs_parent':1,'thermal_continuum_derivative_transfer':'OPEN; uniform continuum value comparison only','external_review':'OPEN','physical_promotion':0,'rows':rows}
(P/'results/JERK_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print('jerk upper',float(thermal_jerk),'fourth',float(fourth),'display',display,'selected halfwidth',chosen['halfwidth'],'total',float(v))
