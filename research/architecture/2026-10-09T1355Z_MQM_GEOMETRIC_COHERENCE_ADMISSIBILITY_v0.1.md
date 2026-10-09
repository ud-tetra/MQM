# MQM Geometric Coherence Admissibility v0.1

Date: 2026-10-09
Status: CANDIDATE architecture principle with exact admission subtests
Physical promotion: 0

Origin: inspired by a user-supplied nested tetrahedral/polyhedral artwork. The artwork is a proposal source, not evidence.

## Visual abstraction

The image exhibits an approximately sixfold radial shell, a large hexagonal boundary, a superposed triangular scaffold, repeated tetrahedral motifs, and nested polyhedral shells. The useful abstraction is repeated local motifs placed into a larger symmetry orbit.

## Candidate principle

A tetrahedral MQM cluster is admissible only when every local attachment is legal and all local frame identifications close globally around the independent cycles of the cluster.

## Admission hierarchy

### Level 0: combinatorial coherence
Require legal common-face/edge/vertex intersections, consistent orientation, and boundary maps satisfying d^2=0.

### Level 1: metric coherence
For cells c and d sharing simplex sigma, the induced metric on sigma must agree. Shared edges have one typed length. Nondegenerate Euclidean tetrahedra must satisfy the corresponding Cayley-Menger positivity condition.

### Level 2: frame and holonomy coherence
Assign each interface (c,d) a transition map T_cd between canonical local frames. For a closed cell-adjacency cycle C define H(C) as the ordered product of interface maps.

For a contractible cycle intended to contain no defect, strict geometry requires H(C)=I.

If the maps act on a subsystem-code frame, closure may be relaxed only to the declared gauge group G: H(C) in G.

Define the protected-logical coherence defect delta(C) as the class of H(C) modulo G. A geometrically trivial cycle is admitted only when delta(C)=I_L.

If delta(C) is nontrivial, the object is either inadmissible for the claimed trivial geometry or must be retyped as a deliberate logical/topological defect.

### Level 3: algebraic/code coherence
Transported gauge generators must remain in the gauge algebra; center generators must remain compatible; intended measurement families must commute; and a cycle claimed to be trivial must not create a protected logical action.

### Level 4: circuit coherence
A geometrically admitted cluster must separately pass extraction-schedule, hook, flag/receipt, loss, reset/readout, decoder, and protected-logical failure tests.

### Level 5: physical coherence
Hardware admission additionally requires source-bound positions, connectivity, routing/motion, timing, native compilation, loss/leakage/readout channels, reset, and classical-control constraints.

## Orbit-shell search grammar

1. Choose a canonical tetrahedral seed K0.
2. Choose a finite symmetry group H acting on attachment ports.
3. Form the shell orbit O_H(K0).
4. Quotient duplicates by cell-complex isomorphism.
5. Test Levels 0-3 before circuit simulation.
6. Send only cycle-closed candidates to expensive circuit/hardware stages.

The image suggests C6/D6-type orbit searches as an exploratory branch. It does not establish that sixfold symmetry is physically preferred by MQM.

## Immediate test

Enumerate symmetry-generated tetrahedral clusters around the current subsystem-8/K4 core, construct interface transition maps, choose a fundamental cycle basis of the cell-adjacency graph, and compute every protected-logical coherence defect delta(C).

Acceptance criterion: every cycle declared geometrically trivial must satisfy delta(C)=I_L.

A nontrivial defect is a scoped NO-GO for that attachment rule, not a failure of the subsystem code.

## Claim ledger

- visual sixfold/nested-tetrahedral interpretation: CANDIDATE
- combinatorial d^2=0 admission: EXACT
- shared-metric consistency: EXACT conditional
- cycle transport/holonomy definition: EXACT
- gauge-relaxed logical defect criterion: DERIVED
- claim that MQM physically prefers the depicted geometry: OPEN
- hardware implication: OPEN
- physical promotion: 0
