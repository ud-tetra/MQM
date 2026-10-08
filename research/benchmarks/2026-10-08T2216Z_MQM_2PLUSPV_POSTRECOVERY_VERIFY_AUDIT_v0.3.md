# MQM 2+PV Conditional Post-Recovery Verification Audit v0.3

**Date:** 2026-10-08  
**Status:** POST-EXPOSURE EXPLORATORY / EXACT THROUGH DEGREE TWO / PASSES PREDECLARED DEVELOPMENT GATE  
**Physical promotion:** 0  
**Freeze:** commit 47783b067628991e7ba361b3a51ce6173cfabf3a  
**Replay:** commit 4d839808da339146339c20759f228ba6ca3ab7b5  
**Result:** commit 9a5a530c95b0318f91c7318bccd3d3053d1ad432  
**GitHub-hosted run:** 37837260022

## Controller

Run two mandatory acquisition rounds.

If their complete center frames disagree, HOLD.

If they agree on \(b\), apply the frozen Pauli-frame recovery selected by \(b\).

- If \(b=0000\), ACCEPT immediately.
- If \(b\neq0000\), execute one verification round **after recovery** and accept only if the post-recovery center syndrome is \(0000\), with no flag or detected loss.

This differs from the frozen NO-GO temporal resolvers: the optional round does not vote on which recovery to apply. It interrogates the residual state produced by the already-selected recovery.

## Exact workload

Mandatory locations:

\[
N_p=358,\qquad N_q=28,\qquad N_l=204.
\]

Conditional verification block:

\[
179,\qquad14,\qquad102.
\]

The exact degree-two replay covered

\[
2242
\]

single realizations,

\[
2503131
\]

mandatory-mandatory pair realizations, and

\[
126673
\]

triggering-mandatory plus verification-fault realizations.

Only

\[
113
\]

unweighted single fault realizations activate verification.

## Accepted logical error

The exact result is

\[
\boxed{
\epsilon_{L|A}^{2+PV}
=
\frac{733381}{225}p^2
+
\frac{19}{15}pq
+
O(3).
}
\]

There is no linear term.

### Exact equality with fixed 2+1 through degree two

The frozen fixed \(2+1\) protocol has

\[
\epsilon_{L|A}^{2+1}
=
\frac{733381}{225}p^2
+
\frac{19}{15}pq
+
O(3).
\]

Therefore

\[
\boxed{
\epsilon_{L|A}^{2+PV}
-
\epsilon_{L|A}^{2+1}
=
0+O(3).
}
\]

This is an exact equality of the frozen degree-two coefficients, not a general theorem or higher-order equivalence.

### Improvement over 2+0

The exploratory \(2+0\) candidate has

\[
\epsilon_{L|A}^{2+0}
=
\frac{9983}{3}p^2
+
\frac{103}{3}pq
+
O(3).
\]

Hence

\[
\boxed{
\epsilon_{L|A}^{2+PV}
-
\epsilon_{L|A}^{2+0}
=
-\frac{15344}{225}p^2
-
\frac{496}{15}pq
+
O(3).
}
\]

Both degree-two coefficients improve for every \(p>0,\ q\ge0\).

## Acceptance

The first-order acceptance is

\[
\boxed{
Y_{2+PV}
=
1-\frac{996}{5}p-16q-204l+O(2).
}
\]

This is exactly the same first-order acceptance as \(2+0\).

Against fixed \(2+1\),

\[
\boxed{
Y_{2+PV}-Y_{2+1}
=
\frac{2269}{15}p
+8q
+102l
+O(2).
}
\]

Thus the candidate meets the predeclared development target at this order: \(2+1\)-level accepted-logical coefficients with \(2+0\)-level first-order acceptance.

## Conditional verification cost

The verification round is activated at first order with probability

\[
\boxed{
P(V)=\frac{389}{15}p+O(2).
}
\]

There is no first-order \(q\) or loss activation term.

Therefore

\[
E[R]
=
2+\frac{389}{15}p+O(2),
\]

\[
E[N_{2q}]
=
78+\frac{5057}{5}p+O(2),
\]

and

\[
E[N_{\rm meas}]
=
28+\frac{5446}{15}p+O(2).
\]

These are perturbative expected-resource expressions under the frozen homogeneous model.

## Information-content ruling

Repeated pre-recovery snapshots can only vote on a proposed recovery. They do not directly test what that recovery leaves behind.

The conditional verification round measures the center syndrome **after** the recovery map. Consequently two pre-recovery fault histories that produce the same selected frame can still be separated if their residual post-recovery syndromes differ.

That additional causal ordering is the information source missing from \(2+C\) and \(2+E\).

## Ruling

The predeclared success target was:

> reduce at least one \(2+0\) accepted-logical degree-two coefficient without increasing the other, while retaining first-order acceptance above fixed \(2+1\) in at least one nonnegative fault direction.

The result exceeds that target:

- both accepted-logical coefficients improve relative to \(2+0\);
- they exactly match fixed \(2+1\) through degree two;
- first-order acceptance exactly matches \(2+0\);
- the verification block is invoked only conditionally.

### CANDIDATE / AUTO_LOCK scoped development result

\[
\boxed{\text{2+PV v0.3 is the brightest adaptive schedule candidate found so far.}}
\]

This remains post-exposure exploratory evidence. It does not replace the frozen \(1+0/2+1/3+1\) benchmark.

## Open gates

- higher-order 125-point adaptive stochastic replay;
- independent implementation of the adaptive exposure logic;
- typed Sqale-channel replay;
- compiled timing/latency accounting;
- hardware execution.

## Promotion ledger

- degree-two replay: **EXACT SAME-AGENT / GitHub-hosted execution**
- equality with \(2+1\) through degree two: **EXACT**
- improvement over \(2+0\) through degree two: **EXACT**
- adaptive architecture win: **CANDIDATE**
- higher-order equivalence: **OPEN**
- hardware validation / threshold / advantage: **OPEN**
- physical promotion: **0**
