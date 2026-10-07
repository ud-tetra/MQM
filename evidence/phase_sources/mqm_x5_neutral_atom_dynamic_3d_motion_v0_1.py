from __future__ import annotations
import math
import itertools
import numpy as np

# Regular tetrahedral shell, circumradius R=1.
V={
    1:np.array((1,1,1),float)/math.sqrt(3),
    2:np.array((1,-1,-1),float)/math.sqrt(3),
    3:np.array((-1,1,-1),float)/math.sqrt(3),
    4:np.array((-1,-1,1),float)/math.sqrt(3),
}
C=np.zeros(3)

# Preferred double-transposition mapping:
# vertex -> opposite-face label represented by opposite vertex.
# 1->face123(opposite4), 2->face124(opposite3), 3->face134(opposite2), 4->face234(opposite1)
OPPOSITE={1:4,2:3,3:2,4:1}

def biased_base(vertex,delta,R=1.0):
    opp=OPPOSITE[vertex]
    rho=1.5-2*math.sqrt(2)*delta
    if rho<=0:
        raise ValueError("rho must be positive")
    face_centroid=-R*V[opp]/3
    direction=R*V[vertex]-face_centroid
    direction=direction/np.linalg.norm(direction)
    base=-rho*R*V[opp] + delta*R*direction
    return base,rho

def gate_poses(vertex,delta,lam,R=1.0):
    """
    Equal fractional approach lam from the balanced biased base toward
    center and assigned vertex.
    """
    B,rho=biased_base(vertex,delta,R)
    Pc=(1-lam)*B + lam*C
    Pv=(1-lam)*B + lam*(R*V[vertex])
    return B,Pc,Pv,rho

def gate_pose_metrics(vertex,delta,lam,R=1.0):
    B,Pc,Pv,rho=gate_poses(vertex,delta,lam,R)
    d0c=float(np.linalg.norm(B-C))
    d0v=float(np.linalg.norm(B-R*V[vertex]))
    gc=float(np.linalg.norm(Pc-C))
    gv=float(np.linalg.norm(Pv-R*V[vertex]))
    shuttle=float(np.linalg.norm(Pc-Pv))
    return {
        "rho":rho,
        "base_center_distance":d0c,
        "base_vertex_distance":d0v,
        "gate_center_distance":gc,
        "gate_vertex_distance":gv,
        "shuttle_distance":shuttle,
    }

def syndrome_schedule(center_order=(1,2,3,4),vertex_order=(2,3,4,1)):
    """
    One center edge + one vertex edge each layer. vertex_order must be a
    derangement of center_order by layer.
    """
    if len(set(center_order))!=4 or len(set(vertex_order))!=4:
        raise ValueError
    if any(c==v for c,v in zip(center_order,vertex_order)):
        raise ValueError("ancilla conflict")
    layers=[]
    for c,v in zip(center_order,vertex_order):
        layers.append((("CENTER",c),("VERTEX",v)))
    return tuple(layers)

def alternating_schedule_pair():
    a=syndrome_schedule((1,2,3,4),(2,3,4,1))
    b=syndrome_schedule((2,3,4,1),(1,2,3,4))
    return a,b

def partner_order(schedule):
    pos={}
    for layer_i,layer in enumerate(schedule):
        for partner,anc in layer:
            pos.setdefault(anc,[]).append((layer_i,partner))
    return {a:tuple(x[1] for x in sorted(v)) for a,v in pos.items()}

def projection_min_separation(points,axis):
    """
    Minimum pairwise Euclidean separation after orthogonal projection to
    plane normal to axis.
    """
    axis=np.asarray(axis,float)
    axis=axis/np.linalg.norm(axis)
    proj=[]
    for p in points:
        p=np.asarray(p,float)
        q=p-np.dot(p,axis)*axis
        proj.append(q)
    best=float("inf")
    for i,j in itertools.combinations(range(len(proj)),2):
        best=min(best,float(np.linalg.norm(proj[i]-proj[j])))
    return best

def coordinate_set(delta=0.2,R=1.0):
    pts=[R*V[i] for i in (1,2,3,4)]
    pts.append(C.copy())
    for i in (1,2,3,4):
        B,_,_,_=gate_poses(i,delta,0.0,R)
        pts.append(B)
    return tuple(pts)
