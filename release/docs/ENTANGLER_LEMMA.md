# Restricted entangler obstruction
MQM 0.5 | 18 September 2026 | Source-reported finite enumeration

**Conditional finite-search lemma.** For two copies of the supplied eight-data-qubit subsystem code, none of the gauge-preserving maps in the three enumerated transversal/pairwise Clifford families below induces an entangling logical map, according to the supplied search records.

| Enumerated family | Tested | Gauge-preserving | Entangling logical maps |
|---|---:|---:|---:|
| Identical two-qubit Clifford symplectic action applied to all eight corresponding cross-block pairs | 720 | 2 | 0 |
| Independently choose I, CNOT A-to-B, CNOT B-to-A or CZ on each of eight corresponding pairs | 65,536 | 1 | 0 |
| Same pair-specific alphabet with SWAP added | 390,625 | 2 | 0 |

**Code specification.** Each block has center generators IIIXXZZI, IIIYIYZZ, IIIXZIXZ, XXXXYYIX; six further gauge generators XIIIIIII, ZIIIIIIZ, IXIIIIII, IZIIIIIZ, IIXIIIII, IIZIIIIZ. Protected logical representatives are IIIYZIZI and IIIXIZIZ. Pauli phases are quotiented out for the symplectic search; 720 counts symplectic maps, not the full Clifford group including Pauli phases.

**Verification route.** Enumerate a family, test preservation of the two-block gauge subspace, descend accepted maps to the protected logical quotient, and classify their logical action. The supplied identical-map output records only logical identity and block exchange; the pair-specific searches record the counts above.

**Evidence status.** The original summary and search output files support this statement. These entangler searches were not rerun in release 0.5; the two canonical replays check other claims. This is a conditional summary of a reported exhaustive computation, not a newly verified universal theorem.

**Limit.** No conclusion is established here for arbitrary multi-round circuits, non-Clifford gates, ancilla-assisted methods, code switching, or temporary-gauge parity surgery. A complete noisy logical CNOT remains unestablished. The scoped parity-surgery proposal is not invalidated by this restricted obstruction.

Source: supplied transversal-entangler lock and its two search-output records; hashes in `PROVENANCE.json`. Formal background: Poulin, arXiv:quant-ph/0508131; Gottesman, arXiv:quant-ph/9705052.
