# MQM v0.5 noisy-instrument / ancilla-concurrency / space-time audit

Date: 2026-10-09. Evidence EXACT finite resource-conflict enumeration; CANDIDATE alternative. Physical promotion 0.

Source: research/benchmarks/2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp, center OPS and ORDERS; previous research/bridges/2026-10-09_MQM_IDEAL_INSTRUMENT_GATE_CONFLICT_v0.4.md; calibrated hardware handoff research/hardware/2026-10-09T2145Z_MQM_MOVE_DECISION_CALIBRATION_PACKET_v0.1.json.

Track 1: Exact branch-resolved noisy CP map for 2+PV is NOT EXECUTED. Original Pauli-signature classifier and limited ideal 64-coordinate projective observable model do not certify a full noisy quantum instrument; leakage, loss, non-Pauli coherent faults and branch-conditioned CP-map invariant span remain unresolved. Neither minimality nor closure is promoted. Required next implementation: explicit trace-nonincreasing Kraus maps per gate, reset, ancilla readout, flag, recovery, verification; reverse Heisenberg span closure; independent checker.

Track 2: Frozen center extraction source contains 27 CNOTs. All touch syndrome ancilla q8 (zero based); all 351 unordered pairs conflict, so frozen CNOT-only disjoint-qubit layer count is exactly 27. A hypothetical 8-ancilla design (4 dedicated syndrome plus 4 dedicated flag), maintaining each check's listed CNOT order and relabeling its two ancillas, gives a dependency-only greedy CNOT layer depth of 12, adding 6 physical ancillas versus the frozen 2-ancilla reuse. This is an exploratory compile lower-cost candidate, NOT a circuit-equivalent, hook-safe, detector-equivalent or noise-equivalent result. Missing basis rotations, readout/reset, global interaction ordering, placement, crosstalk, routing and idle errors invalidate use as runtime/FT evidence.

Track 3: The controller can reference the resource candidate as metadata only. Its immutable ACCEPT/HOLD/QUARANTINE/RETRY_READY and 2+PV semantics are unchanged. D5 spare scheduling and D6-v128 motion choice remain source-bound to MOVE timing, state-retention, loss, dephasing, parallelism and correlated errors. No matched resource and reliability benchmark or source-bound space-time win executed.

Audit fingerprint for frozen check strings/order representation: e4cbb4f2808eeaa43a62c81b7e5d3bb6377a4f2b2c4813d58c348b1b730dfcab.
Claim status: frozen resource conflict EXACT; 12-layer hypothetical CANDIDATE; full noisy instrument OPEN; architecture performance SOURCE-BLOCKED; physical promotion 0.
