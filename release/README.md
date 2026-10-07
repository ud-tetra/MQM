# MQM 0.5 - research evaluation release
18 September 2026 | Benjamin Walker Mayes

MQM is an open evaluation method for tetrahedral quantum-code sketches. Three code branches, replayable algebra, prepared but unrun experiments. No hardware result. No claimed advantage.

This single release supersedes the current public presentation of 0.4. All files below belong to release 0.5; upstream version identifiers exist only in provenance. The review materials are available at no charge. This release does not declare a new software reuse license or claim independent replication.

## Two canonical replay entry points

1. `artifacts/subsystem_algebra.ipynb`: Stim Pauli algebra, dressed-distance enumeration and a new ideal-center syndrome lookup. Execute in Jupyter or use the lightweight runner below. This does **not** restore the missing noisy memory sweep.
2. `artifacts/x5_envelope.py`: the supplied X-only controller driven by Stim extraction rounds. All 1,312 translated round cases agree with the supplied binary model; the 800 incoming-X cases yield 750 zero-X and 50 one-X residuals. The 30 weight-two-plus-extra-X logical failures remain explicit.

Tested with Python 3.12.14, Stim 1.15.0 and NumPy 2.3.5. Install into an isolated environment using `python -m pip install -r requirements.txt`, then run from this folder:

```sh
python -B support/verify_release.py
python -B support/run_notebook.py
python -B artifacts/x5_envelope.py
```

Compare parsed JSON with `expected/subsystem_algebra.json` and `expected/x5_envelope.json`. Case records are in `expected/x5_cases.json`. The verifier checks the file manifest and both expected outputs. Optional `--write` on the X5 entry point regenerates outputs and the ideal round circuit; doing so changes a released file only if output differs, in which case the manifest should fail until intentionally regenerated.

## Reading order

- `branches.json` and `schema/branch.schema.json`: explicit resources, generators, logicals, distance metric, witnesses and one decoder definition per branch. The 8-data ancilla count is null because no extraction circuit is fixed.
- `docs/MISSING_FILES.md`: exact known dependency and missing raw-run inventory. The memory performance table is withdrawn from current publication.
- `docs/ENTANGLER_LEMMA.pdf`: dated one-page restricted-family obstruction, source-reported and not rerun here.
- `docs/TRACK_A_REVIEW.md`: 20-circuit review inventory; not a frozen experiment, not executed.
- `PROVENANCE.json` and `CITATION.cff`: source lineage and citation.

`circuits/x5_round.stim` is one ideal round. The 20 Track A files are draft logical circuits; no vendor compilation, physical timing, loss model, noisy memory circuit or full adaptive hardware controller is provided. Simulator `peek_z` is internal introspection, not an experimental measurement. Reconstructing computational-basis frames between rounds is justified only for this X-only conformance replay, not for proving logical coherence.

## Review success

An independent replay, a reproducible mismatch or a written counterexample is a useful result. A replay performed during release construction is not independent review. Hardware acceptance and matched-baseline performance remain open. Physical promotion remains 0.
