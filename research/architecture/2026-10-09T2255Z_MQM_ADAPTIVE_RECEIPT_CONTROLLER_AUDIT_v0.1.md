# MQM Adaptive Site / Receipt Depth / Integrated Controller Audit v0.1

**Date:** 2026-10-09  
**Physical promotion:** 0

## 1. Adaptive site-calibration controller

The controller accepts measured per-site active-role loss, spare-role loss, and occupancy/readout failure.

For a five-epoch calibration horizon, site \(i\) assigned the spare role \(n_i\) times has cumulative survival

\[
S_i(n_i)=
(1-\ell_{A,i})^{5-n_i}
(1-\ell_{S,i})^{n_i}
(1-r_i)^5.
\]

The primary controller objective is

\[
\max_{\substack{n_i\in\mathbb Z_{\ge0}\\\sum_i n_i=5}}
\min_i S_i(n_i).
\]

A synthetic pre-frozen D5 short/long MOVE-repair matrix is used only as a secondary tie-breaker.

### Homogeneous calibration

With all five sites identical:

\[
\ell_A=0.03,\qquad
\ell_S=0.005,\qquad
r=0.002,
\]

the unique optimum is

\[
\boxed{(1,1,1,1,1)}
\]

with worst-site survival

\[
0.8720928467.
\]

Controller policy:

\[
\boxed{\texttt{UNIFORM}}.
\]

### Known heterogeneous calibration

With

\[
\ell_A=(0.01,0.02,0.03,0.04,0.05),
\]

and common

\[
\ell_S=0.005,\qquad r=0.002,
\]

the unique optimum is

\[
\boxed{(0,0,0,2,3)}
\]

with worst-site survival

\[
0.8501809662.
\]

A canonical five-epoch spare schedule is

\[
(3,3,4,4,4).
\]

Controller policy:

\[
\boxed{\texttt{ASYMMETRIC}}.
\]

Missing required calibration returns

\[
\boxed{\texttt{SOURCE\_BLOCKED}}.
\]

Thus the controller now implements the exact rule previously derived qualitatively:

- homogeneous/unknown site burden -> uniform rotation;
- known heterogeneous site burden -> risk-weighted asymmetric spare frequency.

## 2. Receipt depth versus yield

Three frozen retry-verification modes were compared:

\[
K4\_ONLY,
\qquad
S4\_ONLY,
\qquad
K4+S4.
\]

Their receipt costs are respectively:

\[
6,\quad12,\quad18
\]

bits, with one, one and two receipt layers.

### Exact unsafe orders

K4-only:

\[
U_6
=
4p_6^3(1-p_6)^3
+
3p_6^4(1-p_6)^2
=
4p_6^3+O(p_6^4).
\]

S4-only:

\[
U_{12}
=
6p_{12}^4(1-p_{12})^8
+
16p_{12}^6(1-p_{12})^6
+
9p_{12}^8(1-p_{12})^4
=
6p_{12}^4+O(p_{12}^5).
\]

Combined:

\[
U_{\rm both}
=
4p_6^3+6p_{12}^4+\text{higher/cross terms}.
\]

### Equal-iid receipt benchmark

For every frozen equal-iid point

\[
p\in
\left\{
10^{-4},10^{-3},10^{-2},\frac1{20}
\right\},
\]

the Pareto set is exactly

\[
\boxed{\{K4\_ONLY,\ S4\_ONLY\}}.
\]

The combined two-layer gate is never Pareto under the frozen bit-model objectives.

At

\[
p=0.01,
\]

K4-only:

\[
P_{\rm safe}=0.941480149401,
\]

\[
P_{\rm unsafe}=3.910599\times10^{-6},
\]

\[
P_{\rm HOLD}=0.05851594.
\]

S4-only:

\[
P_{\rm safe}=0.8863848717161292,
\]

\[
P_{\rm unsafe}=5.53797462126\times10^{-8},
\]

\[
P_{\rm HOLD}=0.1136150729041245.
\]

K4+S4:

\[
P_{\rm safe}=0.8345137614500876,
\]

\[
P_{\rm unsafe}=3.51843494125\times10^{-6},
\]

\[
P_{\rm HOLD}=0.1654827201149711.
\]

Therefore the combined gate is not justified merely as a generic iid receipt-bit reliability improvement.

Its justification must be **semantic**: use both layers only when both the native K4 interface receipts and the independent S4 comparison receipts are required.

### Asymmetric frozen grid

At

\[
p_6=10^{-3},\qquad p_{12}=10^{-2},
\]

K4-only becomes the sole Pareto choice.

Other frozen asymmetric points retain K4-only and S4-only as the trade frontier.

### Operational selection rule

\[
\boxed{
\text{Use the shallowest receipt object that actually certifies the required state.}
}
\]

Do not add K4+S4 merely because more verification appears safer.

## 3. Integrated finite-state shell controller

The controller now combines:

1. MOVE calibration;
2. choice of D6 or v128;
3. D5 spare-policy selection;
4. frozen 2+PV execution;
5. channel-loss replacement;
6. configurable K4/S4 receipt verification;
7. fresh retry.

### Configuration policy

If both timing and control+MOVE survival favor v128:

\[
\boxed{\texttt{V128}}.
\]

If both favor D6:

\[
\boxed{\texttt{D6}}.
\]

If the two typed metrics disagree:

\[
\boxed{\texttt{CONFIG\_REVIEW}}.
\]

No scalar weights are invented after exposure.

If required calibration is missing:

\[
\boxed{\texttt{SOURCE\_BLOCKED}}.
\]

All four frozen configuration stress cases return their declared outcomes.

### Repair path

For K4-only:

\[
RUN\_2PV
\to
REPAIRING
\to
RECEIPT\_K4
\to
RETRY\_READY
\to
RUN\_2PV.
\]

For S4-only:

\[
RUN\_2PV
\to
REPAIRING
\to
RECEIPT\_S4
\to
RETRY\_READY
\to
RUN\_2PV.
\]

For both:

\[
RUN\_2PV
\to
REPAIRING
\to
RECEIPT\_K4
\to
RECEIPT\_S4
\to
RETRY\_READY
\to
RUN\_2PV.
\]

The model checker finds

\[
\boxed{0\text{ invariant violations}}
\]

for all three receipt modes.

Locked invariants include:

- ACCEPT only from a current clean 2+PV attempt;
- repair never jumps directly to ACCEPT;
- repaired configurations must pass the configured receipt gate before RETRY_READY;
- RETRY_READY must launch a fresh 2+PV attempt;
- data/hub loss -> QUARANTINE;
- two-or-more detected channel losses -> HOLD;
- no calibration -> SOURCE_BLOCKED;
- conflicting MOVE metrics -> CONFIG_REVIEW.

The latent quantity

\[
UNSAFE\_ACCEPT\_POSSIBLE
\]

from missed channel loss remains an analytic risk object, not an observable controller state.

## Main architecture result

The shell controller now separates three decisions cleanly:

\[
\boxed{
\text{calibrate}
\to
\text{select motion/spare policy}
\to
\text{run}
\to
\text{repair if needed}
\to
\text{verify}
\to
\text{fresh retry}.
}
\]

This removes the previous ambiguity between repair, verification and acceptance.

## Claim ledger

- adaptive calibration-to-spare-policy map: **EXACT under frozen site-channel model**
- receipt depth/yield Pareto result: **EXACT under frozen bit-error families**
- K4+S4 generic iid advantage: **NO-GO under frozen objectives**
- integrated controller invariants: **EXACT model-check pass**
- MOVE hardware selection: **SOURCE-BLOCKED until provider calibration**
- hardware fault tolerance / threshold / quantum advantage: **OPEN**
- physical promotion: **0**
