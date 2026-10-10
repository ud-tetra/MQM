# MQM v0.9 measurement-bound scheduling and complete 16-site geometric proposal

Date: 2026-10-10. Physical promotion 0.

Parent: research/bridges/2026-10-09_MQM_CLIFFORD_DAG_REORDER_AUDIT_v0.8.md
Source: research/benchmarks/2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp
Implementation: python local source-defined H/S/CNOT DAG; exact Pauli generator conjugation for per-check relabeling; unit-time operations. Preserve measurement/reset lifetime barrier between successive center checks.

EXACT within model: 65 center Clifford operations (27 CNOTs). Optimal-as-soon-as-possible per-check DAG layers under resource and noncommutation edges are [7,8,8,11] for both frozen 2-ancilla reuse and 8-ancilla dedicated-per-check relabeling. Total 34 abstract Clifford layers, excluding actual measurement/reset latency and hardware operation durations. Thus v0.8's 29 versus 24 layer comparison was NOT an instrument-preserving benchmark: it omitted check lifecycle barriers. No dedicated speed advantage certified. This is not a global optimization over circuit redesigns.

Fault equivalence: NOT RUN for full single-fault / flag/readout/reset/idle/erasure/conditional 2+PV instrument. Local Pauli relabeling matches per check; this is narrower than detector or FTEC equivalence. Full noisy branch CP maps and minimal retained observables OPEN.

3D exploration: proposed 8 data sites consist of a regular tetrahedron of unit edges plus four illustrative shell coordinates; 8 dedicated ancilla sites offset from check-specific mean data coordinates. First coordinate candidate had exactly coincident sites (NO-GO). Revised candidate minimum pair distance approximately 0.38379682124790976 coordinate units; maximum required data-syndrome geometric separation approximately 1.9479273284565766 units. This is geometry-only; 8-data shell does not establish exact native tri-tetra interaction edge realization, and no calibrated trap range/minimum separation/route constraints supplied. No hardware benefit claimed.

Replay script and result: local files mqm_v09.py and mqm_v09_results.json; source module dependency research/bridges/2026-10-09_MQM_FULL_CLIFFORD_SCHEDULE_NO_GO_v0.7.md. No measured hardware data used. Full 2+PV fault equivalence and complete 3D placement optimization remain OPEN. Physical promotion zero.