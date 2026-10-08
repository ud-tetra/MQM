# MQM 2+C Adaptive Resolver Audit v0.1

**Date:** 2026-10-08  
**Status:** POST-EXPOSURE EXPLORATORY / EXACT THROUGH DEGREE TWO  
**Physical promotion:** 0  
**Candidate freeze:** commit 394c8c7d2b0fb1164b9b3ed1836c817c71cbcd10  
**Replay:** commit 96400d07c0602e3e4ebefa708efd8c621f287cd7  
**Machine result:** commit dcbc7a02e2f293c584ad097a91f2b9ae7621b4d8  

## Candidate rule

Run two mandatory acquisition rounds.

- If either mandatory round flags or reports detected loss, fail closed.
- If the two complete four-bit center frames agree, recover immediately and accept; the third round is not executed.
- If they disagree, execute one conditional resolver round.
- If the resolver frame exactly repeats either prior complete frame, recover using the repeated frame.
- If it matches neither, HOLD.
- No post-recovery verification round is present in this version.

The complete-frame repeat rule was frozen before this candidate was evaluated.

## Exact workload

The mandatory two-round location set is

\[
N_p=358,\qquad N_q=28,\qquad N_{\rm loss}=204.
\]

The optional resolver block has

\[
179,\quad14,\quad102
\]

corresponding locations, but those locations exist only when the first two clean/unflagged records disagree.

Exact replay covered:

\[
2242
\]

single conditional fault realizations in the mandatory prefix,

\[
2503131
\]

mandatory-mandatory pair realizations, and

\[
1076160
\]

triggering-mandatory plus conditional-resolver pair realizations.

There are no resolver-only single-fault trajectories because a fault-free two-round prefix does not execute the resolver.

## Accepted logical error

Let \(l=p_{\rm loss}\). The exact degree-two accepted-logical expansion is

\[
\boxed{
\epsilon_{L|A}^{2+C}
=
\frac{339117}{25}p^2
+
\frac{311}{3}pq
+
O(3).
}
\]

There is no linear term.

Relative to \(2+0\),

\[
\boxed{
\epsilon_{L|A}^{2+C}
-
\epsilon_{L|A}^{2+0}
=
\frac{767776}{75}p^2
+
\frac{208}{3}pq
+
O(3)>0
}
\]

for \(p>0,q\ge0\).

Relative to \(2+1\),

\[
\boxed{
\epsilon_{L|A}^{2+C}
-
\epsilon_{L|A}^{2+1}
=
\frac{2318672}{225}p^2
+
\frac{512}{5}pq
+
O(3)>0.
}
\]

Thus the frozen exact-repeat resolver does **not** recover the accepted-logical quality of either \(2+0\) or \(2+1\) at second order.

The likely mechanism is that a third complete frame can legitimize a repeated but wrong temporal syndrome after a compound fault; exact repetition is not equivalent to post-recovery verification.

## Acceptance yield

The adaptive candidate has

\[
\boxed{
Y_{2+C}
=
1
-
\frac{267}{5}p
-
8q
-
204l
+O(2).
}
\]

This is substantially more permissive than fixed \(2+0\):

\[
Y_{2+C}-Y_{2+0}
=
\frac{729}{5}p+8q+O(2),
\]

with the same first-order loss exposure because the third round is not executed on the clean trajectory.

Against fixed \(2+1\),

\[
Y_{2+C}-Y_{2+1}
=
\frac{4456}{15}p+16q+102l+O(2).
\]

So \(2+C\) is a high-yield candidate, but the yield is purchased with materially larger second-order accepted-logical error.

## Conditional-round activation

The first-order probability that a single mandatory-prefix fault forces the resolver round is

\[
\boxed{
P(R_3\ {\rm executed})
=
\frac{884}{5}p+8q+O(2).
}
\]

Therefore

\[
E[\text{rounds}]
=
2+\frac{884}{5}p+8q+O(2),
\]

and

\[
E[N_{2q}]
=
78
+
\frac{34476}{5}p
+
312q
+
O(2).
\]

This is the architecture advantage the adaptive rule was intended to test: its clean path costs only two rounds.

## Example stress substitution

At the already-frozen hardware-neutral equal-rate point

\[
p=q=l=2^{-15},
\]

substituting only the newly derived degree-two candidate polynomial gives approximately

\[
Y_{2+C}\approx0.9918993,
\]

\[
\epsilon_{L|A}^{2+C}\approx1.2834\times10^{-5},
\]

\[
Y_{\rm good}^{2+C}\approx0.9918866.
\]

This substitution is expository, not a separate higher-order result.

## Ruling

**CANDIDATE / NO-GO for the intended quality target:** the exact-repeat conditional resolver is too permissive at second order to deliver \(2+1\)-like accepted-logical quality.

The candidate remains informative because it demonstrates that adaptive extra rounds cannot be justified by frame repetition alone.

A successor may use a stronger ambiguity receipt, but because this result is exposed, any changed resolver rule is a new version.

## Promotion ledger

- Adaptive state-machine definition: **FROZEN POST-EXPOSURE**
- Degree-two replay: **EXACT SAME-AGENT**
- Linear accepted-logical term: **EXACT zero**
- High-yield behavior: **DERIVED**
- Intended \(2+1\)-quality target: **NO-GO for v0.1**
- Higher-order adaptive ordering: **OPEN**
- Independent reproduction: **OPEN**
- Hardware validation / threshold / advantage: **OPEN**
- Physical promotion: **0**
