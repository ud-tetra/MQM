# MQM Shape–Function / Spacetime Audit v0.1

**Date:** 2026-10-09  
**Status:** EXACT structural specialization + EXACT ideal decoder covariance + EXACT motion-word alternatives  
**Physical promotion:** 0

## Function-specific structural winners

The frozen benchmark separates four proposed functions rather than seeking one globally best shape.

### Packing uniformity

Using the declared edge-spread ratio \(\kappa=\max \ell/\min \ell\):

\[
\kappa_{D5}
=
\frac{2}{\sqrt{3+2/\sqrt5}}
\approx1.01346,
\]

\[
\kappa_{D6}
=
\frac{\sqrt5}{2}
\approx1.11803,
\]

\[
\kappa_{A4}
=
\sqrt{\frac83}
\approx1.63299,
\]

\[
\kappa_{S4}=2.
\]

**Winner: D5.**

### Coordination

Average all-pairs module-graph distance:

\[
D5=\frac32,\qquad
D6=\frac95,\qquad
A4=1,\qquad
S4=\frac65.
\]

**Winner: A4.**

### Native cyclic transport

D5 has a geometric order-5 cycle but the current monomial local-Clifford transition group contains no order-5 element.

D6 has both a geometric six-cycle and an exact order-6 MQM frame lift.

A4 has no order-4 shell generator; S4 has no order-6 shell generator.

**Winner under current MQM transition lift: D6.**

### Receipt redundancy

For edge receipts constrained by cycle-space parity checks, the minimum undetected error weight equals graph edge-connectivity:

\[
d_{\rm receipt}(D5)=2,
\]

\[
d_{\rm receipt}(D6)=2,
\]

\[
d_{\rm receipt}(A4)=3,
\]

\[
d_{\rm receipt}(S4)=4.
\]

Thus S4 detects every edge-bit error of weight 1, 2, or 3 in this graph-receipt model.

**Winner: S4.**

These are function-specific structural results, not an overall architecture ranking.

## 2+PV spacetime decoder covariance

For both A4 and D6, every selected directed interface and all sixteen ideal center syndromes were checked.

Each shell contributes

\[
12\times16=192
\]

mixed decoder/interface plaquettes.

Results:

\[
A4:\quad192/192
\]

strict zero covariance defect,

\[
D6:\quad192/192
\]

strict zero covariance defect.

Thus for the tested ideal decoder,

\[
T\,D(s)=D(s')
\]

exactly in the phase-quotiented Pauli representation, where \(s'\) is the syndrome obtained after transporting the recovery by interface frame \(T\).

Therefore decode-then-transport and transport-then-decode commute exactly for the selected A4/D6 frame interfaces.

The spatial cycle ranks remain

\[
\beta_1(A4)=3,\qquad
\beta_1(D6)=1,
\]

and all tested spatial frame cycles close strictly.

This closes the ideal decoder-coordinate part of the mixed spacetime coherence problem. It does not establish hook/flag/noisy-circuit or hardware covariance.

## Same logical function, different hidden motion

The short-word search used canonical generators:

- \(z\): central \(C_2\);
- \(a,b\): protected-logical-kernel \(S_4\);
- \(c,d\): logical-action \(S_4\).

### Logical identity

The same protected logical identity can ride on frame periods

\[
1,2,3,4,6.
\]

Examples:

\[
I,\quad a,\quad b,\quad ab,\quad zb.
\]

### Logical \(X\leftrightarrow Z\) transposition

The same logical transposition occurs with hidden-frame multiplicities

\[
h=1,2,3,6,
\]

using exact short words

\[
c,\quad dcd,\quad bc,\quad bdcd.
\]

### Logical three-cycle

The same logical three-cycle occurs with

\[
h=1,2,4,
\]

using

\[
d,\quad ad,\quad abd.
\]

Thus logical semantics alone do not determine the internal frame trajectory.

Under the frozen abstract compile cost, the shortest \(h=1\) representatives are also the cheapest among the examples found. No noise advantage for longer hidden-frame cycles is established.

## Current interpretation

The user's intuition is now supported in two different scopes:

1. **EXACT structural specialization:** D5, A4, D6, and S4 optimize different frozen structural functions.
2. **EXACT dynamic semantic multiplicity:** one logical operation admits multiple internal motion clocks and frame paths.

The next physical question is not whether motion has meaning; it is whether a nonminimal hidden-frame path provides a measurable advantage such as lower routing cost, better noise averaging, or more robust receipts.

## Promotion ledger

- function-specific structural winners: **EXACT under frozen metrics**
- 2+PV ideal decoder/frame covariance on A4/D6: **EXACT**
- short motion-word alternatives: **EXACT**
- physical function of each shape: **CANDIDATE**
- physical advantage of longer hidden-frame motion: **OPEN**
- hardware validation / threshold / quantum advantage: **OPEN**
- physical promotion: **0**
