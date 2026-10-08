# MQM Pair Replay v0.1

Purpose: provide a self-contained replay handoff for the frozen 1+0 / 2+1 / 3+1 single- and two-fault classifiers.

## Contents

- `mqm_symbolic_malignant_pair_replay_v01.cpp`: primary exact classifier.
- `mqm_full_stochastic_tail_v01.cpp`: separate P-struct simulation engine.
- `mqm_pair_classifier_crosscheck_v01.cpp`: standalone second classifier.
- `EXPECTED_RAW_AGGREGATES.json`: frozen expected raw sums.
- `MANIFEST.json`: SHA-256 provenance.
- `verify_replay.py`: exact semantic comparison.

## Local replay

```bash
g++ -O3 -std=c++17 mqm_symbolic_malignant_pair_replay_v01.cpp -o primary
./primary > primary.json

g++ -O3 -std=c++17 mqm_pair_classifier_crosscheck_v01.cpp -o independent
./independent > independent.json

python3 verify_replay.py primary.json independent.json
```

Expected terminal status: `PASS_EXTERNAL_RUNTIME_REPLAY`.

This package checks reproducibility of the frozen arithmetic and pair labels. It does not constitute external scientific review, hardware validation, a threshold, or physical promotion.
