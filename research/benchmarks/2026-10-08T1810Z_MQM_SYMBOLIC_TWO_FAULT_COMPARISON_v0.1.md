# MQM Symbolic Two-Fault Comparison v0.1

**Date:** 2026-10-08  
**Status:** EXACT SAME-AGENT ENUMERATION + SAME-AGENT INDEPENDENT COEFFICIENT AGGREGATION  
**Physical promotion:** 0  
**Frozen benchmark:** commit 993eeb1ec575eebdb7cf2f4026df374c48cb05ad  
**Canonical pair ledger:** commit 8e1fdbf9ac541a6f7640b5698d18149ce8208666  
**Primary replay:** commit 3b6ebf456405f573886a53aae35bf87f4ba4d581  
**Primary result:** commit fedac98ccf23087c414db05f1c7badf98ebaee82  
**Independent aggregation replay:** commit 2fba3b4856b8db682796994b3c1c7ce2c1ce134e  
**Independent aggregation result:** commit 360606e9e6ac550e7bf482ef9035631b4599c417  

## 1. Workload executed

The frozen unordered distinct-location pair universes were expanded over the declared conditional Pauli realizations:

\[
1+0:\quad 623245
\]

pair realizations,

\[
2+1:\quad 5639658,
\]

and

\[
3+1:\quad 10032826.
\]

Single-event realizations were also replayed:

\[
1121,\quad3363,\quad4484
\]

respectively.

Thus the total exact single-plus-pair replay workloads were

\[
624366,\quad5643021,\quad10037310.
\]

The single-event controls reproduce the previous scoped campaign after removing stale/missing metadata faults, whose stochastic probability is frozen to zero here:

- \(1+0\): 879 operational ACCEPT, 154 HOLD, 88 QUARANTINE; among ACCEPT, 152 are protected-logical failures.
- \(3+1\): 1969 ACCEPT, 2163 HOLD, 352 QUARANTINE, zero accepted protected-logical failures.

The \(2+1\) branch was a frozen baseline before pair exposure and has no prior single-fault performance claim to preserve.

## 2. Co-primary accepted-logical error

Write \(l=p_{\rm loss}\). All formulas below are exact through total degree two under the frozen independent-location model.

### \(1+0\)

\[
\boxed{
\epsilon_{L|A}^{1+0}
=
\frac{412}{15}p
+
\frac{382987}{225}p^2
+
\frac{3866}{15}pq
+
O(3).
}
\]

The one-round protocol therefore retains a first-order accepted-logical error term in \(p\).

### \(2+1\)

\[
\boxed{
\epsilon_{L|A}^{2+1}
=
\frac{733381}{225}p^2
+
\frac{19}{15}pq
+
O(3).
}
\]

There is no linear term.

### \(3+1\)

\[
\boxed{
\epsilon_{L|A}^{3+1}
=
\frac{3734566}{225}p^2
+
\frac{296}{15}pq
+
O(3).
}
\]

There is likewise no linear term.

### Exact frozen comparison

Subtracting the two repeated protocols gives

\[
\boxed{
\epsilon_{L|A}^{3+1}
-
\epsilon_{L|A}^{2+1}
=
\frac{66693}{5}p^2
+
\frac{277}{15}pq
+
O(3).
}
\]

Therefore, **within the frozen degree-two model**, \(2+1\) has strictly smaller accepted-logical error than \(3+1\) whenever \(p>0\) and \(q\ge0\).

This does not make \(2+1\) the overall architecture winner. Yield, loss exposure and resource cost remain co-primary or required comparison dimensions.

Ideal-detected loss contributes no accepted-logical term through degree two because loss events are rejected. This is a property of the frozen model, not a hardware loss claim.

## 3. Acceptance yield

The first-order acceptance expansions are

\[
\boxed{
Y_{1+0}
=
1-\frac{56}{5}p-4q-102l+O(2),
}
\]

\[
\boxed{
Y_{2+1}
=
1-\frac{5257}{15}p-24q-306l+O(2),
}
\]

and

\[
\boxed{
Y_{3+1}
=
1-\frac{5239}{15}p-20q-408l+O(2).
}
\]

Thus the repeated protocols buy accepted-logical suppression by rejecting much more aggressively at first order.

Relative to \(2+1\), the \(3+1\) majority protocol has a slightly smaller first-order \(p\)-rejection coefficient by

\[
\frac65,
\]

and a smaller \(q\)-rejection coefficient by \(4\), but it carries one additional round of loss exposure:

\[
-408l\quad\text{versus}\quad-306l.
\]

The one-round protocol has much higher first-order acceptance but also the linear protected-logical term above.

## 4. Accepted-good yield

The exact first-order terms are

\[
Y_{\rm good}^{1+0}
=
1-\frac{116}{3}p-4q-102l+O(2),
\]

\[
Y_{\rm good}^{2+1}
=
1-\frac{5257}{15}p-24q-306l+O(2),
\]

and

\[
Y_{\rm good}^{3+1}
=
1-\frac{5239}{15}p-20q-408l+O(2).
\]

For the repeated protocols, accepted-logical failure begins only at second order, so \(Y\) and \(Y_{\rm good}\) have the same first-order coefficients.

There is therefore no target-independent scalar winner. The frozen comparison remains Pareto-valued in

\[
(Y,\epsilon_{L|A},Y_{\rm good},\text{resource cost}).
\]

The nominal two-qubit-gate budgets remain

\[
39,\quad117,\quad156
\]

for \(1+0,2+1,3+1\).

## 5. Independent coefficient aggregation

A separate Python implementation reads only the primary raw conditional sums and independently reconstructs every degree-two coefficient using exact rational arithmetic.

It verifies for all three protocols:

- frozen location counts;
- all primary metric coefficients;
- \(Y_{\rm good}=Y-P(L\cap A)\);
- \(\epsilon_{L|A}\) series division;
- accepted dressed-weight-one ratio;
- resource-per-good-shot series;
- the partition identity

\[
Y+P_{\rm HOLD}+P_{\rm QUARANTINE}
=
1+O(3).
\]

Result:

\[
\boxed{\text{PASS\_EXACT\_INDEPENDENT\_AGGREGATION}.}
\]

This is a **same-agent independent implementation of coefficient aggregation**, not independent scientific review and not an independently written fault-pair classifier.

## 6. Hardware-neutral stress grid frozen after symbolic exposure

No numerical stochastic performance point was evaluated before the grid was frozen.

The common future rate set is

\[
G=
\left\{
0,\,
2^{-21},\,
2^{-19},\,
2^{-17},\,
2^{-15}
\right\}.
\]

The future Cartesian stress grid is

\[
G^3
\]

for \((p,q,p_{\rm loss})\), giving

\[
125=5^3
\]

points, identical for all three protocols.

The grid is intentionally hardware-neutral and was selected from the maximum frozen location count, not from which protocol won the symbolic coefficients.

At the maximum equal-rate point,

\[
p=q=p_{\rm loss}=2^{-15},
\]

the \(3+1\) sum of elementary-event probabilities is

\[
\frac{1180}{32768}
=
\frac{295}{8192}
\approx0.0360107421875.
\]

The elementary-event union bound for at least three events is

\[
\frac{1}{6}\left(\frac{295}{8192}\right)^3
=
\frac{25672375}{3298534883328}
\approx7.7829630\times10^{-6}.
\]

This is an event-count diagnostic, not asserted as a rigorous Taylor-remainder bound.

Substituting the already-exposed degree-two polynomial on this grid is expository only. New evidence would require a separately frozen higher-order/full stochastic replay or source-calibrated hardware model.

## 7. Promotion ledger

- Frozen pair enumeration: **EXACT SAME-AGENT**
- Degree-two coefficient algebra: **EXACT**
- Separate coefficient aggregation: **EXACT SAME-AGENT CHECK**
- \(1+0\) retains \(O(p)\) accepted-logical error: **EXACT within frozen model**
- \(2+1\) and \(3+1\) suppress accepted-logical error to \(O(p^2,pq)\): **EXACT within frozen model**
- \(2+1\) has lower degree-two \(\epsilon_{L|A}\) than \(3+1\) for \(p>0,q\ge0\): **EXACT within frozen model**
- Overall protocol winner: **OPEN**
- Physical \(p,q,p_{\rm loss}\): **OPEN**
- Independent fault-pair reproduction: **OPEN**
- Threshold: **OPEN**
- Hardware validation: **OPEN**
- Quantum advantage: **OPEN**
- Physical promotion: **0**

Any round-count redesign after this result is a new candidate and requires a fresh benchmark version.
