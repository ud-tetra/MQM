# MQM product and methodology presentation gap analysis

Date: 2026-09-18. Baseline: public technical release v0.3. Remediation target: v0.4.

## Decision

Position MQM as a **quantum-architecture research methodology with inspectable code models and prepared experiment designs**. The current evidence supports a concrete technical evaluation offering. It does not support a production quantum platform, a proven hardware product, a general fault-tolerance claim, or a comparative performance promise.

This audit examines the current site source and the already reviewed project evidence. It is an editorial and product-presentation judgment, not a user study, competitive-market survey, independent scientific review, or change to the research canon.

## Gaps and remediation

| ID / priority | Baseline evidence | Visitor impact | Remediation in v0.4 | Acceptance criterion |
|---|---|---|---|---|
| P01 / High | Hero says “Geometry first. Evidence next.” and describes development, without stating an evaluation outcome. | A new visitor cannot quickly identify what MQM helps them do. | Explicit headline about evaluating tetrahedral quantum architecture; short description of available research models. | First viewport states category, task, audience, and maturity without a performance promise. |
| P02 / High | No explicit audience or task-based entry paths. | Code reviewers, control engineers, and experimentalists must infer relevance. | Three evaluator paths tied to Core-X, Core-X5, and the 8Q subsystem; a separate hardware route. | Each path identifies a research question, resource scope, established result, and next unresolved gate. |
| M01 / High | “Engineering target” lists topics but not an executable methodology. | Visitors cannot tell how geometry becomes a code, circuit, or experiment. | Five-stage workflow with declared inputs, concrete output artifacts, and proceed/stop criteria. | Scope → algebra → circuit → fault/readout testing → comparison is explicit; prerequisites are visible. |
| M02 / High | Code cards emphasize names/counts rather than branch selection. | X5 may be mistaken for the perfect five-qubit code; eight total apparatus qubits may be mistaken for eight data qubits. | Task-based branch cards plus retained technical disclosures and a short notation key. | X-only and unrestricted Pauli distances remain distinct; data, gauge, and ancilla resources are labeled. |
| E01 / High | Evidence is spread across several long sections, with mixed labels such as EXACT, CHECKED, and REPLAYED. | Maturity and verification provenance take too long to assess. | Compact evidence-status summary and reader-facing definitions, linked to complete notes. | Exact algebra, same-session replay, source-reported simulation, and hardware-pending status can be distinguished at a glance. |
| E02 / High | Landing page repeats process language (“these packages”, “receipts”, raw internal status names). | The page assumes knowledge of the author’s workflow. | Public copy focuses on the result, model assumptions, and missing evidence; detailed provenance remains in technical notes. | Main narrative stands alone without phase-number or governance vocabulary. |
| A01 / High | Primary CTA scrolls to architecture; downloads contain notes only. | Visitors have no concrete way to start evaluating the method. | Evaluation brief and a curated reproducibility ZIP with executable checks, expected outputs, and verification manifest. | Both downloads resolve; kit checks run from a clean extraction and match expected JSON outputs. |
| A02 / Medium | No explicit collaboration/review task. | An interested researcher has no clear request to respond to. | “Start a technical evaluation” section with inputs to bring, outputs to review, and suggested independent-review questions. | A reviewer can begin without contacting an invented address or entering data into a nonfunctional form. |
| I01 / Medium | Successive evidence additions create a long, unranked research narrative. | Product/methodology understanding is delayed by detailed algebra and simulation tables. | Reorder around overview → paths → method → evidence → hardware → review; retain deep technical content in disclosures. | A quick reader can understand the program before opening detail; original material remains reachable. |
| I02 / Medium | Specialized notation is used without a compact reader key. | Adjacent technical audiences may confuse data qubits, logical qubits, ancillas, and distance. | Inline terminology definitions and explicit branch limits. | Required terms are explained near the first branch comparison. |
| R01 / Medium | Site offers archival notes without a packaged way to replay the newly written checks. | Reproducibility is difficult to assess from the public surface. | Publish only the checks that are actually self-contained; list missing upstream components separately. | Kit excludes sealed truth, credentials, hosting metadata, and unreviewed hardware execution code. It makes no claim to rerun the memory sweep. |
| V01 / Medium | No visual browser QA has been performed for the static site. | Responsive behavior and visual polish are not empirically verified in a browser. | Improve responsive hierarchy, keyboard navigation, focus states, and print layout; run structural/link/artifact checks. | Static checks pass. Visual/browser QA remains explicitly unverified because this static project has no compatible supervised preview. |

## Positioning and offering

Primary readers: quantum error-correction researchers, quantum control engineers, and hardware experimentalists evaluating nonplanar layouts.

Task: determine which tetrahedral code/geometry proposal merits the next mathematical, circuit, or laboratory test before hardware commitment.

Available now: code definitions and selected replayable checks; model-scoped recovery results and counterexamples; source-reported memory estimates with uncertainty; geometry and experiment-design notes; a review worksheet.

Proposed benefit: make assumptions, resources, failure modes, and evidence boundaries inspectable so a team can decide what to test next. This is a process value proposition, not a demonstrated reduction in cost, logical error, or engineering effort.

Research motivation: preserve native tetrahedral relationships long enough to test their engineering consequences. K4 itself is planar; 3D placement must earn its practical value through matched comparisons.

Unavailable/unestablished: a validated QPU implementation; device-level superiority; a complete public replay of the 8Q memory sweep; general Pauli protection from Core-X or X5; a reviewed/frozen hardware protocol with actual data.

## Methodology remediation

The five-stage public method is a synthesis of existing evidence and declared engineering requirements. It is not a new primitive UD law or a promoted theorem.

1. **Define the task:** declare code branch, error model, observable, resource budget, and comparison. Output a scoped evaluation record.
2. **Verify the encoding:** specify checks/gauges, logical operators, code dimension, and distance. Output an algebra check and named counterexamples.
3. **Compile measurement and control:** specify ancillas, interactions, reset, feedback, mapping, and geometry. Output a circuit schedule and resource account.
4. **Stress the declared model:** inject faults, test release behavior, check readout assumptions, and preserve failures. Output replayable results and a supported operating envelope.
5. **Compare and test hardware:** fix baselines, noise/cost assumptions, acceptance rules, and blinding before held-out work. Output either a qualified comparison, a mismatch, or an unresolved result; hardware claims require hardware data.

Each step has a stopping condition. Downstream documentation does not repair missing upstream evidence. The review kit covers selected algebra/model checks only, not all five stages end to end.

## Information and action design

Use two primary actions: choose an evaluation path and download the evaluation brief. Offer the replay kit alongside the evidence summary and the review section. Keep evidence notes and previously published details available. No fabricated contact endpoint, lead form, customer logo, testimonial, pricing, service commitment, or hardware availability claim is introduced.

The absence of a public contact channel is an optional future collaboration-routing decision. The implemented downloadable brief gives researchers a concrete review task without implying a functioning intake service.

## Scientific preservation

No coefficient, hypothesis, decoder, threshold, source status, or experimental interpretation rule changes. Physical promotion stays 0. All evidence claims retain their branch and model. The 30 X5 logical-failure witnesses and the 8Q simulation's lack of demonstrated advantage remain prominent.

The source reports calling a protocol “preregistered” do not establish independent preregistration or non-constructor review in this release. Model replay is not independent replication. Manifest integrity is not validation of a scientific claim.

## Release acceptance record

Status is recorded in `MQM_REFRESH_ACCEPTANCE_v0.4.json` after implementation. The required checks cover local routes, fragment links, downloads, unique identifiers, a single H1, semantic tables/disclosures, unchanged scientific invariants, and clean-extraction execution of the public review kit.

The remaining presentation limitation is visual browser QA. Scientific open items remain scientific gates, not content defects to be removed by copy editing.
