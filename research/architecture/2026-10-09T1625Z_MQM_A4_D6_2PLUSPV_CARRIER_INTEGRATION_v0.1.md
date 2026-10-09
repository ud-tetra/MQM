# MQM A4/D6 + 2+PV carrier integration v0.1

**Status:** FROZEN matched workload / exact resource algebra / typed hardware exposure
**Physical promotion:** 0

## Workload definition

One shell-memory epoch consists of:

1. run the frozen 2+PV controller independently on every subsystem-8 module;
2. perform one matched bidirectional frame-interface sweep over all six undirected shell interfaces, i.e. 12 directed transitions.

This is a memory/frame-coherence workload. It is not an intermodule logical entangling gate.

A4 contains 4 subsystem-8 modules. D6 contains 6.

Each module contains 8 data qubits. The 2+PV controller uses one syndrome and one flag ancilla while a module is active.

## 2+PV round algebra

Per extraction round the exact Sqale-native request ledger is:

- 39 CZ requests;
- 40 GR requests;
- 346 local-Rz site requests;
- 14 reset site requests;
- 14 NDSSR measurements;
- 88 typed data-idle site epochs;
- 14 typed ancilla-cycle epochs.

2+PV always executes two acquisition rounds. Let v_m be the probability that module m activates the conditional post-recovery verification round under the eventual typed hardware channel. Define

V_A = sum over the 4 A4 modules of v_m,

V_D = sum over the 6 D6 modules of v_m.

No numerical v_m is assigned from the old homogeneous p model.

## A4 full-shell extraction ledger

Mandatory extraction rounds:

8 = 4 modules x 2 rounds.

Mandatory requests:

- CZ: 312;
- GR: 320;
- local-Rz site requests: 2768;
- reset sites: 112;
- NDSSR measurements: 112;
- data-idle site epochs: 704;
- ancilla-cycle epochs: 112.

Expected requests including conditional verification are obtained by adding one round per activated module:

- rounds: 8 + V_A;
- CZ: 312 + 39 V_A;
- GR: 320 + 40 V_A;
- Rz: 2768 + 346 V_A;
- reset: 112 + 14 V_A;
- NDSSR: 112 + 14 V_A;
- data-idle site epochs: 704 + 88 V_A;
- ancilla-cycle epochs: 112 + 14 V_A.

Data qubits: 32.

If c modules are extracted concurrently, peak extraction ancillas are 2c, with 1 <= c <= 4. Fully parallel extraction therefore uses 8 ancillas and 40 total active qubits before any provider-specific routing atoms.

## D6 full-shell extraction ledger

Mandatory extraction rounds:

12 = 6 modules x 2 rounds.

Mandatory requests:

- CZ: 468;
- GR: 480;
- local-Rz site requests: 4152;
- reset sites: 168;
- NDSSR measurements: 168;
- data-idle site epochs: 1056;
- ancilla-cycle epochs: 168.

Including conditional verification:

- rounds: 12 + V_D;
- CZ: 468 + 39 V_D;
- GR: 480 + 40 V_D;
- Rz: 4152 + 346 V_D;
- reset: 168 + 14 V_D;
- NDSSR: 168 + 14 V_D;
- data-idle site epochs: 1056 + 88 V_D;
- ancilla-cycle epochs: 168 + 14 V_D.

Data qubits: 48.

At concurrency c, peak extraction ancillas are 2c, with 1 <= c <= 6. Fully parallel extraction uses 12 ancillas and 60 total active qubits before routing atoms.

## Matched interface sweep

Both A4 and D6 shell graphs have six undirected interfaces, so the frozen comparison uses the same 12 directed frame transitions.

A4 physical-canonicalization option adds 48 GR and 360 local-Rz site requests when only the eight data qubits are live during the interface epoch. The 10-live-qubit spectator envelope is 48 GR and 456 Rz requests.

D6 passive frame-relabel adds zero quantum operations.

D6 physical-motion mode has 7 nonfixed data roles per directed transition, hence 84 moved-atom role assignments per matched sweep. Move distance/time/loss are OPEN provider quantities.

## Typed loss/exposure ledger

Do not collapse the hardware exposure to one p_loss.

For extraction, the source-facing exposure vector is reported separately as counts of CZ, NDSSR, reset, idle, GR, and Rz events. For D6 physical-motion mode, MOVE events are an additional typed family.

A source-complete loss model must evaluate, at minimum:

- CZ retained-error and one/two-atom loss;
- NDSSR state-conditioned loss;
- reset-associated loss/leakage;
- idle/storage loss;
- motion-associated loss for D6 physical transfer;
- missed-loss detection.

The former homogeneous check would have counted 102 ideal-detected loss opportunities per abstract round, giving 816 mandatory A4 and 1224 mandatory D6 opportunities, but these are retained only as legacy bookkeeping and are not hardware probabilities.

## Acceptance criteria for the next hardware-facing comparison

A4 and D6 must use the same provider calibration window, same 2+PV decoder/recovery semantics, same acceptance/yield metrics, and the same shell-memory workload above. Hardware ranking is blocked until v_m and the typed MOVE/reset/idle/loss channels are source-bound.

## Ruling

- 2+PV integration into A4: **EXACT resource specification**.
- 2+PV integration into D6: **EXACT resource specification**.
- matched shell-interface workload: **FROZEN**.
- source-bound hardware yield/error comparison: **OPEN**.
- physical promotion: **0**.
