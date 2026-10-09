# MQM v0.7 full-Clifford ordering amendment and architecture gates

Date: 2026-10-09. Physical promotion 0.
Sources: frozen research/benchmarks/2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp; prior v0.5 and v0.6 bridge audits.

## New exact finite scheduling result
Reconstructed source CAND center check circuits including H, S, and CX. Total 65 source Clifford operations, 27 CX. Compare frozen q8/q9 reuse to hypothetical separate syndrome/flag pairs (q8+2i,q9+2i), holding all source orders, same data qubits. Exact Pauli-conjugation commutation checks on X/Z generators give 86 cross-check noncommuting gate pairs in each model.
Using precedence for within-check source order, shared-qubit exclusivity, and source order for noncommuting gate pairs; unit duration for every Clifford operation; both designs require 56 abstract layers. Thus no improvement under this conservative full-Clifford scheduling policy despite prior restricted CNOT-only 27 to 12 difference. Not a global optimal scheduling proof.

## Fault and instrument status
Prior 405 CNOT Pauli data signatures match only within individual check boundaries. Complete single-fault event/flag/reset/verification 1-EC equivalence NOT EXECUTED. Full branch-resolved noisy CP maps and smallest Heisenberg-invariant observable space NOT CONSTRUCTED. Do not claim closure or distance-three FTEC for dedicated candidate.

## 3D placement gate
No source-backed neutral-atom coordinates, route exclusion volume, native gate ranges, movement losses, measured timings or correlated transport channels. D5 spare sites distinct from syndrome/flag ancillas. Placement comparisons remain CANDIDATE / SOURCE_BLOCKED. Geometry alone does not imply lower effective depth or logical error.

## Required next experiment
Create gate-level precedence DAG and separately freeze a lawful commutation-preserving reorder proposal with exact Clifford tableau equivalence and full instrument checks, including ancilla lifecycle boundaries. Test all expanded single faults and matched resource/survival against parent. Preserve v0.5/v0.6 hypotheses and previous results append-only.

Evidence: EXACT source-based finite commutation and abstract layering; NO-GO for claimed advantage under conservative ordering; all hardware claims OPEN.