# MQM v128 / Transport / D5 Replacement Audit v0.1

**Date:** 2026-10-09  
**Physical promotion:** 0

## v128 native compile

Kernel element 128 has exact phase-quotiented transform

\[
p=(4\,6)(5\,7)
\]

with local Clifford words

\[
(I,I,I,HS,HS,SH,SH,I).
\]

An exact batched native local schedule is

1. \(S\) on qubits 6,7;
2. \(H\) on 4,5,6,7;
3. \(S\) on 4,5.

Its signed cycle period is

\[
T_\pm=4.
\]

### Gate-SWAP realization

Over one signed cycle:

\[
104\ GR,\qquad784\ R_Z,\qquad24\ CZ,
\]

with parallel-layer pulse time about

\[
156.584\ \mu s.
\]

The frozen cross-profile coherent unitary infidelity is approximately

\[
0.93792.
\]

This implementation is not viable under the stress model.

### Transport-assisted realization

Replace the two SWAPs per step by ideal atom-role transport while retaining the local Clifford schedule.

Over one signed cycle:

\[
8\ GR,\qquad64\ R_Z,\qquad0\ CZ,
\]

with local-control pulse time

\[
12.2\ \mu s.
\]

Cross-profile coherent unitary infidelity falls to

\[
\boxed{0.03490}.
\]

For comparison, transport-assisted \(b\) requires

\[
24\ GR,\qquad180\ R_Z,\qquad0\ CZ,
\]

about

\[
34.35\ \mu s
\]

of local-control time and gives stress infidelity

\[
0.15775.
\]

Thus v128 materially outperforms b under the same ideal-transport cross-profile control stress.

The transport itself remains ideal in this test. MOVE time, dephasing, heating, collision/crosstalk and atom loss are OPEN.

## Exact spectator-free identity-motion search

Searching all 192 protected-logical-identity elements for either:

- pure permutation transitions; or
- nontrivial uniform local Clifford action on all eight qubits

found exactly

\[
\boxed{12}
\]

candidates, all pure permutations.

There is no nontrivial uniform-local-Clifford identity motion in the current kernel under this criterion.

The strongest zeroth-order coherent averaging in this spectator-free class is the order-6 pair

\[
\boxed{\text{IDs }632,824}
\]

with

\[
\bar A_0=\frac13.
\]

These are the two orientations of the exact D6 order-6 permutation generator family.

They move seven roles per step, giving

\[
42
\]

moved-role exposures per signed cycle, but require zero quantum control gates in the ideal transport model.

Other exact transport trade points include:

\[
\bar A_0=\frac{15}{28}
\]

at 12 moved-role exposures,

\[
\bar A_0=\frac47
\]

at 9 moved-role exposures,

\[
\bar A_0=\frac{13}{21}
\]

at 8 moved-role exposures, and

\[
\bar A_0=\frac{65}{84}
\]

at 4 moved-role exposures.

This makes physical atom transport, rather than global-pulse synthesis, the clean spectator-free motion frontier for the current code.

## D5 four-channel plus spare mapping

Map the four exact hub-cut channels

\[
(8,4),(8,5),(8,6),(8,7)
\]

to four D5 ring slots, leaving the fifth slot as a spare channel ancilla/coupler.

The slot objects are ancillas/couplers. They do not replace data qubits 4--8.

There are

\[
5\cdot4!=120
\]

raw labeled assignments, all sharing the same terminal-distance geometry.

For a fixed spare, two active slots are at replacement distance

\[
2,
\]

and two at distance

\[
1+\sqrt5.
\]

Hence

\[
\boxed{
\bar d_{\rm replace}
=
\frac{3+\sqrt5}{2}
}
\]

and

\[
d_{\max}=1+\sqrt5.
\]

## Exact loss/replacement algebra

Let:

- \(\ell_A\): active channel-ancilla loss probability;
- \(\ell_S\): spare loss probability;
- \(m\): missed active-loss probability;
- \(\mu\): replacement MOVE failure/loss;
- \(\rho\): reset/prepare failure;
- \(\nu\): post-replacement verification failure.

Define

\[
r=(1-m)(1-\mu)(1-\rho)(1-\nu).
\]

The exact probability of ending the epoch with all four channel ancillas active is

\[
\boxed{
P_4
=
(1-\ell_A)^4
+
4\ell_A(1-\ell_A)^3(1-\ell_S)r.
}
\]

The exact unsafe missed-loss probability is

\[
\boxed{
P_{\rm unsafe}
=
1-(1-\ell_A m)^4.
}
\]

Under the frozen fail-closed policy,

\[
P_{\rm HOLD}=1-P_4-P_{\rm unsafe}.
\]

With ideal detection/replacement, the architecture corrects any single active channel-ancilla loss when the spare survives the epoch. Two or more active losses, or one active loss with no spare, fail closed.

Data or hub loss is outside this mechanism and still causes QUARANTINE.

## NDSSR-only stress

Using only the published approximately 1% state-average NDSSR atom-loss value as

\[
\ell_A=\ell_S=0.01
\]

and optimistically setting

\[
m=\mu=\rho=\nu=0,
\]

gives

\[
P_4=0.9990198504.
\]

Without the spare,

\[
P_4^{(0)}=0.99^4=0.96059601.
\]

The absolute availability gain is

\[
0.0384238404.
\]

The apparent failure reduction is about

\[
97.51\%.
\]

This number is an optimistic partial-channel stress only. It is not a hardware prediction because MOVE/reset/loss-detector errors are still source-open, and the 1% number is specifically readout-associated loss.

## Ruling

- v128 gate-SWAP compile: **NO-GO under cross-profile stress**
- v128 transport-assisted compile: **CANDIDATE PASS of the local-control stress; MOVE channel OPEN**
- spectator-free identity-motion class: **EXACTLY 12 pure permutations**
- nontrivial uniform-global identity Clifford: **NO-GO under current kernel**
- D6 order-6 pure transport pair: **bright spectator-free motion frontier**
- D5 four-channel plus one-spare mapping: **EXACT**
- one detected channel-ancilla loss replacement: **EXACT conditional protocol**
- hardware availability advantage: **OPEN**
- physical promotion: **0**
