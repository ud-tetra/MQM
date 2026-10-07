# Track A: bounded collaboration packet
MQM 0.5 | 18 September 2026 | NOT EXECUTED

The 20-circuit inventory is version-frozen as a **review draft**, not as a preregistered or hardware-ready experiment. Its Stim files are logical Clifford IR, not vendor-compiled pulse schedules. S00-S15 cover the 16 X patterns of weight at most two in one ideal parity round. They do not themselves implement the adaptive multi-round recovery controller or prove coherent quantum error correction. `artifacts/x5_envelope.py` specifies that controller replay.

C00 is a five-data GHZ X-parity baseline. C01 repeats the state preparation with ancilla measurement/reset activity and measures data X parity. C02 and C03 check all-zero/all-one data population during ancilla activity. These are control templates; random ideal individual X outcomes must be evaluated through their joint parity.

Begin with the 16 syndrome patterns and a paired baseline/crosstalk control review, not the full historical 1,450-variant inventory. Shot count is not circuit count. A lab must match duration and optical/control exposure for C00/C01; Stim TICK does not assign a duration.

## Required before an experimental freeze
- Named partner, physical qubit mapping and allowed interactions.
- Compiled operations, calibrated durations and error model including idle, reset, measurement and crosstalk.
- Loss/invalid-result handling, controller latency and stopping rule.
- Predeclared shot counts, uncertainty treatment, acceptance thresholds and rejection rules.
- Non-constructor review; freeze before collecting the evaluation data.

No numerical hardware acceptance threshold or 90-day delivery promise is invented. No collaborator has been contacted. A successful review returns a mapping, compiled circuits, declared controls and either a defensible frozen rule or a written blocker. This is a research collaboration packet, not a purchasable service.

Track B remains a geometry proposal outside this execution packet. No apparatus, calibrated fidelity model or demonstrated state/loss readout is supplied.
