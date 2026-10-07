# MQM 0.5 external replay request
Prepared 18 September 2026 | Status: ready to send; no external result received

## The object under review

File: MQM_RESEARCH_RELEASE_0.5.zip

SHA-256: `12479c3490d11faa768f246b5d296630fa656365ada362a243f0ad0e8bb5976b`

Download: https://mqm-research.ben-w-mayes.chatgpt.site/MQM_RESEARCH_RELEASE_0.5.zip

Citation: https://mqm-research.ben-w-mayes.chatgpt.site/release/CITATION.cff

This is the unchanged 18 September 2026 release, not a rebuilt archive. The later website figures are explanatory material outside this ZIP.

## Bounded request

Please try a fresh-environment replay and return either a reproducible match, a failure, or an unstated assumption. No endorsement, hardware time, benchmark, or priority claim is requested. A local rerun by the constructor is not an external review; a CI run initiated by the constructor is only an external-machine execution.

1. Download the ZIP; verify the exact SHA-256 before extracting.
2. Use a fresh Python 3.12 environment. Record OS, Python version and package installation log. The release pins Stim 1.15.0 and NumPy 2.3.5.
3. Install `requirements.txt` from the extracted MQM_0.5 folder.
4. Run `python -B support/verify_release.py` and retain complete stdout/stderr and exit code.
5. Run `python -B support/run_notebook.py` and `python -B artifacts/x5_envelope.py`; compare parsed JSON with the two expected files.
6. Inspect whether the executable check actually supports its stated claim. The subsystem ideal-syndrome lookup is not the missing noisy flag decoder. X5's frame reset is valid only for the declared X-only model, not arbitrary logical coherence.

## Expected observations, not an acceptance shortcut

- All 44 file hashes match.
- Subsystem: center rank 4, gauge rank 10, dressed distance 3, witness IIIIIXXZ; 24 single-data Pauli cases corrected with ideal center syndrome.
- X5: 1,312 round-translation comparisons, 16 clean patterns, 800 incoming cases yielding 750 zero-X and 50 one-X residuals; 30 retained logical-failure witnesses.

Do not modify the supplied ZIP to make a run pass. Report the first failure and preserve the original logs. A proposed repair should be a separate patch with the original mismatch retained.

## Return record

- Reviewer name or stable identifier:
- Date and environment:
- Relationship to release construction:
- Downloaded ZIP SHA-256:
- Dependency installation outcome:
- Commands, exit codes and attached complete logs:
- Parsed JSON comparison outcome:
- First reproducible mismatch, if any:
- Assumption or counterexample identified:
- Scope reviewed / scope not reviewed:
- Permission to quote or publish this review (optional):

No independent-replay claim will be made until a non-constructor returns a review record. Hardware execution, noisy memory behavior and comparative advantage remain outside this request.
