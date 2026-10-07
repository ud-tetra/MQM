# MQM eta-out Parametric Bridge v0.1

**Date:** 2026-10-07  
**Status:** EXACT conditional algebra + SOURCE-BLOCKED physical instantiation  
**Physical promotion:** 0

## Graph partition

For the locked tri-tetra support graph,

\[
|E_{CC}|=6,\qquad |E_{CS}|=4,\qquad |E_{SS}|=5,
\]

and every cut edge is incident on hub 8:

\[
E_{CS}=\{(8,4),(8,5),(8,6),(8,7)\}.
\]

Let the mean nonnegative source-bound weights in the three edge classes be

\[
\bar\omega_{CC},\quad \bar\omega_{CS},\quad \bar\omega_{SS}.
\]

Define

\[
\kappa=\frac{\bar\omega_{CS}}{\bar\omega_{CC}},
\qquad
\lambda=\frac{\bar\omega_{SS}}{\bar\omega_{CC}},
\]

when \(\bar\omega_{CC}>0\). Then

\[
\boxed{
\eta_{\rm cut}
=
\frac{4\kappa}{6+4\kappa}
=
\frac{2\kappa}{3+2\kappa}
}
\]

and

\[
\boxed{
\eta_{\rm shell}
=
\frac{4\kappa+5\lambda}
     {6+4\kappa+5\lambda}.
}
\]

These are ratios of the declared edge-weight object. They are not logical error probabilities.

## Distance-power specialization

If a future source-complete physical model supplies

\[
\omega(r)=K r^{-p},
\]

with one common positive prefactor \(K\), define

\[
\rho_{\rm cut}=\frac{r_{CS}}{r_{CC}},
\qquad
\rho_{\rm shell}=\frac{r_{SS}}{r_{CC}}.
\]

Then

\[
\kappa=\rho_{\rm cut}^{-p},
\qquad
\lambda=\rho_{\rm shell}^{-p}.
\]

A van-der-Waals candidate has \(p=6\); a resonant dipolar/Förster candidate has \(p=3\). These exponents do not identify the actual MQM hardware coupling without a source contract.

## Exact design inversion

For \(0<\epsilon<1\),

\[
\eta_{\rm cut}\le\epsilon
\]

is equivalent to

\[
\boxed{
\kappa
\le
\frac{3\epsilon}{2(1-\epsilon)}.
}
\]

Under the distance-power model,

\[
\boxed{
\rho_{\rm cut}
\ge
\left[
\frac{2(1-\epsilon)}{3\epsilon}
\right]^{1/p}.
}
\]

For \(\epsilon=1/10\),

\[
\kappa\le\frac16,
\]

so

\[
\rho_{\rm cut}\ge6^{1/6}\approx1.348006
\]

for \(p=6\), or

\[
\rho_{\rm cut}\ge6^{1/3}\approx1.817121
\]

for \(p=3\).

For \(\epsilon=1/100\),

\[
\kappa\le\frac1{66},
\]

so

\[
\rho_{\rm cut}\ge66^{1/6}\approx2.010284
\]

for \(p=6\), or

\[
\rho_{\rm cut}\ge66^{1/3}\approx4.041240
\]

for \(p=3\).

These are design sensitivities, not recovered MQM distances.

## Equal-edge diagnostic

If \(\kappa=\lambda=1\),

\[
\eta_{\rm cut}=\frac25,
\qquad
\eta_{\rm shell}=\frac35.
\]

This remains a structural/equal-weight diagnostic unless the frozen coordinate and interaction artifacts independently establish equal source weights.

## Source recovery boundary

The session archive manifest gives frozen hashes for the following source objects:

- MQM_TRI_TETRA_8Q_COORDINATES_v0.1.csv:
  7eabe8d57e0cc94bc4998d38d22e38ec29db01c7e2144c0b961918aec7374ebe
- MQM_TRI_TETRA_CORRELATED_PAIR_RISK_MAP_v0.1.csv:
  ff55a50b9828066130b12f2315dfc778e306d189e1ab4248b9e7a010e1275d06
- MQM_3D_TETRA_VDW_SENTINEL_PULSE_AND_THERMAL_GEOMETRY_ROBUSTNESS_v0.1_LOCK.md:
  b740485c1b5f98cbd87e70193029cc20c45101144a3834c6cb2b0a0094d45f47

Their exact bytes are not currently recoverable through the connected archive path. Therefore \(\kappa,\lambda,\rho_{\rm cut},\rho_{\rm shell}\) are not assigned numerical MQM values here.

## Promotion

- Graph-count formulas: **EXACT**
- Parametric eta formulas: **EXACT**
- Distance-power inversion: **EXACT CONDITIONAL**
- Equal-edge \(2/5,3/5\): **EXACT STRUCTURAL PROXY**
- MQM physical weighted eta: **OPEN / SOURCE-BLOCKED**
- Hardware or logical advantage: **OPEN**
- Physical promotion: **0**
