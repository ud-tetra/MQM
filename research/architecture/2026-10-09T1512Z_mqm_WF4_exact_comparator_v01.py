#!/usr/bin/env python3
from fractions import Fraction
from collections import Counter, deque
import json

def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4)) for j in range(4)) for i in range(4))
I=tuple(tuple(Fraction(int(i==j)) for j in range(4)) for i in range(4))
def refl(a):
    aa=sum(x*x for x in a)
    return tuple(tuple(Fraction(int(i==j))-2*a[i]*a[j]/aa for j in range(4)) for i in range(4))
e=[tuple(Fraction(int(i==j)) for i in range(4)) for j in range(4)]
roots=[
 tuple(e[1][i]-e[2][i] for i in range(4)),
 tuple(e[2][i]-e[3][i] for i in range(4)),
 e[3],
 tuple(Fraction(x,2) for x in (1,-1,-1,-1))
]
gens=[refl(a) for a in roots]
G={I};Q=deque([I])
while Q:
    x=Q.popleft()
    for g in gens:
        y=mm(g,x)
        if y not in G:G.add(y);Q.append(y)
def order(x):
    y=I
    for k in range(1,100):
        y=mm(x,y)
        if y==I:return k
spec=Counter(order(x) for x in G)
assert len(G)==1152
assert spec==Counter({1:1,2:139,3:80,4:228,6:464,8:144,12:96})
mqm={1:1,2:199,3:80,4:312,6:368,12:192}
out={
 "version":"0.1",
 "status":"EXACT_WF4_COMPARATOR",
 "W_F4_order":len(G),
 "W_F4_element_order_spectrum":dict(sorted(spec.items())),
 "MQM_monomial_LC_order":1152,
 "MQM_element_order_spectrum":mqm,
 "isomorphic":False,
 "witness":"W(F4) has 144 elements of order 8 while the MQM monomial local-Clifford automorphism group has none.",
 "physical_promotion":0
}
print(json.dumps(out,indent=2,sort_keys=True))
