from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

VALID={
    (0,0,0):None,
    (1,1,1):1,
    (1,0,0):2,
    (0,1,0):3,
    (0,0,1):4,
}

# (data qubit index 0..3, ancilla/check index 0..2)
# checks G12,G13,G14
LAYERS=(
    ((0,0),(3,2)),
    ((0,1),(1,0)),
    ((0,2),(2,1)),
)

@dataclass(frozen=True)
class XFault:
    kind:str
    layer:int
    op_index:int
    target:int=-1

def weight(bits):
    return sum(bits)

def round_once(data=(0,0,0,0), fault:Optional[XFault]=None):
    d=list(data); a=[0,0,0]
    if fault and fault.kind=='ANCILLA_X' and fault.layer==-1:
        a[fault.target]^=1
    for li,layer in enumerate(LAYERS):
        for oi,(q,anc) in enumerate(layer):
            a[anc]^=d[q]
            if fault and fault.layer==li and fault.op_index==oi:
                if fault.kind in {'DATA_X','CNOT_X_DATA','CNOT_X_BOTH'}:
                    d[q]^=1
                if fault.kind in {'CNOT_X_ANC','CNOT_X_BOTH','ANCILLA_X'}:
                    a[anc]^=1
    if fault and fault.kind=='MEAS_FLIP':
        a[fault.target]^=1
    return tuple(d),tuple(a)

def immediate_correct(data,syndrome):
    if syndrome not in VALID:
        return tuple(data),'UNDECLARED'
    q=VALID[syndrome]
    out=list(data)
    if q is not None:
        out[q-1]^=1
    return tuple(out),q

def stable_consensus_recover(initial=(0,0,0,0), fault:Optional[XFault]=None, max_rounds=8):
    data=tuple(initial); prev=None; trace=[]; used=False
    for r in range(max_rounds):
        f=fault if not used else None
        data,s=round_once(data,f)
        if f is not None: used=True
        trace.append((data,s))
        if s not in VALID:
            prev=None
            continue
        if prev==s:
            data,c=immediate_correct(data,s)
            return {'status':'CORRECTED','data':data,'correction':c,'rounds':r+1,'trace':trace}
        prev=s
    return {'status':'NO_CONSENSUS','data':data,'correction':None,'rounds':max_rounds,'trace':trace}

def all_single_x_faults():
    faults=[]
    for anc in range(3):
        faults.append(XFault('ANCILLA_X',-1,-1,anc))
    for li,layer in enumerate(LAYERS):
        for oi,(q,anc) in enumerate(layer):
            for kind in ('DATA_X','CNOT_X_DATA','CNOT_X_ANC','CNOT_X_BOTH'):
                faults.append(XFault(kind,li,oi,-1))
    for anc in range(3):
        faults.append(XFault('MEAS_FLIP',99,99,anc))
    return tuple(faults)
