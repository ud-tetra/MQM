# MQM research evaluation website

Current release: **0.5, 18 September 2026**. MQM is a research-stage evaluation method, not a quantum product. No hardware result, no claimed advantage, physical promotion 0.

Public routes: `/`, `/codes/`, `/replay/`, `/experiments/`, `/compare/`, `/origin/`.

The authored release is in `release/`; `scripts/build_research_site.py` builds the static pages and a single public review ZIP in `dist/`. `dist/styles.css` is authored directly. The website needs no runtime framework. The research replay dependencies are separate and pinned in `release/requirements.txt`.

Run `python scripts/build_research_site.py` after intentional release edits. The two canonical replay entry points are the subsystem algebra notebook and X5 envelope script. See `release/README.md` for exact scope and commands. `CITATION.cff` provides the dated citation.

The old unreplayable memory presentation is withdrawn from the current public site and ZIP. Prior releases and their checks remain preserved in source history and `evidence/`; they are not current performance claims. Historical Markdown URLs return supersession notices.

See `docs/MQM_RESEARCH_REPOSITIONING_v0.5.md` for the response to the presentation critique, `docs/MQM_RESEARCH_ACCEPTANCE_v0.5.json` for checks, and `docs/MQM_CUSTOM_DOMAIN_HANDOFF.md` for pending DNS setup.

## Architecture record — 7 October 2026

The current source-bound catalogue contains **42 research packages and 42 manuscripts**. Research, Tracker and Updates pages are built from `research/session_catalogue.json` and `scripts/build_session_update.py`. These records preserve code release 0.5 independently. The thermal target has a conditional finite-window certificate; external review, permanent retention and physical implementation remain open. Physical promotion remains 0.

## Integrated archive and offline website

All published research packages and manuscripts are stored in `dist/research/`, with hashes and claim registers in the catalogue. The site source, earlier evidence and code release are included in this repository. Live private artifact repository: **https://github.com/ud-tetra/MQM**. Per-turn capture is required by `AGENTS.md`; capture receipts are in `research/capture_log/`.

See [GitHub integration](docs/GITHUB_INTEGRATION.md) for synchronization rules.

For a complete offline download, extract `offline-build/MQM_OFFLINE_WEBSITE_v1.zip` and open its `index.html`. To browse from a checkout, run `python3 scripts/serve_offline.py`. The GitHub workflow verifies package hashes, local links and offline navigation; it does not independently validate the research claims.


## UD program-wide predictive discovery governance (2026-10-31)

**PROPOSAL / REVIEW PENDING - PHYSICAL PROMOTION 0.** The canonical [UD Predictive Discovery Protocol v1.0](https://github.com/ud-tetra/UD/blob/ff89221626d3258dc458f01408f1fac80a072530/docs/UD_PREDICTIVE_DISCOVERY_PROTOCOL_v1.0.md) (SHA-256 `d5e5f079996863ae156a3d35e1cf8ba5135c2f7b8699bd9f9a4b492828351310`) and [three candidate tests](https://github.com/ud-tetra/UD/blob/ff89221626d3258dc458f01408f1fac80a072530/docs/UD_FIRST_THREE_PREDICTION_CANDIDATES_v1.0.md) (SHA-256 `5d2fe31521e61d79182027f790db9cc3e463e8fa9ca74852443135eb5ab08956`) apply as a governance *proposal* here. Development permits explicitly labeled hypotheses, inverse design and FIT. Independent physical claims require source-complete observable/readout/units/null, frozen pre-exposure criteria, non-constructor review, held-out tests and independent replication. This change does not promote previous claims or deploy any site. See the local governance adoption note and bootloader; effective adoption needs reviewed integration to main.
