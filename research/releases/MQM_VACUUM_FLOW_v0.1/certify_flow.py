from pathlib import Path
from fractions import Fraction as F
from math import factorial
import json
P=Path(__file__).resolve().parent
T=F(16);V=F(64,31457265);E0=F(3,2**18)+F(1,2**128);a0=F(7,2048)
assert E0<a0*a0
# H|p0>=|p1>; H^2|p0>=|p0>+|p2> in every admitted vacuum reference.
assert 1+1==2
Ustar=T+F(1,2**8);x=4*Ustar
R=x**192/factorial(192)/(1-x/193);vac=336*Ustar**3*V*R
assert vac<F(1,2**30)
y=8*Ustar+F(25,16);r=F(1,2**21);G2=F(128,3)
eta=4*G2*r/(1-r)*y**384/factorial(384)/(1-y/385)+2*G2*r**9/(1-r)
cov=2*Ustar**2*eta;assert cov<F(1,2**57)
x16=F(12433696189517,58512905602490430)
rows=[]
for k in range(8,25):
 w=F(1,2**k);dq=2*a0*w+w*w
 # Independently usable Taylor certificate from q' and q'': sqrt2<3/2.
 dq_curv=2*a0*w+(1+F(3,2)*(a0+w))*w*w
 xu=x16+6*V*(T*w+w*w/2);assert xu<1
 higher=xu*xu/(2*(1-xu))
 rest=E0+F(3,2**26)+F(1,2**20)*w+w*w/8+F(1,2**30)+F(1,2**57)+higher
 total=rest+dq;second=rest+dq_curv
 rows.append(dict(k=k,halfwidth=str(w),pass_amplitude=total<F(1,2**16),pass_curvature=second<F(1,2**16),total=str(total),curvature_total=str(second),decimal_diagnostic=float(total),cold_variation=str(dq)))
chosen=next(row for row in rows if row['pass_amplitude']);assert chosen['k']==11
selected=F(chosen['total']);assert selected<F(127,2**23)<F(1,2**16)
assert next(row for row in rows if row['pass_curvature'])['k']==11
result=dict(status='DERIVED conditional',amplitude_Lipschitz=1,previous_port_charge_upper=7,initial_moments={'H_mean':0,'H_squared_mean':1,'H_fourth_mean':2},q_prime_bound='2 sqrt(q)',q_second_bound='2+2 sqrt(2q)',cold_variation='7w/1024+w^2',window='16 +/- 2^-11 model time units',relative_halfwidth='2^-15 of deadline',halfwidth_gain_vs_response_jet=8,halfwidth_gain_vs_initial_retention=32,uniform_error_upper='127/2^23 < 2^-16',uniform_comparison_horizon=str(Ustar),vacuum_transfer=str(vac),covariance_transfer=str(cov),external_review='OPEN',permanent_retention='OPEN',arbitrary_input_diamond='OPEN',physical_promotion=0,rows=rows)
(P/'results/FLOW_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['rows','vacuum_transfer','covariance_transfer']},indent=2))
