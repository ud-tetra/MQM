#!/usr/bin/env python3
"""MQM firewall-aware candidate circuit hook audit v0.2.

Exact scope:
- Reads only release/branches.json for the subsystem-8 code algebra.
- Audits a NEW candidate direct-center schedule; it does not reconstruct or
  silently replace the frozen v0.2 gauge schedule.
- Pauli phases are quotiented, matching the release algebra.
- Hook model: one Pauli fault after one declared two-qubit gate.
- A fault is safe if it is flagged/rejected, or its final data Pauli has dressed
  subsystem weight <= 1 modulo the full gauge group.
- Verified-cat audit also injects X/Y/Z after the cat-root H preparation.
- Prep/measurement bit errors and data-basis-rotation faults are separately
  classified as non-hook single-fault locations; they require repeated syndrome
  / fail-closed policy for full FTEC.
"""

from __future__ import annotations
import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BRANCHES=ROOT/"release"/"branches.json"

CANDIDATE_CHECKS=[
    "IIIXXZZI",  # B1=S1 shell-only
    "IIIZZYYI",  # B2=S2*S3 shell-only
    "IIIYIYZZ",  # B3=S2 cross
    "XXXXYYIX",  # B4=S4 cross, weight 7
]
FLAG_ORDERS_1BASED={
    "IIIXXZZI":[4,5,6,7],
    "IIIZZYYI":[4,5,6,7],
    "IIIYIYZZ":[4,6,7,8],
    "XXXXYYIX":[4,5,6,1,2,3,8],
}
EDGE_CHECKS_1BASED=[(1,2),(1,3),(1,8),(2,3),(2,8),(3,8)]

def pv(s,n=None):
    if n is None:n=len(s)
    x=z=0
    for i,ch in enumerate(s):
        if ch in "XY":x|=1<<i
        if ch in "ZY":z|=1<<i
    return x|(z<<n)

def split(v,n):
    m=(1<<n)-1
    return v&m,(v>>n)&m

def wt(v,n):
    x,z=split(v,n)
    return (x|z).bit_count()

def cnot(v,c,t,n):
    x,z=split(v,n)
    if (x>>c)&1:x^=1<<t
    if (z>>t)&1:z^=1<<c
    return x|(z<<n)

def cz(v,a,b,n):
    x,z=split(v,n)
    if (x>>a)&1:z^=1<<b
    if (x>>b)&1:z^=1<<a
    return x|(z<<n)

def h(v,q,n):
    x,z=split(v,n)
    if ((x>>q)&1)!=((z>>q)&1):
        x^=1<<q;z^=1<<q
    return x|(z<<n)

def s(v,q,n):
    x,z=split(v,n)
    if (x>>q)&1:z^=1<<q
    return x|(z<<n)

def pair_pauli(a,b,pa,pb,n):
    x=z=0
    for q,ch in ((a,pa),(b,pb)):
        if ch in "XY":x|=1<<q
        if ch in "ZY":z|=1<<q
    return x|(z<<n)

def single_pauli(q,p,n):
    x=z=0
    if p in "XY":x|=1<<q
    if p in "ZY":z|=1<<q
    return x|(z<<n)

def span(basis):
    out={0}
    for b in basis:
        out|={x^b for x in tuple(out)}
    return out

def data8(v,n):
    x,z=split(v,n)
    return (x&0xff)|((z&0xff)<<8)

def main():
    branches=json.loads(BRANCHES.read_text())
    branch=next(b for b in branches if b["id"]=="subsystem-8")
    gauges=[pv(s) for s in branch["generators"]["gauge"]]
    gspan=span(gauges)

    @lru_cache(None)
    def dressed(v):
        return min(wt(v^g,8) for g in gspan)

    def pre_ops(check,n):
        ops=[]
        for q,ch in enumerate(check):
            if ch=="X":ops.append(("H",q))
            elif ch=="Y":ops.extend([("S",q),("H",q)]) # symplectic S/Sdg identical
        return ops

    def post_ops(check,n):
        ops=[]
        for q,ch in reversed(list(enumerate(check))):
            if ch=="X":ops.append(("H",q))
            elif ch=="Y":ops.extend([("H",q),("S",q)])
        return ops

    def apply(v,op,n):
        if op[0]=="H":return h(v,op[1],n)
        if op[0]=="S":return s(v,op[1],n)
        if op[0]=="CNOT":return cnot(v,op[1],op[2],n)
        if op[0]=="CZ":return cz(v,op[1],op[2],n)
        raise ValueError(op)

    def flagged(check):
        n=10 # data 0..7, syndrome 8, flag 9
        order=[q-1 for q in FLAG_ORDERS_1BASED[check]]
        ops=pre_ops(check,n)
        dcount=0
        for d in order:
            ops.append(("CNOT",d,8,"D"))
            dcount+=1
            if dcount in (1,3):
                ops.append(("CNOT",9,8,"F")) # flag control -> syndrome target
        ops+=post_ops(check,n)
        twoq=[i for i,o in enumerate(ops) if o[0]=="CNOT"]
        hist=Counter();bad=[]
        for loc in twoq:
            a,b=ops[loc][1],ops[loc][2]
            for pa,pb in itertools.product("IXYZ",repeat=2):
                if pa==pb=="I":continue
                e=pair_pauli(a,b,pa,pb,n)
                for op in ops[loc+1:]:
                    e=apply(e,op,n)
                _,z=split(e,n)
                flag=(z>>9)&1 # X-basis flag measurement
                dw=dressed(data8(e,n))
                hist[(flag,dw)]+=1
                if not flag and dw>1:
                    bad.append((loc,pa+pb,dw))
        return {
            "check":check,
            "data_order_1based":FLAG_ORDERS_1BASED[check],
            "flag_after_data_interactions":[1,3],
            "two_qubit_gates":len(twoq),
            "two_qubit_pauli_faults":15*len(twoq),
            "flag_dressed_hist":{f"flag{f}_dw{d}":n for (f,d),n in sorted(hist.items())},
            "unsafe_unflagged_faults":len(bad),
        }

    def bare_edge(i1,j1):
        n=9
        i,j=i1-1,j1-1
        ops=[("CNOT",i,8),("CNOT",j,8)]
        hist=Counter();bad=[]
        for loc,op in enumerate(ops):
            for pa,pb in itertools.product("IXYZ",repeat=2):
                if pa==pb=="I":continue
                e=pair_pauli(op[1],op[2],pa,pb,n)
                for rest in ops[loc+1:]:
                    e=cnot(e,rest[1],rest[2],n)
                dw=dressed(data8(e,n))
                hist[dw]+=1
                if dw>1:bad.append((loc,pa+pb,dw))
        return {
            "edge":[i1,j1],"two_qubit_gates":2,"two_qubit_pauli_faults":30,
            "dressed_hist":dict(hist),"unsafe_faults":len(bad)
        }

    def verified_cat(check):
        support=[q for q,ch in enumerate(check) if ch!="I"]
        w=len(support); n=9+w
        cats=list(range(8,8+w));vq=8+w
        ops=[("H",cats[0],"rootH")]
        for j in range(1,w):
            ops.append(("CNOT",cats[0],cats[j],f"prep{j}"))
        for j in range(1,w):
            ops.append(("CNOT",cats[0],vq,f"verify{j}a"))
            ops.append(("CNOT",cats[j],vq,f"verify{j}b"))
            ops.append(("MEAS_RESET_Z",vq,f"verify{j}m"))
        for j,d in enumerate(support):
            ops.append(("CZ",cats[j],d,f"data{j}"))

        def unrotate(v):
            for q,ch in enumerate(check):
                if ch=="X":v=h(v,q,n)
                elif ch=="Y":
                    v=h(v,q,n);v=s(v,q,n)
            return v

        faults=[(0,("S",cats[0],p)) for p in "XYZ"]
        for loc,op in enumerate(ops):
            if op[0] in ("CNOT","CZ"):
                for pa,pb in itertools.product("IXYZ",repeat=2):
                    if pa==pb=="I":continue
                    faults.append((loc,("P",op[1],op[2],pa,pb)))
        accepted=Counter();rejected=0;bad=[]
        for inj,flt in faults:
            e=0;det=False
            for loc,op in enumerate(ops):
                if op[0]=="H":e=h(e,op[1],n)
                elif op[0]=="CNOT":e=cnot(e,op[1],op[2],n)
                elif op[0]=="CZ":e=cz(e,op[1],op[2],n)
                elif op[0]=="MEAS_RESET_Z":
                    x,z=split(e,n)
                    if (x>>vq)&1:det=True
                    x&=~(1<<vq);z&=~(1<<vq);e=x|(z<<n)
                if loc==inj:
                    if flt[0]=="S":e^=single_pauli(flt[1],flt[2],n)
                    else:e^=pair_pauli(flt[1],flt[2],flt[3],flt[4],n)
            e=unrotate(e)
            dw=dressed(data8(e,n))
            if det:rejected+=1
            else:
                accepted[dw]+=1
                if dw>1:bad.append((inj,flt,dw))
        twoq=4*w-3
        return {
            "check":check,"weight":w,
            "cat_qubits":w,"verification_qubits_reusable":1,
            "max_ancillas":w+1,
            "two_qubit_gates":twoq,
            "injected_faults":len(faults),
            "accepted_dressed_hist":dict(accepted),
            "rejected_by_verification":rejected,
            "unsafe_accepted_faults":len(bad),
        }

    flag=[flagged(c) for c in CANDIDATE_CHECKS]
    edges=[bare_edge(*e) for e in EDGE_CHECKS_1BASED]
    cats=[verified_cat(c) for c in CANDIDATE_CHECKS]

    flag_center_2q=sum(x["two_qubit_gates"] for x in flag)
    edge_2q=sum(x["two_qubit_gates"] for x in edges)
    cat_center_2q=sum(x["two_qubit_gates"] for x in cats)

    result={
        "status":"EXACT_CONSTRUCTOR_REPLAY",
        "candidate_center":CANDIDATE_CHECKS,
        "flagged":{
            "checks":flag,
            "center_two_qubit_gates":flag_center_2q,
            "edge_two_qubit_gates":edge_2q,
            "full_redundant_cycle_two_qubit_gates":flag_center_2q+edge_2q,
            "center_two_qubit_faults":sum(x["two_qubit_pauli_faults"] for x in flag),
            "edge_two_qubit_faults":sum(x["two_qubit_pauli_faults"] for x in edges),
            "unsafe_unflagged_or_edge_faults":sum(x["unsafe_unflagged_faults"] for x in flag)+sum(x["unsafe_faults"] for x in edges),
            "max_ancillas_beyond_data":2,
        },
        "verified_cat":{
            "checks":cats,
            "center_two_qubit_gates":cat_center_2q,
            "edge_two_qubit_gates":edge_2q,
            "full_redundant_cycle_two_qubit_gates":cat_center_2q+edge_2q,
            "center_injected_faults":sum(x["injected_faults"] for x in cats),
            "edge_two_qubit_faults":sum(x["two_qubit_pauli_faults"] for x in edges),
            "unsafe_accepted_or_edge_faults":sum(x["unsafe_accepted_faults"] for x in cats)+sum(x["unsafe_faults"] for x in edges),
            "max_ancillas_beyond_data":max(x["max_ancillas"] for x in cats),
        },
        "typed_limits":{
            "hook_containment_only":True,
            "full_fault_tolerance":False,
            "measurement_bit_reliability":"OPEN/requires repeated syndrome or fail-closed protocol",
            "loss":"OPEN",
            "idle_noise":"OPEN",
            "hardware":"OPEN",
            "physical_promotion":0,
        }
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
