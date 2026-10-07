# MQM Tetrahedral Gauge-Core Noise Firewall Theorem v0.1

**Date:** 2026-10-07  
**Evidence:** EXACT code algebra / DERIVED architecture consequence / CANDIDATE physical exploitation  
**Physical promotion:** 0  
**Code source:** \`release/branches.json::subsystem-8\`  
**Geometry source:** locked native-3D tri-tetra mapping  
**Replay:** \`2026-10-07T1900Z_mqm_gauge_core_correlated_noise_audit_v01.py\`  
**Machine receipt:** \`2026-10-07T1901Z_MQM_GAUGE_CORE_CORRELATED_NOISE_RESULTS_v0.1.json\`

## Executive result

The native tri-tetra geometry does contain a real code-algebraic correlated-noise advantage, but it is **support selective**, not a generic reduction of bath power.

The locked central tetrahedron

\[
T_C=\{1,2,3,8\}
\]

is exactly the unique four-site region whose entire Pauli operator algebra is correctable on the protected logical subsystem under ideal subsystem recovery.

The two outer tetrahedra,

\[
T_+=\{5,6,7,8\},\qquad
T_-=\{4,6,7,8\},
\]

do not have this property.

Therefore the architecture can exploit correlated noise if the dominant correlated support is confined to \(T_C\). Merely making the bath tetrahedrally symmetric, without support confinement, does not establish an advantage.

---

## 1. Source-bound code structure

The current \([[8,1,3]]\) subsystem branch has center generators

\[
\begin{aligned}
S_1&=\mathrm{IIIXXZZI},\\
S_2&=\mathrm{IIIYIYZZ},\\
S_3&=\mathrm{IIIXZIXZ},\\
S_4&=\mathrm{XXXXYYIX},
\end{aligned}
\]

and six additional gauge generators

\[
X_1,\ X_2,\ X_3,\ Z_1Z_8,\ Z_2Z_8,\ Z_3Z_8,
\]

where the displayed physical labels are one-based.

The locked native-3D geometry identifies these same four sites

\[
\{1,2,3,8\}
\]

as the K4 gauge core \(T_C\).

This typed coincidence is the critical architecture fact: **the geometrically distinguished central tetrahedron is also the subsystem gauge region.**

---

## 2. Exact quotient map

Write an arbitrary Pauli on \(T_C\), modulo global phase, as

\[
E=
\prod_{i\in\{1,2,3,8\}}
X_i^{x_i}Z_i^{z_i},
\qquad x_i,z_i\in\mathbb F_2.
\]

Multiply by gauge generators

\[
X_1^{x_1}X_2^{x_2}X_3^{x_3}
(Z_1Z_8)^{z_1}
(Z_2Z_8)^{z_2}
(Z_3Z_8)^{z_3}.
\]

All support on sites \(1,2,3\) is removed. Hence

\[
E\sim_{\mathcal G}
X_8^{x_8}
Z_8^{z_8+z_1+z_2+z_3},
\]

with addition in \(\mathbb F_2\).

Thus the full four-site Pauli algebra collapses, modulo gauge, to exactly four representatives:

\[
I,\quad X_8,\quad Z_8,\quad Y_8.
\]

### Integer decomposition

There are

\[
4^4=256=2^8
\]

Pauli basis elements on four sites.

The core gauge kernel has

\[
2^6=64
\]

elements, so the quotient has

\[
\frac{256}{64}=4=2^2
\]

cosets.

The frozen center syndrome map likewise sees only four syndromes:

\[
0000,\quad0001,\quad0110,\quad0111,
\]

each with exactly \(64\) core Pauli patterns.

Their frozen decoder representatives are respectively

\[
I,\quad Z_8,\quad X_8,\quad Y_8.
\]

This is an exact finite-field compression from eight binary Pauli exponents to two effective syndrome bits.

---

## 3. EXACT theorem — gauge-core operator-algebra correctability

### Statement

For the frozen subsystem-8 code, the operator algebra supported on

\[
T_C=\{1,2,3,8\}
\]

is correctable on the protected logical subsystem under ideal subsystem recovery.

Equivalently: any CPTP noise channel whose Kraus operators remain supported entirely on \(T_C\) can arbitrarily disturb the gauge degrees of freedom while leaving the recovered protected logical state unchanged.

### Proof

Take a Pauli basis \(\{P_a\}\) for the operator algebra on \(T_C\).

For any pair \(P_a,P_b\),

\[
P_a^\dagger P_b
\]

is another Pauli supported on \(T_C\).

By the quotient map above it is gauge-equivalent to one of

\[
I,\ X_8,\ Y_8,\ Z_8.
\]

If the representative is \(I\), the operator is gauge and therefore acts as identity on the protected logical subsystem.

If the representative is \(X_8,Y_8,\) or \(Z_8\), it has nonzero center syndrome, so projection back onto the code sector vanishes.

Hence the operator-QEC condition has the form

\[
P P_a^\dagger P_b P
=
I_L\otimes M_{ab}
\]

for all \(a,b\), where \(P\) is the code projector and \(M_{ab}\) acts only on the gauge subsystem.

Therefore the entire \(T_C\) operator algebra is correctable on the protected logical subsystem.

Because arbitrary Kraus operators on \(T_C\) are linear combinations of this Pauli basis, the result extends from Pauli channels to arbitrary channels with support confined to \(T_C\).

### Scope

This is exact code algebra. It is not a statement that a physical bath remains confined to \(T_C\), and it is not a fault-tolerant circuit theorem.

---

## 4. Cleaning receipt

The protected logical generators can be moved completely off \(T_C\).

The release representative

\[
\bar X=\mathrm{IIIYZIZI}
\]

is stabilizer-equivalent to

\[
\bar X'\sim \mathrm{IIIZYZII},
\]

supported only on physical sites \(4,5,6\).

Likewise

\[
\bar Z=\mathrm{IIIXIZIZ}
\]

is stabilizer-equivalent to

\[
\bar Z'\sim \mathrm{IIIYXYII},
\]

also supported only on physical sites \(4,5,6\).

These cleaned representatives anticommute and generate the protected logical algebra while avoiding the entire gauge core.

This is a direct geometric receipt that logical information can be represented outside \(T_C\).

---

## 5. Exhaustive uniqueness audit

All

\[
\binom84=70=2\cdot5\cdot7
\]

four-site subsets were tested with all \(256\) supported Pauli patterns.

Only one subset returned protected logical class \(I\) for all \(256\) patterns:

\[
\boxed{T_C=\{1,2,3,8\}}.
\]

The two locked outer tetrahedra give

\[
T_+:\quad
64I+64X_L+64Y_L+64Z_L,
\]

and

\[
T_-:\quad
64I+64X_L+64Y_L+64Z_L.
\]

Therefore a uniform four-site Pauli stress test with identical physical support size is logically invisible on \(T_C\) but distributes equally across all four logical Pauli classes on either outer tetrahedron.

This is an internal equal-cardinality control. It does **not** by itself prove a hardware performance advantage.

---

## 6. Correlated pair-fault structure

Let the four core sites be \(G=T_C\) and the remaining four sites be the shell \(S\).

For all nonidentity two-site Pauli combinations:

| pair location | patterns | logical \(I\) | logical \(X\) | logical \(Y\) | logical \(Z\) |
|---|---:|---:|---:|---:|---:|
| \(G-G\) | 54 | 54 | 0 | 0 | 0 |
| \(G-S\) | 144 | 36 | 36 | 36 | 36 |
| \(S-S\) | 54 | 0 | 18 | 18 | 18 |

Thus every two-site Pauli fault inside the gauge core is benign to the protected logical subsystem under ideal recovery. Every two-site Pauli fault entirely in the shell is logically nontrivial after the frozen minimum-weight recovery.

### Amplitude-damping / excitation-exchange components

For the four Pauli components appearing in

\[
\sigma_i^-\sigma_j^-
=
\frac14
\left(
X_iX_j+iX_iY_j+iY_iX_j-Y_iY_j
\right),
\]

the exact class counts are:

| pair location | components | logical \(I\) | logical \(X\) | logical \(Y\) | logical \(Z\) |
|---|---:|---:|---:|---:|---:|
| \(G-G\) | 24 | 24 | 0 | 0 | 0 |
| \(G-S\) | 64 | 24 | 12 | 16 | 12 |
| \(S-S\) | 24 | 0 | 9 | 6 | 9 |

For internal pair components of the three physical tetrahedra:

\[
T_C:\ 24/24\ \text{logical-}I,
\]

while

\[
T_+:\ 0/24\ \text{logical-}I,
\qquad
T_-:\ 0/24\ \text{logical-}I.
\]

The hub/site-8 bridge is therefore the critical escape route: correlations that remain inside \(T_C\) are absorbed by the gauge structure, whereas correlations that cross from the core into the protected shell are not guaranteed benign.

---

## 7. What the geometry actually buys

### EXACT

The native 3D layout places a complete correctable operator algebra on a geometrically distinct tetrahedral cell.

This is stronger than merely diagonalizing a correlated covariance matrix.

### DERIVED

The architecture admits a **noise-routing strategy**:

- tolerate or intentionally place stronger common-mode/control disturbance on \(T_C\);
- keep core-to-shell correlated propagation small;
- reserve the outer shell for protected logical support and syndrome-bearing interactions.

If the physical implementation can make the dominant correlated bath mode live primarily on \(T_C\), then logical performance can depend on **support leakage out of the core**, rather than on total core noise strength.

### CANDIDATE metric

A future physical comparison should report a core-confinement quantity such as

\[
\eta_{\mathrm{out}}
=
\frac{\text{noise weight with support intersecting }S}
{\text{total noise weight}},
\]

with the numerator defined from the actual source-bound Kraus, Lindblad, covariance, or process representation.

The useful architecture question is then not merely “is the noise correlated?” but:

> How much correlated noise remains inside the correctable K4 gauge algebra, and how much leaks across the hub into the logical shell?

---

## 8. NO-GO boundaries

This result does **not** establish:

1. that tetrahedral geometry lowers total physical noise power;
2. that an \(S_4\)-symmetric bath is automatically beneficial;
3. that active gates preserve \(T_C\)-support confinement;
4. that the frozen syndrome-extraction circuit is fault tolerant under arbitrary core noise;
5. a threshold, logical lifetime, hardware result, or quantum advantage.

Correlated noise can worsen QEC performance when it produces multi-site faults outside a correctable algebra. The current theorem identifies a special correctable support algebra; it does not make arbitrary correlations favorable.

---

## 9. Literature scope

This result uses the standard operator/subsystem-QEC principle that gauge transformations may change gauge degrees of freedom without changing protected encoded information. Relevant foundations include:

- D. Poulin, *Stabilizer Formalism for Operator Quantum Error Correction*, Phys. Rev. Lett. 95, 230504 (2005).
- D. W. Kribs, R. Laflamme, D. Poulin, M. Lesosky, *Operator Quantum Error Correction*, Quantum Information & Computation 6, 382–399 (2006).
- D. Bacon, *Operator Quantum Error-Correcting Subsystems for Self-Correcting Quantum Memories*, Phys. Rev. A 73, 012340 (2006).

The project-specific claim here is only the exact algebraic alignment of the frozen MQM subsystem-8 code with the locked tri-tetra \(T_C\) region. No literature novelty claim is made.

---

## 10. Promotion status

- Gauge-core quotient map: **EXACT**
- 256/256 core Pauli replay: **EXACT**
- uniqueness among 70 four-site subsets: **EXACT**
- arbitrary core-supported channel correctability under ideal subsystem recovery: **DERIVED EXACT from operator-QEC condition**
- geometry-enabled physical noise routing: **CANDIDATE**
- finite-time reservoir logical advantage: **OPEN**
- active-schedule support confinement: **OPEN**
- hardware validation: **OPEN**
- quantum advantage: **OPEN**
- physical promotion: **0**

## AUTO_LOCK / AUTO_FREEZE

**AUTO_LOCK — scoped mathematical layer:** \(T_C=\{1,2,3,8\}\) is the unique four-site correctable gauge-core region under the current subsystem-8 algebra and frozen ideal recovery.

**AUTO_FREEZE — unsupported promotion:** “tetrahedral geometry suppresses physical noise” or “MQM has a correlated-noise hardware advantage” remains unsupported until source-bound dynamics show that dominant physical correlations are actually confined to \(T_C\) and a matched baseline is beaten.
