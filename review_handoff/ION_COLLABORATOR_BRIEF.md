# First trapped-ion contact candidate
Prepared 18 September 2026 | Candidate, not an established collaborator

**Thomas Monz — Quantum Engineering group, University of Innsbruck.**
Public professional address: **Thomas.Monz@uibk.ac.at**.

Identity and current research focus are verified on the university's [research groups page](https://www.uibk.ac.at/en/exphys/research/), which names Thomas Monz as head of Quantum Engineering and lists the address above. Its stated focus includes quantum error correction and coherent control. Monz also coauthored [Demonstration of fault-tolerant universal quantum gate operations](https://arxiv.org/abs/2111.12654), which reports trapped-ion logical gate work. These support relevance; they do not establish availability, interest, suitability of a particular apparatus, or willingness to collaborate.

The fit is an inference: a group with published QEC and trapped-ion control experience can assess whether the nine-qubit controller-conformance draft asks a meaningful and implementable question. Ask for a replay or feasibility review first. Do not present X5 as a distance-three code or native-3D hardware proposal.

## Concrete first ask

A fresh replay of the unchanged 0.5 ZIP, or referral to someone willing to review it; then, if useful, a feasibility comment on the 16 X-pattern + four-control draft. The 20 circuits are logical templates, not vendor-compiled or experimentally frozen. Seek the first blocking assumption before seeking ion time.

## Draft email — not sent

To: Thomas.Monz@uibk.ac.at
Subject: Small X-only controller-conformance draft — request for replay or feasibility review

Dear Dr. Monz,

I’m seeking a critical first reader for a small research-method release, MQM. Your group’s work on trapped-ion error correction and logical operations makes you a relevant person to ask.

The immediate question is narrow: does the supplied Stim replay support its stated X-only controller envelope, and is the accompanying nine-qubit conformance draft worth refining with a laboratory?

The release contains a separate eight-data-qubit subsystem algebra check and a five-data-qubit repetition controller with four ancillas. The latter has unrestricted quantum distance one. Its 800 labeled incoming-X cases end with 750 zero-X and 50 one-X residuals; 30 outside-envelope logical failures are retained. No hardware result or advantage is claimed.

The experiment draft is 16 clean X-pattern checks plus four baseline/control templates. It still needs a physical mapping, matched timing, measurement/reset and crosstalk characterization, and a reviewed acceptance rule.

Would you or a colleague be willing to replay the release or identify the first assumption that makes this conformance experiment unhelpful? A counterexample or a referral would be useful; I’m not asking for endorsement or QPU time at this stage.

Release and instructions: https://mqm-research.ben-w-mayes.chatgpt.site/replay/
SHA-256: 12479c3490d11faa768f246b5d296630fa656365ada362a243f0ad0e8bb5976b

Best regards,
Benjamin Walker Mayes

## Send boundary

This is a local, reviewable draft. No message has been sent, no relationship is implied, and no person is listed as a collaborator on the website. Sending requires the user's explicit authorization for this recipient and message.
