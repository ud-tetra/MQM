from __future__ import annotations

"""
MQM Core-X5 central-extension X-fault syndrome simulator v0.1.

Data order:
0 = center c
1..4 = tetrahedral vertex data qubits

Ancilla/check order:
0..3 = checks G_i = Z_c Z_i for vertices i=1..4.

Preferred 4-layer schedule:
L1: c->a1, q2->a2
L2: c->a2, q3->a3
L3: c->a3, q4->a4
L4: c->a4, q1->a1
"""

from dataclasses import dataclass
from typing import Optional

LAYERS=(
    ((0,0),(2,1)),
    ((0,1),(3,2)),
    ((0,2),(4,3)),
    ((0,3),(1,0)),
)

@dataclass(frozen=True)
class XFault:
    kind:str
    layer:int
    op_index:int
    target:int=-1

def weight(bits):
    return sum(bits)

def syndrome_to_correction(s):
    """
    Exact minimum-weight decoder for 5-bit repetition weight<=2 sector.
    Returns tuple of data indices 0..4 to flip.
    """
    if len(s)!=4 or any(b not in (0,1) for b in s):
        return "INVALID"
    w=sum(s)
    if w==0:
        return ()
    if w==1:
        return (1+s.index(1),)
    if w==2:
        return tuple(i+1 for i,b in enumerate(s) if b)
    if w==3:
        return (0,1+s.index(0))
    if w==4:
        return (0,)

def round_once(data=(0,0,0,0,0),fault:Optional[XFault]=None):
    d=list(data)
    a=[0,0,0,0]

    # Preparation-X fault on one ancilla.
    if fault and fault.kind=="ANCILLA_X" and fault.layer==-1:
        a[fault.target]^=1

    for li,layer in enumerate(LAYERS):
        for oi,(q,anc) in enumerate(layer):
            # CNOT control=data, target=ancilla: parity accumulation.
            a[anc]^=d[q]

            if fault and fault.layer==li and fault.op_index==oi:
                if fault.kind in {"DATA_X","CNOT_X_DATA","CNOT_X_BOTH"}:
                    d[q]^=1
                if fault.kind in {"CNOT_X_ANC","CNOT_X_BOTH","ANCILLA_X"}:
                    a[anc]^=1

    if fault and fault.kind=="MEAS_FLIP":
        a[fault.target]^=1

    return tuple(d),tuple(a)

def apply_correction(data,correction):
    if correction=="INVALID":
        return tuple(data)
    d=list(data)
    for q in correction:
        d[q]^=1
    return tuple(d)

def all_single_x_faults():
    out=[]
    for anc in range(4):
        out.append(XFault("ANCILLA_X",-1,-1,anc))
    for li,layer in enumerate(LAYERS):
        for oi,(q,anc) in enumerate(layer):
            for kind in ("DATA_X","CNOT_X_DATA","CNOT_X_ANC","CNOT_X_BOTH"):
                out.append(XFault(kind,li,oi,-1))
    for anc in range(4):
        out.append(XFault("MEAS_FLIP",99,99,anc))
    return tuple(out)
