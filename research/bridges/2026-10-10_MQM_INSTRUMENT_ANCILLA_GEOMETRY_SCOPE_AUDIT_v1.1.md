# MQM v1.1 scoped execution record — 2026-10-10

Physical promotion: 0. No frozen 2+PV changes.

Track 1 (noisy instrument): Ran an independently coded, **illustrative one-qubit** branch-resolved projective-Z-measure-and-reset test with K0=|0><0|, K1=|0><1|. Both branch maps are CP, K0^dag K0+K1^dag K1=I; span{I,Z} invariant under both adjoints. This is **not** the complete subsystem-8 2+PV quantum instrument. The |+> and |-> Z-only-record / X-measurement counterexample confirms insufficiency under changed instrument family. Complete noisy 2+PV minimal invariant space remains OPEN.

Track 2 (fault replay): Checked the existing v1.0 source-bound 15 set partitions of four checks into 1..4 syndrome/flag ancilla pairs (1,7,6,1): each has 34 abstract unit-time Clifford layers under strict measurement/reset lifecycle barriers. No new full 2+PV single-fault equivalence campaign was executed. Historical 4564-case 3+1 campaign is a **different frozen protocol** and must not be used as 2+PV or redesigned ancilla evidence. Preserve previously scoped 405 CNOT within-check probes only.

Track 3 (3D): Prior 16-site dimensionless placement and exploratory radius checks remain candidate geometry only. No source-certified hardware positions, connectivity, transport loss, correlated routes, or timing; no performance promotion.

Reproducible local audit: mqm_v11_verify.py and mqm_v11_results.json (SHA256 parent result 5a2b803e5c3d8b998c2cc33743b7780f01c6a7774fbce3c53f09b9826cae3bfd). All local checks passed their declared limited contracts. Scope: mathematical example + regression, NOT a quantum hardware or distance-three fault-tolerance certificate.

Next technical gate: build the actual native syndrome/flag instruments from the frozen gate list including reset and destructive readout, then replay all declared 2+PV one-fault locations against a separately implemented comparator; independently source-confirm placement and MOVE channels.