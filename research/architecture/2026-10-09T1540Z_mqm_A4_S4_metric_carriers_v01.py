#!/usr/bin/env python3
import json, itertools, math
from fractions import Fraction

def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
           -a[1]*(b[0]*c[2]-b[2]*c[0])
           +a[2]*(b[0]*c[1]-b[1]*c[0]))
def sub(a,b): return tuple(a[i]-b[i] for i in range(3))
def dist2(a,b): return sum((a[i]-b[i])**2 for i in range(3))
def vol4(P):
    a,b,c,d=P
    return abs(det3(sub(b,a),sub(c,a),sub(d,a)))/6

# A4: stellar subdivision of a regular tetrahedron by its centroid.
O=(0,0,0)
outer=[(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
A4=[]
for omit in range(4):
    face=[outer[i] for i in range(4) if i!=omit]
    A4.append([O]+face)
assert all(abs(vol4(t)-Fraction(2,3))<1e-12 for t in A4)
# Pairwise cells share O plus two outer vertices => one full triangular face.
def face_sets(cells):
    fs=[]
    for t in cells:
        fs.append([frozenset(t[:i]+t[i+1:]) for i in range(4)])
    return fs
def dual_edges(cells):
    fs=face_sets(cells); E=[]
    for i in range(len(cells)):
        for j in range(i+1,len(cells)):
            if set(fs[i]) & set(fs[j]): E.append((i,j))
    return E
EA=dual_edges(A4)
assert len(EA)==6
assert all(sum(i in e for e in EA)==3 for i in range(4))
A4_edges=sorted(set(round(math.sqrt(dist2(a,b)),12) for t in A4 for a,b in itertools.combinations(t,2)))
assert A4_edges==[round(math.sqrt(3),12),round(2*math.sqrt(2),12)]
# Cayley-Menger = 288 V^2.
CM_A=288*(Fraction(2,3)**2)
assert CM_A==128

# S4: cube subdivided by center + six face centers + boundary edges.
# Each cube face module contains 4 congruent tetrahedra; 24 total.
cube=list(itertools.product((-1,1), repeat=3))
faces=[]
# axis, sign; collect cyclic square vertices by angle in plane.
for ax in range(3):
  for sg in (-1,1):
    vs=[v for v in cube if v[ax]==sg]
    # order around face center by atan2 in the two other coordinates
    oth=[i for i in range(3) if i!=ax]
    vs.sort(key=lambda v: math.atan2(v[oth[1]],v[oth[0]]))
    F=tuple(sg if i==ax else 0 for i in range(3))
    faces.append((ax,sg,F,vs))
S4=[]; module=[]
for mi,(ax,sg,F,vs) in enumerate(faces):
    ids=[]
    for k in range(4):
        A=vs[k]; B=vs[(k+1)%4]
        ids.append(len(S4)); S4.append([O,F,A,B])
    module.append(ids)
assert len(S4)==24
vols=[vol4(t) for t in S4]
assert all(abs(v-Fraction(1,3))<1e-12 for v in vols)
assert abs(sum(vols)-8)<1e-12
CM_S=288*(Fraction(1,3)**2)
assert CM_S==32
S4_edges=sorted(set(round(math.sqrt(dist2(a,b)),12) for t in S4 for a,b in itertools.combinations(t,2)))
assert S4_edges==[1.0,round(math.sqrt(2),12),round(math.sqrt(3),12),2.0]
# Module adjacency by shared full triangular faces between tetrahedra of different modules.
FS=face_sets(S4)
ME=set()
for i in range(6):
  for j in range(i+1,6):
    hit=False
    for a in module[i]:
      for b in module[j]:
        if set(FS[a]) & set(FS[b]): hit=True
    if hit: ME.add((i,j))
assert len(ME)==12
assert all(sum(i in e for e in ME)==4 for i in range(6))
# Opposite cube faces are exactly the nonedges among distinct modules.
nonedges=[(i,j) for i in range(6) for j in range(i+1,6) if (i,j) not in ME]
assert len(nonedges)==3

# Exact no-go for a six-tetrahedron one-cell-per-module S4/octrahedron dual.
# Octahedron graph has degree 4, so each tetrahedron's four faces are paired.
# A finite face-to-face tetrahedral complex embedded in R3 with disjoint interiors
# would then have empty topological boundary, impossible for a nonempty compact subset of R3.
no_go={
 "assumptions":[
   "six nondegenerate Euclidean tetrahedra",
   "face-to-face complex in R3 with disjoint interiors",
   "each module adjacency is realized by a distinct shared full triangular face",
   "module adjacency graph is the octahedron graph"
 ],
 "face_incidences":24,
 "shared_faces":12,
 "boundary_faces":0,
 "conclusion":"NO_GO: no finite nonempty compact face-to-face Euclidean 3-complex in R3 can have empty boundary.",
 "minimal_symmetric_repair_tested":"24 tetrahedra, four per cube-face module"
}

out={
 "version":"0.1",
 "status":"EXACT_A4_S4_METRIC_CARRIERS",
 "physical_promotion":0,
 "A4":{
   "carrier":"regular outer tetrahedron stellarly subdivided by centroid",
   "coordinates":{"center":O,"outer":outer},
   "tetrahedra":4,"module_graph":"K4","module_edges":EA,
   "congruent":True,
   "cell_edge_lengths_exact":["sqrt(3) x3","2 sqrt(2) x3"],
   "cell_volume_exact":"2/3",
   "cell_cayley_menger_exact":"128",
   "outer_volume_exact":"8/3",
   "symmetry":"orientation-preserving tetrahedral A4 acts transitively on the four cells"
 },
 "S4":{
   "one_tetrahedron_per_module":no_go,
   "literal_repair":{
      "carrier":"cube barycentric face-star subdivision",
      "cube_vertices":cube,
      "center":O,
      "face_centers":[x[2] for x in faces],
      "modules":6,
      "tetrahedra_per_module":4,
      "tetrahedra_total":24,
      "module_graph":"octahedron",
      "module_edges":sorted(ME),
      "module_nonedges_opposites":nonedges,
      "congruent_cells":True,
      "cell_edge_lengths_exact":["1","sqrt(2) x2","sqrt(3) x2","2"],
      "cell_volume_exact":"1/3",
      "cell_cayley_menger_exact":"32",
      "total_volume_exact":"8",
      "symmetry":"full cube/octahedron symmetry permutes the six face modules and 24 tetrahedral cells"
   }
 },
 "comparison":{
   "D6_previous_cells":6,
   "A4_cells":4,
   "S4_cells_for_full_literal_symmetric_carrier":24,
   "typed_note":"module count and tetrahedral-cell count are distinct objects"
 }
}
print(json.dumps(out,indent=2,sort_keys=True))
