#!/usr/bin/env python3
import json, math
from fractions import Fraction

def bipyramid(m,h,R):
    d=2*math.pi/m
    a=2*h
    b=2*R*math.sin(math.pi/m)
    c=math.sqrt(R*R+h*h)
    V=h*R*R*math.sin(d)/3
    CM=288*V*V
    return {"m":m,"central_edge":a,"ring_edge":b,"four_spokes":c,"volume":V,"cayley_menger":CM,"dihedral_about_axis_deg":360/m}

# Exact D6 congruent tetrahedral decomposition of a hexagonal bipyramid.
d6=bipyramid(6,1,2)
assert abs(d6["central_edge"]-2)<1e-12 and abs(d6["ring_edge"]-2)<1e-12
assert abs(d6["four_spokes"]-math.sqrt(5))<1e-12
assert d6["volume"]>0 and d6["cayley_menger"]>0

# D5 minimax-near-regular exact ring: choose central=edge ring=2, solve R sin(pi/5)=1.
R5=1/math.sin(math.pi/5)
d5=bipyramid(5,1,R5)
assert abs(d5["central_edge"]-2)<1e-12 and abs(d5["ring_edge"]-2)<1e-12

def spread(x):
    L=[x["central_edge"],x["ring_edge"],x["four_spokes"]]
    return max(L)/min(L)

k5=spread(d5); k6=spread(d6)
# Numerical exhaustive confirmation of minimax R/h in a broad interval.
def scan(m):
    best=(9,None)
    for i in range(300000):
        t=0.5+3.5*i/299999
        x=bipyramid(m,1,t)
        k=spread(x)
        if k<best[0]:best=(k,t)
    return best
s5=scan(5);s6=scan(6)
assert abs(s5[1]-R5)<5e-4
assert abs(s6[1]-2)<5e-4

theta=math.acos(1/3)
clock={}
for m in range(3,9):
    res=m*theta-2*math.pi
    clock[str(m)]={"signed_deg":res*180/math.pi,"abs_deg":abs(res)*180/math.pi,"gap_or_overlap":"gap" if res<0 else "overlap"}

# Standard D6 hexagonal-bipyramid vertex action vs subsystem code D6 generator.
# Standard rotation has cycle type 6+1+1 on 8 vertices.
# Code generator r has cycle type 3+2+2+1.
standard_cycle_type=[6,1,1]
code_cycle_type=[3,2,2,1]

# An alternative orthogonal order-6 action can realize 3+2+2+1:
# r_geo = diag(R_120, -1), s_geo = reflection y->-y.
# But any period-3 orbit has z=0 and the unique fixed point is the origin,
# so the K4 core {1,2,3,8} is coplanar and has zero volume.
def R120(p):
    x,y,z=p
    a=2*math.pi/3
    return (math.cos(a)*x-math.sin(a)*y,math.sin(a)*x+math.cos(a)*y,-z)
q1=(1,0,0);q2=R120(q1);q3=R120(q2);q8=(0,0,0)
def det3(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
vol_core=abs(det3(q1,q2,q3))/6 # with q8=origin
assert vol_core<1e-12

out={
 "version":"0.1",
 "status":"EXACT_DM_TETRAHEDRAL_REALIZATION_AND_COMPARATOR",
 "physical_promotion":0,
 "general_family":{
   "cells":"T_i={N,S,v_i,v_(i+1)} in a regular m-gonal bipyramid",
   "coordinates":"N=(0,0,h), S=(0,0,-h), v_i=(R cos(2pi i/m), R sin(2pi i/m),0)",
   "edge_lengths":"a=2h, b=2R sin(pi/m), c=sqrt(R^2+h^2) with c repeated four times",
   "cell_volume":"V=h R^2 sin(2pi/m)/3",
   "cayley_menger":"288 V^2 > 0 for h,R>0,m>2",
   "central_edge_dihedral":"2pi/m exactly",
   "global_symmetry":"D_m on the tetrahedral cell ring"
 },
 "D6_literal_shell":{
   "choice":"h=1,R=2",
   "edges_exact":["2","2","sqrt(5) x4"],
   "metrics":d6,
   "conclusion":"Six congruent nonregular tetrahedra close exactly around the central edge with D6 cell-shell symmetry."
 },
 "D5_near_regular_comparator":{
   "choice":"h=1,R=csc(pi/5), so central and ring edges both equal 2",
   "metrics":d5,
   "minimax_edge_ratio":k5,
   "minimax_edge_spread_percent":100*(k5-1),
   "scan_optimum_R_over_h":s5[1],
   "conclusion":"The exact five-cell ring is much closer to a regular tetrahedron than the exact six-cell ring under max/min edge spread."
 },
 "D6_minimax_edge_ratio":k6,
 "D6_minimax_edge_spread_percent":100*(k6-1),
 "D6_scan_optimum_R_over_h":s6[1],
 "regular_tetra_clock":clock,
 "representation_bridge":{
   "standard_hexagonal_bipyramid_vertex_cycle_type":standard_cycle_type,
   "subsystem_code_D6_generator_cycle_type":code_cycle_type,
   "standard_vertex_action_matches_code_permutation":False,
   "alternative_orthogonal_action":"diag(R_120deg,-1) has cycle structure 3+2+2+1",
   "K4_core_volume_under_alternative_action":vol_core,
   "direct_non_degenerate_K4_vertex_realization":"NO_GO for this exact orthogonal permutation action",
   "interpretation":"The exact D6 code action is naturally a frame/module symmetry, not the literal standard spatial permutation of the eight bipyramid vertices."
 },
 "scope":{
   "exact":"Euclidean D_m bipyramid construction, congruent-cell closure, metric positivity, D5/D6 distortion comparator, representation mismatch",
   "open":"mapping six D6 tetrahedral modules to the subsystem-8 frame orbit with fault-tolerant intermodule circuits"
 }
}
print(json.dumps(out,indent=2,sort_keys=True))
