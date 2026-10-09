# MQM Finite-Pulse / K192 / D5 Coupler Audit v0.1

**Date:** 2026-10-09  
**Physical promotion:** 0

## 1. Finite-pulse Sqale stress result

The benchmark intentionally keeps two public source profiles distinct:

- Radnaev et al., PRX Quantum 6, 030334 (2025): pulse durations, T2*, GR/Rz fidelities, CZ survival and Rz leakage.
- Chung et al., npj Quantum Information 11, 193 (2025): coherent GR overrotation and Rz angle-bias model.

Combining those profiles is a **cross-profile stress test**, not a calibrated backend prediction.

Public timing/profile values used:

\[
t_{GR(\pi)}=4.1\ \mu s,
\qquad
t_{R_Z(\pi)}=0.25\ \mu s,
\qquad
t_{CZ}=0.416\ \mu s,
\]

\[
T_2^*=12.7\ {\rm ms}.
\]

The finite signed cycles compile as:

### a

\[
N_{GR}=24,\quad
N_{R_Z}=180,\quad
N_{CZ}=6,
\]

parallel-layer pulse time

\[
36.096\ \mu s.
\]

Cross-profile coherent unitary average infidelity:

\[
0.17848.
\]

### b

\[
N_{GR}=168,\quad
N_{R_Z}=1260,\quad
N_{CZ}=36,
\]

parallel-layer pulse time

\[
250.926\ \mu s.
\]

Cross-profile coherent unitary average infidelity:

\[
0.99610.
\]

### zb

\[
N_{GR}=336,\quad
N_{R_Z}=2532,\quad
N_{CZ}=72,
\]

parallel-layer pulse time

\[
501.852\ \mu s.
\]

Cross-profile coherent unitary average infidelity:

\[
0.98911.
\]

The ideal compiled cycles close to identity to numerical roundoff, so the large modeled residuals come from the injected source-profile coherent control errors.

The timing itself is not the dominant burden:

\[
t_b/T_2^*\approx0.0198,
\qquad
t_{zb}/T_2^*\approx0.0395.
\]

Instead the canonical selective-control/SWAP realization accumulates very large GR/Rz/CZ exposure.

Independent-product diagnostics also fall rapidly:

\[
a:\ 0.8637,\qquad
b:\ 0.3669,\qquad
zb:\ 0.1336.
\]

These products are exposure diagnostics, not physical success probabilities.

### Ruling

The canonical physical H/S/SWAP realization of \(b\) and \(zb\) is **NO-GO under this frozen cross-profile stress model**.

This does not falsify the ideal coherent-averaging theorem. It says the present physical implementation cost overwhelms it under the tested public source parameters.

A lower-cost native or virtual-frame implementation is required before logical-identity motion becomes a plausible hardware mechanism.

## 2. Full 192-element logical-identity search

All

\[
|K_{192}|=192
\]

protected-logical-identity frame elements were evaluated exactly using:

- zeroth-order weight-2 coherent residual;
- second-order equal-two-term Magnus metric;
- signed-cycle physical exposure;
- direct step cost;
- shortest word length in the frozen kernel generator alphabet.

Reference \(b\):

\[
\bar A_0=\frac{55}{126},
\qquad
A_1=\frac{15616}{170775},
\]

\[
N_{\rm cycle}=72,
\qquad
C_{\rm step}=12,
\qquad
|w|=1.
\]

No element dominates \(b\) in all five frozen metrics:

\[
\boxed{N_{\rm dominates}(b)=0.}
\]

Therefore \(b\) remains an exact Pareto point.

However the full search found materially stronger trade alternatives.

### Brightest balanced challenger: v = element 128

\[
T_\pm=4,
\qquad
C_{\rm step}=14,
\qquad
N_{\rm cycle}=56,
\]

\[
\bar A_0=\frac{23}{63},
\qquad
A_1=\frac{78}{1265},
\qquad
|w|=1.
\]

Compared with \(b\), \(v\) has:

- lower zeroth residual;
- lower second-order metric;
- lower total cycle exposure;
- equal generator-word length;
- but larger direct step complexity \(14>12\).

So it cannot dominate \(b\) under the frozen five-metric rule, but it is the brightest current lower-exposure challenger.

Other notable points include element 320:

\[
N_{\rm cycle}=68,\quad
\bar A_0=\frac{71}{252},\quad
A_1=\frac{346}{6325},
\]

and element 1021:

\[
N_{\rm cycle}=60,\quad
\bar A_0=\frac{95}{252},\quad
A_1=\frac{62}{1265}.
\]

These trade stronger suppression for higher direct step or word complexity.

### Ruling

The Phase-A label "b is the strongest balanced motion" survives as a Pareto statement, not as a unique optimum.

The full kernel exposes a new frontier, especially element 128, that should receive the next finite-pulse native-implementation test.

## 3. D5 repurposed as coupler/ancilla fiber

The D5 hypothesis was moved away from the 8-data-qubit carrier role and retested as a local redundant two-terminal ancilla/coupler fiber.

Normalize:

- terminal separation \(N-S=2\);
- adjacent ring-slot spacing \(=2\);
- \(m\) equivalent ancilla slots around the axis.

Then

\[
R_m=\csc(\pi/m),
\]

and every slot has exactly equal distance to both terminals:

\[
d(N,v_i)=d(S,v_i)
=
\sqrt{1+\csc^2(\pi/m)}.
\]

Thus terminal coupling-length asymmetry is exactly zero for every slot.

Define the multiscale edge ratio

\[
\kappa_m=
\frac{\max(2,c_m)}{\min(2,c_m)}.
\]

Because \(c_m\) increases monotonically with integer \(m\ge3\), the global integer minimum lies around the crossing \(c_m=2\). Exact comparison of \(m=5,6\) gives:

\[
\boxed{
m=5\text{ is the unique global integer minimum.}
}
\]

For D5:

\[
\boxed{
\kappa_5
=
\frac{2}{\sqrt{3+2/\sqrt5}}
\approx1.01346.
}
\]

It provides five symmetry-equivalent slots and one spare if four channels are active.

For D6:

\[
\kappa_6=\frac{\sqrt5}{2}\approx1.11803,
\]

with six slots and two spares.

The frozen \(m=3,\dots,8\) Pareto set is

\[
\{5,6,7,8\},
\]

reflecting the trade between geometric regularity and spare-slot count.

### Ruling

D5 now has a mathematically cleaner candidate role:

> **minimum-distortion redundant two-terminal coupler/ancilla fiber.**

This role is exact geometrically and does not conflict with the prior NO-GO for D5 as the full subsystem-8 data layout.

A source-bound coupling/loss/crosstalk model is still required before claiming hardware advantage.

## Overall status

- finite-pulse gate realization of current \(b,zb\): **NO-GO under cross-profile stress**
- full K192 second-order search: **EXACT**
- \(b\) strict dominator found: **NO**
- element 128 as lower-exposure challenger: **CANDIDATE priority**
- D5 full 8Q data geometry: **NO-GO under frozen mapping**
- D5 local coupler fiber: **EXACT geometric specialization**
- hardware validation / threshold / advantage: **OPEN**
- physical promotion: **0**
