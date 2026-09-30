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
| [SBL \| Research \| Is the core hypothesis already falsified?](issues/01-is-the-core-hypothesis-already-falsified.md) | Compositional generalization, hierarchical prediction, interlingua ceiling, parser error compounding | in flight |
| [SBL \| Research \| Does this already exist, and where is it used?](issues/02-does-this-already-exist.md) | Nearest neighbours incl. UMR/AMR; deployed usage; novelty test | in flight |
| [SBL \| Engineering \| Can the first milestone be built with tools that exist?](issues/03-can-the-first-milestone-be-built-with-tools-that-exist.md) | Tamil tooling gap, UD→semantics path, parallel corpora, serialization | in flight |
| [SBL \| Engineering \| What does it take to reach the final state?](issues/04-what-does-it-take-to-reach-the-final-state.md) | Per-phase software/hardware/data/people/cost inventory | in flight |
| [SBL \| Research \| Would anyone adopt a shared semantic ID space?](issues/05-would-anyone-adopt-a-shared-semantic-id-space.md) | Adoption mechanisms; where the GPS analogy breaks | in flight |

## Decisions so far

<!-- the index: one line per closed ticket, then zoom the link for the detail the ticket holds -->

_None yet — v01 charted the map and opened the tickets._

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
