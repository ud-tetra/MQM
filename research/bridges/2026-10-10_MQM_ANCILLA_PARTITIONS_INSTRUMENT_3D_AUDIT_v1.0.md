# MQM v1.0 — ancilla allocation, instrument gate, 3D radius audit

Date: 2026-10-10. Physical promotion 0. Append-only scoped continuation of v0.9.
Frozen source: research/benchmarks/2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp.

## Exact ancilla allocation enumeration
Four center checks assigned to k reusable syndrome/flag pairs, with k in {1,2,3,4}, up to pair relabeling. Set-partition multiplicities are 1,7,6,1 respectively, summing to Bell(4)=15. This assumes **complete measurement/reset lifecycle barrier after every check**, so no two checks overlap. Reconstruct all frozen within-check H/S/CNOT sequences; each allocation retains 65 total Clifford operations, 27 CX, and 34 unit-time Clifford layers. Per-check layers 7+8+8+11. Therefore 2 ancillas minimize ancilla count with no increased ideal depth in this frozen policy. This is not a general optimal circuit or full single-fault test; 4/6/8 ancilla alternatives do not inherit FTEC certificates automatically.

## Noisy quantum-channel instrument
FULL CP/KRAUS BRANCH MAPS NOT CONSTRUCTED. Exact obstruction: |+> and |-> have same retained Z expectation zero, yet P(X+=1) differs (1 vs 0). Any sufficient retained observable space V must satisfy E_j^dagger(V) subset V for every admitted branch j, retaining branch weights before conditional renormalization. The previous 64-coordinate ideal model has not been promoted to the noisy 2+PV circuit.

## 3D geometry
Reused v0.9 16-site coordinate proposal, distinct typed roles: 8 data + 8 ancilla. All-site minimum Euclidean separation 0.38379682124790976 dimensionless units. Required data-syndrome and flag-syndrome couplings: 23; maximum distance 1.9479273284565766. Count <= proposed dimensionless ranges: r=0.5:5, r=1.0:8, r=1.5:15, r=2.0:23. No target backend coordinates, native range, transport latency/loss or crosstalk verified. This is a diagnostic, not calibrated connectivity proof. Extra D5 spare roles remain separate from syndrome and flag ancillas.

Evidence level EXACT computational enumeration under frozen assumptions; insufficient for full instrument sufficiency, fault tolerance, or physical performance. Next: construct branch-resolved native circuit including measurement/reset, compare complete single faults for recompiled alternatives, then test source-calibrated 3D geometry. No claim promotion; physical promotion 0.
