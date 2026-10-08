# MQM Sqale Native Round Compile Audit v0.1a

**Date:** 2026-10-08  
**Status:** EXACT NATIVE-GATE ALGEBRA / ROUTING + TIMING OPEN  
**Physical promotion:** 0  
**Compiler source:** commit de8308b8abc1d859c80de403f4b8bfe8f1062115  
**Generated schedule:** commit 073d05ce54871bc8a5759897187a0cc25c02a219  
**Hash receipt:** commit c560e3810e5435d30d6842e721b72f13190ecadd  
**Successful GitHub-hosted run:** 37837226921

## Scope

This artifact compiles one frozen MQM firewall extraction round to the public Sqale native gate algebra

\[
GR_{\theta,\phi},\qquad R_Z^{(i)}(\alpha),\qquad CZ_{ij},
\]

plus typed reset and nondestructive-readout macros.

It is not yet a backend-executable pulse schedule because atom motion/routing, gate concurrency, reset timing, NDSSR timing, and external-spectator handling remain source-bound OPEN quantities.

## Active-register assumption

The exact algebraic compile uses ten live qubits: data \(1,\dots,8\), syndrome ancilla \(9\), and flag ancilla \(10\).

Either no other live qubit is exposed to the global rotation during this isolated job, or the production compiler must independently decouple every external spectator.

## Exact selective-rotation identity

Let \(T\) be the desired target subset and \(S\) its spectator complement.

The chronological sequence

\[
GR_y(\theta/2);
\quad R_Z^S(\pi);
\quad GR_y(\theta/2);
\quad R_Z^S(-\pi)
\]

implements

\[
R_y^T(\theta)\otimes I_S.
\]

For a spectator,

\[
R_Z(-\pi)R_y(\theta/2)R_Z(\pi)R_y(\theta/2)=I,
\]

while a target receives

\[
R_y(\theta/2)R_y(\theta/2)=R_y(\theta).
\]

The physical basis transforms are folded into this selective rotation:

\[
R_y(\pi/2)R_Z(\pi)=-iH,
\]

\[
R_y(\pi/2)R_Z(\pi/2)=-iHS^\dagger,
\]

\[
R_Z(\pi)R_y(-\pi/2)=-iH,
\]

\[
R_Z(-\pi/2)R_y(-\pi/2)=SH.
\]

Thus the phase-quotiented S/H abstractions used in the algebraic simulator are converted to signed physical \(R_Z\) angles.

## Parity-chain identity

Every frozen data/flag-to-syndrome CNOT chain is compiled by

\[
\prod_j \operatorname{CNOT}_{j\to s}
=
H_s
\left(\prod_j CZ_{j,s}\right)
H_s.
\]

Because every interaction in a given check shares syndrome target \(s\), adjacent syndrome Hadamards cancel and the frozen temporal interaction order can be preserved as a CZ sequence.

## Exact round counts

The generated one-round schedule has

\[
\boxed{39\ CZ\ requests},
\]

\[
\boxed{40\ GR\ pulses},
\]

\[
\boxed{346\ local\ R_Z\ site\ requests},
\]

\[
\boxed{14\ reset\ site\ requests},
\]

and

\[
\boxed{14\ NDSSR\ site\ measurements}.
\]

The JSON generator emits **66 \(R_Z\) instruction groups**. This is a compiler grouping count, not a physical parallel-depth claim.

| check | CZ | GR | local-\(R_Z\) site requests |
|---|---:|---:|---:|
| B1 | 6 | 4 | 32 |
| B2 | 6 | 4 | 32 |
| B3 | 6 | 4 | 32 |
| B4 | 9 | 4 | 22 |
| E12 | 2 | 4 | 38 |
| E13 | 2 | 4 | 38 |
| E18 | 2 | 4 | 38 |
| E23 | 2 | 4 | 38 |
| E28 | 2 | 4 | 38 |
| E38 | 2 | 4 | 38 |
| **total** | **39** | **40** | **346** |

The lower B4 \(R_Z\) count occurs because nine of the ten live qubits participate in its selective-H layer, leaving only one spectator to echo.

## Frozen CZ temporal order

The two flag interactions remain after data interactions 1 and 3 exactly as in the firewall circuit.

For B4 the CZ order is

\[
(4,s),(f,s),(5,s),(6,s),(f,s),(1,s),(2,s),(3,s),(8,s).
\]

The ideal CZs commute, but they are not reordered because the circuit-level fault certificate depends on temporal fault propagation.

## Routing boundary

The generated schedule records 39 required CZ pair interactions but does not invent atom coordinates, move paths, move concurrency, move durations, transport loss/dephasing, or spectator locations.

These must come from the provider/compiler handoff.

## Replay provenance

The first v0.1 replay failed before promotion because its bookkeeping assertion expected 60 \(R_Z\) “time slices”; the generated program actually contained 66 instruction groups.

The gate sequence and exact site-request count were unchanged. v0.1a removed the unsupported timing interpretation and replayed successfully.

Successful source SHA-256:

6ac3049456718eff9a821c9e3f4e484ff52d82fe439ed5cbf38384a2579002ca

Generated schedule SHA-256:

88cea4ea0dafce67cb9ba1701b3cf78229a06683ef56aa496c8a2fc2156eb651

Workflow artifact SHA-256:

96f701f0460ff131bc889478daf575c997e57ef1d6587105a51512b20fafa081

## Ruling

- native gate algebra: **EXACT**
- one-round native request ledger: **EXACT**
- local-H selective-rotation construction: **EXACT**
- physical routing/motion schedule: **OPEN**
- physical gate durations/parallel depth: **OPEN**
- typed hardware-noise score: **OPEN pending provider handoff**
- hardware validation / threshold / advantage: **OPEN**
- physical promotion: **0**
