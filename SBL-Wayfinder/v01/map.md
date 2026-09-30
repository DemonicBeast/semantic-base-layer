# SBL Wayfinder — Map (v01)

Label: `wayfinder:map`

## Destination

An **SBL v0.1 feasibility spec**: the ontology, relationship set, and wire-format
specification for a model-independent semantic layer, scoped to the design doc's
own §20 first measurable goal — paired with a researched verdict on whether the
underlying hypothesis is worth building on.

The spec's first section is the verdict: what already exists, what is genuinely
new, and the minimum conditions that must hold for SBL to work. Reaching the end
of this map means Phase 0 is specified and the go/no-go call is made on evidence.

Source: `../../semantic-base-layer-design-5.md` (SBL v0.1, research concept).

## Notes

- **Domain**: AI semantics; knowledge representation; multilingual NLP;
  neuro-symbolic AI; semantic interoperability standards.
- **Tracker**: local markdown, in this folder. **No file is ever overwritten** —
  a revision of this map becomes `v02/`, and this folder stays frozen.
- **Standing preference (user-set)**: append-only. Keep versions.
- **Scope decisions** (user, this session):
  - Destination is **§20** (100 concepts, 30 relationships, English + Tamil, simple
    sentences). **§19**'s universal-grammar architecture is the horizon, tracked as
    fog, not as requirements.
  - Feasibility is ranked **(b) scientific → (a) engineering → (c) interoperability**.
    (b) can kill the project outright, so it is researched first; (a) is cheap to
    confirm; (c) is untestable at v0.1 scale and only informs design.
- **Naming**: every ticket is referred to by its title. Ids ride inside the name.
- **Research tickets**: resolved by subagents that call the `research` skill.
  Each writes an artifact next to its ticket as `NN-findings.md`. The ticket links
  to the artifact; the findings are never pasted into the ticket body.
- **HITL tickets** (`grilling`): resolved only in live conversation with the user.
  Do not answer the human's side of one.
- **Never resolve more than one non-research ticket per session.**

## Research in flight (v01)

Dispatched in parallel. Each writes `NN-findings.md` beside its ticket.

| Ticket | Question | Status |
| --- | --- | --- |
| [SBL \| Research \| Is the core hypothesis already falsified?](issues/01-is-the-core-hypothesis-already-falsified.md) | Compositional generalization, hierarchical prediction, interlingua ceiling, parser error compounding | **resolved** — [findings](issues/01-findings.md) |
| [SBL \| Research \| Does this already exist, and where is it used?](issues/02-does-this-already-exist.md) | Nearest neighbours incl. UMR/AMR; deployed usage; novelty test | **resolved** — [findings](issues/02-findings.md) |
| [SBL \| Engineering \| Can the first milestone be built with tools that exist?](issues/03-can-the-first-milestone-be-built-with-tools-that-exist.md) | Tamil tooling gap, UD→semantics path, parallel corpora, serialization | **resolved** — [findings](issues/03-findings.md), reconstructed from transcript |
| [SBL \| Engineering \| What does it take to reach the final state?](issues/04-what-does-it-take-to-reach-the-final-state.md) | Per-phase software/hardware/data/people/cost inventory | **resolved** — [findings](issues/04-findings.md) |
| [SBL \| Research \| Would anyone adopt a shared semantic ID space?](issues/05-would-anyone-adopt-a-shared-semantic-id-space.md) | Adoption mechanisms; where the GPS analogy breaks | **resolved** — [findings](issues/05-findings.md) |

All five were stopped mid-flight at the user's request. A consolidated account of what
was recovered, what it does to the map, and what was lost is in
[the research recovery report](11-research-recovery-report.md).

## Decisions so far

<!-- the index: one line per closed ticket, then zoom the link for the detail the ticket holds -->

- [SBL \| Research \| Is the core hypothesis already falsified?](issues/01-is-the-core-hypothesis-already-falsified.md): **Partly yes.** COGS's failure result was walked back by ReCOGS (it measured LF formatting, not composition); compositional gains come from training-distribution design, not symbolic structure; §13's proposed test is a non-discriminating mix-and-match split; §6 has no inference-time support in the literature; Tamil LAS ~62 caps end-to-end fidelity. Detail: [findings](issues/01-findings.md).
- [SBL \| Research \| Does this already exist, and where is it used?](issues/02-does-this-already-exist.md): **Yes — UMR occupies the niche**, actively NSF-funded, six languages, parser at SMATCH++ 91. UD proves the shared-inventory governance model works. The novelty claim as written does not survive; only model-interoperability (§7) and hierarchical prediction (§6) remain candidates. Detail: [findings](issues/02-findings.md).
- [SBL \| Engineering \| Can the first milestone be built with tools that exist?](issues/03-can-the-first-milestone-be-built-with-tools-that-exist.md): **Phase 1 yes; Phase 2 blocked twice over.** Tamil LAS ~51–62 vs English ~88–90, spaCy has no Tamil, and the only Tamil treebank with training data is CC BY-NC-SA 3.0 (non-commercial) while the permissive one is test-only. Detail: [findings](issues/03-findings.md).
- [SBL \| Engineering \| What does it take to reach the final state?](issues/04-what-does-it-take-to-reach-the-final-state.md): **Compute is cheap, annotation is not.** Phase 1 is a laptop; Phase 5 wants 24 GB VRAM (~$0.69/hr). The dominant cost is native Tamil semantic annotation — 1,000 pairs is a $2.5k–15k estimate at double annotation, and the roadmap runs to 100,000. Detail: [findings](issues/04-findings.md).
- [SBL \| Research \| Would anyone adopt a shared semantic ID space?](issues/05-would-anyone-adopt-a-shared-semantic-id-space.md): **Unfalsifiable at §20's scale** — with 100 concepts the only emitter is SBL itself. Six minimum conditions stated. Every successful standard paid its adopter at the point of use; the W3C Semantic Web is the closest negative precedent; ONNX won by being narrow. Detail: [findings](issues/05-findings.md).

- [SBL \| Engineering \| Is a front-end semantic interlingua for code already built?](issues/12-findings.md): **Yes — the niche is occupied.** Kythe, SCIP, LSIF and Glean already normalise many source languages into one shared structure for tools to reason over without compiling; `scip-dotnet` is a Roslyn-built C# indexer. A ~100-concept ontology is *lossier* than Roslyn's semantic model, and SCIP's own design doc rejects the nodes-and-edges shape §10/§11 propose. **The design doc's §11 premise is falsified as stated.** The only uncovered gap is behaviour/intent, for which SBL proposes no mechanism. Detail: [findings](issues/12-findings.md).

## Not yet specified

In scope, toward the destination, but not yet sharp enough to ticket. These
graduate only when the frontier clears the fog ahead of them.

- **Neural architecture for §6 hierarchical semantic prediction.** Whether a
  category → subcategory → concept → surface-token predictor is trainable at all,
  what it would be built from, and whether it beats flat next-token prediction on
  compute. Blocked behind the scientific-feasibility finding, which decides
  whether this is worth specifying.
- **The consumption interface** — the exact mechanism by which a model consumes
  SBL structures (§7, Phase 7). Serialization candidates, context reconciliation,
  and how ambiguity is resolved jointly by the model and the layer. Depends on the
  ID-space policy decision.
- **Ontology governance and versioning** — who may add concepts, semantic
  versioning rules, stability guarantees, deprecation. Depends on the ID-space
  policy decision, since minting your own space and aligning to an existing one
  carry different governance costs.
- **Multilingual expansion beyond English + Tamil** — the per-language marginal
  cost, and which language families are cheapest and hardest to add.
- **Scale-up protocol** — the experiment ladder that decides whether the
  representation has demonstrated value before a larger model is considered.
  Depends on success criteria being set for the first experiment.
- **Cross-domain transfer to programming languages** (design doc §11, Phase 6).
  Whether the same layer can carry program semantics, and whether AST-level
  interlingua prior art already settles it.
- **Repository and packaging layout** (design doc §17) — implementation detail
  that cannot be fixed until the specification it implements exists.

## Out of scope

Ruled beyond this destination. These do not graduate; they return only if the
destination is redrawn, and then as a fresh effort.

- Replacing neural networks or LLMs (design doc §15 — the doc rules this out itself).
- Encoding all human knowledge.
- A production or hosted service; deployment, SLOs, on-call.
- AGI (design doc §20 rules this out explicitly).
- Building the Phase 2–7 engine as part of this map. The destination is a
  specification plus a verdict; implementation is a separate effort.
