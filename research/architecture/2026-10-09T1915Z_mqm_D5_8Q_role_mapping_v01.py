#!/usr/bin/env python3
import itertools, json, math
from collections import Counter

R=1/math.sin(math.pi/5)
sites={"N":(0.0,0.0,1.0),"S":(0.0,0.0,-1.0),"O":(0.0,0.0,0.0)}
for i in range(5):
    sites[f"v{i}"]=(R*math.cos(2*math.pi*i/5),R*math.sin(2*math.pi*i/5),0.0)

tets={"T_C":[1,2,3,8],"T_plus":[5,6,7,8],"T_minus":[4,6,7,8]}
edges=sorted(set(tuple(sorted(e)) for t in tets.values() for e in itertools.combinations(t,2)))
assert len(edges)==15
deg={q:sum(q in e for e in edges) for q in range(1,9)}
assert deg=={1:3,2:3,3:3,4:3,5:3,6:4,7:4,8:7}

def d(a,b): return math.dist(sites[a],sites[b])
D={frozenset((a,b)):d(a,b) for a,b in itertools.combinations(sites,2)}
def dd(a,b): return D[frozenset((a,b))]

best=None; reps=[]; total=0
for perm in itertools.permutations(list(sites)):
    total+=1
    mp=dict(zip(range(1,9),perm))
    L=[dd(mp[a],mp[b]) for a,b in edges]
    mean=sum(L)/len(L)
    k=max(L)/min(L)
    cv=(sum((x-mean)**2 for x in L)/len(L))**0.5/mean
    maxmean=max(L)/mean
    key=(round(k,12),round(cv,12),round(maxmean,12),round(sum(L),12))
    if best is None or key<best:
        best=key; reps=[(mp,L)]
    elif key==best:
        reps.append((mp,L))
assert total==40320
mp,L=reps[0]
cls=Counter(round(x,12) for x in L)
nearest=min(D.values())
unused_nearest=[]
for pair,x in D.items():
    if abs(x-nearest)<1e-12:
        a,b=tuple(pair)
        qa=next(q for q,s in mp.items() if s==a)
        qb=next(q for q,s in mp.items() if s==b)
        if tuple(sorted((qa,qb))) not in edges:
            unused_nearest.append(sorted((qa,qb)))

out={
 "version":"0.1",
 "status":"EXACT_EXHAUSTIVE_D5_8Q_ROLE_MAPPING",
 "physical_promotion":0,
 "enumerated_bijections":total,
 "best_tie_count":len(reps),
 "frozen_interaction_edges":[list(e) for e in edges],
 "role_degrees":deg,
 "canonical_best_mapping":{str(q):s for q,s in mp.items()},
 "best_metrics":{
   "required_edge_kappa_exact":"sqrt((5+sqrt(5))/2)",
   "required_edge_kappa":best[0],
   "coefficient_of_variation":best[1],
   "max_over_mean":best[2],
   "required_edge_length_sum":best[3]
 },
 "required_edge_distance_classes":{
   "csc(pi/5)":cls[round(R,12)],
   "sqrt(3+2/sqrt(5))":cls[round(math.sqrt(3+2/math.sqrt(5)),12)],
   "2":cls[2.0],
   "1+sqrt(5)":cls[round(1+math.sqrt(5),12)]
 },
 "unused_shortest_site_pairs":{
   "distance":nearest,
   "count":len(unused_nearest),
   "mapped_qubit_pairs":unused_nearest
 },
 "baseline":{
   "ideal_tri_tetra_required_edge_kappa":1,
   "ideal_tri_tetra_CV":0,
   "comparison":"NO_GO for D5 improving frozen required-edge length uniformity; ideal tri-tetra is exactly uniform by construction."
 },
 "scope":"natural D5+axis-midpoint eight-site augmentation only; alternative eighth-site optimization remains a new candidate"
}
print(json.dumps(out,indent=2,sort_keys=True))
