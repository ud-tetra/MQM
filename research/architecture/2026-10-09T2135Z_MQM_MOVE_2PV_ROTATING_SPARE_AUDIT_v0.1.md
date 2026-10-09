# MQM MOVE / 2+PV / Rotating-Spare Audit v0.1

**Date:** 2026-10-09  
**Physical promotion:** 0

## 1. v128 versus pure D6 transport

The comparison keeps motion channels symbolic.

### Ideal coherent-motion diagnostic

\[
v128:
\qquad
A_0=\frac{23}{63},
\qquad
K_2=\frac{78}{1265},
\]

\[
D6:
\qquad
A_0=\frac13,
\qquad
K_2=\frac{413}{6325}.
\]

D6 has the lower zeroth-order residual, while v128 has the lower second-order coefficient.

For the frozen diagnostic

\[
R(\eta)=\sqrt{A_0}+\eta\sqrt{K_2},
\]

the crossing is

\[
\eta_* \approx 3.72273.
\]

Thus D6 is preferred below this diagnostic crossing and v128 above it. This is an ideal Magnus comparison, not a hardware threshold.

### MOVE timing

Let \(\tau_M\) be one concurrent atom-transport epoch.

Then

\[
t_v=12.2+4\tau_M
\]

and

\[
t_{D6}=6\tau_M.
\]

Therefore

\[
\boxed{\tau_M^*=6.1\ \mu s}.
\]

D6 is faster below \(6.1\,\mu s\) per move epoch; v128 is faster above it.

For fully serial role moves with per-role duration \(\tau_r\),

\[
t_v=12.2+16\tau_r,
\]

\[
t_{D6}=42\tau_r,
\]

giving

\[
\boxed{\tau_r^*=\frac{12.2}{26}\approx0.46923\ \mu s}.
\]

### MOVE loss

Ignoring local-control exposure:

\[
S_v=(1-\ell_M)^{16},
\]

\[
S_{D6}=(1-\ell_M)^{42}.
\]

Therefore v128 has strictly larger move-only survival for every

\[
0<\ell_M<1.
\]

Including the previously frozen v128 local-control product diagnostic

\[
C_v=0.9570935821134408,
\]

compare

\[
S_v=C_v(1-\ell_M)^{16}
\]

against

\[
S_{D6}=(1-\ell_M)^{42}.
\]

The crossing is

\[
\boxed{
\ell_M^*
=
1-C_v^{1/26}
\approx0.00168527
}
\]

or approximately

\[
0.1685\%
\]

per moved-role exposure.

Below that diagnostic loss, pure D6 has the larger product; above it, v128 does.

This is a typed product diagnostic, not a calibrated success probability.

### T2* timing/product diagnostic

Using the public \(T_2^*=12.7\) ms value and multiplying by an exponential idle diagnostic gives much larger break-even move durations:

- concurrent move epoch: approximately \(284.57\,\mu s\);
- serial moved-role duration: approximately \(21.89\,\mu s\).

These numbers reflect the v128 local-control exposure product and are not a measured dephasing law.

## 2. D5 channel layer integrated with 2+PV

Let the frozen 2+PV controller outcome probabilities, before channel-layer faults, be

\[
A+H+Q=1,
\]

for ACCEPT, HOLD and QUARANTINE.

Define:

- \(\ell_A\): active channel-ancilla loss;
- \(\ell_S\): spare loss;
- \(m\): missed active-loss probability;
- \(\mu\): replacement MOVE failure/loss;
- \(\rho\): reset/prepare failure;
- \(\nu\): post-replacement verification failure.

### Channel probabilities

No active channel loss:

\[
P_{\rm clean}=(1-\ell_A)^4.
\]

No detected loss but at least one missed active loss:

\[
\boxed{
P_{\rm unsafe}
=
(1-\ell_A(1-m))^4-(1-\ell_A)^4.
}
\]

At least one detected active loss:

\[
P_{\rm det}
=
1-(1-\ell_A(1-m))^4.
\]

Exactly one detected loss, with successful spare replacement:

\[
P_{\rm repair}
=
4\ell_A(1-m)(1-\ell_A)^3
(1-\ell_S)(1-\mu)(1-\rho)(1-\nu).
\]

### Combined state machine

Safe ACCEPT:

\[
\boxed{
P_{\rm SA}
=
A(1-\ell_A)^4.
}
\]

Possible unsafe ACCEPT:

\[
\boxed{
P_{\rm UA}
=
A\left[
(1-\ell_A(1-m))^4-(1-\ell_A)^4
\right].
}
\]

HOLD:

\[
\boxed{
P_{\rm HOLD}
=
H+A\left[1-(1-\ell_A(1-m))^4\right].
}
\]

QUARANTINE remains

\[
\boxed{P_{\rm Q}=Q}.
\]

The successfully repaired subset of HOLD is

\[
\boxed{
P_{\rm restored\ HOLD}
=
(A+H)P_{\rm repair}.
}
\]

A successful replacement does **not** retroactively validate the interrupted attempt. It restores the four-channel configuration for a fresh 2+PV retry.

### First-order active-loss behavior

\[
P_{\rm clean}
=
1-4\ell_A+O(\ell_A^2),
\]

\[
P_{\rm unsafe}
=
4\ell_A m+O(\ell_A^2),
\]

\[
P_{\rm det}
=
4\ell_A(1-m)+O(\ell_A^2).
\]

So missed-loss detection enters at linear order.

### NDSSR-only optimistic stress

With

\[
A=1,\quad H=Q=0,
\]

\[
\ell_A=\ell_S=0.01,
\]

and ideal

\[
m=\mu=\rho=\nu=0,
\]

the current attempt has

\[
P_{\rm SAFE\ ACCEPT}=0.96059601,
\]

\[
P_{\rm HOLD}=0.03940399.
\]

Of that HOLD mass,

\[
0.0384238404
\]

is successfully restored and ready for a fresh retry.

Therefore the earlier \(0.9990198504\) figure must be interpreted as **post-repair four-channel readiness**, not same-attempt ACCEPT probability.

This distinction is now locked.

## 3. Rotating D5 spare schedule

### Five-epoch base cycle

At epoch \(t\), slot \(A_t\) is spare and channel \(C_j\) uses

\[
A_{t+j+1\pmod5}.
\]

Over five epochs, exactly:

- every physical slot is spare once;
- every physical slot is active four times;
- every physical slot receives five total occupancy/readout checks;
- every logical channel visits every physical slot exactly once.

Thus slot burden is exactly equalized.

However replacement distance is channel-biased in this shortest five-epoch cycle:

- two channel labels always see the short distance \(2\);
- two always see the long distance \(1+\sqrt5\).

### Ten-epoch balanced supercycle

Use channel offsets

\[
(1,2,3,4)
\]

for the first five epochs and

\[
(2,1,4,3)
\]

for the second five.

Then exactly:

- every slot is spare twice;
- every slot is active eight times;
- every slot receives ten total checks;
- every channel visits every slot twice;
- every channel sees five short and five long replacement opportunities.

Hence every channel has the same mean replacement distance

\[
\boxed{
\bar d
=
\frac{3+\sqrt5}{2}.
}
\]

This closes the deterministic burden-equalization problem.

### Homogeneous-loss NO-GO

If every slot has identical iid active/spare loss channels, rotating the spare cannot change per-epoch loss probabilities because every epoch still contains four active slots and one spare.

Therefore rotation has **no reliability advantage in the homogeneous iid model**.

Its candidate value is specifically against:

- site-dependent loss;
- site drift;
- readout wear;
- motion/crosstalk asymmetry.

Those hardware channels remain OPEN.

## Ruling

- MOVE break-even surfaces: **DERIVED / typed**
- v128 move-only survival advantage: **EXACT conditional on equal per-role loss**
- pure D6 zeroth-order coherent advantage: **EXACT ideal-model**
- 2+PV + D5 state composition: **EXACT**
- same-attempt replacement ACCEPT: **NO-GO**
- fresh-retry restoration: **EXACT**
- five-epoch physical-slot equalization: **EXACT**
- ten-epoch slot + channel-distance equalization: **EXACT**
- rotating-spare homogeneous reliability gain: **NO-GO**
- hardware MOVE/detector/site-heterogeneity advantage: **OPEN**
- physical promotion: **0**
