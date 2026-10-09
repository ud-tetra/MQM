# MQM MOVE / Heterogeneous Spare / Receipt-Gated Retry Audit v0.1

**Date:** 2026-10-09  
**Physical promotion:** 0

## 1. MOVE calibration closure packet

The D6-versus-v128 decision is now reduced to a concrete provider calibration packet.

### Exact candidate contracts

v128 uses four signed frame steps, four moved roles per step, and a 12.2 microsecond local-control burden per signed cycle.

Pure D6 uses six frame steps, seven moved roles per step, and zero local quantum-control gates in the transport-only model.

### Candidate-specific timing inequality

Let tau_v and tau_D denote measured critical-path MOVE durations for one v128/D6 frame step.

v128 is faster iff

\[
12.2+4\tau_v<6\tau_D.
\]

If every transport batch has the same measured duration tau and the machine can move at most P atoms concurrently, the exact break-even is

\[
\tau^*(P)=
\frac{12.2}{
6\lceil 7/P\rceil
-
4\lceil 4/P\rceil
}.
\]

The frozen table is:

| parallel capacity P | v128 batches/step | D6 batches/step | break-even batch duration |
|---:|---:|---:|---:|
| 1 | 4 | 7 | 0.46923 us |
| 2 | 2 | 4 | 0.76250 us |
| 3 | 2 | 3 | 1.22000 us |
| 4 | 1 | 2 | 1.52500 us |
| 5 | 1 | 2 | 1.52500 us |
| 6 | 1 | 2 | 1.52500 us |
| 7 | 1 | 1 | 6.10000 us |
| 8 | 1 | 1 | 6.10000 us |

### Candidate-specific loss inequality

Let ell_v and ell_D denote measured per-moved-role loss probabilities under the actual compiled routes.

Using the already frozen v128 local-control exposure diagnostic

\[
C_v=0.9570935821134408,
\]

v128 has the larger control-plus-MOVE survival product iff

\[
\boxed{
C_v(1-\ell_v)^{16}
>
(1-\ell_D)^{42}.
}
\]

For equal MOVE loss,

\[
\ell^*
=
1-C_v^{1/26}
\approx0.00168527,
\]

or

\[
0.168527\%
\]

per moved-role exposure.

### Required provider measurements

The minimum MOVE record is now explicit:

- candidate/step ID and moved role IDs;
- start/end coordinates and route length;
- duration and parallel group;
- maximum parallel move count;
- retained-state process/PTM or equivalent channel;
- coherent phase shift and dephasing/contrast loss;
- atom-loss probability with uncertainty;
- heating/recapture;
- spectator and route-interaction errors;
- MOVE-loss false-negative and false-positive probabilities;
- raw trials, exclusions, uncertainty method;
- backend, compiler, operating point and calibration window.

Public Sqale material confirms dynamic atom arrays and ongoing atom-motion development, but it does not yet close this per-in-array MOVE record. The 2026 public static-field transport result concerns long-distance atom delivery/cooling and is not interchangeable with in-QPU role transport.

Therefore the hardware decision remains **SOURCE-BLOCKED**.

## 2. Heterogeneous rotating-spare theorem

For site i over T epochs, let n_i be the number of epochs in which site i is assigned the spare role.

Under independent active, spare and check channels,

\[
S_i(n_i)
=
(1-\ell_{A,i})^{T-n_i}
(1-\ell_{S,i})^{n_i}
(1-r_i)^T.
\]

Define negative-log risk

\[
R_i(n_i)
=
-\log S_i(n_i)
=
T(a_i+c_i)-n_i(a_i-s_i),
\]

where

\[
a_i=-\log(1-\ell_{A,i}),
\quad
s_i=-\log(1-\ell_{S,i}),
\quad
c_i=-\log(1-r_i).
\]

The minimax scheduling problem is

\[
\min_{\substack{n_i\in\mathbb Z_{\ge0}\\\sum_i n_i=T}}
\max_i R_i(n_i).
\]

### Homogeneous theorem

If all five sites have identical parameters and active exposure is more costly than spare exposure, the objective is minimized by maximizing the minimum spare count.

For T=5 and five sites,

\[
\boxed{n=(1,1,1,1,1)}
\]

is the unique minimax spare-count vector.

So uniform rotation is exact minimax under homogeneous site parameters.

### Known heterogeneity NO-GO for uniform rotation

Frozen stress profile:

\[
\ell_A=(0.01,0.02,0.03,0.04,0.05),
\]

\[
\ell_S=0.005,
\qquad
r=0.002
\]

at every site.

Uniform rotation gives worst-site survival

\[
0.8023617341.
\]

Exhausting all 126 five-epoch spare-count allocations gives the unique optimum

\[
\boxed{n=(0,0,0,2,3)}
\]

with worst-site survival

\[
0.8501809662.
\]

Absolute gain:

\[
0.0478192320.
\]

Therefore:

\[
\boxed{
\text{known site heterogeneity falsifies uniform rotation as the reliability-minimax policy.}
}
\]

### Unknown/adversarial site labels

If only the frozen multiset of site risks is known and an adversary may assign those risks to physical labels after the schedule is chosen, exhaustive permutation minimax restores

\[
\boxed{n=(1,1,1,1,1)}
\]

as the unique optimum.

Thus rotation has two distinct functions:

- **known calibrated heterogeneity:** adapt the spare frequency to site risk;
- **unknown/adversarial heterogeneity:** uniform rotation is the robust minimax policy.

## 3. D5 replacement + S4 receipt-gated fresh retry

A successful D5 replacement remains a RESTORED_HOLD state. It does not authorize immediate 2+PV acceptance.

The new gate is:

\[
\text{RESTORED\_HOLD}
\to
\text{fresh K4 receipts}
\to
\text{fresh S4 comparison receipts}
\to
\text{RETRY\_READY or HOLD\_RECEIPT}.
\]

All pre-loss receipts are discarded.

### Native K4 receipt layer

The six A4 interface receipt bits form the exact

\[
[6,3,3]
\]

K4 cut-space code with nonzero spectrum

\[
3^4,\qquad4^3.
\]

For iid receipt flip probability p6, the exact nonzero undetected probability is

\[
\boxed{
U_6
=
4p_6^3(1-p_6)^3
+
3p_6^4(1-p_6)^2.
}
\]

Therefore every weight-1 and weight-2 receipt error is detected.

### S4 comparison layer

The 12 octahedral comparison bits form the exact

\[
[12,5,4]
\]

cut-space code with nonzero spectrum

\[
4^6,\qquad6^{16},\qquad8^9.
\]

For iid comparison-bit flip probability p12,

\[
\boxed{
U_{12}
=
6p_{12}^4(1-p_{12})^8
+
16p_{12}^6(1-p_{12})^6
+
9p_{12}^8(1-p_{12})^4.
}
\]

Every error of weight 1, 2 or 3 is detected.

### Combined receipt gate

Let

\[
Z_6=(1-p_6)^6,
\qquad
Z_{12}=(1-p_{12})^{12}.
\]

Under the frozen independent-layer analytic model,

\[
P_{\rm safe}=Z_6Z_{12},
\]

\[
\boxed{
P_{\rm unsafe\ pass}
=
(Z_6+U_6)(Z_{12}+U_{12})-Z_6Z_{12},
}
\]

and

\[
P_{\rm HOLD\ receipt}
=
1-(Z_6+U_6)(Z_{12}+U_{12}).
\]

Leading unsafe order is

\[
\boxed{
4p_6^3+6p_{12}^4+\text{higher/cross terms}.
}
\]

At the frozen 1% iid receipt stress,

\[
P_{\rm unsafe\ pass}
\approx3.5184\times10^{-6},
\]

while

\[
P_{\rm safe}\approx0.834514
\]

and

\[
P_{\rm HOLD\ receipt}\approx0.165483.
\]

This large HOLD cost is expected because two fresh receipt layers are required. It is a verification/yield trade, not a quantum logical-error result.

### Retry rule

Only a receipt-clean restored configuration transitions to RETRY_READY and starts a fresh 2+PV attempt.

Any detected receipt inconsistency remains HOLD_RECEIPT.

## Ruling

- MOVE calibration packet and decision inequalities: **EXACT / DERIVED**
- public quantitative Sqale MOVE closure: **SOURCE-BLOCKED**
- homogeneous rotating spare minimax: **EXACT**
- known-heterogeneity uniform rotation: **NO-GO**
- robust unknown-label uniform rotation: **EXACT minimax for frozen benchmark**
- D5 + K4 + S4 receipt-gated retry: **EXACT analytic protocol**
- receipt code distances: **EXACT binary receipt objects**
- receipt/hardware reliability: **OPEN**
- physical promotion: **0**
