# MQM Sqale Source Calibration Audit v0.1

**Date:** 2026-10-08  
**Platform:** Infleqtion Sqale / cesium neutral-atom processor  
**Status:** EMPIRICAL-HARDWARE SOURCE VALUES + PARTIAL MODEL BRIDGE / NO-GO for the frozen scalar triple  
**MQM physical promotion:** 0

## Objective

Attempt to bind the frozen abstract stochastic parameters

\[
(p,q,p_{\rm loss})
\]

to public measured values from one named neutral-atom platform before making any hardware-ranking or threshold claim.

The result is **partial**. Public Sqale measurements constrain several typed hardware quantities, but they do not support a single source-complete value for each of the three homogeneous benchmark parameters.

## Public source values

### Entangling gate

The 2025 Infleqtion logical-qubit experiment reports an array-median **loss-post-selected CZ fidelity**

\[
F_{\rm CZ|retained}=99.48\%.
\]

The corresponding conditional infidelity is

\[
1-F_{\rm CZ|retained}
=
0.0052
=
\frac{13}{2500}.
\]

This is a measured/post-selected CZ quantity. It is not automatically the probability of a uniformly random two-qubit Pauli.

An earlier PRX Quantum hardware characterization reports \(99.35(4)\%\) CZ fidelity including leakage from the computational basis and \(99.73(3)\%\) when atom-loss events are excluded. Those differently conditioned fidelities must not be subtracted and relabeled as a standalone loss probability without a common operational definition.

### Single-qubit gates

The same 2025 system-performance summary gives median fidelities approximately

\[
F_{R_Z}=99.81\%,\qquad
F_{\rm GR}=99.96\%.
\]

Their raw infidelity scales are therefore

\[
1-F_{R_Z}=0.0019,
\qquad
1-F_{\rm GR}=0.0004.
\]

These are materially different from the CZ infidelity.

### Measurement

The source's circuit-level noise model, informed by hardware characterization, gives asymmetric NDSSR state-conversion probabilities

\[
\epsilon_{1\to0}=0.028=\frac{7}{250},
\]

\[
\epsilon_{0\to1}=0.004=\frac{1}{250}.
\]

Therefore the frozen benchmark's single symmetric measurement bit-flip rate \(q\) has **no unique source-complete value** without fixing the bright/dark population presented to every measurement.

Two useful but non-canonical projections are:

- equal-population average:
  \[
  q_{\rm bal}
  =
  \frac{0.028+0.004}{2}
  =
  0.016
  =
  \frac{2}{125};
  \]
- conservative state-independent envelope:
  \[
  q_{\max}=0.028=\frac{7}{250}.
  \]

Both introduce an additional modeling rule. Neither is the measured object itself.

### Atom loss

For NDSSR in the 2025 logical experiment, the source reports approximately

\[
p_{\rm loss}^{\rm NDSSR}=0.01
\]

state-average atom loss per site during state measurement.

The earlier PRX Quantum characterization reports nondestructive readout with

\[
0.9(3)\%
\]

loss.

These values calibrate **readout-associated loss**, not a uniform loss probability at every MQM inter-check boundary, gate, reset, or ancilla epoch.

## Frozen benchmark compatibility audit

### Scalar \(p\): NO-GO as hardware calibration

The frozen stochastic benchmark applies one \(p\) to:

- 39 two-qubit gates per round;
- 38 one-qubit basis-rotation locations;
- 14 preparation/reset locations;
- 88 idle locations.

Sqale exposes materially different error scales for CZ, \(R_Z\), and global rotations, while public source-complete preparation/reset and idle error probabilities aligned to the MQM locations are not available.

Therefore

\[
\boxed{\text{one hardware-calibrated scalar }p\text{ is not source-supported}.}
\]

A conservative **stress projection**

\[
p^\star=0.0052=\frac{13}{2500}
\]

may be applied to every \(p\)-location only if explicitly labeled as a two-qubit-dominant envelope/proxy. It is not a calibrated hardware model.

### Scalar \(q\): NO-GO without state distribution

The measured readout channel is asymmetric:

\[
q_{1\to0}\ne q_{0\to1}.
\]

The frozen symmetric \(q\) therefore requires a separately frozen state/population model or a conservative envelope.

No unique hardware-calibrated scalar \(q\) is admitted.

### Uniform \(p_{\rm loss}\): NO-GO

The frozen benchmark supplies one \(p_{\rm loss}\) to 102 loss opportunities per round, including 88 data-boundary epochs and 14 ancilla epochs.

The public Sqale number is specifically a per-site loss rate associated with nondestructive state readout.

Assigning

\[
p_{\rm loss}=0.01
\]

to every frozen loss epoch would multiply one typed readout-loss measurement across physically different locations without evidence.

Therefore

\[
\boxed{\text{the frozen uniform }p_{\rm loss}\text{ cannot be hardware calibrated from the current public record}.}
\]

## Typed partial calibration

The admissible source-bound hardware ledger is instead

\[
p_{\rm CZ|retained}\approx0.0052,
\]

\[
p_{R_Z,\rm infidelity}\approx0.0019,
\]

\[
p_{\rm GR,\rm infidelity}\approx0.0004,
\]

\[
q_{1\to0}\approx0.028,
\qquad
q_{0\to1}\approx0.004,
\]

\[
p_{\rm loss}^{\rm NDSSR}\approx0.01.
\]

These values are not equal typed objects and must not be collapsed silently.

Preparation/reset, idle, motion-associated loss, entangling-gate loss, and missed-loss probabilities aligned to the MQM schedule remain OPEN.

## Required successor model

A hardware-facing Sqale benchmark should replace the scalar triple with at least

\[
p_{\rm CZ},
\quad
p_{R_Z},
\quad
p_{\rm GR},
\quad
p_{\rm prep/reset},
\quad
p_{\rm idle},
\]

\[
q_{1\to0},
\quad
q_{0\to1},
\]

and typed loss rates

\[
\ell_{\rm readout},
\quad
\ell_{\rm gate},
\quad
\ell_{\rm motion/idle},
\]

plus missed-loss detection if present.

Only after each MQM circuit location maps to one of those source-bound channels can the \(1+0,2+0,2+1,3+1\) schedules receive a hardware-facing comparison.

## Current 2026 platform context

Infleqtion's September 2026 public Sqale announcement reports 30 logical qubits encoded in 80 atoms and continues to cite a median two-qubit fidelity of 99.48% after post-selection for atom loss from the earlier hardware generation. It does not provide a new complete calibration table for the 30-logical-qubit run.

Therefore the 2025 characterized values are the best source-complete public quantities found for this calibration attempt, not a claim that they describe every August 2026 run.

## Ruling

- Measured Sqale hardware quantities: **EMPIRICAL-HARDWARE**
- Mapping of those typed quantities to their like-for-like MQM locations: **CANDIDATE / PARTIAL**
- Single scalar \(p,q,p_{\rm loss}\) hardware calibration: **NO-GO with current public data/model**
- Hardware ranking of MQM schedules: **BLOCKED**
- Threshold claim: **BLOCKED**
- MQM hardware validation: **OPEN**
- Physical promotion: **0**

### Public sources

1. Bedalov et al., *Fault-tolerant operation and materials science with neutral atom logical qubits*, npj Quantum Information 11, 193 (2025), DOI 10.1038/s41534-025-01095-w.
2. *PRX Quantum* 6, 030334 (2025), DOI 10.1103/66s8-jj18, hardware characterization of individually addressed neutral-atom gates and nondestructive readout.
3. Infleqtion, *Demonstration of 30 Logical Qubits on Sqale*, 24 September 2026.
