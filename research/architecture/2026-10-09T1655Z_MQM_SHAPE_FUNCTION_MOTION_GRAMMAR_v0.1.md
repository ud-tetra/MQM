# MQM Shape–Function–Motion Grammar v0.1

**Date:** 2026-10-09  
**Status:** EXACT operational grammar + CANDIDATE functional interpretations  
**Physical promotion:** 0

## Core principle

Different geometric carriers need not serve the same role. A shape constrains what interactions and cycle structures are available. A motion pattern is a time-ordered sequence of admissible frame transitions on that carrier. Its additional meaning is the monodromy induced by that sequence.

The typed separation is:

\[
\boxed{
\text{shape} \to \text{structural affordance},
\qquad
\text{motion word} \to \text{frame transformation},
\qquad
\text{monodromy} \to \text{logical function}.
}
\]

No physical function is inferred from symmetry alone.

## Static shape object

For a carrier \(K\), define the structural signature

\[
\Sigma(K)=
(V,E,\beta_1,\deg,\operatorname{diam},\operatorname{Aut}(K),
\kappa_{\rm metric},C_{\rm interface},N_{\rm cell}).
\]

Current exact examples:

| carrier | graph | \(V\) | \(E\) | \(\beta_1\) | degree | diameter | literal tetrahedral cells |
|---|---|---:|---:|---:|---:|---:|---:|
| D5 local ring | \(C_5\) | 5 | 5 | 1 | 2 | 2 | 5 |
| D6 module ring | \(C_6\) | 6 | 6 | 1 | 2 | 3 | 6 |
| A4 module shell | \(K_4\) | 4 | 6 | 3 | 3 | 1 | 4 |
| S4 module shell | octahedron | 6 | 12 | 7 | 4 | 2 | 24 in the exact literal repair |

Metric distortion within the declared tetrahedral families:

\[
\kappa_{D5}\approx1.01346,
\qquad
\kappa_{D6}=\frac{\sqrt5}{2}\approx1.11803,
\]

while the A4 centroid-subdivision cells have

\[
\kappa_{A4}=\sqrt{\frac83}\approx1.63299.
\]

These are structural facts, not performance laws.

## Candidate functional affordances

The following are hypotheses to test, not promoted functions.

### D5 — local metric packing / low-distortion fiber

Proposal source:
- exact fivefold closure;
- smallest near-regular edge spread among the D5/D6 common-edge comparators tested.

Candidate function:
- local physical packing;
- local interaction-length equalization;
- low-strain geometric fiber.

Acceptance requires a source-bound physical model showing reduced coupling variance, motion cost, loss, or logical error.

### A4 — compact coordination / module-control carrier

Proposal source:
- four modules;
- \(K_4\) all-to-all adjacency;
- diameter 1;
- exact literal four-tetrahedron carrier;
- selected interfaces require only local-Clifford frame changes in the current compile.

Candidate function:
- compact coherence/coordination hub;
- low-hop syndrome or state-control exchange;
- module-scale code organization.

Acceptance requires matched circuit/hardware comparison.

### D6 — cyclic transport / frame-address carrier

Proposal source:
- \(C_6\) ring with \(\beta_1=1\);
- exact order-6 code-frame symmetry;
- frame transition can be passive relabeling;
- literal six-tetrahedron nonregular carrier exists.

Candidate function:
- cyclic addressing;
- frame transport;
- periodic scheduling;
- low-cycle-rank circulation.

Acceptance requires a compiled routing/timing benefit relative to A4.

### S4 — redundant verification / cross-check carrier

Proposal source:
- octahedron module graph;
- degree 4;
- \(\beta_1=7\);
- many independent cycles;
- exact protected-logical-coherent frame shell.

Candidate function:
- redundant consistency checks;
- cross-validation / receipt diversity;
- fault-localization structure.

Acceptance requires showing that cycle redundancy lowers undetected logical error enough to justify the 24-cell literal carrier and higher interface count.

## Motion object

Let the exact admissible transition group be

\[
G=C_2\times S_4\times S_4,
\]

with protected-logical quotient

\[
\pi:G\to S_3
\]

and kernel

\[
K_{192}\cong C_2^3\times S_4.
\]

For a time-ordered motion word

\[
w=(g_1,g_2,\ldots,g_T),
\]

define its monodromy

\[
M(w)=g_T\cdots g_2g_1.
\]

The protected logical meaning of the complete pattern is

\[
L(w)=\pi(M(w))\in S_3.
\]

Thus two motion histories can traverse different gauge/frame states yet have the same protected-logical meaning.

## Exact motion semantics theorem

For any one-step monodromy \(g\in G\):

\[
T_F=\operatorname{ord}(g)\in\{1,2,3,4,6,12\},
\]

while

\[
T_L=\operatorname{ord}(\pi(g))\in\{1,2,3\}.
\]

Since quotient order divides element order,

\[
\boxed{T_L\mid T_F}.
\]

Define the hidden frame multiplicity

\[
h=\frac{T_F}{T_L}.
\]

This measures how many internal gauge/frame clock steps occur per protected-logical cycle.

Exact exhaustive counts over all 1152 transitions:

### Protected-logical motion type

\[
\boxed{
192\ \text{logical identity},
\quad
576\ \text{axis transpositions},
\quad
384\ \text{axis 3-cycles}.
}
\]

The first 192 are gauge/frame motions with no protected-logical transformation.

### Joint full-frame / logical period

\[
\begin{array}{c|r}
(T_F,T_L) & \#\\
\hline
(1,1)&1\\
(2,1)&79\\
(2,2)&120\\
(3,1)&8\\
(3,3)&72\\
(4,1)&48\\
(4,2)&264\\
(6,1)&56\\
(6,2)&96\\
(6,3)&216\\
(12,2)&96\\
(12,3)&96
\end{array}
\]

### Hidden-frame multiplicity spectrum

\[
\boxed{
h=1:193,\quad
h=2:559,\quad
h=3:104,\quad
h=4:144,\quad
h=6:152.
}
\]

These are exact group counts, not physical probabilities.

## Operational interpretation of motion

### Gauge/frame circulation

If

\[
\pi(M)=I,
\]

the pattern changes only internal frame/gauge state.

Candidate uses:
- syndrome scheduling;
- frame cycling;
- dynamical averaging;
- route/address changes without a protected logical operation.

Only the algebraic classification is established. Noise suppression is OPEN.

### Logical transposition

If

\[
\operatorname{ord}(\pi(M))=2,
\]

the pattern exchanges two protected Pauli axes. This is a phase-quotiented logical Clifford frame transformation.

### Logical 3-cycle

If

\[
\operatorname{ord}(\pi(M))=3,
\]

the pattern cycles the three protected Pauli axes.

Thus the same static shape can support distinct operational meanings depending on the time word placed on it.

## Spatiotemporal coherence

Let \(K\) be the spatial carrier graph and \(C_T\) a temporal clock cycle. The moving architecture is represented on the product

\[
X=K\times C_T.
\]

Assign transition maps to the directed spatial and temporal edges.

For a closed spacetime loop \(\gamma\), define

\[
H(\gamma)=\prod_{e\in\gamma}T_e.
\]

### Memory/coherence condition

For every spacetime cycle declared logically trivial,

\[
\boxed{\pi(H(\gamma))=I.}
\]

For strict frame closure require the stronger

\[
H(\gamma)=I.
\]

### Intended logical operation

For a designated temporal cycle intended to implement logical frame operation \(L\),

\[
\boxed{\pi(H(\gamma_T))=L.}
\]

This turns "shape in motion" into an exact schedule-admission test.

## Shape-function falsification rule

A functional label is promoted only when the shape wins a predeclared matched workload on the metric associated with that proposed function.

Examples:

- "D5 is a packing geometry" requires lower source-bound physical interaction variance or motion burden.
- "A4 is a coordination geometry" requires lower matched communication/extraction cost.
- "D6 is a transport geometry" requires lower matched routing/frame-change cost.
- "S4 is a verification geometry" requires lower undetected-error probability after charging all added cells/cycles.

Until then these remain CANDIDATE functional interpretations.

## Current strongest conclusion

The user intuition is mathematically viable when restated as:

> geometry supplies distinct structural affordances, while time-ordered admissible transitions supply additional group-valued semantics.

The static carrier and the motion pattern are separate typed objects and should be optimized separately before being composed.
