# Missing inputs and withdrawn memory presentation
MQM 0.5 | 18 September 2026

The former memory pseudothreshold table is withdrawn from the current public presentation. It is not a reproducible public result in this release. This withdraws its use as evidence; it does not assert that its numerical values have been disproved. Prior release history is retained.

| Missing object | Why it matters | Current treatment |
|---|---|---|
| `MQM_K4_8Q_FAULT_TOLERANT_GAUGE_MEASUREMENT_SCHEDULE_v0.2_LOCK.json` | Hard-coded dependency supplies standard recovery and flag lookup tables. The script contains some gate ordering, but the complete schedule/recovery contract is absent. | Do not reconstruct it from the reported answer. |
| Full raw outputs and run provenance for the reported memory sweep | Needed to reconcile trial counts, seeds, failure totals, uncertainty and schedule identity. Exact complete filenames were not supplied. | No public memory-performance number. |
| Calibrated gate, idle, reset and measurement noise; matched baseline | Needed for an interpretable noisy comparison. | Comparison remains empty. |

The new ideal-center lookup in `branches.json` is explicitly **not** a restoration of the historical flag decoder. Ideal operations in the deterministic algebra/envelope checks are a declared scope, not a realistic idle-noise model. No zero-idle-noise performance number remains in this release.

The critique mentions 200,000-trial files. Their exact inventory has not been recovered; that trial count is not asserted as a verified property here.
