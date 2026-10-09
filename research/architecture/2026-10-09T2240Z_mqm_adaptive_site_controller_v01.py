#!/usr/bin/env python3
import itertools, json
from fractions import Fraction

T=5
sites=range(5)

def F(s):
    if isinstance(s,Fraction): return s
    if isinstance(s,int): return Fraction(s,1)
    a,b=s.split("/")
    return Fraction(int(a),int(b))

profiles={
 "homogeneous":{
   "ell_active":[F("3/100")]*5,
   "ell_spare":[F("1/200")]*5,
   "check":[F("1/500")]*5
 },
 "known_heterogeneous":{
   "ell_active":[F(x) for x in ["1/100","2/100","3/100","4/100","5/100"]],
   "ell_spare":[F("1/200")]*5,
   "check":[F("1/500")]*5
 }
}

short=F("999/1000"); long=F("998/1000")
pair=[[None]*5 for _ in sites]
for i in sites:
  for j in sites:
    if i==j: continue
    sep=(i-j)%5
    pair[i][j]=short if sep in (1,4) else long

counts=[]
for n0 in range(6):
  for n1 in range(6-n0):
    for n2 in range(6-n0-n1):
      for n3 in range(6-n0-n1-n2):
        counts.append((n0,n1,n2,n3,5-n0-n1-n2-n3))
assert len(counts)==126

def site_survival(n,ea,es,rc):
    return (1-ea)**(T-n)*(1-es)**n*(1-rc)**T

def count_score(c,p):
    vals=[site_survival(c[i],p["ell_active"][i],p["ell_spare"][i],p["check"][i]) for i in sites]
    primary=min(vals)
    used=[j for j,n in enumerate(c) if n>0]
    pairvals=[]
    for j in used:
      for i in sites:
        if i!=j:
          pairvals += [pair[i][j]]*c[j]
    secondary_min=min(pairvals) if pairvals else Fraction(1,1)
    secondary_mean=sum(pairvals,Fraction(0,1))/len(pairvals) if pairvals else Fraction(1,1)
    return primary,secondary_min,secondary_mean,vals

def optimize(p):
    scored=[]
    for c in counts:
        pr,mn,av,vals=count_score(c,p)
        scored.append((pr,mn,av,c,vals))
    best=max(scored,key=lambda x:(x[0],x[1],x[2],tuple(-z for z in x[3])))
    ties=[x for x in scored if x[:3]==best[:3]]
    c=best[3]
    label="UNIFORM" if c==(1,1,1,1,1) else "ASYMMETRIC"
    # canonical schedule: lexicographically sorted multiset; exact order is secondary here.
    schedule=[]
    for i,n in enumerate(c): schedule += [i]*n
    return best,ties,label,schedule

out={"version":"0.1","status":"EXACT_ADAPTIVE_SITE_CALIBRATION_CONTROLLER","physical_promotion":0,"profiles":{}}
for nm,p in profiles.items():
    best,ties,label,schedule=optimize(p)
    pr,mn,av,c,vals=best
    out["profiles"][nm]={
      "policy":label,
      "optimal_counts":list(c),
      "canonical_spare_schedule":schedule,
      "worst_site_survival_exact":f"{pr.numerator}/{pr.denominator}",
      "worst_site_survival":float(pr),
      "site_survivals":[float(x) for x in vals],
      "secondary_min_pair_repair":float(mn),
      "secondary_mean_pair_repair":float(av),
      "optimal_tie_count":len(ties)
    }

# Source-blocked branch is a controller outcome, not a numerical profile.
out["missing_calibration_policy"]="SOURCE_BLOCKED"
assert out["profiles"]["homogeneous"]["optimal_counts"]==[1,1,1,1,1]
assert out["profiles"]["known_heterogeneous"]["optimal_counts"]==[0,0,0,2,3]
print(json.dumps(out,indent=2,sort_keys=True))
