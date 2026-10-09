# MQM Equivariant Shell + Transition Group Structure Audit v0.1

**Date:** 2026-10-09  
**Status:** EXACT algebraic/frame results + scoped geometric carrier results  
**Physical promotion:** 0

## 1. Six-module D6 carrier

The literal geometric carrier is the exact nonregular hexagonal-bipyramid tetrahedral ring from the prior Dm construction:

[
T_i={N,S,v_i,v_{i+1}},qquad iinmathbb Z_6.
]

Assign the six module frames

[
F_i=r^iF_0
]

using the exact protected-logical-trivial order-6 code automorphism

[
r=(1,2,3)(4,5)(6,7).
]

For each oriented face interface (T_i	o T_{i+1}), use transition

[
T_{i,i+1}=r,
]

and reverse transition (r^{-1}).

The cell-adjacency graph is (C_6):

[
V=6,qquad E=6,qquad eta_1=1.
]

The only independent shell holonomy is

[
H(C_6)=r^6=I.
]

Thus the literal six-tetrahedral module ring is strictly frame-coherent, and every interface transition is protected-logically trivial.

Replay metrics:

- modules: 6;
- interfaces: 6;
- cycle rank: 1;
- nontrivial protected-logical interfaces: 0;
- total moved-qubit count over the six interfaces: 42;
- local-axis changes: 0;
- maximum declared interface complexity: 7.

This is an exact module/frame bridge. It does not identify the eight subsystem data sites with the eight Euclidean bipyramid vertices.

## 2. A4 shell

Use the protected-logical-kernel (S_4) factor of the monomial local-Clifford transition group and its exact (A_4) subgroup.

Carrier graph:

- four module ports on the faces of a tetrahedral shell;
- adjacency graph (K_4).

Therefore

[
V=4,qquad E=6,qquadeta_1=3.
]

Frame representatives are chosen from the four cosets of a (C_3) stabilizer. Interface transitions are the exact relative local-Clifford maps between representatives.

All three independent cycles close strictly:

[
H(C)=I
]

and all six interfaces lie in the protected-logical coherence kernel.

Replay metrics:

- modules: 4;
- interfaces: 6;
- cycle rank: 3;
- nontrivial protected-logical interfaces: 0;
- total physical-qubit permutation moves: 0;
- total local Pauli-axis changes: 12;
- maximum declared interface complexity: 2.

This is an explicit frame-shell construction. A literal face-sharing tetrahedral-cell realization for this (A_4) transition shell remains a separate metric-gluing problem.

## 3. S4 shell

Use the exact protected-logical-kernel (S_4) factor directly.

Carrier graph:

- six module ports on cube faces, equivalently octahedron vertices;
- octahedron adjacency graph.

Thus

[
V=6,qquad E=12,qquadeta_1=7.
]

The six module states are cosets of a cyclic (C_4) vertex stabilizer. The (C_4) stabilizer has one four-element orbit on the other vertices, producing the octahedron's degree-4 adjacency.

All seven fundamental cycles close strictly to identity and all twelve interface transitions remain protected-logically trivial.

Replay metrics:

- modules: 6;
- interfaces: 12;
- cycle rank: 7;
- nontrivial protected-logical interfaces: 0;
- total physical-qubit permutation moves: 28;
- total local-axis changes: 12;
- maximum declared interface complexity: 5.

## 4. Shell comparison

| shell | modules | interfaces | cycle rank | logical-twisting interfaces | total permutation moves | total local-axis changes | max interface complexity |
|---|---:|---:|---:|---:|---:|---:|---:|
| D6 tetrahedral ring | 6 | 6 | 1 | 0 | 42 | 0 | 7 |
| A4 tetrahedral-face shell | 4 | 6 | 3 | 0 | 0 | 12 | 2 |
| S4 cube-face/octahedron shell | 6 | 12 | 7 | 0 | 28 | 12 | 5 |

The complexity columns are exact for the selected frame representatives and declared cost function, but they are not physical gate counts.

The principal structural contrast is:

- (D_6): simplest cycle topology, permutation-heavy interfaces;
- (A_4): smallest shell and lowest local interface complexity;
- (S_4): richest cycle topology, moderate mixed transition complexity.

No architecture winner follows without circuit compilation and hardware costs.

## 5. Exact transition-group identification

The full phase-quotiented monomial local-Clifford automorphism group has order

[
1152.
]

The exact decomposition replay found two commuting (S_4) subgroups, a central (C_2), trivial pairwise intersections as required, and complete product coverage of all 1152 elements.

Therefore

[
oxed{
operatorname{Aut}^{m mon}_{LC}(mathcal G)
cong
C_2	imes S_4	imes S_4.
}
]

Exact structural checks:

[
|Z(G)|=2,
]

[
|[G,G]|=144=|A_4	imes A_4|,
]

[
|G_{m ab}|=8,
]

and the protected-logical kernel is

[
oxed{
K_{192}cong C_2^3	imes S_4.
}
]

The second (S_4) factor intersects the logical kernel in its normal Klein four subgroup (V_4). Consequently the protected logical action is

[
S_4/V_4cong S_3.
]

So the exact quotient structure is naturally

[
1	o
C_2	imes S_4	imes V_4
	o
C_2	imes S_4	imes S_4
	o
S_3
	o1.
]

This explains the previously observed six equal logical action classes of size 192.

## 6. Triality hypothesis resolved

The order

[
1152
]

and quotient/kernel pattern initially suggested the Weyl group (W(F_4)), which is related to (D_4) triality.

That identification is **NO-GO**.

An independent exact rational reflection enumeration of (W(F_4)) gives element-order spectrum

[
1^1, 
2^{139},3^{80},4^{228},6^{464},8^{144},12^{96}.
]

The MQM monomial local-Clifford group has

[
1^1,2^{199},3^{80},4^{312},6^{368},12^{192},
]

with no order-8 elements.

Hence

[
oxed{
operatorname{Aut}^{m mon}_{LC}(mathcal G)

otcong W(F_4).
}
]

The deeper structural result is instead

[
oxed{
C_2	imes S_4	imes S_4.
}
]

So the earlier "triality-type" suggestion is frozen as a useful analogy source but rejected as a group isomorphism.

## 7. Development consequence

The current geometric-coherence hierarchy is now:

[
	ext{metric shell}
longrightarrow
	ext{module/frame shell}
longrightarrow
K_{192}	ext{-coherent interfaces}
longrightarrow
	ext{circuit compilation}.
]

All three tested frame shells (D_6,A_4,S_4) can be built with zero protected-logical interface twist and strict fundamental-cycle closure.

The next discriminator is therefore no longer algebraic admissibility alone. It is the **compiled circuit/resource cost of the interface transitions and intermodule syndrome schedule**.

## AUTO_LOCK

Scoped exact results:

1. explicit (D_6) six-module tetrahedral carrier with (r^6=I);
2. exact (A_4) four-module and (S_4) six-module coherent frame shells;
3. exact shell cycle ranks and declared transition-complexity ledgers;
4. exact group isomorphism (C_2	imes S_4	imes S_4);
5. exact protected-logical kernel (C_2^3	imes S_4);
6. exact logical quotient (S_3cong S_4/V_4);
7. exact NO-GO for (W(F_4)) identification.

## OPEN

1. interface-circuit synthesis for (A_4,S_4,D_6);
2. fault-tolerant intermodule gates/syndrome schedules;
3. metric tetrahedral-cell gluing for the (A_4/S_4) module shells;
4. hardware resource/performance comparison;
5. independent external review.

Physical promotion remains 0.
