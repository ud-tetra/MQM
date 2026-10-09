# MQM Identity-Motion Exposure Amendment v0.1

**Date:** 2026-10-09  
**Status:** VERSIONED CORRECTION / NO SCIENTIFIC RESULT DELETED  
**Physical promotion:** 0

The first identity-motion dynamics report used the phase-quotiented frame order \(T_F\) when reporting primitive exposure for one coherent averaging cycle.

The second-order Magnus benchmark requires the **signed Pauli-conjugation period** \(T_\pm\), because the coherent toggling sequence does not close until Pauli signs also return.

Therefore the correct physical primitive exposure for a complete coherent averaging cycle is

\[
N_{\rm coh}=C_{\rm step}T_\pm.
\]

Corrected values are:

| motion | old frame-order exposure | signed period | corrected coherent-cycle exposure |
|---|---:|---:|---:|
| \(I\) | 0 | 1 | 0 |
| \(a\) | 6 | 2 | 6 |
| \(b\) | 36 | 6 | 72 |
| \(ab\) | 36 | 8 | 72 |
| \(zb\) | 54 | 12 | 108 |

The prior qualitative loss conclusion is unchanged and strengthened:

for independent per-primitive loss \(\ell>0\),

\[
P_{\rm survive}=(1-\ell)^{N_{\rm coh}},
\]

so added physical controls reduce survival unless a separate compensating mechanism is demonstrated.

Virtual frame tracking still adds zero primitive exposure.

This amendment does not alter the previously reported first-order coherent averaging metrics or stochastic Pauli NO-GO result.
