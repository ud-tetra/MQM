# MQM Session State Snapshot — 2026-10-09

**Status:** consolidated append-only session capture  
**Physical promotion:** 0  
**Manifest:** `research/session/2026-10-09T2345Z_MQM_SESSION_MANIFEST_v0.1.json`

## Current architecture

The session converged on a typed multi-function geometry and control stack:

[
D_5	ext{ coupler/spare fiber}
;oplus;
A_4	ext{ module coordination}
;oplus;
D_6	ext{ pure transport/frame cycle}
;oplus;
S_4	ext{ receipt verification}.
]

The protected-logical frame transition group remains

[
G=C_2	imes S_4	imes S_4,
qquad
pi:G	o S_3,
qquad
|kerpi|=192.
]

## Motion layer

- Static shape/function specialization is exact under frozen structural metrics.
- Motion monodromy gives exact protected-logical semantics.
- The same logical operation admits multiple hidden-frame clocks.
- Full (K_{192}) second-order search found no strict dominator of (b), but element (v=128) is the strongest lower-exposure challenger.
- Canonical gate-SWAP motion implementations are NO-GO under the frozen cross-profile finite-pulse stress.
- Transport-assisted (v=128) is materially better than transport-assisted (b) in that stress model.
- The spectator-free logical-identity class contains exactly 12 pure permutations; the strongest zeroth-order pair is the order-6 D6 transport family.
- Hardware D6-v128 selection is SOURCE-BLOCKED by missing in-array MOVE timing/loss/dephasing/parallelism data.

## D5 replacement layer

The natural D5+midpoint 8Q data mapping is NO-GO for improving the frozen 15-edge interaction-length uniformity.

D5 instead has an exact specialized role as a redundant two-terminal coupler/ancilla fiber:

[
kappa_5=rac{2}{sqrt{3+2/sqrt5}}approx1.01346.
]

The five equivalent slots map naturally to four hub-cut channel ancillas plus one spare.

Single detected channel-ancilla loss can be repaired conditionally on spare survival and MOVE/reset/verification success. Repair produces HOLD and requires a fresh retry; it never authorizes immediate ACCEPT.

## Spare scheduling

- Homogeneous site channels: unique minimax spare count ((1,1,1,1,1)).
- Known heterogeneous site channels: uniform rotation is NO-GO in general; the frozen stress optimum is ((0,0,0,2,3)).
- Unknown/adversarial site labeling restores uniform rotation as the unique robust minimax allocation.
- Online Hoeffding-UCB adaptation is implemented only at completed superframe boundaries; ACCEPT/HOLD/QUARANTINE criteria remain immutable.

## Receipt layer

Native K4 receipt object:

[
[6,3,3].
]

S4/octahedral comparison receipt object:

[
[12,5,4].
]

Under the frozen equal-iid bit-error objectives, K4-only and S4-only form the Pareto front; K4+S4 is not generically Pareto.

The selector therefore uses:

[
	ext{semantic coverage}
ightarrow
	ext{unsafe target}
ightarrow
	ext{layers}
ightarrow
	ext{bits}
ightarrow
	ext{HOLD}.
]

Both layers are required only when both typed receipt objects must independently be certified.

## Integrated shell controller

The abstract executable shell stack is:

[
oxed{
	ext{CALIBRATE}
ightarrow
	ext{LEARN}
ightarrow
	ext{SELECT MOTION}
ightarrow
	ext{ASSIGN SPARE}
ightarrow
	ext{RUN }2+PV
ightarrow
	ext{REPAIR}
ightarrow
	ext{SELECT RECEIPT}
ightarrow
	ext{VERIFY}
ightarrow
	ext{FRESH RETRY}.
}
]

A machine-readable branching event graph exists for D6/v128 motion selection, D5 spare assignment, frozen (2+PV), recovery/verify, repair, K4/S4 receipt gating, and fresh retry.

Model checks report zero safety-invariant violations for K4-only, S4-only, and K4+S4 receipt modes.

## Hardware/source boundary

Still OPEN / SOURCE-BLOCKED:

- in-array MOVE duration;
- MOVE loss and retained-state channel;
- MOVE dephasing/phase shift;
- transport parallelism and correlated motion error;
- reset/idle typed channels;
- missed-loss detection;
- backend-timed executable schedule;
- hardware fault-tolerance evidence;
- threshold;
- quantum advantage.

Simulation/algebra results do not promote these claims.

## Repository capture

The session manifest records **132** timestamped/session-specific files across workflows, architecture, hardware, protocols, amendments, and capture logs, including failed and repaired artifacts. No overwrite, deletion, or force push was used.
