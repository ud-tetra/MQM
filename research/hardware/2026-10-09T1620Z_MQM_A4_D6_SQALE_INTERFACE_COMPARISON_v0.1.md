# MQM A4 versus D6 Sqale interface comparison v0.1

**Status:** DERIVED typed implementation comparison / hardware ranking OPEN
**Physical promotion:** 0

## Matched workload

Compare one bidirectional shell-interface sweep: six undirected interfaces traversed in both directions, so both A4 and D6 contribute 12 directed interface transitions.

## A4 physical local-Clifford implementation

The exact selected A4 transition on every directed interface is two parallel HSH words on two data qubits. Therefore each interface contains exactly four H primitives and two S primitives; the shell sweep contains 48 H and 24 S.

Using the frozen Sqale selective-local-H construction on an 8-live-data register, one two-target H layer requires 2 global GR pulses and 14 local-Rz site requests. Two H layers plus the two-target S layer therefore require per directed interface:

- 4 GR requests;
- 30 local-Rz site requests;
- 0 CZ requests;
- 0 atom-motion requests.

For all 12 directed A4 interfaces:

- **48 GR requests**;
- **360 local-Rz site requests**.

If syndrome and flag atoms remain live during interface canonicalization, the spectator set rises from 6 to 8 and the Rz exposure becomes 38 per interface, 456 per shell sweep. This is an explicit scheduling envelope, not a hardware timing result.

The source-bound Sqale model supplies coherent GR and Rz error/leakage objects, but not a complete interface-level stochastic channel. Hardware error probability remains OPEN.

## A4 virtual Clifford-frame mode

Because every A4 interface is a code automorphism, the local Clifford may instead be tracked as a classical Clifford frame and absorbed into subsequent compiled measurements/gates. The interface itself then has zero quantum operations, but a separate transformed-extraction compilation is required before claiming zero total cost. This mode is **CANDIDATE** until that compile is verified.

## D6 virtual frame relabel

The exact D6 interface is the pure permutation

r=(1 2 3)(4 5)(6 7), with qubit 8 fixed.

As a passive module-frame relabel, the interface requires zero quantum gates and zero atom motion. This is exact as a coordinate transformation, but is not physical state transport.

## D6 atom-motion realization

If the same frame permutation is realized physically, exactly seven of eight data roles move on every directed interface. The matched 12-interface sweep therefore contains **84 moved-atom role assignments**. The route lengths, move concurrency, duration, transport dephasing, heating, and loss are provider-channel OPEN quantities.

No scalar comparison against A4 is authorized until the Sqale MOVE channel and compiled positions are supplied.

## D6 gate-SWAP baseline

The previous three-CNOT SWAP canonicalization is retained only as a comparison baseline. It uses 4 SWAPs = 12 two-qubit primitives per directed interface and failed the scoped one-error recovery audit. It is not the preferred neutral-atom implementation.

## Ruling

- D6 passive frame relabel: **EXACT zero interface-gate cost**, no state-transfer claim.
- D6 physical atom motion: **exact 7 moved roles/interface; performance OPEN**.
- A4 physical local Clifford: **exact 48 GR + 360 Rz site requests per matched shell sweep** under the 8-live-data compile.
- A4 virtual Clifford frame: **CANDIDATE zero-transition-cost mode; transformed extraction still OPEN**.
- Fair hardware ranking: **OPEN** because the MOVE channel and transformed-frame schedule are not yet source-complete.
