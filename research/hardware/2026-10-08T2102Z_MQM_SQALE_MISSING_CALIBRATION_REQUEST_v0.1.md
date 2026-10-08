# MQM Sqale Missing-Calibration Request Matrix v0.1

**Status:** HARDWARE HANDOFF / SOURCE-GAP MATRIX  
**Physical promotion:** 0

This matrix specifies the measurements and machine artifacts required to convert the typed Sqale-channel contract into a hardware-facing MQM comparison. It deliberately asks for typed channels rather than one scalar `p`, `q`, or `p_loss`.

## Highest-priority closure requests

1. **Compiled native schedule and timing manifest.** Return exact CZ, local Rz, global GR, NDSSR, reset, idle, and motion events with timestamps and parallel groups. Without this, local-H macros cannot be translated into a source-bound GR/Rz exposure count.
2. **Mid-circuit reset + missed-loss detection.** These directly determine whether the fail-closed architecture remains safe when loss detection and ancilla reuse are nonideal.
3. **Target-backend CZ retained-error + loss channel.** Separate retained-qubit error from one-/two-atom loss at the same operating point; do not infer loss by subtracting differently conditioned fidelities.
4. **Duration-resolved idle/motion channels.** MQM has 88 data site-epochs per abstract round before compilation; these cannot be assigned an error probability without durations and transport details.
5. **Asymmetric NDSSR channel.** Preserve ε(1→0) and ε(0→1) separately and include leakage-state classification. A symmetric measurement rate is not an admissible hardware object without a frozen population model.

## Acceptance format

Preferred handoff is machine-readable JSON/CSV with backend ID, calibration timestamp, uncertainty, site/pair distribution, and raw counts or sufficient statistics. Values from different operating points must remain separately tagged.

The companion CSV `MQM_SQALE_MISSING_CALIBRATION_MATRIX_v0.1.csv` contains the full 16-field request set and explicit closure criteria.

## Claim boundary

Receiving these data would enable a typed hardware-noise simulation. It would **not** by itself establish a threshold, fault tolerance on hardware, or quantum advantage.
