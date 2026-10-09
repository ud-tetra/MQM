# MQM Geometric Coherence Enumeration Audit v0.1

**Date:** 2026-10-09  
**Status:** EXACT code-frame enumeration + scoped metric no-go + candidate architecture interpretation  
**Physical promotion:** 0  
**Replay:** commit 4da6e64112282ccef48cf41bc9154016bb413b8d  
**Machine result:** commit 33fe9b4e5a559316d41de70b8e6f7c815565dc32  
**GitHub-hosted run:** 37942210035

## 1. Exact subsystem-8 permutation automorphism theorem

Exhaustive enumeration of all

[
8!=40320
]

physical-qubit permutations found exactly

[
oxed{12}
]

permutations that preserve the full phase-quotiented subsystem-8 gauge group.

Their element-order spectrum is

[
1^1,qquad 2^7,qquad 3^2,qquad 6^2.
]

A convenient generating pair is

[
r=(1,2,3)(4,5)(6,7),
]

[
s=(2,3),
]

with

[
r^6=s^2=1,qquad srs=r^{-1}.
]

Therefore

[
oxed{
operatorname{Aut}_{m perm}(mathcal G)
cong S_3	imes C_2
cong D_6
}
]

where (D_6) means the order-12 symmetry group of a hexagon.

Every one of the 12 automorphisms fixes both protected logical (X_L) and (Z_L) modulo the gauge group.

Thus

[
oxed{
phi:operatorname{Aut}_{m perm}(mathcal G)
	ooperatorname{Aut}(mathcal P_L)
}
]

is trivial for this permutation subgroup.

This is an exact code-algebra result. It does not establish a physical hexagonal qubit layout.

## 2. Six-frame orbit

The group decomposition gives a natural six-state frame orbit

[
{1,2,3}	imes C_2.
]

Under (r), a representative orbit is

[
(1,+)
	o(2,-)
	o(3,+)
	o(1,-)
	o(2,+)
	o(3,-)
	o(1,+).
]

This is the first exact internal MQM result that produces a sixfold frame cycle without inserting (C_6) by hand.

It is a frame/orientation orbit, not yet six Euclidean tetrahedral cells.

## 3. Fundamental-cycle coherence

A central-frame plus orbit-shell wheel was built at the frame-adjacency level.

### C3 shell

The (C_3) wheel has

[
V=4,qquad E=6,qquad
eta_1=E-V+1=3.
]

All three fundamental cycle holonomies close exactly to identity.

### C6 shell

The (C_6) wheel has

[
V=7,qquad E=12,qquad
eta_1=6.
]

All six fundamental cycle holonomies close exactly to identity.

The same wheel admits the reflection (s), so the frame graph supports the full (D_6) action.

These results establish code-frame coherence for the constructed orbit shells. They do not establish a simplicial or Euclidean six-cell realization.

## 4. Symmetry-family admission at the code-frame layer

The exact automorphism group provides an immediate subgroup filter.

| candidate global symmetry | code-frame lift |
|---|---|
| (C_3) | **PASS** |
| (C_4) | **NO-GO** — no element of order 4 |
| (C_6) | **PASS** |
| (D_6), order 12 | **PASS** — full automorphism group |
| tetrahedral rotations (A_4) | **NO-GO** — wrong order spectrum |
| octahedral rotations (S_4) | **NO-GO** — order 24 exceeds 12 |
| icosahedral rotations (A_5) | **NO-GO** — order 60 exceeds 12 |

The tetrahedral (A_4) entry is **not** a no-go for the tetrahedral/K4 primitive. It says only that the complete (A_4) shell action does not lift as a physical-qubit permutation automorphism of this subsystem-8 gauge algebra.

Likewise, octahedral and icosahedral shells are not excluded from MQM by geometry alone; they fail this particular permutation-lift admission gate and would require a richer transition representation.

## 5. Defect-spectrum repair and result

There are two typed defect objects.

### Pure geometric/permutation holonomy

A physical-qubit permutation holonomy is a code automorphism, not a Pauli offset. Therefore assigning it directly an (X/Y/Z) Pauli defect is a type error.

For the exact 12-element geometric automorphism group:

[
oxed{
N(I_L {m automorphism})=12,qquad
N({m nontrivial logical automorphism})=0.
}
]

Nonidentity geometric holonomy can still violate strict frame closure even when the protected logical action is trivial.

### Pauli-frame holonomy

The phase-quotiented Pauli centralizer of the four center generators has size

[
oxed{4096=2^{12}}.
]

The gauge group has size

[
oxed{1024=2^{10}}.
]

Hence

[
N(mathcal Z(mathcal S))/mathcal G
]

contains exactly four protected Pauli cosets:

[
I_L, X_L, Y_L, Z_L.
]

The exact group-theoretic spectrum is

[
oxed{
1024, 1024, 1024, 1024.
}
]

If one forms the affine product with all 12 geometric automorphisms, the total frame space has

[
12	imes4096=49152
]

elements and each protected Pauli defect class has

[
oxed{12288}
]

representatives.

These are uniform group counts, **not physical probabilities**.

## 6. Regular-tetrahedral metric clock no-go

For a regular tetrahedron, the internal dihedral angle is

[
	heta=arccos!left(rac13ight).
]

Because (cos	heta=1/3) is rational but is not one of the rational cosine values permitted for a rational multiple of (pi), (	heta/pi) is irrational.

Therefore the modular angle clock

[
m	hetapmod{2pi}
]

never returns exactly to zero for finite integer (m>0).

So:

[
oxed{
	ext{no finite ring of congruent regular tetrahedra closes exactly around one common edge.}
}
]

Small-(m) residues are:

- (m=3): (148.414^circ) gap;
- (m=4): (77.885^circ) gap;
- (m=5): (7.356^circ) gap;
- (m=6): (63.173^circ) overlap.

Thus the image's sixfold organization must **not** be interpreted as six congruent regular tetrahedra packed around one common edge.

The sixfold code-frame symmetry and Euclidean tetrahedral metric closure are distinct typed objects.

## 7. Architecture ruling

The visual hypothesis produced a real mathematical discriminator:

[
oxed{
	ext{the subsystem-8 gauge algebra itself has an exact }D_6	ext{ permutation symmetry.}
}
]

This makes (C_6/D_6) a mathematically motivated frame-shell frontier rather than an arbitrary aesthetic choice.

However:

- Euclidean six-cell tetrahedral realization remains OPEN;
- metric gluing remains OPEN;
- circuit advantage remains OPEN;
- hardware preference remains OPEN;
- physical promotion remains 0.

## AUTO_LOCK

Scoped exact results:

1. (operatorname{Aut}_{m perm}(mathcal G)cong S_3	imes C_2cong D_6), order 12.
2. Every such permutation acts trivially on the protected logical Pauli quotient.
3. The six-state frame orbit exists exactly.
4. The constructed (C_3) and (C_6) wheel cycle bases close exactly.
5. (C_3,C_6,D_6) pass the permutation-lift gate; (C_4,A_4,S_4,A_5) do not.
6. Pauli-frame defect cosets are exactly (1024) each for (I,X,Y,Z).
7. No finite regular-tetrahedron common-edge ring closes exactly.

## OPEN

1. literal simplicial (D_6) tetrahedral shell;
2. Euclidean coordinates and shared-face/edge metric compatibility;
3. physical qubit placement;
4. whether the (D_6) symmetry reduces circuit resources or logical error;
5. independent reproduction.
