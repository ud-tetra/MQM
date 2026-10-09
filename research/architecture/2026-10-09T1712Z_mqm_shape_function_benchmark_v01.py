#!/usr/bin/env python3
import itertools, json, math
from fractions import Fraction

def graph_cycle(n):
    return {i:{(i-1)%n,(i+1)%n} for i in range(n)}
def graph_K4():
    return {i:{j for j in range(4) if j!=i} for i in range(4)}
def graph_octa():
    opp={(0,1),(1,0),(2,3),(3,2),(4,5),(5,4)}
    return {i:{j for j in range(6) if j!=i and (i,j) not in opp} for i in range(6)}
def graph_metrics(g):
    n=len(g); ds=[]
    for i in range(n):
        dist={i:0}; q=[i]
        for u in q:
            for v in g[u]:
                if v not in dist:
                    dist[v]=dist[u]+1; q.append(v)
        for j in range(i+1,n): ds.append(dist[j])
    E=sum(len(v) for v in g.values())//2
    lam=E
    edges=[(i,j) for i in range(n) for j in g[i] if i<j]
    for mask in range(1,(1<<n)-1):
        cut=sum(1 for i,j in edges if ((mask>>i)&1)!=((mask>>j)&1))
        if cut: lam=min(lam,cut)
    return {"V":n,"E":E,"beta1":E-n+1,"diameter":max(ds),"average_pair_distance":sum(ds)/len(ds),"edge_connectivity":lam}

graphs={"D5":graph_cycle(5),"D6":graph_cycle(6),"A4":graph_K4(),"S4":graph_octa()}
gm={k:graph_metrics(v) for k,v in graphs.items()}
assert gm["D5"]["average_pair_distance"]==1.5
assert gm["D6"]["average_pair_distance"]==1.8
assert gm["A4"]["average_pair_distance"]==1.0
assert gm["S4"]["average_pair_distance"]==1.2
assert [gm[x]["edge_connectivity"] for x in ("D5","D6","A4","S4")]==[2,2,3,4]

packing={
  "D5":{"exact":"2/sqrt(3+2/sqrt(5))","value":2/math.sqrt(3+2/math.sqrt(5))},
  "D6":{"exact":"sqrt(5)/2","value":math.sqrt(5)/2},
  "A4":{"exact":"sqrt(8/3)","value":math.sqrt(8/3)},
  "S4":{"exact":"2","value":2.0}
}

transport={
  "D5":{"geometric_single_cycle_order":5,"geometric_pass":True,"current_MQM_transition_lift":False,"reason":"monomial LC transition group has no order-5 element"},
  "D6":{"geometric_single_cycle_order":6,"geometric_pass":True,"current_MQM_transition_lift":True,"reason":"exact order-6 D6 frame generator exists"},
  "A4":{"geometric_single_cycle_order":None,"geometric_pass":False,"current_MQM_transition_lift":False,"reason":"A4 has no order-4 element acting as a four-module cycle"},
  "S4":{"geometric_single_cycle_order":None,"geometric_pass":False,"current_MQM_transition_lift":False,"reason":"S4 has no order-6 element acting as a six-module cycle"}
}

for k in gm:
    gm[k]["receipt_code_distance"]=gm[k]["edge_connectivity"]
    gm[k]["guaranteed_edge_bit_detection_weight_lt"]=gm[k]["edge_connectivity"]

out={
 "version":"0.1",
 "status":"EXACT_STRUCTURAL_SHAPE_FUNCTION_BENCHMARK",
 "physical_promotion":0,
 "packing_uniformity":packing,
 "coordination_graph_metrics":gm,
 "cyclic_transport":transport,
 "function_winners":{
   "packing_uniformity":"D5",
   "coordination_average_pair_distance":"A4",
   "cyclic_transport_with_current_MQM_code_frame_lift":"D6",
   "receipt_redundancy_distance":"S4"
 },
 "claim_boundary":"Function-specific structural winners only; no overall architecture or hardware winner."
}
print(json.dumps(out,indent=2,sort_keys=True))
