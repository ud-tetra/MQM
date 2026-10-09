# MQM coherent-noise motion gate

Status CANDIDATE protocol / source coefficients MISSING / physical promotion 0.

Inherited ideal equal-dwell instantaneous-control metrics: b (A0=55/126,K2=15616/170775,cycle exposure=72); v128 (A0=23/63,K2=78/1265,exposure=56); D6 (A0=1/3,K2=413/6325). These are ensemble metrics, not source-specific logical error rates.

For source-provided H=sum h_j P_j, candidate toggling H_k=U_k† H U_k and dwell t_k, calculate Hbar0=(sum t_k H_k)/T; Hbar1=-(i/(2T))sum_{j>k} t_j t_k[H_j,H_k]. Include Hbar0/Hbar1 cross terms. Finite physical pulses require time integration and MOVE-channel modeling, not instantaneous frame approximation.

Compare I,b,v128,D6 using frozen 2+PV circuit, coherent and stochastic channels, acceptance/yield and full time, routing and control cost. Freeze coefficients, train/holdout division, thresholds and resource objective before held-out scoring. Equal logical work required. Prior stochastic Pauli no-benefit result remains binding in its frozen scope.

Provider-specific Hamiltonian/process coefficients: MISSING. Source-bound motion winner: OPEN. Threshold/hardware benefit/advantage: OPEN.
