#!/usr/bin/env python3
"""Exact GF(2) firewall/schedule-support audit for MQM subsystem-8.

This script deliberately does NOT reconstruct the archived v0.2 gate schedule.
It audits schedule-independent invariants and an equivalent center-generator
basis directly from release/branches.json.

Evidence types:
- exact Pauli/subsystem algebra and finite enumeration;
- exact locked tri-tetra graph combinatorics from the declared tetrahedra;
- no hardware or finite-time noise-rate claim.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BRANCHES = ROOT / "release" / "branches.json"

CORE_PHYS = (1,2,3,8)
SHELL_PHYS = (4,5,6,7)
TETS = {
    "T_C": (1,2,3,8),
    "T_plus": (5,6,7,8),
    "T_minus": (4,6,7,8),
}

def pauli_vec(s: str) -> int:
    n=len(s); x=z=0
    for i,ch in enumerate(s):
        if ch in "XY": x |= 1<<i
        if ch in "ZY": z |= 1<<i
    return x | (z<<n)

def split(v: int, n: int):
    mask=(1<<n)-1
    return v&mask,(v>>n)&mask

def pauli_str(v: int, n: int) -> str:
    x,z=split(v,n); out=[]
    for i in range(n):
        out.append({(0,0):"I",(1,0):"X",(0,1):"Z",(1,1):"Y"}[((x>>i)&1,(z>>i)&1)])
    return "".join(out)

def symp(a: int,b: int,n: int) -> int:
    ax,az=split(a,n); bx,bz=split(b,n)
    return (((ax&bz).bit_count()+(az&bx).bit_count())&1)

def span(vals):
    out={0}
    for b in vals: out |= {x^b for x in tuple(out)}
    return out

def rank4(vals):
    rows=list(vals); r=0
    for bit in (8,4,2,1):
        p=next((i for i in range(r,len(rows)) if rows[i]&bit),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and rows[i]&bit: rows[i]^=rows[r]
        r+=1
    return r

def tet_edges(tet):
    return {tuple(sorted(e)) for e in itertools.combinations(tet,2)}

def main():
    branches=json.loads(BRANCHES.read_text())
    b=next(x for x in branches if x["id"]=="subsystem-8")
    n=b["n_data"]
    stabs=[pauli_vec(s) for s in b["generators"]["center"]]
    gauges=[pauli_vec(s) for s in b["generators"]["gauge"]]
    gauge_span=span(gauges)
    lx=pauli_vec(b["logicals"]["X"]); lz=pauli_vec(b["logicals"]["Z"])
    decoder={tuple(map(int,k)):pauli_vec(v) for k,v in b["decoder"]["lookup"].items()}

    def syndrome(v): return tuple(symp(v,s,n) for s in stabs)
    def lclass(v):
        for nm,l in (("I",0),("X",lx),("Z",lz),("Y",lx^lz)):
            if v^l in gauge_span: return nm
        raise AssertionError("residual outside logical quotient")

    core={i-1 for i in CORE_PHYS}; shell={i-1 for i in SHELL_PHYS}

    center=[]
    for coeff in range(1,16):
        v=0
        for k,s in enumerate(stabs):
            if coeff>>k&1: v^=s
        ps=pauli_str(v,n)
        supp={i for i,ch in enumerate(ps) if ch!="I"}
        center.append({
            "coeff":coeff,"pauli":ps,
            "core_count":len(supp&core),"shell_count":len(supp&shell),
            "weight":len(supp),"cross":bool(supp&core and supp&shell),
            "hub8":7 in supp,
        })
    byc={e["coeff"]:e for e in center}
    shell_only=[e["coeff"] for e in center if e["core_count"]==0]
    hub_avoiding=[e["coeff"] for e in center if not e["hub8"]]
    shell_only_rank=rank4(shell_only)
    hub_avoiding_rank=rank4(hub_avoiding)
    assert shell_only_rank==2 and hub_avoiding_rank==2

    bases=[]
    for comb in itertools.combinations(center,4):
        coeffs=[e["coeff"] for e in comb]
        if rank4(coeffs)<4: continue
        score=(sum(e["cross"] for e in comb),
               sum(e["core_count"] for e in comb),
               sum(e["weight"] for e in comb),
               max(e["weight"] for e in comb),
               sum(e["hub8"] for e in comb))
        bases.append((score,coeffs))
    opt_score=min(score for score,_ in bases)
    optimal=[coeffs for score,coeffs in bases if score==opt_score]

    current=(1,2,4,8)
    candidate=(1,6,2,8)
    def metrics(coeffs):
        es=[byc[c] for c in coeffs]
        return {
            "coeffs":list(coeffs),"paulis":[e["pauli"] for e in es],
            "cross_checks":sum(e["cross"] for e in es),
            "hub8_checks":sum(e["hub8"] for e in es),
            "core_incidences":sum(e["core_count"] for e in es),
            "shell_incidences":sum(e["shell_count"] for e in es),
            "total_pauli_weight":sum(e["weight"] for e in es),
            "weights":[e["weight"] for e in es],
        }
    curm=metrics(current); candm=metrics(candidate)
    assert curm["cross_checks"]==3 and candm["cross_checks"]==2
    assert curm["hub8_checks"]==3 and candm["hub8_checks"]==2
    assert curm["total_pauli_weight"]==candm["total_pauli_weight"]==19

    new_decoder={}
    for sold,corr in b["decoder"]["lookup"].items():
        s=tuple(map(int,sold)); nb=(s[0],s[1]^s[2],s[1],s[3])
        new_decoder["".join(map(str,nb))]=corr
    assert len(new_decoder)==16

    one_shell=Counter(); one_shell_by_site={p:Counter() for p in SHELL_PHYS}
    for chars in itertools.product("IXYZ",repeat=4):
        s=["I"]*n
        for i,ch in zip(sorted(core),chars): s[i]=ch
        for p in SHELL_PHYS:
            for q in "XYZ":
                ss=s.copy(); ss[p-1]=q
                e=pauli_vec("".join(ss)); r=e^decoder[syndrome(e)]
                c=lclass(r); one_shell[c]+=1; one_shell_by_site[p][c]+=1
    assert one_shell==Counter({"I":768,"X":768,"Y":768,"Z":768})

    E=set()
    for tet in TETS.values(): E |= tet_edges(tet)
    cc={e for e in E if e[0] in CORE_PHYS and e[1] in CORE_PHYS}
    ss={e for e in E if e[0] in SHELL_PHYS and e[1] in SHELL_PHYS}
    cs=E-cc-ss
    assert len(E)==15 and len(cc)==6 and len(cs)==4 and len(ss)==5
    assert cs=={(4,8),(5,8),(6,8),(7,8)}

    result={
        "status":"EXACT_CONSTRUCTOR_REPLAY",
        "scope":"schedule-independent code/graph invariants; archived v0.2 gate-list location audit remains source-blocked",
        "center_basis":{
            "shell_only_subspace_rank":shell_only_rank,
            "hub8_avoiding_subspace_rank":hub_avoiding_rank,
            "minimum_cross_checks_in_any_center_basis":2,
            "minimum_hub8_checks_in_any_center_basis":2,
            "current":curm,
            "candidate":candm,
            "candidate_new_decoder":dict(sorted(new_decoder.items())),
            "syndrome_map":"b=(s1,s2 xor s3,s2,s4); inverse s=(b1,b3,b2 xor b3,b4)",
            "optimal_basis_count_under_lexicographic_score":len(optimal),
            "optimal_score_tuple":"(cross_checks,core_incidences,total_weight,max_weight,hub8_checks)",
            "optimal_score":list(opt_score),
        },
        "core_plus_one_shell_pauli":{
            "patterns":3072,
            "logical_classes":dict(one_shell),
            "per_shell_site":{str(k):dict(v) for k,v in one_shell_by_site.items()},
            "interpretation":"uniform Pauli-basis enumeration only; not a physical probability distribution",
        },
        "tri_tetra_graph":{
            "edges_total":15,"core_core_edges":6,"core_shell_edges":4,"shell_shell_edges":5,
            "core_shell_cut_edges":[list(e) for e in sorted(cs)],
            "all_cut_edges_incident_to_hub8":True,
            "equal_edge_structural_eta_shell":"(4+5)/15=3/5",
            "equal_edge_structural_eta_escape_given_core_touch":"4/(6+4)=2/5",
            "physical_eta_out":"OPEN: requires source-bound edge/process weights",
        },
        "physical_promotion":0,
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__": main()
