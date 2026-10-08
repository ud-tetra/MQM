# MQM Repeated Firewall FTEC Addendum v0.1

**Date:** 2026-10-08
**Status:** EXACT finite replay / AUTO_LOCK scoped
**Physical promotion:** 0
**Protocol freeze:** commit d47138705508094f05d629e2a6f2622d02b1e569
**Metric clarification freeze:** commit 841bfe81a322df075997561def441c05b36bcfae
**Replay:** commit 92b824293d0f7309f7e35f775f90637b8c0c05b8
**Machine result:** commit 072c8f5ff38a0df45191c43a98d5fcac78ed38b3

## Result

The firewall-aware 39-two-qubit-interaction extraction candidate does **not** satisfy the expanded fault contract when used as a one-round recovery controller.

Under the frozen one-round protocol, 1141 exact single-fault cases were tested:

\[
1141=7\cdot163.
\]

The result is:

\[
727\ {\rm ACCEPT},\quad
174\ {\rm HOLD},\quad
88\ {\rm QUARANTINE},\quad
152\ {\rm FAIL}.
\]

The 152 failures factor as

\[
152=2^3\cdot19.
\]

They arise from:

- 87 two-qubit Pauli faults;
- 44 basis-rotation Pauli faults;
- 21 data-idle Pauli faults.

No one-round failure is attributed to the six core-edge circuits.

The failure mechanism is temporal: one physical fault can change the data while the four center checks are being collected, so a single sequential syndrome frame can combine pre-fault and post-fault information. The resulting internally inconsistent frame can select a Pauli-frame recovery that produces a protected logical error.

The earlier 0/585 hook certificate remains valid in its narrower scope. It did not certify the noisy syndrome record plus recovery decision.

## Repeated state machine

The frozen repair was fixed before evaluation.

### Acquisition

Run three complete extraction rounds:

\[
R_1,\ R_2,\ R_3.
\]

For each of the four center syndrome coordinates, take the bitwise majority

\[
m_i={\rm maj}(b_i^{(1)},b_i^{(2)},b_i^{(3)}).
\]

Thus

\[
m=(m_1,m_2,m_3,m_4).
\]

Map the firewall basis coordinates back to the frozen release coordinates:

\[
s=(m_1,m_3,m_2\oplus m_3,m_4).
\]

Apply the frozen minimum-weight recovery as a **classical Pauli-frame update**. No physical recovery gate is introduced.

Any center flag, missing receipt, stale receipt or detected ancilla loss returns HOLD. Detected data loss returns QUARANTINE.

### Verification

Run one complete verification round \(R_V\).

Accept only if:

1. the verification record is complete and fresh;
2. no center flag fires;
3. no loss is detected;
4. the center syndrome relative to the updated Pauli frame is \(0000\).

A nonzero verification syndrome returns HOLD.

If a single fault occurs late in the verification round after the relevant syndrome information has already been collected, acceptance is still permitted only when the final residual has protected logical class \(I\) and dressed subsystem weight at most one.

## Exact single-fault campaign

Each round contains 1141 declared fault cases:

- 585 two-qubit Pauli faults;
- 264 data-idle Pauli faults;
- 114 basis-rotation Pauli faults;
- 88 ideally detected data-loss cases;
- 30 syndrome reset/preparation Pauli faults;
- 14 ancilla-loss cases;
- 12 flag reset/preparation Pauli faults;
- 10 stale-receipt cases;
- 10 missing-receipt cases;
- 6 edge-measurement bit flips;
- 4 center-syndrome measurement bit flips;
- 4 center-flag measurement bit flips.

Across four possible fault rounds,

\[
4564=2^2\cdot7\cdot163
\]

single-fault cases were evaluated.

The exact result is

\[
\boxed{
1969\ {\rm ACCEPT},\
2243\ {\rm HOLD},\
352\ {\rm QUARANTINE},\
0\ {\rm FAIL}
}
\]

under the frozen fault model.

Among accepted outputs,

\[
1608
\]

end with dressed residual weight zero and

\[
361
\]

with dressed residual weight one. Every accepted case has protected logical class \(I\).

The 361 accepted weight-one residuals all occur when the unique fault is in the terminal verification round. This is the expected distance-3 1-EC behavior: a fault in the correction gadget may leave at most one correctable physical error but must not create a protected logical error.

## Standard input-error condition

The second 1-EC condition was tested separately.

For each of

\[
8\cdot3=24
\]

single-qubit nonidentity Pauli input errors, with no circuit fault, the repeated state machine:

- accepts;
- returns zero center syndrome after Pauli-frame recovery;
- leaves dressed residual weight zero;
- preserves logical class \(I\).

Result:

\[
\boxed{24/24\ {\rm PASS}}.
\]

## Scoped FTEC ruling

### EXACT / AUTO_LOCK

Within the frozen model:

- subsystem-8 algebra from the release;
- firewall-aware direct-center basis;
- declared Clifford extraction circuits;
- Pauli faults after declared gates;
- declared preparation/reset and measurement faults;
- declared idle faults;
- ideal loss indication;
- fail-closed HOLD/QUARANTINE;
- classical Pauli-frame recovery;

the repeated three-acquisition-plus-one-verification state machine satisfies the tested distance-3 **single-fault 1-EC conditions**.

This is a scoped FTEC state-machine certificate, not a threshold theorem.

### NOT promoted

The result does not establish:

- stochastic logical error rate on hardware;
- missed-loss behavior;
- leakage outside the Pauli/erasure model;
- coherent overrotation or non-Pauli gate noise;
- correlated multi-location faults;
- decoder latency bounds;
- a fault-tolerant logical gate exRec;
- a threshold;
- hardware advantage;
- quantum advantage.

# Noisy decoder comparison

A separate frozen phenomenological benchmark isolates syndrome-readout noise.

## Input ensemble

Condition on one incoming physical Pauli error, uniformly over all 24 single-qubit Pauli errors.

The data error remains fixed while syndrome frames are read.

Each of the four center syndrome bits flips independently with probability \(q\).

No circuit fault, loss or flag process is included in this separate benchmark.

For logical scoring only, after the tested noisy recovery an analysis-only ideal cleanup of any residual syndrome is applied. A failure means the resulting normalizer element is nonidentity in the protected logical quotient.

## One-round decoder

Exact failure counts by number \(k\) of flipped center bits are:

\[
\begin{array}{c|cc}
k & {\rm cases} & {\rm logical\ failures}\\
\hline
0&24&0\\
1&96&60\\
2&144&102\\
3&96&72\\
4&24&18
\end{array}
\]

Therefore

\[
\boxed{
F_1(q)
=
\frac52q-\frac{13}{4}q^2+2q^3-\frac12q^4.
}
\]

The leading readout-induced logical term is first order:

\[
F_1(q)=\frac52q+O(q^2).
\]

## Three-round majority decoder

For one syndrome bit, three-read majority has effective error probability

\[
\boxed{
r(q)=3q^2-2q^3.
}
\]

Because the four center-bit majority votes use disjoint independent readout bits,

\[
\boxed{
F_3(q)=F_1(r(q)).
}
\]

Expanded,

\[
\begin{aligned}
F_3(q)
={}&
\frac{15}{2}q^2
-5q^3
-\frac{117}{4}q^4
+39q^5
+41q^6
-108q^7\\
&+\frac{63}{2}q^8
+92q^9
-108q^{10}
+48q^{11}
-8q^{12}.
\end{aligned}
\]

A direct enumeration of

\[
98304=2^{15}\cdot3
\]

raw three-round readout patterns independently reproduces the same polynomial.

No logical failures occur at raw readout Hamming weight zero or one.

Thus

\[
F_3(q)
=
\frac{15}{2}q^2+O(q^3).
\]

### Exact dominance

For

\[
0<q<\frac12,
\]

\[
q-r(q)
=
q(1-q)(1-2q)>0.
\]

Also

\[
F_1'(q)
=
\frac{(1-q)\left(4(q-1)^2+1\right)}{2}
>0
\]

through that interval.

Therefore

\[
\boxed{
F_3(q)<F_1(q)
\qquad
(0<q<1/2).
}
\]

So the frozen three-round majority decoder suppresses the readout-induced protected-logical failure term from first order to second order in \(q\) for this phenomenological benchmark.

## Resource debit

The protection is not free.

One full candidate round uses

\[
39=3\cdot13
\]

two-qubit gates and 14 measurements.

The fixed three-acquisition-plus-one-verification state machine uses at most

\[
4\cdot39
=
156
=
2^2\cdot3\cdot13
\]

two-qubit gates and

\[
4\cdot14=56
\]

measurements.

Peak extra ancillas remain two because the same syndrome/flag pair can be reset and reused sequentially.

Thus the mathematical closure is a **correctness-for-latency/yield trade**. Physical usefulness requires a stochastic noise model and matched baseline that charge the fourfold circuit exposure and the HOLD/QUARANTINE rate.

## Promotion ledger

- One-round expanded single-fault controller: **NO-GO under frozen contract**
- Repeated 3+1 single-fault state machine: **EXACT / AUTO_LOCK scoped**
- 24 single-input-error condition: **EXACT / AUTO_LOCK scoped**
- Readout polynomial \(F_1\): **EXACT**
- Three-majority polynomial \(F_3\): **EXACT**
- \(F_3<F_1\) for \(0<q<1/2\): **EXACT**
- Full stochastic circuit logical rate: **OPEN**
- Hardware loss/readout calibration: **OPEN**
- Fault-tolerance threshold: **OPEN**
- Hardware validation: **OPEN**
- Quantum advantage: **OPEN**
- Physical promotion: **0**
