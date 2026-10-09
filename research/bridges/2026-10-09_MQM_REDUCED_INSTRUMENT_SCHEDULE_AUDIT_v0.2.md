# MQM reduced-instrument / interface composition / schedule audit v0.2

Date: 2026-10-09. Physical promotion: 0. Evidence: exact finite-field checks + algebraic composition criterion; NOT a full noisy-instrument closure certificate.

## Source
- Frozen subsystem code algebra: research/bridges/2026-10-07T1902Z_MQM_TETRA_GAUGE_CORE_NOISE_FIREWALL_THEOREM_v0.1.md
- Frozen 2+PV state machine: research/protocols/2026-10-08T2210Z_MQM_2PLUS_POSTRECOVERY_VERIFY_v0.3_FREEZE.json
- Previous 23D to 6D classical gate lift: research/bridges/2026-10-09_MQM_UD_23D_6D_GATE_INTERTWINING_v0.1.md

## Exact finite-field verification
Use Pauli strings S1=IIIXXZZI, S2=IIIYIYZZ, S3=IIIXZIXZ, S4=XXXXYYIX. Gauge X1, X2, X3, Z1Z8, Z2Z8, Z3Z8. Logical X=IIIYZIZI and Z=IIIXIZIZ.
- Stabilizer mutual commutation PASS.
- Stabilizer/gauge commutation PASS.
- Logical X/Z anticommutation PASS.
- Enumerate all 256 Pauli basis elements supported on T_C={1,2,3,8}: exactly four center-syndrome classes 0000, 0001, 0110, 0111.
- I, X_L and Z_L have identical center syndrome 0000: NO-GO for reconstructing arbitrary logical state from syndrome alone. This does NOT refute code-specific syndrome sufficiency for a declared restricted error and recovery instrument.

## Exact theorem: quotient instrument criterion
For a linear retention map R on operator/state space and quantum channels E_j (including branch-resolved trace-nonincreasing CP maps), a closed reduced operation exists only when ker(R) is invariant under every branch E_j on the admitted linear span (equivalently R E_j = F_j R for a well-defined linear F_j). Outcome probabilities additionally require that trace(E_j rho) factors through R. For classical histories the retention must include all branch information used by conditional controller transitions. Nonlinear conditioning after probability normalization is not licensed without branch weights.
If R E_1 = F_1 R and R E_2 = F_2 R, then R E_2 E_1 = F_2 F_1 R. Reordering requires F_2 F_1 = F_1 F_2 for reduced semantics, or full-channel commutation for full-state equivalence. Example H and phase-Clifford maps do not commute on Pauli X. Thus test pairwise reduced commutators and hardware resource overlap before allowing concurrency.

## Schedule partial order
Required precedence: R1 and R2 precede comparison; comparison precedes Pauli-frame recovery; nonzero agreed syndrome requires recovery before optional V; V precedes its ACCEPT gate; zero agreed syndrome may accept without V; flagged/ancilla loss must HOLD; detected data/hub loss QUARANTINE. No arbitrary numeric geometric interval follows from this DAG.
Native primitive duration, classical latency, MOVE/settle/reset/measurement time, spectator constraints and parallelism are still source-bound. A legal start time obeys t(v)>=max_{u->v}(t(u)+duration(u)+required latency(u,v)) and nonoverlapping resource occupancy. Without measured durations this determines ordering, not absolute timing.

## Verification boundary
Verified GF(2) finite checks and composition algebra; full syndrome/gauge/history quantum instrument kernel-invariance NOT RUN. Independent scientific review absent. No threshold, hardware validation, quantum advantage, or physical promotion.
