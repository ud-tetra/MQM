# MQM Second-Order Motion / D5 Mapping / Instruction Audit v0.1

**Date:** 2026-10-09  
**Physical promotion:** 0

## 1. Second-order coherent motion

The frozen equal-dwell, ideal-instantaneous-control Magnus test computes

\[
\bar H^{(0)}=\frac1T\sum_j H_j,
\]

and

\[
\frac{\bar H^{(1)}}{\tau}
=
-\frac{i}{2T}
\sum_{j>k}[H_j,H_k].
\]

The complete coherent cycle uses the signed Pauli-conjugation period \(T_\pm\), not merely the phase-quotiented frame period.

Corrected physical primitive exposures are

\[
I:0,\qquad
a:6,\qquad
b:72,\qquad
ab:72,\qquad
zb:108.
\]

### Zeroth-order correlated weight-2 residual

\[
I:1,
\]

\[
a:\frac{65}{84},
\]

\[
b:\frac{55}{126},
\]

\[
ab:\frac{41}{84},
\]

\[
zb:\frac37.
\]

Thus \(zb\) remains the strongest first-order average suppressor in this frozen basis metric.

### Second-order two-term Magnus metric

Over all

\[
\binom{276}{2}=37950
\]

equal-weight two-term Pauli Hamiltonians:

\[
I:0,
\]

\[
a:\frac{127}{6325},
\]

\[
b:\frac{15616}{170775},
\]

\[
ab:\frac{933}{6325},
\]

\[
zb:\frac{31679}{170775}.
\]

The corresponding frozen crossover diagnostic

\[
\sqrt{A_0}
+
\eta\sqrt{A_1}
=1
\]

gives approximately:

- \(a\): \(0.8492\);
- \(b\): \(1.1221\);
- \(ab\): \(0.7847\);
- \(zb\): \(0.8018\).

This is not a rigorous Magnus convergence radius. It is a predeclared finite-dwell comparison diagnostic.

**Finding:** \(b\) has the widest second-order diagnostic margin among the nontrivial identity motions tested. \(zb\) has slightly stronger zeroth-order suppression but materially larger second-order correction and control exposure.

The motion \(ab\) is dominated by \(b\) under zeroth residual, second-order metric, exposure, and word length.

A useful structural detail is that \(a\) has zero second-order correction for every single weight-1 and weight-2 Pauli basis Hamiltonian; its nonzero second-order score arises only from cross-commutators in multi-term Hamiltonians.

## 2. D5 mapping to the subsystem-8 interaction graph

The frozen data interaction graph is the 15-edge union of the three tetrahedral sets

\[
T_C=\{1,2,3,8\},
\]

\[
T_+=\{5,6,7,8\},
\]

\[
T_-=\{4,6,7,8\}.
\]

The exact D5 fiber has seven vertices. The frozen eight-site candidate augments it with the midpoint \(O\) of the central edge and exhausts all

\[
8!=40320
\]

role-to-site bijections.

The best interaction-length uniformity has

\[
\boxed{
\kappa
=
\sqrt{\frac{5+\sqrt5}{2}}
\approx1.902113.
}
\]

Its coefficient of variation is approximately

\[
0.219929.
\]

One canonical optimal mapping is

\[
1\to O,\ 
2\to v_0,\ 
3\to v_1,\ 
4\to N,\ 
5\to v_2,\ 
6\to S,\ 
7\to v_3,\ 
8\to v_4.
\]

There are 960 tied optimum mappings under the frozen lexicographic metric.

The 15 required edges occupy distance classes

\[
3\times\csc(\pi/5),
\]

\[
5\times\sqrt{3+2/\sqrt5},
\]

\[
5\times2,
\]

and

\[
2\times(1+\sqrt5).
\]

The two shortest physical site pairs, of length 1, are unused by the required interaction graph in the canonical optimum.

The ideal tri-tetra carrier has every frozen required edge equal by construction:

\[
\kappa_{\rm tri}=1,
\qquad
CV_{\rm tri}=0.
\]

Therefore:

\[
\boxed{
\text{D5+midpoint is NO-GO as an improvement of the frozen 15-edge interaction-length uniformity.}
}
\]

This does not falsify D5 as a local metric fiber. It falsifies the stronger proposal that this natural eight-site D5 augmentation should replace the existing subsystem-8 interaction geometry for length uniformity.

## 3. Phase-A motion instruction set

The frozen Pareto search uses the current short-word library rather than claiming global optimality over all 1152 transitions.

### Logical identity front

The exact non-dominated motion choices are

\[
\boxed{I,\ a,\ b,\ zb}.
\]

The motion \(ab\) is dominated by \(b\).

Interpretation:

- \(I\): no control cost, no coherent suppression;
- \(a\): low exposure, modest suppression, small second-order burden;
- \(b\): strongest current balance between first-order suppression and second-order robustness;
- \(zb\): maximum zeroth-order suppression among this library, at the highest control and second-order cost.

### Nonidentity logical instructions

For the frozen short-word library, all hidden-frame \(h>1\) alternatives are dominated by the \(h=1\) representatives under the declared nonidentity objectives.

Canonical representatives are therefore:

\[
\boxed{
c:\ X_L\leftrightarrow Z_L
}
\]

and

\[
\boxed{
d:\ \text{logical three-cycle}.
}
\]

Both have abstract primitive cost 12 and word length 1.

### Carrier Pareto layer

Under literal-cell count, interface count, and receipt distance:

- \(A4\) is the low-overhead Pareto carrier;
- \(S4\) remains Pareto because receipt distance 4 trades against its 24-cell and 12-interface burden;
- \(D6\) is dominated by \(A4\) under this particular Pareto objective set.

That last result does **not** remove D6 from MQM. Its exact function-specific role is cyclic frame/address transport, which is outside this instruction-cost objective set.

## Current instruction grammar

The current scoped instruction library is:

\[
\text{IDLE}=I,
\]

\[
\text{LIGHT\_AVERAGE}=a,
\]

\[
\text{ROBUST\_AVERAGE}=b,
\]

\[
\text{MAX\_FIRST\_ORDER\_AVERAGE}=zb,
\]

\[
\text{LOGICAL\_SWAP}_{XZ}=c,
\]

\[
\text{LOGICAL\_CYCLE}_{XYZ}=d.
\]

These names describe mathematical roles only; they are not hardware ISA opcodes.

## Claim ledger

- second-order Magnus metrics: **EXACT under frozen ideal-control model**
- corrected coherent-cycle exposure: **EXACT**
- \(b\) widest frozen second-order diagnostic margin: **DERIVED**
- D5+midpoint 8Q interaction-uniformity advantage: **NO-GO**
- Phase-A instruction Pareto front: **EXACT within frozen library**
- global optimum over all 1152 transitions: **OPEN**
- finite pulse-width / hardware-noise advantage: **OPEN**
- physical promotion: **0**
