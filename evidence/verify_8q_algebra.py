"""Independent finite Pauli enumeration from the supplied 8Q generator strings.

Binary Pauli labels ignore global phases. This checks the subsystem algebra and
dressed distance, not physical implementation or fault-tolerant composition.
"""
from itertools import product
import json

N = 8
CENTER = ['IIIXXZZI', 'IIIYIYZZ', 'IIIXZIXZ', 'XXXXYYIX']
GAUGE = CENTER + ['XIIIIIII', 'ZIIIIIIZ', 'IXIIIIII', 'IZIIIIIZ', 'IIXIIIII', 'IIZIIIIZ']
LX, LZ = 'IIIYZIZI', 'IIIXIZIZ'

def bits(p):
    return sum((c in 'XY') << i for i, c in enumerate(p)) | (sum((c in 'YZ') << i for i, c in enumerate(p)) << N)

def symp(a, b):
    mask = (1 << N) - 1
    return (((a & mask) & (b >> N)).bit_count() + ((b & mask) & (a >> N)).bit_count()) % 2

def span(gens):
    values = {0}
    for g in gens:
        values |= {x ^ g for x in tuple(values)}
    return values

def check():
    gs, cs = list(map(bits, GAUGE)), list(map(bits, CENTER))
    group, center = span(gs), span(cs)
    actual_center = {x for x in group if all(symp(x, g) == 0 for g in gs)}
    assert actual_center == center
    assert len(group) == 1024 and len(center) == 16
    x, z = bits(LX), bits(LZ)
    assert all(symp(l, g) == 0 for l in (x, z) for g in gs)
    assert x not in group and z not in group and symp(x, z) == 1
    min_weight, witness, counts = N + 1, None, {}
    for labels in product('IXYZ', repeat=N):
        p = ''.join(labels)
        b = bits(p)
        if b not in group and all(symp(b, s) == 0 for s in cs):
            w = sum(c != 'I' for c in p)
            counts[w] = counts.get(w, 0) + 1
            if w < min_weight:
                min_weight, witness = w, p
    assert min_weight == 3
    for a, b in [(0,1),(0,2),(0,7),(1,2),(1,7),(2,7)]:
        p = ['I'] * N
        p[a] = p[b] = 'Z'
        assert bits(p) in group
    return {'n':8, 'k':1, 'gauge_qubits':3, 'dressed_distance':min_weight,
            'convention':'[[n,k,d,r]]', 'gauge_binary_rank':10, 'center_binary_rank':4,
            'distance_witness':witness, 'six_K4_Z_edges_in_gauge':True,
            'nontrivial_dressed_logical_counts_by_weight':counts,
            'physical_promotion':0, 'independent_replication':False}

if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
