#!/usr/bin/env python3
import itertools,json,math
from collections import Counter

def cut_code(n,edges):
    words=set()
    for bits in itertools.product((0,1),repeat=n):
        words.add(tuple(bits[i]^bits[j] for i,j in edges))
    weights=[sum(w) for w in words if any(w)]
    return {"length":len(edges),"dimension":int(round(math.log2(len(words)))),"distance":min(weights),"nonzero_weight_spectrum":dict(sorted(Counter(weights).items()))}

k4=list(itertools.combinations(range(4),2))
line=[]
for i,e in enumerate(k4):
    for j,f in enumerate(k4):
        if i<j and set(e)&set(f): line.append((i,j))
deg=[sum(v in e for e in line) for v in range(6)]
assert len(k4)==6 and len(line)==12 and deg==[4]*6
native=cut_code(4,k4)
aug=cut_code(6,line)
assert native["length"]==6 and native["dimension"]==3 and native["distance"]==3
assert aug["length"]==12 and aug["dimension"]==5 and aug["distance"]==4
out={
 "version":"0.1","status":"EXACT_COMPOSITE_RECEIPT_OVERLAY","physical_promotion":0,
 "A4_module_graph":{"vertices":4,"edges":6},
 "S4_overlay":{"vertices":6,"edges":12,"degrees":deg,"identity":"line graph L(K4) is the octahedron graph"},
 "native_K4_interface_receipt_code":native,
 "augmented_octahedral_receipt_code":aug,
 "typed_counts":{"D5_cells_per_A4_module":5,"A4_modules":4,"D5_local_cells_total":20,"D6_frame_phases_per_module":6,"module_frame_states":24,"D5_A4_D6_typed_addresses":120},
 "scope":"binary receipt topology only; not quantum-code distance or hardware performance"
}
print(json.dumps(out,indent=2,sort_keys=True))
