# MQM 2+E K4 Edge-Receipt Resolver Audit v0.2

**Date:** 2026-10-08  
**Status:** POST-EXPOSURE EXPLORATORY / EXACT THROUGH DEGREE TWO / AUTO_FREEZE NO-GO FOR INTENDED QUALITY TARGET  
**Physical promotion:** 0  
**Protocol freeze:** commit 7f8c6512debf235f82940192271e0bfc30634fca  
**Replay source:** commit 7e5ac349c7b2db11233f53c809008f7f539b7122  
**Machine result:** commit 3bb56b96ce0906acf737624307c5fdd5b1de438f  
**GitHub-hosted run:** 37833646689

## 1. Stronger temporal receipt

Each round uses

\[
\rho_r=(b_r,e_r)
\]

with four center bits and six K4 core-edge gauge bits.

The edge order is

\[
(12,13,18,23,28,38).
\]

The six ideal edge parities lie in the rank-3 K4 cut space and obey

\[
e_{12}\oplus e_{13}\oplus e_{23}=0,
\]

\[
e_{12}\oplus e_{18}\oplus e_{28}=0,
\]

\[
e_{13}\oplus e_{18}\oplus e_{38}=0.
\]

Absolute edge values are gauge-state dependent. Only cycle validity and temporal equality are used for control.

The candidate uses no additional quantum measurements relative to the existing round block.

## 2. Frozen controller

- Run R1 and R2.
- If both receipts are cycle-valid and \(\rho_1=\rho_2\), recover immediately.
- Otherwise run R3.
- R3 must be cycle-valid.
- Accept only when \(\rho_3\) exactly repeats one and only one cycle-valid prior receipt.
- Otherwise HOLD.
- Flags and detected loss remain fail-closed.

## 3. Exact workload

Mandatory two-round locations:

\[
N_p=358,\qquad N_q=28,\qquad N_l=204.
\]

Conditional resolver locations:

\[
179,\qquad14,\qquad102.
\]

Exact replay covered

\[
2242
\]

single conditional fault realizations,

\[
2503131
\]

mandatory-mandatory pair realizations, and

\[
1437122
\]

triggering-mandatory plus resolver pair realizations.

## 4. Accepted-logical error

The exact degree-two result is

\[
\boxed{
\epsilon_{L|A}^{2+E}
=
\frac{559903}{45}p^2
+
\frac{311}{3}pq
+
O(3).
}
\]

There is no linear accepted-logical term.

### Versus 2+0

\[
\boxed{
\epsilon_{L|A}^{2+E}
-
\epsilon_{L|A}^{2+0}
=
\frac{410158}{45}p^2
+
\frac{208}{3}pq
+
O(3)>0
}
\]

for \(p>0,\ q\ge0\).

### Versus 2+1

\[
\boxed{
\epsilon_{L|A}^{2+E}
-
\epsilon_{L|A}^{2+1}
=
\frac{2066134}{225}p^2
+
\frac{512}{5}pq
+
O(3)>0.
}
\]

Therefore v0.2 still does not approach the accepted-logical quality of the fixed 2+0 or 2+1 protocols.

### Versus prior adaptive v0.1

The pure-\(p^2\) coefficient improves:

\[
\epsilon_{L|A}^{2+E}
-
\epsilon_{L|A}^{2+C}
=
-\frac{252538}{225}p^2
+
0\cdot pq
+
O(3).
\]

So the K4 edge receipt is not useless: it removes a finite subset of pure quantum-fault malignant pairs.

However, the mixed coefficient remains exactly

\[
\frac{311}{3}pq
\]

in both adaptive candidates.

**CANDIDATE interpretation:** the added edge-history witness narrows some two-quantum-fault temporal ambiguity but does not close the quantum-plus-readout ambiguity responsible for the mixed term.

## 5. Yield

The first-order acceptance is

\[
\boxed{
Y_{2+E}
=
1-\frac{1136}{15}p-8q-204l+O(2).
}
\]

Relative to 2+0,

\[
Y_{2+E}-Y_{2+0}
=
\frac{1852}{15}p+8q+O(2),
\]

so the adaptive edge-receipt path remains more permissive at first order.

Relative to 2+1,

\[
Y_{2+E}-Y_{2+1}
=
\frac{4121}{15}p+16q+102l+O(2).
\]

Thus the candidate again demonstrates the same core trade: substantially higher yield/resource economy but insufficient accepted-logical protection.

## 6. Ruling

The frozen stop rule was:

> If the degree-two accepted-logical coefficients are larger than 2+0 in every nonnegative \(p/q\) direction, AUTO_FREEZE v0.2 as a no-go for the intended quality target.

That condition is met exactly.

### AUTO_FREEZE

\[
\boxed{\text{2+E v0.2 is NO-GO for the intended adaptive quality target.}}
\]

Valid narrower result retained:

- the K4 edge receipt and cycle checks are exact gauge-history objects;
- they reduce the pure \(p^2\) malignant coefficient relative to v0.1;
- they do not justify recovery from temporal repetition alone.

Any successor must add information not already contained in repeated center+edge snapshots, e.g. a pre-fault temporal receipt, flagged sub-check timing information, or a post-recovery verification object.

## 7. Promotion ledger

- K4 edge cut-space/cycle algebra: **EXACT**
- 2+E degree-two replay: **EXACT SAME-AGENT / GitHub-hosted execution**
- improvement over 2+C pure-\(p^2\): **EXACT**
- intended adaptive quality target: **NO-GO**
- higher-order v0.2 run: **NOT RUN per frozen stop rule**
- hardware validation: **OPEN**
- threshold: **OPEN**
- physical promotion: **0**
