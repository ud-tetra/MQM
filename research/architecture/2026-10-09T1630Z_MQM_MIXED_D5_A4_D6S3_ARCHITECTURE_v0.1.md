# MQM mixed D5/A4/D6-S3 architecture v0.1

**Status:** CANDIDATE layered architecture with exact cross-layer admissibility checks
**Physical promotion:** 0

## Proposal

Do not require one symmetry to dominate every typed layer.

Use:

1. **D5 local metric fiber** — the exact five-tetrahedron bipyramid ring, chosen because its minimax edge spread is only about 1.346% from equality within the Dm family;
2. **A4 module carrier** — four congruent tetrahedral modules in the exact centroid subdivision of a regular outer tetrahedron;
3. **D6 / S3 information frame** — the exact subsystem code-frame symmetries living in the monomial local-Clifford transition group.

These are distinct carriers.

## Exact Euclidean nesting

Every A4 module is a nondegenerate tetrahedron and therefore contains an open ball. The bounded D5 bipyramid cluster can be uniformly scaled and rigidly placed inside that ball. Because all four A4 modules are congruent, choose one embedded D5 reference fiber and carry it to the other modules by the A4 spatial rotations.

Therefore an A4-equivariant nested geometry with one D5 five-cell fiber per module exists exactly.

Counts:

- outer A4 carrier: 4 tetrahedral module cells;
- internal D5 fibers: 4 x 5 = 20 tetrahedral local cells.

If both scales are counted there are 24 tetrahedral motifs, but **these are not 24 cells of one face-to-face simplicial tessellation**. The 4 outer carrier cells and 20 embedded fiber cells are typed objects at different scales.

## Code-transition compatibility

The exact transition group is

G = C2 x S4_A x S4_B.

The A4 module-transition subgroup is the normal alternating subgroup

A4_A normal in S4_A.

Hence

A4_A normal in G.

Therefore every global D6 frame element contained in G normalizes the A4 module-transition family. Applying a global D6 frame transformation cannot move an admissible A4 transition outside the A4 transition subgroup.

The protected-logical action is carried by

S4_B / V4 ~= S3.

Because the two S4 factors commute exactly,

[A4_A, S4_B] = 1.

Thus the A4 module transitions commute with the full information-frame S4_B action and therefore with its logical S3 quotient.

This gives an exact algebraic compatibility result:

**A4 module coherence and global logical S3 frame control can coexist without generating cross-layer protected-logical holonomy.**

## D6 versus S3 typing

D6 and S3 are not the same object.

- D6 is an exact gauge-preserving frame/permutation symmetry available in the full transition group.
- S3 is the six-element protected-logical Clifford quotient S4_B/V4.

The mixed architecture may use D6 for gauge/frame addressing and S3 for logical-axis bookkeeping without identifying the two.

## Geometric-coherence admission

### Local metric layer

D5 fiber: **PASS**. Exact five-cell closure; near-regular metric within the declared Dm distortion measure.

### Module geometry layer

A4 carrier: **PASS**. Exact four-cell Euclidean tetrahedral carrier with K4 dual graph.

### Module transition layer

A4 kernel transitions: **PASS**. Protected-logically trivial and strict cycle closure already established.

### Global frame layer

D6 normalization of A4 transitions: **PASS** by normality of A4_A in G.

Logical S3 commutation with A4 transitions: **PASS** by direct-product factorization.

### Circuit/hardware layer

**OPEN.** The construction does not yet establish that local D5 geometry improves qubit noise, that the nested fibers should be physical qubit positions, or that D6/S3 frame operations reduce hardware cost.

## Interpretation

The earlier apparent tension is resolved:

- near-regular tetrahedral geometry can prefer fivefold local organization;
- the module carrier can prefer the fourfold tetrahedral A4 shell;
- the quantum information frame can retain exact sixfold D6 and logical S3 structure.

No symmetry needs to be promoted beyond the typed layer where it is actually supported.

## Ruling

- nested D5-in-A4 Euclidean construction: **EXACT existence**;
- A4 x logical-S3 compatibility: **EXACT**;
- D6 normalization of A4 module transitions: **EXACT**;
- claim that the mixed hierarchy improves physical performance: **OPEN**;
- claim that the D5 fibers are actual qubit geometry rather than architecture motifs: **OPEN**;
- physical promotion: **0**.
