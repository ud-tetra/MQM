from __future__ import annotations
from itertools import combinations, permutations

VERTICES=(1,2,3,4)
CENTER=5
FACES=(
    frozenset((1,2,3)),frozenset((1,2,4)),
    frozenset((1,3,4)),frozenset((2,3,4)),
)

def syndrome(error_vertices):
    E=set(error_vertices)
    ec=1 if CENTER in E else 0
    return tuple(ec ^ (1 if i in E else 0) for i in VERTICES)

def decode_weight_le2(s):
    if len(s)!=4 or any(b not in (0,1) for b in s):
        return 'INVALID'
    w=sum(s)
    if w==0: return frozenset()
    if w==1: return frozenset((1+s.index(1),))
    if w==2: return frozenset(i+1 for i,b in enumerate(s) if b)
    if w==3: return frozenset((CENTER,1+s.index(0)))
    if w==4: return frozenset((CENTER,))

def vertex_face_matchings():
    out=[]
    for perm in permutations(FACES):
        if all(v in f for v,f in zip(VERTICES,perm)):
            out.append(tuple(zip(VERTICES,perm)))
    return tuple(out)

def check_schedule(matching):
    anc=['a'+''.join(map(str,sorted(f))) for v,f in matching]
    layers=[]
    for k in range(4):
        leaf=(k+1)%4
        layers.append(((CENTER,anc[k]),(VERTICES[leaf],anc[leaf])))
    return tuple(layers)
