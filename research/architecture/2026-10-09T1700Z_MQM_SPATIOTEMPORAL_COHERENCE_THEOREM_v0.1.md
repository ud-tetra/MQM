# MQM Spatiotemporal Coherence Theorem v0.1

**Date:** 2026-10-09  
**Status:** EXACT topology/group framework + CANDIDATE functional interpretation  
**Physical promotion:** 0

## Shape in motion

Let \(K\) be a connected spatial carrier graph with first Betti number

\[
b=\beta_1(K)=E-V+1.
\]

Let one periodic schedule be represented by a temporal circle \(S^1_T\). The periodic moving architecture has product carrier

\[
X=K\times S^1_T.
\]

By the Kunneth theorem,

\[
H_1(X;\mathbb Z)
\cong
H_1(K;\mathbb Z)\oplus H_1(S^1;\mathbb Z)
\cong
\mathbb Z^{b+1},
\]

and

\[
H_2(X;\mathbb Z)
\cong
H_1(K;\mathbb Z)\otimes H_1(S^1;\mathbb Z)
\cong
\mathbb Z^b.
\]

Therefore adding a periodic motion does two exact things:

1. adds one independent temporal 1-cycle;
2. creates \(b\) independent mixed spatial-temporal 2-cycles.

This is the first precise sense in which "shape in motion" contains strictly more structure than the static shape.

## Current carriers

For the current MQM carriers:

| carrier | \(\beta_1(K)\) | \(\operatorname{rank}H_1(K\times S^1)\) | \(\operatorname{rank}H_2(K\times S^1)\) |
|---|---:|---:|---:|
| D5 ring \(C_5\) | 1 | 2 | 1 |
| D6 ring \(C_6\) | 1 | 2 | 1 |
| A4 shell \(K_4\) | 3 | 4 | 3 |
| S4 shell / octahedron | 7 | 8 | 7 |

Thus S4 carries the richest mixed spacetime cycle structure, A4 is intermediate, and the D5/D6 rings are minimal.

This is topology, not a statement that more cycles are better.

## Group-valued schedule

Let the exact transition group be

\[
G=C_2\times S_4\times S_4
\]

with protected-logical quotient

\[
\pi:G\to S_3
\]

and kernel \(K_{192}\).

Assign an admissible transition \(T_e\in G\) to every oriented edge of the spacetime cell complex.

For any closed loop \(\gamma\),

\[
H(\gamma)=\prod_{e\in\gamma}T_e
\]

is the frame holonomy.

### Strict coherence

A loop declared strictly trivial must satisfy

\[
H(\gamma)=I.
\]

### Protected-logical coherence

A loop may carry internal gauge/frame holonomy without logical effect when

\[
H(\gamma)\in K_{192},
\]

equivalently

\[
\pi(H(\gamma))=I.
\]

### Intended operation

A designated temporal cycle may intentionally implement logical frame action \(L\in S_3\):

\[
\pi(H(\gamma_T))=L.
\]

This makes motion semantics operational rather than metaphorical.

## Mixed plaquette test

Every independent spatial cycle \(c_i\) generates a mixed spacetime torus

\[
c_i\times S^1_T.
\]

Its boundary can be decomposed into elementary spacetime plaquettes. If every elementary mixed plaquette has holonomy in \(K_{192}\), then no contractible mixed loop creates a protected-logical defect.

For strict frame coherence require identity holonomy on every elementary mixed plaquette.

This supplies an exact schedule-level admission test for moving geometries.

## Functional interpretation

The current candidate functional map is:

- D5: low-distortion local metric fiber;
- A4: compact coordination carrier;
- D6: cyclic frame/address carrier;
- S4: redundant verification carrier.

The spatiotemporal theorem refines those proposals:

- low-\(b\) rings expose fewer independent mixed coherence constraints;
- high-\(b\) carriers expose more independent mixed cycles that may be used as consistency receipts, but also create more places for temporal inconsistency;
- motion monodromy determines whether a periodic pattern is gauge-only, a logical transposition, or a logical 3-cycle.

None of those candidate functions is promoted until matched workloads verify an advantage.

## Exact motion clock

For any one-step monodromy \(g\in G\),

\[
T_F=\operatorname{ord}(g)\in\{1,2,3,4,6,12\}
\]

and

\[
T_L=\operatorname{ord}(\pi(g))\in\{1,2,3\}.
\]

Thus

\[
T_L\mid T_F.
\]

The ratio

\[
h=T_F/T_L
\]

is a typed hidden-frame multiplicity: the internal frame can have a longer clock than the protected logical motion.

The exhaustive spectrum is:

\[
h=1:193,\quad
h=2:559,\quad
h=3:104,\quad
h=4:144,\quad
h=6:152.
\]

## Promotion ledger

- product-space homology ranks: **EXACT**
- group-valued holonomy rules: **EXACT**
- mixed plaquette protected-logical admission condition: **DERIVED**
- shape-specific functional labels: **CANDIDATE**
- physical dynamical meaning: **OPEN**
- physical promotion: **0**
