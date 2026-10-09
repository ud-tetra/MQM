# MQM D5/D6 Geometric Realization + Local-Clifford Coherence Audit v0.1

**Date:** 2026-10-09
**Physical promotion:** 0

## 1. Literal Dm tetrahedral shell

For any integer m>2 define

N=(0,0,h),
S=(0,0,-h),
v_i=(R cos(2 pi i/m), R sin(2 pi i/m),0),

and tetrahedral cells

T_i={N,S,v_i,v_(i+1)}.

Every cell is congruent. Its six edge lengths are

a=2h,
b=2R sin(pi/m),
c=sqrt(R^2+h^2) repeated four times.

The tetrahedral volume is

V = h R^2 sin(2 pi/m)/3,

so the Cayley-Menger determinant is

288 V^2 > 0

for h,R>0 and m>2.

The dihedral angle about the common central edge NS is exactly

2 pi/m.

Therefore a literal D_m face-sharing tetrahedral ring exists for every m>2 once regularity is relaxed.

### Exact D6 realization

Choose h=1 and R=2.

Then each of the six tetrahedra has edge multiset

{2,2,sqrt(5),sqrt(5),sqrt(5),sqrt(5)},

volume

2 sqrt(3)/3,

and Cayley-Menger determinant 384.

The six dihedral wedges about NS are exactly 60 degrees and close to 360 degrees.

Thus:

**EXACT:** a nonregular, congruent, six-tetrahedron D6 shell exists.

This resolves the earlier regular-tetrahedron edge-ring no-go without contradicting it.

## 2. Fivefold comparator

The same D_m family permits an exact D5 ring.

Normalize h=1 and choose

R=csc(pi/5),

so the central edge and ring edge are both exactly 2.

The four remaining spokes have length

sqrt(1+csc^2(pi/5))
=
sqrt(3+2/sqrt(5))
approximately 1.97343031065.

Within this D_m bipyramid family, minimizing the scale-free max/min edge ratio gives

kappa_5 =
2/sqrt(3+2/sqrt(5))
approximately 1.01346370794,

so the minimum edge spread from equality is approximately

1.346370794 percent.

For D6 the corresponding minimax point is R/h=2, with

kappa_6=sqrt(5)/2
approximately 1.11803398875,

or approximately

11.803398875 percent

edge spread.

Therefore, under this declared geometric distortion metric,

**EXACT:** the closed D5 tetrahedral ring is much closer to regular tetrahedra than the closed D6 ring.

This is a geometric closeness statement, not an energy or physical-persistence law.

## 3. Regular-tetrahedron clock interpretation

For the regular tetrahedron,

theta=acos(1/3)
approximately 70.5287793655 degrees.

Five cells give a total gap

360 degrees - 5 theta
approximately 7.35610317245 degrees.

Six cells give a total overlap

6 theta - 360 degrees
approximately 63.1726761931 degrees.

So the regular tetrahedral metric naturally sits near fivefold closure, while the subsystem code-frame algebra has exact sixfold/D6 symmetry.

These are different typed carriers:

- metric carrier: near-D5;
- code-frame carrier: exact D6.

They need not select the same symmetry family.

## 4. Representation bridge and no-go

The literal hexagonal-bipyramid D6 rotation acts on its eight vertices with cycle type

6+1+1.

The exact subsystem-8 code automorphism generator has cycle type

3+2+2+1.

Therefore the standard spatial vertex action of the D6 bipyramid is not the code's D6 qubit-permutation representation.

One can realize cycle type 3+2+2+1 by the finite orthogonal order-6 map

R_120 degrees direct-sum (-1),

with a planar three-cycle, two axial two-cycles, and one fixed point.

However the period-3 orbit lies in the rotation plane and the unique fixed point lies at the origin of that same plane. Hence the four code-core sites {1,2,3,8} have zero tetrahedral volume.

Thus:

**NO-GO:** the exact code D6 permutation action cannot simultaneously be interpreted as an ordinary nondegenerate spatial symmetry of the four-site K4 core in this direct eight-vertex realization.

The exact D6 result is therefore naturally a frame/module symmetry. A literal D6 tetrahedral module shell can exist, but its cell symmetry must be bridged to the code's internal frame action rather than identified with the eight data-qubit vertex permutation.

## 5. Monomial local-Clifford transition group

The transition search was enlarged from pure physical-qubit permutations to phase-quotiented monomial local Cliffords:

- arbitrary physical-qubit permutation;
- independent single-qubit Clifford Pauli-axis permutation on each qubit;
- exact preservation of the subsystem-8 gauge group.

Support invariants reduce the 8! permutation search to 144 candidate permutations.

Exhausting all local Pauli-axis maps over those candidates gives exactly

1152 = 2^7 * 3^2

gauge-preserving monomial local-Clifford automorphisms.

Element-order spectrum:

- order 1: 1
- order 2: 199
- order 3: 80
- order 4: 312
- order 6: 368
- order 12: 192

There are no order-5 elements.

## 6. Protected-logical transition spectrum

The induced action on the protected logical Pauli pair (X_L,Z_L) realizes all six phase-quotiented one-logical-qubit Clifford actions.

Each logical action occurs exactly 192 times.

Therefore the logical-action homomorphism is surjective:

1 -> K_192 -> Aut_LC^mon(G) -> S3_L -> 1,

with protected-logical coherence kernel

|K_192|=192.

For a geometrically trivial cycle, protected-logical coherence at this enlarged transition layer requires the cycle holonomy to land in K_192. Strict frame closure remains the stronger requirement that the holonomy itself be identity.

This is the local-Clifford version of the coherence-defect spectrum.

## 7. Reopening A4/S4/A5

The pure permutation layer previously rejected tetrahedral A4 and octahedral S4 shell actions.

The monomial local-Clifford automorphism group changes that result.

An exact subgroup search found:

- tetrahedral A4: **PASS**, witness subgroup of order 12;
- octahedral S4: **PASS**, witness subgroup of order 24;
- icosahedral A5: **NO-GO within this transition class**, because the full 1152-element group contains no order-5 element.

Thus A4 and S4 are reopened at the **code-transition layer**.

This does not yet construct a Euclidean tetrahedral or octahedral shell, nor prove cycle holonomies are protected-logically trivial. It removes the former permutation-only obstruction.

A5 remains blocked for monomial local Clifford transitions, but could in principle reopen under a larger nonlocal/entangling Clifford transition group or a different code.

## 8. Evidence ledger

### EXACT / AUTO_LOCK scoped
- D_m congruent tetrahedral bipyramid family and Cayley-Menger positivity.
- Exact nonregular D6 six-tetrahedron shell.
- Exact D5 comparator and D5/D6 minimax edge-spread values within the declared family.
- Direct eight-site spatial realization no-go for the code D6 action with nondegenerate K4 core.
- Monomial local-Clifford automorphism group size 1152 and element-order spectrum.
- Full logical S3 action with kernel size 192.
- A4 and S4 subgroup existence.
- A5 no-go in the monomial local-Clifford automorphism group due absence of order-5 elements.

### OPEN
- physical preference between D5 and D6;
- energy/stability model;
- Euclidean shell carrying the internal code-frame D6 action equivariantly;
- cycle-holonomy acceptance for specific A4/S4 shell complexes;
- entangling-Clifford reopening of A5;
- hardware validation.

Physical promotion remains 0.
