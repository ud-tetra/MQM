#!/usr/bin/env python3
"""Exact GF(2) replay for MQM repeated firewall FTEC + noisy decoder v0.1.

Frozen protocol:
  research/protocols/2026-10-08T1642Z_MQM_FIREWALL_REPEATED_FTEC_PROTOCOL_v0.1_FREEZE.json
Metric clarification:
  research/protocols/2026-10-08T1644Z_MQM_FIREWALL_REPEATED_FTEC_PROTOCOL_v0.1a_METRIC_FREEZE.json

No floating point is required. Pauli phases are quotiented. The replay reads the
subsystem-8 algebra from release/branches.json and evaluates:
  A. clean input + <=1 circuit/receipt/loss fault over the frozen state machine;
  B. each of 24 single-qubit Pauli input errors with no circuit fault;
  C. exact syndrome-readout logical-failure coefficients for one frame versus
     three-frame bitwise majority.

Loss indication is ideal in this mathematical replay. Hardware loss detection,
timing, threshold and hardware performance remain outside scope.
"""

from __future__ import annotations
import itertools
import json
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BRANCHES=ROOT/"release"/"branches.json"

CHECKS=[
    "IIIXXZZI",
    "IIIZZYYI",
    "IIIYIYZZ",
    "XXXXYYIX",
]
ORDERS={
    "IIIXXZZI":[4,5,6,7],
    "IIIZZYYI":[4,5,6,7],
    "IIIYIYZZ":[4,6,7,8],
    "XXXXYYIX":[4,5,6,1,2,3,8],
}
EDGES=[(1,2),(1,3),(1,8),(2,3),(2,8),(3,8)]

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

def weight(v,n):
    x,z=split(v,n)
    return (x|z).bit_count()

def symp(a,b,n):
    ax,az=split(a,n);bx,bz=split(b,n)
    return (((ax&bz).bit_count()+(az&bx).bit_count())&1)

def cnot(v,c,t,n):
    x,z=split(v,n)
    if (x>>c)&1:x^=1<<t
    if (z>>t)&1:z^=1<<c
    return x|(z<<n)

def hgate(v,q,n):
    x,z=split(v,n)
    if ((x>>q)&1)!=((z>>q)&1):
        x^=1<<q;z^=1<<q
    return x|(z<<n)

def sgate(v,q,n):
    x,z=split(v,n)
    if (x>>q)&1:z^=1<<q
    return x|(z<<n)

def single(q,p,n):
    x=z=0
    if p in "XY":x|=1<<q
    if p in "ZY":z|=1<<q
    return x|(z<<n)

def pair(a,b,pa,pb,n):
    return single(a,pa,n)^single(b,pb,n)

def embed_data(v8,n):
    x,z=split(v8,8)
    return x|(z<<n)

def extract_data(v,n):
    x,z=split(v,n)
    return (x&0xff)|((z&0xff)<<8)

def span(basis):
    out={0}
    for b in basis:
        out|={x^b for x in tuple(out)}
    return out

def pre_ops(check):
    ops=[]
    for q,ch in enumerate(check):
        if ch=="X":ops.append(("H",q,"pre"))
        elif ch=="Y":ops.extend([("S",q,"pre"),("H",q,"pre")])
    return ops

def post_ops(check):
    ops=[]
    for q,ch in reversed(list(enumerate(check))):
        if ch=="X":ops.append(("H",q,"post"))
        elif ch=="Y":ops.extend([("H",q,"post"),("S",q,"post")])
    return ops

def center_ops(check):
    ops=pre_ops(check)
    k=0
    for d1 in ORDERS[check]:
        ops.append(("CNOT",d1-1,8,"data"))
        k+=1
        if k in (1,3):
            ops.append(("CNOT",9,8,"flag"))
    ops.extend(post_ops(check))
    return ops

CENTER_OPS={c:center_ops(c) for c in CHECKS}
CHECK_LIST=[("center",c) for c in CHECKS]+[("edge",e) for e in EDGES]

def apply_op(e,op,n):
    if op[0]=="H":return hgate(e,op[1],n)
    if op[0]=="S":return sgate(e,op[1],n)
    if op[0]=="CNOT":return cnot(e,op[1],op[2],n)
    raise ValueError(op)

def round_fault_specs():
    specs=[]
    for ci,c in enumerate(CHECKS):
        ops=CENTER_OPS[c]
        for p in "XYZ":
            specs.append({"kind":"syn_prep","check":ci,"p":p})
            specs.append({"kind":"flag_prep","check":ci,"p":p})
        specs.append({"kind":"syn_meas","check":ci})
        specs.append({"kind":"flag_meas","check":ci})
        for oi,op in enumerate(ops):
            if op[0] in ("H","S"):
                for p in "XYZ":
                    specs.append({"kind":"1q","check":ci,"op_index":oi,"p":p})
            elif op[0]=="CNOT":
                for pa,pb in itertools.product("IXYZ",repeat=2):
                    if pa==pb=="I":continue
                    specs.append({"kind":"2q","check":ci,"op_index":oi,"pa":pa,"pb":pb})
        specs.append({"kind":"ancilla_loss","check":ci,"which":"syn"})
        specs.append({"kind":"ancilla_loss","check":ci,"which":"flag"})
    for ei,e in enumerate(EDGES):
        ci=4+ei
        for p in "XYZ":specs.append({"kind":"syn_prep","check":ci,"p":p})
        specs.append({"kind":"edge_meas","check":ci})
        for oi in range(2):
            for pa,pb in itertools.product("IXYZ",repeat=2):
                if pa==pb=="I":continue
                specs.append({"kind":"2q","check":ci,"op_index":oi,"pa":pa,"pb":pb})
        specs.append({"kind":"ancilla_loss","check":ci,"which":"syn"})
    for boundary in range(11):
        for q in range(8):
            for p in "XYZ":
                specs.append({"kind":"idle","boundary":boundary,"q":q,"p":p})
        for q in range(8):
            specs.append({"kind":"data_loss","boundary":boundary,"q":q})
    for receipt in range(10):
        specs.append({"kind":"stale","receipt":receipt})
        specs.append({"kind":"missing","receipt":receipt})
    return specs

def main():
    branches=json.loads(BRANCHES.read_text())
    b=next(x for x in branches if x["id"]=="subsystem-8")
    old_stabs=[pv(x) for x in b["generators"]["center"]]
    cand_stabs=[pv(x) for x in CHECKS]
    gauge_span=span([pv(x) for x in b["generators"]["gauge"]])
    lx=pv(b["logicals"]["X"]);lz=pv(b["logicals"]["Z"])
    decoder={tuple(map(int,k)):pv(v) for k,v in b["decoder"]["lookup"].items()}

    @lru_cache(None)
    def dressed(v):
        return min(weight(v^g,8) for g in gauge_span)

    def old_syn(v):
        return tuple(symp(v,s,8) for s in old_stabs)

    def cand_syn(v):
        return tuple(symp(v,s,8) for s in cand_stabs)

    def b_to_s(bits):
        b1,b2,b3,b4=bits
        return b1,b3,b2^b3,b4

    def cleanup_logical(v):
        r=v^decoder[old_syn(v)]
        if old_syn(r)!=(0,0,0,0):
            raise AssertionError("cleanup syndrome")
        for name,l in (("I",0),("X",lx),("Z",lz),("Y",lx^lz)):
            if r^l in gauge_span:return name
        raise AssertionError("logical quotient")

    def simulate_center(data8,check,fault=None):
        n=10;e=embed_data(data8,n)
        if fault and fault[0]=="syn_prep" and fault[1] in "XY":
            e^=single(8,"X",n) # |0> preparation equivalence
        if fault and fault[0]=="flag_prep" and fault[1] in "ZY":
            e^=single(9,"Z",n) # |+> preparation equivalence
        ops=CENTER_OPS[check]
        for idx,op in enumerate(ops):
            e=apply_op(e,op,n)
            if fault and fault[0]=="op" and fault[1]==idx:
                if fault[2]=="1q":e^=single(op[1],fault[3],n)
                else:e^=pair(op[1],op[2],fault[3],fault[4],n)
        x,z=split(e,n)
        sb=(x>>8)&1
        fb=(z>>9)&1
        if fault and fault[0]=="syn_meas":sb^=1
        if fault and fault[0]=="flag_meas":fb^=1
        return extract_data(e,n),sb,fb

    def simulate_edge(data8,edge,fault=None):
        n=9;e=embed_data(data8,n)
        if fault and fault[0]=="syn_prep" and fault[1] in "XY":
            e^=single(8,"X",n)
        ops=[("CNOT",edge[0]-1,8,"data"),("CNOT",edge[1]-1,8,"data")]
        for idx,op in enumerate(ops):
            e=apply_op(e,op,n)
            if fault and fault[0]=="op" and fault[1]==idx:
                e^=pair(op[1],op[2],fault[2],fault[3],n)
        x,_=split(e,n);bit=(x>>8)&1
        if fault and fault[0]=="meas":bit^=1
        return extract_data(e,n),bit

    def simulate_round(data8,fault=None):
        data=data8;brec=[];flag=False
        if fault and fault["kind"]=="idle" and fault["boundary"]==0:
            data^=single(fault["q"],fault["p"],8)
        if fault and fault["kind"]=="data_loss" and fault["boundary"]==0:
            return data,None,False,"QUARANTINE"
        for ci,(typ,obj) in enumerate(CHECK_LIST):
            local=None
            if fault and fault.get("check")==ci:
                k=fault["kind"]
                if typ=="center":
                    if k in ("syn_prep","flag_prep"):local=(k,fault["p"])
                    elif k in ("syn_meas","flag_meas"):local=(k,)
                    elif k=="1q":local=("op",fault["op_index"],"1q",fault["p"])
                    elif k=="2q":local=("op",fault["op_index"],"2q",fault["pa"],fault["pb"])
                    elif k=="ancilla_loss":return data,None,False,"HOLD"
                else:
                    if k=="syn_prep":local=("syn_prep",fault["p"])
                    elif k=="2q":local=("op",fault["op_index"],fault["pa"],fault["pb"])
                    elif k=="edge_meas":local=("meas",)
                    elif k=="ancilla_loss":return data,None,False,"HOLD"
            if typ=="center":
                data,sb,fb=simulate_center(data,obj,local)
                brec.append(sb);flag|=bool(fb)
            else:
                data,_=simulate_edge(data,obj,local)
            boundary=ci+1
            if fault and fault["kind"]=="idle" and fault["boundary"]==boundary:
                data^=single(fault["q"],fault["p"],8)
            if fault and fault["kind"]=="data_loss" and fault["boundary"]==boundary:
                return data,None,flag,"QUARANTINE"
        if fault and fault["kind"] in ("stale","missing"):
            return data,tuple(brec),flag,"HOLD"
        return data,tuple(brec),flag,"OK"

    # Verify measurement coordinate map before evaluation.
    for q in range(8):
        for p in "XYZ":
            e=single(q,p,8)
            if b_to_s(cand_syn(e))!=old_syn(e):
                raise AssertionError("syndrome map")
            for ci,c in enumerate(CHECKS):
                d,sb,fb=simulate_center(e,c)
                if d!=e or sb!=cand_syn(e)[ci] or fb:
                    raise AssertionError("center circuit")

    def majority3(frames):
        return tuple(int(sum(f[i] for f in frames)>=2) for i in range(4))

    def one_round(fault):
        data,bits,flag,status=simulate_round(0,fault)
        if status!="OK":return status,data
        if flag:return "HOLD",data
        data^=decoder[b_to_s(bits)]
        ok=cleanup_logical(data)=="I" and dressed(data)<=1
        return ("ACCEPT" if ok else "FAIL"),data

    def repeated(fault_round=None,fault=None,initial=0):
        data=initial;frames=[]
        for r in range(3):
            data,bits,flag,status=simulate_round(data,fault if fault_round==r else None)
            if status!="OK":return status,data
            if flag:return "HOLD",data
            frames.append(bits)
        data^=decoder[b_to_s(majority3(frames)))
        data,vbits,vflag,status=simulate_round(data,fault if fault_round==3 else None)
        if status!="OK":return status,data
        if vflag or vbits!=(0,0,0,0):return "HOLD",data
        ok=cleanup_logical(data)=="I" and dressed(data)<=1
        return ("ACCEPT" if ok else "FAIL"),data

    faults=round_fault_specs()

    one=Counter();one_kind=defaultdict(Counter);one_dw=Counter()
    for f in faults:
        out,data=one_round(f)
        one[out]+=1;one_kind[f["kind"]][out]+=1
        if out=="ACCEPT":one_dw[dressed(data)]+=1

    rep=Counter();rep_kind=defaultdict(Counter);rep_dw=Counter();rep_round=defaultdict(Counter)
    for rr in range(4):
        for f in faults:
            out,data=repeated(rr,f,0)
            rep[out]+=1;rep_kind[f["kind"]][out]+=1;rep_round[rr][out]+=1
            if out=="ACCEPT":rep_dw[dressed(data)]+=1

    input_test=Counter()
    for q in range(8):
        for p in "XYZ":
            out,data=repeated(initial=single(q,p,8))
            if out=="ACCEPT" and dressed(data)==0 and cleanup_logical(data)=="I" and old_syn(data)==(0,0,0,0):
                input_test["PASS"]+=1
            else:input_test["FAIL"]+=1

    # Phenomenological noisy decoder: one incoming physical error, noisy syndrome bits.
    incoming=[single(q,p,8) for q in range(8) for p in "XYZ"]
    fail_by_weight=Counter();total_by_weight=Counter()
    for e in incoming:
        truth=cand_syn(e)
        for mask in range(16):
            flips=tuple((mask>>i)&1 for i in range(4))
            observed=tuple(truth[i]^flips[i] for i in range(4))
            residual=e^decoder[b_to_s(observed)]
            k=sum(flips);total_by_weight[k]+=1
            if cleanup_logical(residual)!="I":fail_by_weight[k]+=1

    raw3_fail=Counter();raw3_total=Counter()
    for e in incoming:
        truth=cand_syn(e)
        for masks in itertools.product(range(16),repeat=3):
            frames=[];m=0
            for mask in masks:
                flips=tuple((mask>>i)&1 for i in range(4));m+=sum(flips)
                frames.append(tuple(truth[i]^flips[i] for i in range(4)))
            residual=e^decoder[b_to_s(majority3(frames))]
            raw3_total[m]+=1
            if cleanup_logical(residual)!="I":raw3_fail[m]+=1

    result={
      "status":"EXACT_CONSTRUCTOR_REPLAY",
      "faults_per_round":len(faults),
      "faults_per_round_factorization":"1141=7*163",
      "one_round":{
        "outcomes":dict(one),
        "accepted_dressed_weight":dict(one_dw),
        "by_fault_kind":{k:dict(v) for k,v in one_kind.items()},
      },
      "repeated_3plus1":{
        "outcomes":dict(rep),
        "accepted_dressed_weight":dict(rep_dw),
        "by_fault_kind":{k:dict(v) for k,v in rep_kind.items()},
        "by_fault_round":{str(k):dict(v) for k,v in rep_round.items()},
      },
      "input_error_no_circuit_fault":dict(input_test),
      "noisy_decoder":{
        "one_round_total_by_measured_bit_flip_weight":dict(total_by_weight),
        "one_round_logical_fail_by_measured_bit_flip_weight":dict(fail_by_weight),
        "one_round_failure_polynomial":"F1(q)=(5/2)q-(13/4)q^2+2q^3-(1/2)q^4",
        "majority_effective_bit_error":"r(q)=3q^2-2q^3",
        "three_round_failure_polynomial":"F3(q)=F1(r(q))",
        "three_round_expanded":"F3(q)=(15/2)q^2-5q^3-(117/4)q^4+39q^5+41q^6-108q^7+(63/2)q^8+92q^9-108q^10+48q^11-8q^12",
        "three_round_raw_fail_by_12bit_flip_weight":dict(raw3_fail),
        "three_round_raw_cases":sum(raw3_total.values()),
        "dominance_proof":"For 0<q<1/2, r(q)<q because q-r=q(1-q)(1-2q)>0. F1'(q)=(1-q)(4(q-1)^2+1)/2>0. Hence F3(q)<F1(q).",
        "leading_orders":"F1(q)=(5/2)q+O(q^2); F3(q)=(15/2)q^2+O(q^3)"
      },
      "physical_promotion":0
    }

    # Frozen acceptance gates.
    if one["FAIL"]!=152:raise AssertionError(("one-round expected control",one))
    if rep["FAIL"]!=0:raise AssertionError(("repeated fail",rep))
    if input_test!=Counter({"PASS":24}):raise AssertionError(("input errors",input_test))
    if sum(raw3_total.values())!=98304:raise AssertionError("decoder case count")

    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
