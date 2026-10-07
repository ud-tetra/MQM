# MQM project handoff

## Live artifact capture

The user authorizes capture of each substantive MQM development turn in the private repository https://github.com/ud-tetra/MQM, default branch `main`. Preserve this destination and repository privacy.

At the end of each development turn:
1. Record source-bound protocols, code, data receipts, manuscripts, claim registers, amendments, failure records and dependencies in the repository. Include all new user-facing artifacts or document their explicit exclusions and regeneration paths.
2. Rebuild the website and offline export when accepted milestones change. Run the artifact/hash/link verification appropriate to the changes.
3. Append a dated capture receipt in `research/capture_log/` with scope, evidence levels, tests, excluded files and unresolved gates. Never silently replace a frozen hypothesis or erase a failed result.
4. Capture on GitHub using the connected GitHub plugin or authorized Git transport. Preserve the current branch head as parent; do not force-push. Fetch/verify the resulting commit and report its link. If access is blocked, preserve local results and explicitly report capture as pending.
5. Update the Sites production source and tracker when relevant. GitHub and Sites are distinct repositories; matching files do not imply matching commit objects. Record both source SHAs when both have been updated. GitHub pushes do not automatically deploy Sites.

This is a turn-completion workflow, not a scheduled background automation. A future assistant must read these instructions and execute the capture; no unattended synchronization is claimed.

## Evidence governance

Distinguish EXACT, DERIVED, CANDIDATE, SIMULATED, EMPIRICAL-HARDWARE, scoped NO-GO and OPEN. Physical promotion remains 0 until independently supported. Keep mathematical, logical, physical and ancilla resources distinct. Future PDFs use IEEEtran A4 two-column formatting. Preserve existing licensing; do not invent a license.
