# MQM–Sqale Minimal Experimental Request Packet v0.1

**Purpose:** obtain only the measurements needed to turn the typed MQM native schedule into a hardware-facing replay. This packet does **not** ask for one scalar p, q, or p_loss.

## P0 — blocking deliverables

1. **Compiled MQM schedule + timing manifest.** Compile the supplied one-round MQM circuit to Sqale and return native GR, RZ, CZ, NDSSR, reset, idle, and motion events with qubit IDs, start times, durations, parallel groups, backend ID, compiler version, and calibration window.
2. **CZ retained-error + loss channel at the same operating point.** For the CZ pairs used by the compile, return retained-subspace process/PTM/Pauli or source-native five-level channel plus one-atom and two-atom loss probabilities. Fidelity alone is insufficient.
3. **Mid-circuit reset channel.** For syndrome/flag reuse, return output-state distribution and loss/leakage conditioned on the prior NDSSR result, together with reset duration.
4. **NDSSR channel.** Preserve 0→1 and 1→0 errors separately; include leakage classification and state-conditioned atom loss.
5. **Loss-detector confusion.** Return false-negative and false-positive rates after CZ, NDSSR, reset, idle, and motion. MQM's current mathematical model assumes ideal loss indication, so this item directly gates hardware promotion.
6. **Idle/storage channel at compiled wait times.** Characterize dephasing/coherent drift, leakage, and loss for the exact idle-duration set appearing in the compiled schedule.
7. **Motion channel if the compiler moves atoms.** For each move class, provide distance, duration, dephasing/error channel, heating/rearrangement failure, and loss.
8. **GR and local-RZ channels for the exact compiled angles.** Preserve coherent angle bias and spatial/shot covariance rather than converting them to depolarizing probabilities.

## P1 — correlation closure

Provide parallel-CZ correlated errors/spectator effects and GR spatial/shot covariance for the concurrency actually used by the compiled schedule.

## Data format

Return one JSON document conforming to `MQM_SQALE_PROVIDER_HANDOFF_SCHEMA_v0.1.json`, plus referenced raw-count files. Every value must carry its operating-point/calibration provenance and uncertainty. Values from different Sqale generations or calibration windows must remain separately tagged.

## Acceptance boundary

The handoff is **source-complete** for an MQM hardware-noise simulation only when every native event in the compiled schedule maps to a typed measured channel or to an explicitly justified ideal operation. Missing events remain OPEN; they are not filled by medians from another gate family.

Receiving this packet permits a typed simulation. It does not establish a threshold, hardware fault tolerance, or quantum advantage.
