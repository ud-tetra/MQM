# MQM Symbolic Two-Fault Interpretation Confirmation v0.1

**Date:** 2026-10-08
**Status:** INTERPRETATION CONFIRMATION / NO DATA CHANGE
**Physical promotion:** 0
**Parent comparison:** research/benchmarks/2026-10-08T1810Z_MQM_SYMBOLIC_TWO_FAULT_COMPARISON_v0.1.md
**Parent result:** research/benchmarks/2026-10-08T1741Z_MQM_SYMBOLIC_MALIGNANT_PAIR_RESULTS_v0.1.json

## Confirmed scope

The frozen pair workloads are:

\[
623245,\qquad5639658,\qquad10032826
\]

for \(1+0,2+1,3+1\).

The accepted-logical-error difference is exactly

\[
\epsilon_{L|A}^{3+1}-\epsilon_{L|A}^{2+1}
=
\frac{66693}{5}p^2+\frac{277}{15}pq+O(3),
\]

because

\[
\frac{3734566-733381}{225}
=
\frac{66693}{5},
\qquad
\frac{296-19}{15}
=
\frac{277}{15}.
\]

Thus through total degree two,

\[
\epsilon_{L|A}^{3+1}>
\epsilon_{L|A}^{2+1}
\]

for every \(p>0,\ q\ge0\).

The \(1+0\) protocol alone retains a first-order accepted-logical term:

\[
\epsilon_{L|A}^{1+0}
=
\frac{412}{15}p+O(2).
\]

## Acceptance and loss interpretation

The first-order loss coefficients in \(Y\),

\[
102,\qquad306,\qquad408,
\]

equal the frozen ideal-detected loss-location counts for \(1,3,4\) rounds respectively.

The first-order \(p\) and \(q\) coefficients are smaller than their corresponding location counts because some such elementary faults still produce ACCEPT outcomes.

This is an internal consistency check, not a hardware calibration.

## Pareto ruling

The frozen degree-two result does not establish an architecture winner.

- \(1+0\) has the strongest first-order acceptance but retains first-order accepted-logical error.
- \(2+1\) suppresses accepted-logical error to second order and has the lowest degree-two accepted-logical coefficients of the repeated branches.
- \(3+1\) rejects slightly less aggressively in the first-order \(p\) and \(q\) coefficients than \(2+1\), but carries one additional round of ideal-detected loss exposure and larger degree-two accepted-logical coefficients.

The comparison remains Pareto-valued across

\[
Y,\qquad
\epsilon_{L|A},\qquad
Y_{\rm good},\qquad
\text{resource cost}.
\]

## Grid interpretation

The frozen \(125=5^3\) hardware-neutral grid remains unevaluated.

At

\[
p=q=p_{\rm loss}=2^{-15},
\]

the \(3+1\) sum of elementary-event probabilities is

\[
1180\,2^{-15}
=
\frac{295}{8192}
\approx0.0360107421875.
\]

This is an expected elementary-event-count diagnostic under the independent-location model.

Substitution of the already-exposed degree-two polynomial on the grid would be expository only and would not constitute new evidence.

A full higher-order stochastic run on the same frozen grid is a separate confirmatory task.

## Independent-check scope

The Fraction-based implementation independently checks:

- coefficient aggregation from primary raw conditional sums;
- the partition
  \[
  Y+P_{\rm HOLD}+P_{\rm QUARANTINE}=1+O(3);
  \]
- rational quotient construction for \(\epsilon_{L|A}\);
- other derived series.

It is **not** an independently implemented fault-pair classifier.

The implementation-repair ledger remains material provenance:

- syndrome-key coordinate ordering was repaired;
- the Pauli state container was enlarged from an insufficient 16-bit representation to a 20-bit-capable implementation for the 10-qubit data+ancilla symplectic state.

The latter defect would have suppressed flag propagation if left unfixed.

## Promotion ledger

- Degree-two comparison: **EXACT SAME-AGENT**
- Separate coefficient aggregation: **EXACT SAME-AGENT CHECK**
- Architecture win: **OPEN**
- Higher-order ordering: **OPEN**
- Independent fault-pair classifier: **OPEN**
- Hardware-calibrated rates: **OPEN**
- Threshold: **OPEN**
- Hardware validation: **OPEN**
- Quantum advantage: **OPEN**
- Physical promotion: **0**
