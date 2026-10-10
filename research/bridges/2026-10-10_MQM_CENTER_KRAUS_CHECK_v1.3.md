# MQM v1.3 — single center Kraus check

2026-10-10; physical promotion 0. Frozen 2+PV unchanged.

Source: research/benchmarks/2026-10-08T1920Z_mqm_full_stochastic_tail_v01.cpp; CHECKS[0]=IIIXXZZI, ORDERS[0]=[4,5,6,7]. Reconstructed 4-data/2-ancilla unitary with original H/CNOT sequence. Syndrome initialized |0>, flag initialized |+>; syndrome measured Z and flag measured X. Four 16x16 Kraus blocks from 64x64 unitary obey sum KdagK=I with max matrix entry error 8.881784197001252e-16 (complex128). Branch ranks for (s,f)=(0,0),(0,1),(1,0),(1,1): 8,0,8,0. Initial wrong flag preparation |0> produced spurious flag branches: repaired and preserved as a distinct preparation convention test.

This is only ideal single-center measurement completeness, not minimal invariant observables or full noisy 2+PV. Full independent single-fault circuit classifier NOT RUN. 3D hardware MOVE/route calibration missing; SOURCE_BLOCKED. Public Sqale claims do not provide candidate-specific per-MOVE measurements. No physical, threshold or advantage claim.

Reproduction: local mqm_center_instrument_v13.py SHA256 d9eff9da2eed67d6b82da48aa3c38523a232df50c1493cd272d910ab0db6d9fb; result mqm_center_instrument_v13.json SHA256 0e0a5f0b94405609e89dbc75e486fb7ca81c6f48f07127cbeb174b7e543a5c0a.
