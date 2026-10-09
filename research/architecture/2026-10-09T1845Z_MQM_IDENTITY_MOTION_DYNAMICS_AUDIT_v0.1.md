# MQM Logical-Identity Motion Dynamics Audit v0.1

**Date:** 2026-10-09  
**Status:** EXACT finite-frame / first-order coherent-control result + scoped NO-GO results  
**Physical promotion:** 0

## Frozen candidates

All five candidates have protected-logical identity:

\[
I,\quad a,\quad b,\quad ab,\quad zb.
\]

Their phase-quotiented frame periods are

\[
1,\ 2,\ 3,\ 4,\ 6.
\]

Under the canonical signed \(H/S/\mathrm{SWAP}\) lifts, the coherent-control periods are instead

\[
1,\ 2,\ 6,\ 8,\ 12.
\]

Thus several motions close in the phase-quotiented frame before their signed Pauli action closes.

## Static coherent Hamiltonian averaging

The benchmark assumes ideal instantaneous controls, equal dwell times, and a static Hamiltonian between frame updates. Only the zeroth-order average Hamiltonian is scored.

### Weight-1 Pauli Hamiltonian basis

There are 24 single-site Pauli terms.

| cycle | invariant rank | basis terms averaged exactly to zero | mean squared residual norm |
|---|---:|---:|---:|
| \(I\) | 24 | 0 | \(1\) |
| \(a\) | 21 | 0 | \(7/8\) |
| \(b\) | 16 | 6 | \(2/3\) |
| \(ab\) | 17 | 6 | \(17/24\) |
| \(zb\) | 16 | 6 | \(2/3\) |

### Weight-2 correlated Pauli Hamiltonian basis

There are

\[
\binom82 3^2=252
\]

two-site Pauli terms.

| cycle | invariant rank | basis terms averaged exactly to zero | mean squared residual norm |
|---|---:|---:|---:|
| \(I\) | 252 | 0 | \(1\) |
| \(a\) | 195 | 0 | \(65/84\) |
| \(b\) | 110 | 102 | \(55/126\) |
| \(ab\) | 123 | 110 | \(41/84\) |
| \(zb\) | 108 | 102 | \(3/7\) |

Therefore nontrivial logical-identity motion can suppress the **first-order static coherent-error subspace** without changing the protected logical operation.

Examples:

\[
b:\quad
1-\frac{55}{126}
=
\frac{71}{126}
\]

reduction in the mean squared weight-2 basis response relative to doing nothing.

For \(zb\),

\[
1-\frac37=\frac47.
\]

These are average-Hamiltonian statements, not logical-error probabilities.

The \(ab\) cycle zeros more individual weight-2 basis terms than \(b\) or \(zb\), even though its average residual norm is larger. Therefore error-spectrum alignment can matter; there is no universal coherent-noise winner without a source-bound Hamiltonian.

## Stochastic Pauli benchmark — scoped NO-GO

For each of all 252 weight-2 phase-quotiented Pauli errors, the clock phase was averaged over the complete frame cycle and scored by the frozen ideal-center decoder.

For **every** candidate:

\[
\boxed{
\text{improved}=0,\quad
\text{worsened}=0,\quad
\text{equal}=252.
}
\]

The global harmful fraction remains

\[
\frac{162}{252}=\frac9{14}.
\]

The nine fixed Pauli-type correlated families are also unchanged by all five cycles:

\[
XX,XY,XZ:\quad \frac5{14},
\]

and

\[
YX,YY,YZ,ZX,ZY,ZZ:\quad \frac{11}{14}.
\]

Thus:

\[
\boxed{
\text{logical-identity frame cycling gives no benefit for this ideal stochastic weight-2 Pauli model.}
}
\]

This is a useful NO-GO. The observed coherent benefit is not a generic error-correction improvement; it depends on temporal coherence of the underlying error.

## Loss exposure — scoped NO-GO for physical control

Abstract physical primitive exposure for one complete cycle is:

\[
I:0,\quad
a:6,\quad
b:36,\quad
ab:36,\quad
zb:54.
\]

Under independent per-primitive loss probability \(\ell>0\),

\[
P_{\rm survive}=(1-\ell)^N.
\]

Therefore adding physical control operations strictly decreases survival unless some separate mechanism compensates for that burden.

A virtual frame update has

\[
N=0
\]

additional physical primitives and therefore does not incur this added loss term.

## Dynamic-resource ruling

Logical-identity motion is **not** generically beneficial.

It has three distinct regimes in the frozen tests:

1. **static coherent noise:** genuine first-order averaging resource;
2. **memoryless Pauli noise + ideal decoder:** no benefit;
3. **independent operation loss:** physical motion is strictly burdensome, virtual frame motion is neutral.

This is the strongest current interpretation of "motion has additional meaning":

> a motion pattern can be an operation on the noise frame even when it is the identity on the protected logical state.

That function is noise-model dependent and must remain typed.

## Current Pareto picture

- \(I\): zero control cost, zero coherent suppression.
- \(a\): small exposure, modest suppression.
- \(b\): strong average coherent suppression at 36 primitive exposures.
- \(ab\): same 36-exposure scale, larger exact-zero subspace for weight-2 terms but worse mean residual than \(b\).
- \(zb\): strongest average weight-2 suppression among these candidates, but 54 primitive exposures.

The correct next comparison requires source-bound coherent-noise spectrum and control/loss rates.

## Claim ledger

- signed-period distinction: **EXACT**
- first-order coherent averaging metrics: **EXACT under frozen ideal-control model**
- stochastic weight-2 no-benefit result: **EXACT scoped NO-GO**
- independent physical-loss benefit: **NO-GO absent compensating mechanism**
- virtual-frame dynamical-decoupling benefit on hardware: **OPEN**
- hardware validation / threshold / quantum advantage: **OPEN**
- physical promotion: **0**
