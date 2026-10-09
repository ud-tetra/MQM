#!/usr/bin/env python3
import itertools, json
from fractions import Fraction

T=5
profiles=[
  (Fraction(1,100),Fraction(1,200),Fraction(1,500)),
  (Fraction(2,100),Fraction(1,200),Fraction(1,500)),
  (Fraction(3,100),Fraction(1,200),Fraction(1,500)),
  (Fraction(4,100),Fraction(1,200),Fraction(1,500)),
  (Fraction(5,100),Fraction(1,200),Fraction(1,500)),
]

counts=[]
for n0 in range(6):
  for n1 in range(6-n0):
    for n2 in range(6-n0-n1):
      for n3 in range(6-n0-n1-n2):
        counts.append((n0,n1,n2,n3,5-n0-n1-n2-n3))

def surv(n,p):
  ea,es,r=p
  return (1-ea)**(T-n)*(1-es)**n*(1-r)**T

def min_surv(c,ps):
  vals=[surv(n,p) for n,p in zip(c,ps)]
  return min(vals),vals

# Known heterogeneous site labels.
known=max((min_surv(c,profiles)[0],c,min_surv(c,profiles)[1]) for c in counts)
uniform=(1,1,1,1,1)
u_score,u_vals=min_surv(uniform,profiles)

# Unknown/adversarial site relabeling of the same risk multiset.
def robust(c):
  worst=Fraction(1,1); witness=None
  for perm in itertools.permutations(profiles):
    x,_=min_surv(c,perm)
    if x<worst:
      worst=x;witness=perm
  return worst,witness

rob=max((robust(c)[0],c) for c in counts)
rties=[c for c in counts if robust(c)[0]==rob[0]]
assert rties==[uniform]

# Homogeneous theorem check on a concrete active>spare profile.
hp=(Fraction(3,100),Fraction(1,200),Fraction(1,500))
homo=[hp]*5
hbest=max((min_surv(c,homo)[0],c) for c in counts)
hties=[c for c in counts if min_surv(c,homo)[0]==hbest[0]]
assert hties==[uniform]

def f(x): return float(x)
def q(x): return f"{x.numerator}/{x.denominator}"

out={
 "version":"0.1",
 "status":"EXACT_HETEROGENEOUS_ROTATING_SPARE_MINIMAX",
 "physical_promotion":0,
 "theorem":{
   "risk_coordinate":"R_i(n_i)=-log S_i(n_i)=T[a_i+c_i]-n_i(a_i-s_i), with a_i=-log(1-ell_active_i), s_i=-log(1-ell_spare_i), c_i=-log(1-r_check_i)",
   "homogeneous":"if all sites share the same parameters and active exposure is worse than spare exposure, minimizing max_i R_i is equivalent to maximizing min_i n_i. With five spare epochs over five sites, the unique minimax count vector is (1,1,1,1,1).",
   "known_heterogeneity":"uniform rotation is not generally minimax; spare epochs should be biased toward higher-risk sites according to the discrete minimax allocation.",
   "unknown_adversarial_labels":"for a known multiset of site risks but unknown/adversarial assignment to physical labels, equal spare counts are the unique minimax allocation in the frozen five-site/five-epoch benchmark."
 },
 "stress_profile":{
   "active_loss":["1/100","2/100","3/100","4/100","5/100"],
   "spare_loss":["1/200"]*5,
   "check_failure":["1/500"]*5
 },
 "known_heterogeneity":{
   "uniform_counts":list(uniform),
   "uniform_worst_survival_exact":q(u_score),
   "uniform_worst_survival":f(u_score),
   "uniform_site_survivals":[f(x) for x in u_vals],
   "optimal_counts":list(known[1]),
   "optimal_worst_survival_exact":q(known[0]),
   "optimal_worst_survival":f(known[0]),
   "optimal_site_survivals":[f(x) for x in known[2]],
   "worst_survival_absolute_gain":f(known[0]-u_score),
   "ruling":"known heterogeneity falsifies uniform rotation as the reliability-minimax schedule for this stress profile"
 },
 "robust_unknown_labels":{
   "unique_optimal_counts":list(rob[1]),
   "worst_case_survival_exact":q(rob[0]),
   "worst_case_survival":f(rob[0]),
   "ruling":"uniform rotation is restored as the unique minimax schedule when site identities are not known before scheduling and an adversary may permute the frozen risk multiset"
 },
 "scope":"independent per-epoch site channels; counts theorem only. Channel-to-slot path costs and temporal correlations remain separate."
}
print(json.dumps(out,indent=2,sort_keys=True))
