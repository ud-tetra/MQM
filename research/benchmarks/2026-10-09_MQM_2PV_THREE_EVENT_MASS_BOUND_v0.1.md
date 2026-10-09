# MQM 2+PV three-event mass bound (independent rederivation)
Status: EXACT bound only; full higher-order classifier NOT RUN; physical promotion 0.

Parent: research/protocols/2026-10-09_MQM_2PV_HIGHER_ORDER_EXTENSION_v0.1_FREEZE.json

Exact method: truncate a convolution of three binomial fault-location counts at degrees 0,1,2. For n event locations of probability t, B0=(1-t)^n, B1=n*t*(1-t)^(n-1), B2=binom(n,2)*t^2*(1-t)^(n-2). Convolve them and compute P(N>=3)=1-P0-P1-P2 using exact rational arithmetic.

Conservative always-exposed three-round envelope: Np=537, Nq=42, Nloss=306. Because the optional V block is conditional, 2+PV has no larger event mass than this common-rate envelope. At p=q=loss=2^-15, P(N>=3)<=3.2069612979213957e-6. This is an exact arithmetic calculation reported to 16 decimal digits, not a Monte Carlo interval.

The 125 rate-grid polynomial checks compare frozen O(2) coefficients only; 2+PV equals 2+1 at degree two (125/125), and is lower than 2+0 and 3+1 on all 100 p>0 points at degree two. These inherited comparisons do not certify all-orders orderings.

REMAINING: full conditional-exposure classifier; 200000 conditioned-tail draws per nonzero grid point; frozen confidence propagation and resource/yield metrics; separately authored fault classifier.
