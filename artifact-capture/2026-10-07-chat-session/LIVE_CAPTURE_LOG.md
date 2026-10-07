# MQM live artifact capture log — 2026-10-07

**Repository:** `ud-tetra/MQM`  
**Folder:** `artifact-capture/2026-10-07-chat-session/`  
**Physical promotion:** 0

## Baseline capture — COMPLETE

The current ChatGPT session workspace was frozen into an exact compressed archive.

- Generated artifacts captured: **216**
- Uncompressed generated-artifact bytes: **3,566,144**
- Compressed archive bytes: **2,039,050**
- Archive SHA-256: `53062d4d3dc95076c8d2f8b986ee3700360e2a9deccc713907113b560229c64d`
- Source manifest SHA-256: `d6bf33aef115242609f378a7b5adf2de08f07d8fb89f0077ee699abc87c1b247`
- Archive parts committed: **27**
- Reconstruction verified locally byte-for-byte before commit.

The user-supplied source inputs are not duplicated into the generated-artifact archive:
- `UD Tetra Quantum architecture.pdf`
- `17875249175482803232469895174120.png`

Their exclusion is provenance-preserving: they are inputs, not assistant-generated artifacts.

## Transport intermediates

Temporary base64 staging files used only to move binary archive chunks through the connector are not treated as independent scientific artifacts. Their decoded bytes are exactly the committed archive-part blobs and therefore introduce no unique project content.

## Per-turn rule — ACTIVE

For every subsequent substantive turn in this chat that creates or modifies an MQM artifact:

1. preserve the local artifact;
2. append or update its GitHub copy under this session folder or a clearly linked canonical MQM repo path;
3. record path, SHA-256, evidence status, and supersession relationship;
4. never silently replace a frozen artifact;
5. use a new version when scientific content changes;
6. record AUTO_FREEZE/NO-GO artifacts with the same priority as positive results;
7. keep **physical promotion = 0** unless an independently qualified hardware bridge closes.

GitHub is the live artifact ledger. A commit does not increase evidence strength.

## Baseline archive commit chain

- Session capture folder initialized: `247a9aa3eb62c90ac1ac81d1de28e491ee4337cd`
- Binary archive attached by tree commit: `f2d66185c600489739a5f5e532cfd36bf03f98a9`
- Complete browsable manifest repaired: `0b08dd81cd544ba6334a46979054d82619566d8e`
- Archive reconstruction/part ledger: recorded in `ARCHIVE_PARTS.json`

## Reconstruct

```bash
cat archive/MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst.part* > MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst
sha256sum MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst
# 53062d4d3dc95076c8d2f8b986ee3700360e2a9deccc713907113b560229c64d

mkdir restored
tar --zstd -xf MQM_SESSION_ARTIFACTS_2026-10-07.tar.zst -C restored
```
