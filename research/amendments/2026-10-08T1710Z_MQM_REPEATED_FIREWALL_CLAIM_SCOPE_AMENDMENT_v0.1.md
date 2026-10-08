# MQM Repeated Firewall Claim-Scope Amendment v0.1

**Date:** 2026-10-08  
**Status:** CLAIM-SCOPE REPAIR / NO DATA CHANGE  
**Physical promotion:** 0  
**Parent result:** research/bridges/2026-10-08T1655Z_MQM_REPEATED_FTEC_NOISY_DECODER_RESULTS_v0.1.json  
**Parent report:** research/bridges/2026-10-08T1658Z_MQM_REPEATED_FIREWALL_FTEC_ADDENDUM_v0.1.md

## Ruling

The arithmetic and exact same-agent constructor replay are retained.

The broad wording "single-fault FTEC pass" is narrowed. The result is more accurately classified as:

> **EXACT SAME-AGENT / FAIL-CLOSED SINGLE-FAULT SAFETY CERTIFICATE under the frozen model.**

It is not yet a high-yield correction result.

Independent reproduction remains OPEN.

## Exact campaign accounting

The one-round campaign remains:

\[
727+174+88+152=1141=7\cdot163.
\]

The 152 FAIL cases remain scoped to the expanded controller test and do not contradict the earlier 0/585 hook-containment result.

The repeated campaign remains:

\[
1969+2243+352+0=4564=4\cdot1141.
\]

Under the frozen criterion:

- ACCEPT = 1969;
- HOLD = 2243;
- QUARANTINE = 352;
- FAIL = 0.

HOLD plus QUARANTINE is

\[
2595
\]

of 4564 enumerated single-fault cases:

\[
\frac{2595}{4564}
\approx 0.5685801928.
\]

The ACCEPT fraction in the same **uniform enumeration of fault cases** is

\[
\frac{1969}{4564}
\approx 0.4314198072.
\]

### Typed provenance

These fractions are **not physical yield probabilities**. The campaign enumerates fault cases equally; a physical yield requires a frozen stochastic weighting using \(p\), \(q\), and \(p_{\rm loss}\) or a more detailed source-bound noise model.

Nevertheless, HOLD and QUARANTINE are non-corrections and must be charged as rejected yield in any performance comparison.

## Accepted residuals

Among the 1969 ACCEPT outcomes:

\[
1608
\]

have dressed residual weight 0 and

\[
361
\]

have dressed residual weight 1.

Thus

\[
\frac{361}{1969}\approx0.1833417979
\]

of the accepted **enumerated fault cases** retain one correctable dressed error.

All 361 occur when the unique fault lies in the terminal verification round.

Therefore ACCEPT means:

- protected logical class \(I\);
- residual dressed weight at most one;

not necessarily an error-free physical data block.

## Separate 24/24 condition

The

\[
24/24
\]

single-qubit input-error result is a separate fault-free-extraction condition.

It is not included in the 4564 clean-input single-circuit-fault cases and must not be combined with that denominator.

## Decoder scope

The identities

\[
r(q)=3q^2-2q^3,
\]

\[
F_1(q)=\frac52q-\frac{13}{4}q^2+2q^3-\frac12q^4,
\]

and

\[
F_3(q)=F_1(r(q))
\]

remain exact within the frozen phenomenological decoder model.

The direct enumeration count

\[
98304=2^{15}\cdot3
\]

belongs to that separate decoder benchmark, not the circuit-fault campaign.

The result that the leading readout-induced protected-logical term changes from

\[
O(q)
\]

to

\[
O(q^2)
\]

does not price two-qubit faults, idle faults, reset faults, or loss.

## Resource accounting

The resource debit remains

\[
39\to156
\]

two-qubit gates and

\[
14\to56
\]

measurements, with peak extra ancillas equal to two.

Ideal-detected loss remains an assumption.

## Corrected promotion ledger

- One-round expanded controller: **NO-GO under frozen contract**
- Repeated 3+1 zero-FAIL enumeration: **EXACT SAME-AGENT**
- Repeated 3+1 accepted-output logical safety under the frozen single-fault model: **EXACT SAME-AGENT**
- High-yield error correction: **OPEN**
- Physical acceptance yield: **OPEN**
- Independent circuit replay: **OPEN**
- Multi-fault logical rate: **OPEN**
- Threshold: **OPEN**
- Hardware validation: **OPEN**
- Quantum advantage: **OPEN**
- Physical promotion: **0**

The phrase "AUTO_LOCK scoped FTEC certificate" is therefore superseded for interpretation by:

> **AUTO_LOCK scoped fail-closed single-fault safety certificate; deterministic/high-yield correction not established.**

## Next-gate metric

A two-fault/stochastic campaign is not decision-relevant unless the noise weighting is frozen before evaluation.

At minimum freeze:

\[
p,\qquad q,\qquad p_{\rm loss},
\]

with explicit per-location semantics.

For each candidate and baseline report separately:

\[
Y=P({\rm ACCEPT}),
\]

\[
P_{\rm hold}=P({\rm HOLD}),
\qquad
P_{\rm quarantine}=P({\rm QUARANTINE}),
\]

and the primary quality metric

\[
\boxed{
\epsilon_{L|A}
=
P(\text{protected logical failure}\mid {\rm ACCEPT})
=
\frac{P(\text{logical failure}\cap{\rm ACCEPT})}{Y}.
}
\]

Do not count HOLD or QUARANTINE as successful correction.

A useful throughput companion is

\[
Y_{\rm good}
=
P({\rm ACCEPT\ and\ logical\ success})
=
Y(1-\epsilon_{L|A}).
\]

Resource-normalized comparison may additionally report two-qubit gates, measurements, latency, and executions per accepted-good shot.

## Freeze requirement for next campaign

Before any two-fault evaluation:

1. define the exact stochastic meaning of \(p\), \(q\), \(p_{\rm loss}\);
2. freeze location counts and mutually-exclusive/simultaneous fault semantics;
3. freeze ACCEPT/HOLD/QUARANTINE/FAIL classification;
4. freeze the baseline;
5. freeze \(\epsilon_{L|A}\) and \(Y\) as co-primary outputs;
6. freeze any numerical parameter points or report an exact symbolic polynomial;
7. do not retune the schedule after result exposure without a new version and fresh evaluation.
