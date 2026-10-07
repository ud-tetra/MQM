from __future__ import annotations

"""
General Pauli hook propagation across the 8-CNOT Core-X5 syndrome schedule.

Qubits:
0..4 data (center + 4 vertices)
5..8 ancillas a1..a4.

Fault: any nonidentity two-qubit Pauli inserted after one CNOT, propagated
through all subsequent CNOTs.
"""

PAULIS=("I","X","Y","Z")
CNOTS=(
    (0,5),(2,6),
    (0,6),(3,7),
    (0,7),(4,8),
    (0,8),(1,5),
)

def bits(p):
    return {"I":(0,0),"X":(1,0),"Z":(0,1),"Y":(1,1)}[p]

def label(x,z):
    return {(0,0):"I",(1,0):"X",(0,1):"Z",(1,1):"Y"}[(x,z)]

def propagate_cnot(x,z,c,t):
    x=list(x);z=list(z)
    x[t] ^= x[c]
    z[c] ^= z[t]
    return tuple(x),tuple(z)

def propagate_fault(location,p_control,p_target):
    c,t=CNOTS[location]
    x=[0]*9;z=[0]*9
    x[c],z[c]=bits(p_control)
    x[t],z[t]=bits(p_target)

    for c2,t2 in CNOTS[location+1:]:
        x,z=propagate_cnot(x,z,c2,t2)

    out=tuple(label(x[i],z[i]) for i in range(9))
    data=out[:5]
    return {
        "location":location,
        "gate":CNOTS[location],
        "fault":p_control+p_target,
        "final_paulis":"".join(out),
        "data_paulis":"".join(data),
        "data_weight":sum(p!="I" for p in data),
        "data_X_or_Y_weight":sum(p in {"X","Y"} for p in data),
        "data_Z_or_Y_weight":sum(p in {"Z","Y"} for p in data),
    }

def enumerate_faults():
    rows=[]
    for loc in range(len(CNOTS)):
        for pc in PAULIS:
            for pt in PAULIS:
                if pc==pt=="I":
                    continue
                rows.append(propagate_fault(loc,pc,pt))
    return rows
