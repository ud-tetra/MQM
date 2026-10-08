# MQM 2+0 Post-Exposure Candidate Audit v0.1

**Date:** 2026-10-08  
**Status:** POST-EXPOSURE EXPLORATORY CANDIDATE  
**Physical promotion:** 0  
**Candidate freeze:** commit 35b4083881c0950645f5a2c9c5cb76431c4584bf  
**Evaluator:** commit aba1c04b2fa519849cb03883a96cc2c805bbea79  
**Result:** commit d836182b8dfae6677e82cd443aedcfd02d082fdd  

## 1. Candidate

The new candidate is

\[
\boxed{2+0}
\]

with two acquisition rounds, no verification round.

Both complete unflagged center frames must agree bit-for-bit. Disagreement returns HOLD. On agreement, the frozen decoder is applied as a Pauli-frame update and the block is accepted immediately.

This candidate was selected **after** exposure of the frozen \(1+0/2+1/3+1\) benchmark. It cannot retroactively alter or confirm that benchmark.

Resources:

\[
78
\]

two-qubit gates,

\[
28
\]

measurements, and two peak extra ancillas.

Location counts are

\[
N_p=358,\qquad
N_q=28,\qquad
N_{\rm loss}=204.
\]

## 2. Single-fault order

The accepted-logical raw single-event sum is exactly zero.

Therefore the candidate has no first-order accepted-logical error under the frozen stochastic model.

Its first-order acceptance is

\[
\boxed{
Y_{2+0}
=
1-\frac{996}{5}p-16q-204p_{\rm loss}+O(2).
}
\]

Thus it sits strictly between \(1+0\) and \(2+1\) in scheduled exposure.

## 3. Exact degree-two accepted-logical error

The exact pair coefficients give

\[
\boxed{
\epsilon_{L|A}^{2+0}
=
\frac{9983}{3}p^2
+
\frac{103}{3}pq
+
O(3).
}
\]

Against the frozen \(2+1\) branch,

\[
\epsilon_{L|A}^{2+0}
-
\epsilon_{L|A}^{2+1}
=
\frac{15344}{225}p^2
+
\frac{496}{15}pq
+
O(3).
\]

Both coefficients are positive.

Therefore \(2+1\) retains the lower accepted-logical error through degree two for \(p>0,\ q\ge0\).

The corresponding first-order yield difference is

\[
Y_{2+0}-Y_{2+1}
=
\frac{2269}{15}p+8q+102p_{\rm loss}+O(2),
\]

so \(2+0\) gains first-order acceptance in every nonnegative rate direction.

This is an explicit quality-versus-yield/resource trade.

## 4. Higher-order frozen-grid exploratory result

The same frozen rate grid and higher-order tail method were applied as an exploratory post-exposure evaluation.

### \(2+0\) versus \(1+0\)

For every one of the 100 frozen grid points with \(p>0\),

\[
\boxed{
\epsilon_{L|A}^{2+0}
<
\epsilon_{L|A}^{1+0}
}
\]

is certified by disjoint intervals.

However, \(1+0\) has higher \(Y_{\rm good}\) at all 124 nonzero grid points.

### \(2+0\) versus \(2+1\)

For accepted-logical error over the 100 positive-\(p\) points:

- \(2+1\) is certified lower at 89 points;
- 11 points are interval-overlap / INCONCLUSIVE;
- \(2+0\) is certified lower at zero points.

For accepted-good yield over the full 125-point grid:

- \(2+0\) is certified higher at all 124 nonzero points;
- the zero-noise point is equal.

Thus \(2+0\) is a new Pareto point: more accepted-good throughput and lower resource cost, but somewhat worse accepted-logical quality than \(2+1\).

### \(2+0\) versus \(3+1\)

For \(p>0\):

- \(2+0\) is certified lower in accepted-logical error at 99 of 100 points;
- one point is interval-overlap / INCONCLUSIVE;
- zero points favor \(3+1\).

For accepted-good yield, \(2+0\) is certified higher at all 124 nonzero points.

Within this exploratory hardware-neutral grid, \(3+1\) therefore has no demonstrated Pareto advantage over \(2+0\).

That statement is **CANDIDATE / exploratory**, because \(2+0\) was selected after exposure.

## 5. Equal-rate maximum grid point

At

\[
p=q=p_{\rm loss}=2^{-15},
\]

the exploratory \(2+0\) result is approximately

\[
Y=0.9872905804,
\]

\[
\epsilon_{L|A}=3.1284761\times10^{-6},
\]

\[
Y_{\rm good}=0.9872874917,
\]

and

\[
\text{two-qubit gates per accepted-good shot}
\approx79.00434.
\]

For comparison, at the same frozen stress point:

\[
2+1:
\quad
Y_{\rm good}\approx0.9794475761,
\quad
\epsilon_{L|A}\approx3.0344813\times10^{-6},
\]

with roughly 119.4551 two-qubit gates per accepted-good shot.

Thus at this point \(2+0\) pays only a small accepted-error increase while materially improving accepted-good throughput and scheduled-resource cost.

This is not a hardware prediction.

## 6. Development ruling

**CANDIDATE:** \(2+0\) becomes the brightest new round-count frontier.

Reason:

- it preserves second-order accepted-logical suppression in the frozen model;
- it uses two blocks rather than three or four;
- it dominates \(3+1\) on accepted-good yield throughout the nonzero frozen grid and on accepted-logical error at 99/100 positive-\(p\) points;
- it trades only a modest accepted-logical penalty versus \(2+1\) while gaining substantial yield and resource reduction.

It is not promoted above the frozen benchmark because it was selected after exposure.

Any adaptive successor such as verify-on-disagreement must be a new version with a fresh freeze.

## 7. Promotion ledger

- \(2+0\) candidate definition: **FROZEN POST-EXPOSURE**
- Single-fault accepted-logical linear term: **EXACT zero under frozen model**
- Degree-two coefficients: **EXACT SAME-AGENT**
- Higher-order grid: **SIMULATED / exploratory with frozen confidence enclosure**
- Pareto superiority over \(3+1\): **CANDIDATE within this grid**
- Superiority over \(2+1\): **NOT ESTABLISHED; explicit trade**
- Independent reproduction: **OPEN**
- Hardware validation: **OPEN**
- Threshold: **OPEN**
- Quantum advantage: **OPEN**
- Physical promotion: **0**
