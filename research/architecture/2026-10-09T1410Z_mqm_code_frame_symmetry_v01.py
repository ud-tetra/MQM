#!/usr/bin/env python3
import json,itertools,math
from collections import Counter
B=json.load(open("release/branches.json"))
b=next(x for x in B if x["id"]=="subsystem-8"); n=8
def pv(s):
 x=z=0
 for i,c in enumerate(s):
  if c in "XY":x|=1<<i
  if c in "ZY":z|=1<<i
 return x|(z<<n)
def sp(v):return v&255,(v>>8)&255
def span(vs):
 S={0}
 for v in vs:S|={x^v for x in tuple(S)}
 return S
G=span(map(pv,b["generators"]["gauge"])); C=span(map(pv,b["generators"]["center"]))
LX=pv(b["logicals"]["X"]);LZ=pv(b["logicals"]["Z"]);LY=LX^LZ
LC={"I":G,"X":{g^LX for g in G},"Y":{g^LY for g in G},"Z":{g^LZ for g in G}}
def pc(v,p):
 x,z=sp(v);a=c=0
 for i,j in enumerate(p):
  if x>>i&1:a|=1<<j
  if z>>i&1:c|=1<<j
 return a|(c<<8)
def lc(v):
 for k,S in LC.items():
  if v in S:return k
I=tuple(range(8))
def mul(a,b):return tuple(a[b[i]] for i in range(8))
def inv(p):
 q=[0]*8
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def order(p):
 x=I
 for k in range(1,50):
  x=mul(p,x)
  if x==I:return k
def cyc(p):
 seen=set();o=[]
 for i in range(8):
  if i in seen:continue
  c=[];j=i
  while j not in seen:seen.add(j);c.append(j+1);j=p[j]
  if len(c)>1:o.append(c)
 return c if False else o
def pm(cs):
 p=list(range(8))
 for cy in cs:
  q=[x-1 for x in cy]
  for a,d in zip(q,q[1:]+q[:1]):p[a]=d
 return tuple(p)
A=set()
for p in itertools.permutations(range(8)):
 if all(pc(pv(s),p) in G for s in b["generators"]["gauge"]):A.add(p)
assert len(A)==12
assert all(lc(pc(LX,p))=="X" and lc(pc(LZ,p))=="Z" for p in A)
r=pm([(1,2,3),(4,5),(6,7)]);s=pm([(2,3)])
assert r in A and s in A and order(r)==6 and order(s)==2 and mul(mul(s,r),s)==inv(r)
def pw(g,k):
 x=I
 for _ in range(k):x=mul(g,x)
 return x
# six frame ports = {1,2,3} x C2 shell polarity
def tau(p):return int(p[3]==4)
def act(p,x):return (p[x[0]-1]+1,x[1]^tau(p))
orb=[];x=(1,0)
for _ in range(6):orb.append(x);x=act(r,x)
assert x==(1,0) and len(set(orb))==6
# wheel holonomy: frames c=I, p_i=r^(step*i), T_uv=g_v g_u^-1
def wheel(m,step):
 f={"c":I}|{f"p{i}":pw(r,step*i) for i in range(m)}
 ok=[]
 for i in range(m):
  j=(i+1)%m; h=I
  path=["c",f"p{i}",f"p{j}","c"]
  for u,v in zip(path,path[1:]):h=mul(mul(f[v],inv(f[u])),h)
  ok.append(h==I)
 return {"vertices":m+1,"edges":2*m,"cycle_rank":m,"basis_cycles_close":ok}
# center Pauli normalizer and defect cosets
def sym(a,b):
 ax,az=sp(a);bx,bz=sp(b)
 return ((ax&bz).bit_count()+(az&bx).bit_count())&1
CV=list(map(pv,b["generators"]["center"]))
N={v for v in range(1<<16) if all(not sym(v,c) for c in CV)}
PS={k:len(S&N) for k,S in LC.items()}
assert len(N)==4096 and PS=={"I":1024,"X":1024,"Y":1024,"Z":1024}
OS=dict(sorted(Counter(order(p) for p in A).items()))
fam={
 "C3":{"pass":any(order(p)==3 for p in A),"order":3},
 "C4":{"pass":any(order(p)==4 for p in A),"order":4},
 "C6":{"pass":any(order(p)==6 for p in A),"order":6},
 "D6_order12":{"pass":True,"order":12},
 "tetrahedral_A4":{"pass":OS=={1:1,2:3,3:8},"order":12},
 "octahedral_S4":{"pass":False,"order":24},
 "icosahedral_A5":{"pass":False,"order":60}}
th=math.acos(1/3)
res={str(m):{"deg":(m*th-2*math.pi)*180/math.pi,"kind":"gap" if m*th<2*math.pi else "overlap"} for m in (3,4,5,6)}
out={"version":"0.1","status":"EXACT_CODE_FRAME_ENUMERATION","physical_promotion":0,
 "gauge_size":len(G),"center_size":len(C),
 "aut_perm":{"size":len(A),"isomorphism":"S3 x C2 ~= D6(order12)","r":cyc(r),"s":cyc(s),"order_spectrum":OS,
  "protected_logical_action":{"I":12,"nontrivial":0}},
 "six_frame_port_orbit":orb,
 "frame_shells":{"C3":wheel(3,2),"C6":wheel(6,1),"D6":"C6 wheel plus reflection s"},
 "symmetry_family_admission":fam,
 "defect_spectrum":{"center_normalizer":len(N),"gauge":len(G),"pauli_cosets":PS,
  "affine_total":len(A)*len(N),"affine_logical_counts":{k:12*v for k,v in PS.items()}},
 "regular_tetra_edge_clock":{"theta":"acos(1/3)","theta_over_pi":"irrational; no finite exact edge-ring closure","residuals":res},
 "scope":{"open":["Euclidean six-cell realization","metric gluing","hardware preference"],"not_claimed":"D6 physical preference"}}
print(json.dumps(out,indent=2,sort_keys=True))
