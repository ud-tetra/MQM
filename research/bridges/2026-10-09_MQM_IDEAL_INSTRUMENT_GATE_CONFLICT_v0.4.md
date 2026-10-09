# MQM instrument/concurrency/shell gate v0.4

Date 2026-10-09. Physical promotion 0.

EXACT IDEAL: The frozen firewall center basis is not the original stabilizer basis. Corrected the verifier to use CAND=(IIIXXZZI, IIIZZYYI, IIIYIYZZ, XXXXYYIX) for four-bit observed syndromes and b_to_s before indexing the original decoder table. The first attempted assertion failed under the wrong basis and is preserved as a repair note, not a passed result.

For ideal projective center measurement followed by Pauli-frame correction, the formal 16-sector by 4-logical-Pauli observable span has 64 coordinates. Finite conjugation checks verify 64 nonzero branch transformations: Pauli recovery moves the selected syndrome sector to zero, while each logical Pauli coefficient gains its source-derived commutation sign. This is an explicit sufficient (not proved minimum) observable carrier for the IDEAL measurement-and-recovery fragment; it is NOT a full noisy 2+PV instrument certificate.

Controller predicate enumeration: among 256 pairs of 4-bit center frames, 240 mismatch -> HOLD, one equal zero -> direct ACCEPT, fifteen equal nonzero -> conditional verification; across those 240 verification syndromes, 15 zero -> ACCEPT and 225 nonzero -> HOLD, absent flags/loss. Counts are combinatorial, not probabilities.

Frozen source-level four center circuits contain 27 CNOTs (4+2+4+2+4+2+7+2). All use common syndrome ancilla q8, including flag operations involving q9. Under exclusive two-qubit gate resource constraints at most one of these CNOTs may execute per layer; lower bound 27 such layers. This says nothing about possible compilation/parallelism of other gates and does not establish hardware runtime savings.

The existing D5/A4/D6/S4 shell is sufficient as an abstract deterministic controller using current receipt and motion metadata; two 4-bit frames must be preserved logically until equality comparison. No measured classical space, time or quantum resource saving is established.

OPEN: branch-resolved noisy circuit CP superoperators, the smallest Heisenberg-invariant logical/syndrome/flag/receipt space, native routing, calibrated MOVE and timing, higher-order 2+PV benchmark, independent review. 0 physical promotion.
