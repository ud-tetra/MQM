# MQM Firewall Schedule + η_out Audit v0.1

**Date:** 2026-10-07  
**Evidence:** EXACT / DERIVED / CANDIDATE / SOURCE-BLOCKED separated below  
**Physical promotion:** 0  
**Source branch:** subsystem-8 in release/branches.json  
**Concurrent source incorporated:** commit 5d72f2b0a7145f011ba00bc066fdcfdcfd1c6753  
**Replay:** 2026-10-07T1955Z_mqm_firewall_schedule_leakage_audit_v01.py  
**Machine result:** 2026-10-07T1956Z_MQM_FIREWALL_SCHEDULE_LEAKAGE_RESULTS_v0.1.json

## RESULT

Three requested fronts were executed together.

1. **Schedule propagation:** the archived v0.2 gate list is not byte-readable through the present connector, so a location-by-location claim on that immutable schedule is **SOURCE-BLOCKED**. However, schedule-independent operator-algebra limits and exact syndrome-support audits are closed below.
2. **η_out:** the locked tri-tetra graph gives an exact cut decomposition and proves that **100% of first-hop core-to-shell graph leakage passes through hub site 8**. Physical weighted η_out remains OPEN until source-bound coupling/process weights are restored.
3. **Redesign:** the current center-generator basis is not firewall-optimal. An equivalent basis reduces cross-boundary/hub-8 checks from 3 to the exact minimum 2, with unchanged total Pauli weight 19 and an invertible syndrome-coordinate map.

No frozen schedule was altered.

---

## 1. Exact core/shell partition

Use the locked tri-tetra mapping

\[
T_C=\{1,2,3,8\},\quad
T_+=\{5,6,7,8\},\quad
T_-=\{4,6,7,8\}.
\]

Define

\[
C=\{1,2,3,8\},\qquad S=\{4,5,6,7\}.
\]

The union of the three tetrahedral K4 edge sets contains exactly

\[
15=3\cdot 5
\]

unique edges:

\[
|E_{CC}|=6,\qquad |E_{CS}|=4,\qquad |E_{SS}|=5.
\]

The four cut edges are exactly

\[
E_{CS}=\{(8,4),(8,5),(8,6),(8,7)\}.
\]

### EXACT

Every graph-local first hop from the correctable core into the logical shell passes through physical site 8.

This statement is independent of coupling magnitude.

---

## 2. Typed η metrics

Let each declared physical interaction/noise edge carry a nonnegative source-bound weight \(\omega_e\). The weight can be a rate, integrated process weight, covariance contribution, or another declared measure, but the type must be fixed before comparison.

Define

\[
W_{CC}=\sum_{e\in E_{CC}}\omega_e,\qquad
W_{CS}=\sum_{j=4}^{7}\omega_{8j},\qquad
W_{SS}=\sum_{e\in E_{SS}}\omega_e.
\]

Two different quantities are useful and MUST NOT be conflated.

### Shell-intersecting fraction

\[
\boxed{
\eta_{\rm shell}
=
\frac{W_{CS}+W_{SS}}
     {W_{CC}+W_{CS}+W_{SS}}
}
\]

answers: how much of the total declared edge-noise weight touches the logical shell?

### Core-escape fraction

\[
\boxed{
\eta_{\rm cut}
=
\frac{W_{CS}}
     {W_{CC}+W_{CS}}
}
\]

answers: among declared interactions touching the core, how much lies on a first-hop escape edge?

Because

\[
W_{CS}=\omega_{84}+\omega_{85}+\omega_{86}+\omega_{87},
\]

hub 8 carries **all** first-hop firewall leakage in this graph.

### Equal-edge structural proxy only

If, only as a topology diagnostic, all fifteen edges are assigned equal weight,

\[
\eta_{\rm shell}^{\rm eq}=\frac{4+5}{15}=\frac35,
\]

and

\[
\eta_{\rm cut}^{\rm eq}=\frac4{6+4}=\frac25.
\]

These fractions are **not physical noise estimates**. They expose graph structure only.

### OPEN

The archived coordinate/risk-map artifacts are hashed in the session manifest, but the exact source weights are not byte-readable in this runtime. Therefore no \(r^{-6}\), \(r^{-12}\), van-der-Waals, thermal, or calibrated hardware weighting is inferred here.

Physical \(\eta_{\rm shell}\) and \(\eta_{\rm cut}\) remain OPEN.

---

## 3. Exact firewall-break stress test

The prior theorem establishes that all \(4^4=256\) Pauli operators supported on \(C\) are benign to the protected logical subsystem under frozen ideal recovery.

The next exact test multiplies every core Pauli by one nonidentity Pauli on exactly one shell site.

The workload contains

\[
256\cdot4\cdot3=3072=2^{10}\cdot3
\]

patterns.

The frozen ideal-center recovery gives

\[
768I_L+768X_L+768Y_L+768Z_L.
\]

For each shell site \(j=4,5,6,7\) separately, the 768 patterns split as

\[
192I_L+192X_L+192Y_L+192Z_L.
\]

### EXACT interpretation

A single shell-supported Pauli is enough to destroy the universal 256/256 firewall property.

Under a **uniform Pauli-basis enumeration**, three quarters of the resulting basis patterns are logically nonidentity after the frozen minimum-weight recovery.

This 3/4 is **not a physical failure probability**; no physical distribution over basis operators has been supplied.

---

## 4. Direct cross-partition entangler NO-GO

Let

\[
\mathcal A_C=\mathcal B(\mathcal H_C)\otimes I_S
\]

be the full core operator algebra.

Suppose a unitary \(U\) across the core/shell partition preserved the firewall algebra exactly:

\[
U\mathcal A_C U^\dagger=\mathcal A_C.
\]

Then conjugation by \(U\) is a *-automorphism of the full matrix algebra \(\mathcal B(\mathcal H_C)\). Every such finite-dimensional automorphism is inner, so there exists a core unitary \(V_C\) such that

\[
U(A\otimes I)U^\dagger
=
V_C A V_C^\dagger\otimes I
\]

for every \(A\).

Set

\[
W=(V_C^\dagger\otimes I)U.
\]

Then \(W\) commutes with every \(A\otimes I\), hence lies in the commutant

\[
\mathcal A_C'=I_C\otimes\mathcal B(\mathcal H_S).
\]

Therefore

\[
U=V_C\otimes V_S.
\]

### EXACT / NO-GO

Any genuinely entangling direct unitary across \(C|S\) must move **some** core operator outside the core algebra.

Therefore gate ordering alone cannot make the full arbitrary-core firewall invariant under a direct core-shell entangler.

A working schedule must instead use at least one of:

- recovery/segmentation before unsafe propagation;
- flagged or otherwise detected propagation;
- verified ancilla-mediated measurement whose faults are bounded;
- an encoded interaction that preserves a different correctable algebra.

This is gate-set independent.

---

## 5. Center-basis optimization

The current center generators are

\[
\begin{aligned}
S_1&=\mathrm{IIIXXZZI},\\
S_2&=\mathrm{IIIYIYZZ},\\
S_3&=\mathrm{IIIXZIXZ},\\
S_4&=\mathrm{XXXXYYIX}.
\end{aligned}
\]

With \(C=\{1,2,3,8\}\):

- \(S_1\) is shell-only;
- \(S_2,S_3,S_4\) cross the firewall;
- \(S_2,S_3,S_4\) all touch hub 8.

So the current basis has

\[
N_{\rm cross}=3,\qquad
N_8=3,\qquad
N_{\rm core\,inc}=6,
\]

with total Pauli weight

\[
4+4+4+7=19.
\]

### Exact lower bound

Enumerating all 15 nonidentity elements of the rank-4 center gives:

\[
\operatorname{rank}(\text{shell-only center subspace})=2,
\]

and

\[
\operatorname{rank}(\text{center elements avoiding site 8})=2.
\]

Therefore every four-generator center basis requires at least

\[
\boxed{2}
\]

cross-boundary generators and at least

\[
\boxed{2}
\]

hub-8-touching generators.

The minimum total number of core incidences among such bases is 5.

### Firewall-aware optimal basis

One exact optimum is

\[
\begin{aligned}
B_1&=S_1=\mathrm{IIIXXZZI},\\
B_2&=S_2S_3=\mathrm{IIIZZYYI},\\
B_3&=S_2=\mathrm{IIIYIYZZ},\\
B_4&=S_4=\mathrm{XXXXYYIX}.
\end{aligned}
\]

It has

\[
N_{\rm cross}=2,\qquad
N_8=2,\qquad
N_{\rm core\,inc}=5,
\]

while retaining total Pauli weight 19 and weights \((4,4,4,7)\).

Relative to the current basis:

- cross checks: \(3\to2\), a reduction of \(1/3\);
- hub-8 checks: \(3\to2\), a reduction of \(1/3\);
- core incidences: \(6\to5\), a reduction of \(1/6\);
- total Pauli weight: unchanged at 19.

There are 96 bases tied under the replay's lexicographic optimum. A physical platform cost model is required to select among them.

---

## 6. Decoder-preserving syndrome transform

Let the old syndrome be

\[
s=(s_1,s_2,s_3,s_4).
\]

For the candidate basis define

\[
\boxed{
b=(s_1,\ s_2\oplus s_3,\ s_2,\ s_4).
}
\]

This map is invertible:

\[
\boxed{
s=(b_1,\ b_3,\ b_2\oplus b_3,\ b_4).
}
\]

### EXACT

No ideal logical decoder fitting is required.

The new measurement result can be transformed back to the original frozen syndrome coordinates before applying the existing ideal decoder.

A physical measurement circuit, noisy decoder and fault-tolerance proof are still separate obligations.

---

## 7. Firewall-aware scheduling rule

### DERIVED design rule

For any ancilla that sequentially interacts with both shell and core support of a cross-boundary check, order the data interactions so the **shell segment precedes the core segment** where compatible with the selected parity-extraction convention.

The intent is to bias late propagating ancilla hooks toward the already-correctable gauge core rather than back into shell data.

This does not eliminate early hooks and is not yet a fault-tolerance theorem.

### CANDIDATE protection hierarchy

For the two unavoidable cross checks \(B_3,B_4\):

1. use a fresh syndrome ancilla per check;
2. never reuse one syndrome ancilla across both cross checks without measurement/reset;
3. interact with shell support before core support where compatible with the chosen native gate convention;
4. add a flag or verified-cat mechanism capable of detecting a fault that would span the shell/core boundary;
5. transform \(b\to s\) only after the measurement record is accepted;
6. HOLD rather than infer recovery on a flagged or incomplete temporal receipt.

A higher-resource verified-cat/Shor-style measurement is the conservative candidate because no single syndrome ancilla must serially bridge several data sites. A lower-resource single-ancilla+flag construction remains CANDIDATE until exhaustive fault injection passes.

---

## 8. Interaction with the new Gate-1 temporal result

Concurrent commit 5d72f2b0a7145f011ba00bc066fdcfdcfd1c6753 strengthens the temporal constraint.

Under one known loss plus one arbitrary subsequent survivor Pauli:

- lost sites 1,2,3: a fresh pre-loss frame of four commuting survivor-supported gauge checks can remove ambiguity;
- lost sites 4,5,6,7,8: even the entire survivor-supported gauge algebra is insufficient for universal recovery in that strong post-loss fault model.

### DERIVED consequence

The firewall redesign needs **temporal receipts before information is destroyed or propagated**.

A post-event syndrome schedule cannot reconstruct information that was never preserved.

This independently supports segmenting the schedule and preserving pre-boundary measurement history.

---

## 9. Frozen-schedule audit status

### SOURCE-BLOCKED / AUTO_FREEZE

The immutable artifact MQM_K4_8Q_FAULT_TOLERANT_GAUGE_MEASUREMENT_SCHEDULE_v0.2_LOCK.json is present in the archived session manifest with SHA-256

87e477ceaf8cbc2fa21c5d81345ebd79015fdd648b8b09a8d54453b6b159967f

but its binary archive bytes are not directly exportable through the connected runtime.

Therefore this turn does **not** claim:

- every location of v0.2 was injected;
- v0.2 fails the firewall;
- the candidate basis beats v0.2 in logical error.

### Reopening criterion

Recover the exact schedule bytes matching the frozen SHA-256, then run exhaustive single-fault injection at every preparation, one-qubit gate, two-qubit gate, measurement, reset, modeled idle and modeled loss location.

The logical failure criterion must distinguish CORRECT, detected HOLD, leakage/loss quarantine, and undetected protected-logical failure.

---

## 10. Promotion status

- tri-tetra cut topology: **EXACT**
- hub-8 first-hop cut dominance: **EXACT**
- equal-edge η fractions: **EXACT STRUCTURAL PROXY**
- physical weighted η_out: **OPEN**
- 3072-pattern firewall-break enumeration: **EXACT**
- direct entangler algebra-preservation obstruction: **EXACT / NO-GO**
- minimum two cross/hub center checks: **EXACT**
- 3→2 firewall-aware center-basis reduction: **EXACT**
- ideal decoder coordinate preservation: **EXACT**
- shell-first/core-last ordering: **CANDIDATE / DERIVED heuristic until circuit-specific injection**
- archived v0.2 location-by-location fault audit: **SOURCE-BLOCKED**
- hardware advantage / threshold / quantum advantage: **OPEN**
- physical promotion: **0**
