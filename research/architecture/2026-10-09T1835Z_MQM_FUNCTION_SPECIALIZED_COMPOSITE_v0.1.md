# MQM Function-Specialized Composite Architecture v0.1

**Date:** 2026-10-09  
**Status:** EXACT typed construction + CANDIDATE physical interpretation  
**Physical promotion:** 0

## Layer assignment

This construction deliberately assigns different geometric jobs to different typed layers:

1. **D5 metric layer** — five-cell near-regular local packing fiber.
2. **A4 module layer** — four subsystem-8 modules in a K4 coordination carrier.
3. **D6 frame layer** — six-state cyclic internal frame/address clock inside each module.
4. **S4 receipt layer** — verification topology acting on the six A4 interface receipts.

No layer is reinterpreted as another.

## D5 local fiber

Each A4 module receives one exact D5 five-tetrahedron local metric fiber.

With four A4 modules:

\[
4\times5=20
\]

typed local D5 cells.

This is a metric/layout proposal. The D5 cells are not automatically individual qubits.

## A4 coordination base

The module carrier is

\[
K_4
\]

with:

\[
V=4,\qquad E=6,\qquad \beta_1=3,
\]

and diameter 1.

Thus every module is one hop from every other module.

Each module carries one subsystem-8 code block.

Total data-qubit count before ancillas:

\[
4\times8=32.
\]

## D6 internal frame clock

Inside each module use the exact protected-logical-identity order-6 frame generator

\[
r=(1\,2\,3)(4\,5)(6\,7).
\]

The six internal frame phases form

\[
F_t=r^tF_0,\qquad t\in\mathbb Z_6.
\]

After six updates,

\[
r^6=I.
\]

Across four A4 modules there are

\[
4\times6=24
\]

typed module/frame states.

Combining the five D5 local sectors, four A4 modules and six D6 frame phases yields

\[
5\times4\times6=120
=
2^3\cdot3\cdot5
\]

typed geometric/frame addresses.

This factorization is bookkeeping only; no physical numerology is inferred from 120.

## S4 receipt overlay appears naturally

A4 has six module interfaces: the six edges of \(K_4\).

Construct the line graph

\[
L(K_4).
\]

Its vertices are the six K4 edges. Two receipt channels are adjacent when the corresponding K4 interfaces share a module.

Exactly:

\[
|V(L(K_4))|=6,
\qquad
|E(L(K_4))|=12,
\]

and every vertex has degree 4.

Therefore

\[
\boxed{L(K_4)\cong \text{octahedron graph}.}
\]

Its automorphism symmetry is the same \(S_4\) permutation action inherited from K4.

So the S4 verification layer does not need to be introduced arbitrarily: it arises as the natural adjacency geometry of the six A4 interface receipts.

## Native six-receipt code

Take one binary receipt on each of the six K4 module interfaces and require the receipt vector to lie in the K4 cut space.

This binary linear code has

\[
\boxed{[6,3,3]}.
\]

Thus every one- or two-bit receipt error is detected.

The seven nonzero valid cut words have weights:

\[
3^4,\qquad4^3.
\]

This is an information/receipt result, not a quantum code distance.

## Optional augmented S4 receipt layer

If an additional comparison bit is placed on every edge of the octahedron receipt graph, there are 12 bits.

The octahedron cut space has

\[
\boxed{[12,5,4]}.
\]

Therefore every one-, two-, or three-bit comparison error is detected.

Its nonzero cut-weight spectrum is

\[
4^6,\qquad6^{16},\qquad8^9.
\]

This is the exact stronger S4 verification layer previously suggested by the structural benchmark.

It costs 12 comparison receipts and is optional; it is not automatically justified.

## One composite epoch

A single proposed functional epoch is:

1. **local geometry:** retain the D5 fiber as the module's low-distortion physical layout proposal;
2. **module memory:** run frozen 2+PV independently on the four A4 subsystem-8 modules;
3. **coordination:** exchange/update the six A4 interface receipts;
4. **frame address:** advance the virtual D6 frame clock \(t\mapsto t+1\bmod6\);
5. **verification:** apply the native [6,3,3] K4 receipt checks; invoke the optional [12,5,4] S4 overlay only when its extra receipt cost passes a frozen benefit criterion.

After six epochs the D6 frame clock closes exactly.

## Admissibility

### Metric layer
D5 local fiber: **EXACT existence**, physical mapping OPEN.

### Module layer
A4 K4 carrier: **EXACT**.

### Frame layer
D6 six-state logical-identity clock: **EXACT**.

### Receipt layer
\[
L(K_4)\cong O_6
\]
and the [6,3,3] / [12,5,4] receipt codes: **EXACT**.

### Cross-layer logical coherence
A4 module transitions and the D6/S3 information-frame actions are compatible by the exact
\[
C_2\times S_4\times S_4
\]
factorization established previously.

### Hardware function
Whether this layered specialization lowers logical error, latency, motion, or loss: **OPEN**.

## Main result

The four-shape hierarchy is not merely a collection of unrelated motifs.

The A4 module geometry itself produces six interfaces whose line graph is the S4/octahedral receipt topology, while D6 supplies an independent internal frame clock and D5 supplies the local metric fiber.

Therefore the specialized stack has an exact compositional relation:

\[
\boxed{
D5_{\rm metric}
\;\to\;
A4_{\rm modules}
\;\to\;
D6_{\rm frame\ clock}
\;\oplus\;
S4_{\rm interface\ receipts}.
}
\]

This is an architecture grammar, not a hardware-performance claim.
