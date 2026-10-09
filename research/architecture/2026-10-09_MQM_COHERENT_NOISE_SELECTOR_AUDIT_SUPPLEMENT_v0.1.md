# Coherent-noise candidate selector audit
Status: CANDIDATE protocol and diagnostic consistency; no source-specific physical winner.

Candidate basis: I, b, v128, D6. Prior averages are source-independent, equal-dwell ideal-control metrics. They must NOT be reused as source-specific logical failure probabilities.

H=sum_j h_j P_j. For each tested physical pulse sequence compute actual toggling frame H(t); benchmark ideal average Hbar0, first Magnus correction Hbar1, and the cross term in ||Hbar0+Hbar1||^2. Model MOVE loss/dephasing/correlated transport and actual control timing; feed channels through the unchanged 2+PV acceptance/decoder and compare accepted logical error, yield and cost. Training calibration windows are separate from frozen held-out evaluation.

The prior memoryless Pauli no-benefit result is still binding. Source-bound Hamiltonian coefficients and matching compiled MOVE pulse channels were not available during this execution. Motion advantage is therefore OPEN; physical promotion 0.
