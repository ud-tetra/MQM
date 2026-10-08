# MQM Higher-Order Grid + Classifier Audit v0.1

**Date:** 2026-10-08  
**Physical promotion:** 0  
**Frozen higher-order protocol:** commit d1b1c9fc8a76e9902fc74ba9ed4287fc07f7e658  
**Higher-order evaluator:** commit 35c56038055fa42a72df6c067b6f039fcec3c670  
**Grid result:** commit 97f5db4fb38b3e7b5ec98c82cadc72eb911ee7be  
**Grid summary:** commit c4fdf1568d892b672a89f5a48c62b2437b943377  
**Separate classifier source:** commit 7fb0c8055e9499661ad5a8d1fe274960c8930ba7  
**Separate classifier output:** commit fb94ad7f995481fa7e46f7eb677fc65a778225f9  

## 1. Evidence type

The all-orders grid evaluation is **SIMULATED / statistically enclosed**, not exact enumeration of every higher-order trajectory.

For every protocol/grid point:

1. zero-, one-, and two-event contributions are enumerated exactly;
2. the exact independent-Bernoulli probability of the complete \(N\ge3\) event tail is computed from binomial-count convolution;
3. the conditional \(N\ge3\) tail is sampled with the frozen 200000-shot importance sampler;
4. each tail metric receives the frozen simultaneous Hoeffding enclosure.

The conditional-tail Hoeffding halfwidth is

\[
h=0.006246452998941145.
\]

Maximum tail probabilities over the frozen grid are

\[
1+0:\ 1.1957323558\times10^{-7},
\]

\[
2+1:\ 3.2069612979\times10^{-6},
\]

\[
3+1:\ 7.5570240242\times10^{-6}.
\]

Therefore the maximum direct metric halfwidths contributed by tail sampling are respectively below approximately

\[
7.47\times10^{-10},\qquad
2.01\times10^{-8},\qquad
4.73\times10^{-8}.
\]

These are simulation/enclosure uncertainties, not hardware uncertainties.

## 2. Frozen-grid accepted-logical ordering

There are

\[
125=5^3
\]

common grid points and \(100\) points with \(p>0\).

### Repeated protocols versus one round

For all 100 positive-\(p\) grid points,

\[
\boxed{
\epsilon_{L|A}^{2+1}
<
\epsilon_{L|A}^{1+0}
}
\]

is certified by disjoint frozen confidence intervals.

Likewise, for all 100 positive-\(p\) points,

\[
\boxed{
\epsilon_{L|A}^{3+1}
<
\epsilon_{L|A}^{1+0}.
}
\]

At the 25 points with \(p=0\), the accepted-logical intervals overlap at or near zero.

### \(2+1\) versus \(3+1\)

For \(p>0\):

- 95 / 100 points certify
  \[
  \epsilon_{L|A}^{2+1}<\epsilon_{L|A}^{3+1};
  \]
- 5 / 100 are statistically INCONCLUSIVE under the frozen tail interval;
- 0 / 100 reverse the ordering.

The five unresolved points are all at the smallest nonzero

\[
p=2^{-21}
\]

and largest frozen loss rate

\[
p_{\rm loss}=2^{-15},
\]

across the five \(q\) values.

Thus the higher-order run does **not** produce a reversal of the degree-two \(2+1\) ordering anywhere on the grid.

It also does not certify the ordering at those five low-\(p\), high-loss points.

## 3. Yield and accepted-good output

The all-orders grid retains the Pareto split.

### \(1+0\)

Relative to both repeated protocols, \(1+0\) has higher

\[
Y
\]

and higher

\[
Y_{\rm good}
\]

at all 124 nonzero grid points, with equality only at the zero-noise point.

This does not make it the quality winner because it retains the much larger accepted-logical error.

### \(2+1\) versus \(3+1\)

For acceptance yield:

- \(2+1\) is certified higher at 93 points;
- \(3+1\) is certified higher at 31 points;
- one point, zero noise, is equal/overlapping.

For accepted-good yield:

- \(2+1\) is certified higher at 94 points;
- \(3+1\) is certified higher at 30 points;
- one point is equal/overlapping.

This is consistent with the first-order competition

\[
Y_{3+1}-Y_{2+1}
=
\frac65p+4q-102p_{\rm loss}+O(2).
\]

The extra round helps the \(p/q\)-rejection behavior of \(3+1\) but adds 102 ideal-detected loss locations.

## 4. Equal-rate stress line

At

\[
p=q=p_{\rm loss}=2^{-15},
\]

the all-orders estimates are approximately:

### \(1+0\)

\[
Y=0.9964296984,
\]

\[
\epsilon_{L|A}=8.4003521\times10^{-4},
\]

\[
Y_{\rm good}=0.9955926624.
\]

### \(2+1\)

\[
Y=0.9794505482,
\]

\[
\epsilon_{L|A}=3.0344813\times10^{-6},
\]

\[
Y_{\rm good}=0.9794475761.
\]

### \(3+1\)

\[
Y=0.9765685815,
\]

\[
\epsilon_{L|A}=1.5446044\times10^{-5},
\]

\[
Y_{\rm good}=0.9765534974.
\]

These are hardware-neutral simulated stress values, not empirical predictions.

## 5. Separate fault-pair classifier

The new higher-order engine reconstructs the candidate circuits using a separate Pauli representation

\[
P=(x,z),\qquad x,z\in\mathbb F_2^n,
\]

rather than the original packed \(x|(z\ll n)\) primary-classifier representation.

It independently rebuilds every frozen single-event signature and every unordered fault-pair classification.

It does **not** read the primary raw aggregates.

After converting the independently accumulated rational weights to the frozen integer numerators:

- all \(1+0\) raw aggregates match;
- all \(2+1\) raw aggregates match;
- all \(3+1\) raw aggregates match;
- all metrics \(Y\), HOLD, QUARANTINE, \(L\cap A\), accepted dressed-weight one, and \(Y_{\rm clean}\) match;
- mismatch count = 0.

Result:

\[
\boxed{\text{PASS\_EXACT\_RAW\_CLASSIFIER\_MATCH}.}
\]

This is materially stronger than the earlier Fraction aggregation check because the circuit event signatures and pair labels are reconstructed.

It remains a **same-agent implementation check**, not independent scientific review.

The standalone cross-check wrapper shares the new P-struct simulation engine with the higher-order evaluator; independence is relative to the original primary classifier, not between those two new artifacts.

## 6. Promotion

- Exact <=2 event contributions: **EXACT SAME-AGENT**
- Higher-order \(N\ge3\) outcome contribution: **SIMULATED with frozen confidence enclosure**
- Full-grid \(2+1<3+1\) accepted-error ordering: **CERTIFIED on 95/100 positive-\(p\) points; OPEN on 5; no reversals**
- Repeated protocols below \(1+0\) accepted-error: **CERTIFIED on 100/100 positive-\(p\) points**
- Separate raw pair classifier match: **EXACT SAME-AGENT CHECK**
- Overall architecture winner: **OPEN**
- Independent external reproduction: **OPEN**
- Hardware calibration: **OPEN**
- Threshold: **OPEN**
- Quantum advantage: **OPEN**
- Physical promotion: **0**
