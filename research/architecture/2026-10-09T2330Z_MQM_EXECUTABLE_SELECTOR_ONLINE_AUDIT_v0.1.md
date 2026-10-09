# MQM Executable Schedule / Receipt Selector / Online Learning Audit v0.1

**Date:** 2026-10-09  
**Physical promotion:** 0

## 1. Executable shell schedule

A machine-readable branching event graph now exists for:

1. configuration;
2. D5 spare assignment;
3. D6 or v128 motion selection;
4. two mandatory 2+PV acquisition rounds;
5. compare / recovery / optional verify;
6. detected channel-loss repair;
7. K4, S4, or combined receipt gating;
8. RETRY_READY;
9. a fresh 2+PV attempt.

Each native extraction round references the frozen request ledger

\[
39\ CZ,\quad40\ GR,\quad346\ R_Z,
\quad14\ RESET,\quad14\ NDSSR.
\]

Three concrete machine-readable examples are emitted:

- D6 + uniform spare + K4 receipt;
- v128 + asymmetric spare + S4 receipt;
- v128 + asymmetric spare + K4+S4 receipt.

Model checking gives:

\[
\boxed{0\text{ invariant violations}}
\]

for every receipt mode.

The checked state-instance counts are 15, 15 and 17 for K4-only, S4-only and K4+S4 respectively.

The schedule is executable as an abstract event/state graph. MOVE durations and final backend timing remain source-bound.

## 2. Receipt-mode selector

The selector follows the frozen order:

\[
\boxed{
\text{semantic coverage}
\rightarrow
\text{unsafe target}
\rightarrow
\text{layers}
\rightarrow
\text{bits}
\rightarrow
\text{HOLD}.
}
\]

Typed semantics are preserved:

- required K4 receipt: S4-only is inadmissible;
- required S4 receipt: K4-only is inadmissible;
- BOTH: K4+S4 is mandatory;
- GENERIC: any mode may compete.

Frozen tests:

### Generic integrity, p6=p12=1%

With unsafe target \(10^{-6}\),

\[
\boxed{S4\_ONLY}
\]

is selected, with unsafe pass

\[
5.53797462126\times10^{-8}.
\]

### K4 semantic object, p6=p12=1%

With target \(10^{-5}\),

\[
\boxed{K4\_ONLY}
\]

is selected.

### Generic asymmetric case

For

\[
p_6=10^{-3},\qquad p_{12}=10^{-2},
\]

with target \(10^{-6}\),

\[
\boxed{K4\_ONLY}
\]

is selected.

### BOTH semantic objects

For

\[
p_6=10^{-2},\qquad p_{12}=10^{-3},
\]

the selector returns

\[
\boxed{K4+S4}
\]

despite its extra depth, because the semantic contract requires both receipt objects.

This closes the ambiguity between bit-model Pareto optimality and semantic coverage.

## 3. Online site-quality learning

The online learner uses a one-sided Hoeffding upper confidence bound fixed before exposure:

\[
\hat p+
\sqrt{
\frac{\log(2K/\alpha)}
{2n}
},
\]

with

\[
\alpha=0.05,\qquad K=15,
\]

and minimum 100 trials per site/channel.

Only the five-epoch spare-frequency schedule may adapt. The following remain immutable:

- ACCEPT criterion;
- HOLD/QUARANTINE transitions;
- receipt unsafe targets;
- MOVE decision thresholds.

Updates occur only at completed five-epoch superframe boundaries.

### Window 0: homogeneous observations

The controller selects

\[
\boxed{(1,1,1,1,1)}
\]

and policy UNIFORM.

### Window 1: early heterogeneous evidence

Because the confidence bounds are still broad, the conservative optimizer selects

\[
\boxed{(1,1,1,2,0)}.
\]

This differs from the static point-estimate optimum and is a useful warning: limited calibration can change the risk-minimax schedule.

### Window 2: calibration-rich heterogeneous evidence

As uncertainty contracts, the controller converges to

\[
\boxed{(0,0,0,2,3)},
\]

the same asymmetric count vector found by the static known-heterogeneity minimax calculation.

Thus the controller demonstrates a lawful adaptive pathway:

\[
\boxed{
\text{UNIFORM}
\rightarrow
\text{conservative asymmetric}
\rightarrow
\text{calibration-supported asymmetric}
}
\]

without changing any safety/acceptance rule after exposure.

This is a synthetic-controller result, not a hardware convergence theorem.

## Main architecture result

The current MQM shell stack is now executable at the abstract control layer:

\[
\boxed{
\text{CALIBRATE}
\rightarrow
\text{LEARN}
\rightarrow
\text{SELECT MOTION}
\rightarrow
\text{ASSIGN SPARE}
\rightarrow
\text{RUN }2+PV
\rightarrow
\text{REPAIR}
\rightarrow
\text{SELECT RECEIPT}
\rightarrow
\text{VERIFY}
\rightarrow
\text{FRESH RETRY}.
}
\]

Adaptive behavior is restricted to configuration and scheduling. Acceptance criteria remain frozen.

## Claim ledger

- executable abstract shell schedule: **EXACT implementation artifact**
- schedule safety invariants: **EXACT model-check pass**
- receipt-mode selector: **EXACT under frozen receipt formulas**
- semantic-coverage preservation: **EXACT**
- confidence-bound online spare adaptation: **EXACT controller behavior on frozen synthetic stream**
- online hardware learning performance: **OPEN**
- backend-timed executable schedule: **SOURCE-BLOCKED by MOVE/native timing**
- fault tolerance / threshold / quantum advantage: **OPEN**
- physical promotion: **0**
