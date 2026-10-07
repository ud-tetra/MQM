# MQM live artifact capture — 2026-10-07 chat session

**Repository:** `ud-tetra/MQM`  
**Capture mode:** append-only per chat turn  
**Physical promotion:** 0

This folder is the live artifact sink for the current ChatGPT/MQM session.

## Scope

Captured:
- every assistant-generated artifact currently present in the session workspace;
- exact filenames and relative directory structure;
- SHA-256 manifest;
- a lossless compressed session archive split into GitHub-safe binary parts.

Excluded because they are user-provided source inputs rather than generated artifacts:
- `UD Tetra Quantum architecture.pdf`
- `17875249175482803232469895174120.png`

The compressed archive contains **216 generated artifacts** totaling **3,566,144 bytes** before archive compression.

## Archive

Reassemble:

```bash
cat archive/MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst.part* > MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst
sha256sum MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst
# expected:
# 53062d4d3dc95076c8d2f8b986ee3700360e2a9deccc713907113b560229c64d

mkdir restored
tar --zstd -xf MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst -C restored
```

The internal `SESSION_MANIFEST.json` records every generated artifact path, byte count, and SHA-256.

## Live-capture rule

For each subsequent substantive turn that generates or modifies artifacts:
1. append the new/changed artifacts to this repository;
2. update the live manifest/change log;
3. preserve superseded artifacts rather than silently overwriting scientific history;
4. record AUTO_LOCK / AUTO_FREEZE status in the artifact itself;
5. never promote simulation or algebra to hardware evidence merely because it is committed here.

GitHub is the artifact ledger, not truth authority.
