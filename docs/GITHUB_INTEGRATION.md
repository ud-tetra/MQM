# Integrated GitHub research repository

Authorized private destination: `ud-tetra/MQM`, branch `main`. The user created it and authorized per-turn live artifact capture on 7 October 2026.

This repository contains the website source, generated website, all 36 published architecture replay packages and manuscripts, the immutable code review release 0.5, claim registers, source-bound protocols, failures and amendments. Package hashes live in `research/session_catalogue.json`. Nested dependency packages preserve the earlier research inputs.

## Offline use

Download the offline ZIP from the GitHub Actions artifact; alternatively run `python3 scripts/build_offline_site.py` to generate `offline-build/MQM_OFFLINE_WEBSITE_v1.zip`, extract it, and open `MQM_OFFLINE_WEBSITE/index.html`. Navigation is rewritten for direct file browsing; manuscripts and replay archives retain their original bytes. External scholarly references still need internet access.

Alternatively, clone the repository and run `python3 scripts/serve_offline.py`, then open `http://127.0.0.1:8000/`. This serves the same checked-in pages locally.

## Updating both copies

The Sites source repository remains the production publishing destination. GitHub is an additional research mirror; this mirror does not automatically link GitHub pushes to Sites deployment. Keep the two repositories aligned by capturing the same reviewed file state in both destinations. Connector-created GitHub commits and Sites commits may have different identities; verify file trees rather than equating commit numbers. Future assistant work must record both resulting commit SHAs and verify the artifact catalogue before claiming synchronization.

Before each synchronization:

```
python3 scripts/build_research_site.py
python3 scripts/build_offline_site.py
python3 scripts/verify_session_site.py
```

The GitHub Actions workflow repeats these checks and supplies an offline-download artifact on each push. It does not run the numerical research simulations or certify a theorem independently.

## Scope

The complete captured public corpus is included. This does not imply recovery of every historical conversation or unpublished attachment. Numerical checkpoints explicitly excluded by release protocols can be regenerated from their replay code. No private tokens, credentials, local machine settings, or ephemeral workspaces belong in this repository. No license is added without an author decision; existing notices remain intact.

Mathematical, simulation, hardware, and comparative-advantage evidence remain distinct. Physical promotion: **0**.

## Per-turn capture

`AGENTS.md` requires capture after each substantive development turn, with an append-only receipt under `research/capture_log/`. This is an agent handoff requirement, not a claim that synchronization occurs without an executing agent.
