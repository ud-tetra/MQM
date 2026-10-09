# MQM v0.8 Clifford reorder and 3D reference audit

Date 2026-10-09. Physical promotion 0. Source: frozen research/benchmarks/2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp. Reuses source center checks, gate order and H/S/CNOT semantics. Append-only successor to v0.7.

Exact finite computational result: 65 source center-check Clifford operations, 27 CNOT. Build original-order pairwise DAG edges when operations share a physical qubit OR Pauli-conjugation does not commute. Greedy earliest-as-possible layering under unit-duration assumption gives 29 layers using syndrome/flag ancillas 8,9; hypothetical dedicated check-wise ancillas 8+2i,9+2i gives 24 layers. Full X/Z generator conjugation matches original for each relabeling under corresponding Pauli space, modulo global Clifford phase. Gate-based depth difference 5/29, not a measured improvement. Both reorderings can cross original measurement/reset boundaries because those barriers are deliberately absent: NOT an instrument-equivalent or fault-tolerant circuit claim.

Prior v0.7 56/56 layers remain EXACT under the stronger intra-check source-order constraint. Prior 27/12 CNOT-only figures remain scoped CNOT-only. No contradictory theorem.

Quantum fault gate: full branch-resolved noisy CP map, flag/readout/reset, idle, erasures and complete 2+PV fault equivalence NOT EXECUTED. Source-preserving gate tableau alone cannot promote FTEC. Introduce barrier nodes for measurement/reset and ancilla lifetime, then replay matched full single-fault outcome ledger.

3D reference: K4 regular tetrahedron of unit edge length, vertices (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1) scaled by 1/sqrt(8). Four optional ancilla trial positions at face centroids plus outward normal offset 0.35. Not an embedding of all 8 data/8 ancilla sites, nor a calibrated placement. Target backend coordinates, connectivity, MOVE loss, collision spacing and timing SOURCE_BLOCKED.

Prior baseline and stop rules unchanged. Hardware validation, threshold, advantage OPEN. Physical promotion 0.
