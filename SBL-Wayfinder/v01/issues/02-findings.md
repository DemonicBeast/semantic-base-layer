# T02 — Prior art census: findings

Artifact for [02-prior-art-census.md](02-prior-art-census.md).

**Status: PARTIAL.** Research was cut off by a time budget. The nearest-neighbour
ranking, UMR, AMR, and Universal Dependencies are primary-source verified and
detailed. The lexical-resource tier (WordNet, BabelNet, ConceptNet, FrameNet,
PropBank, VerbNet, OntoLex-Lemon), the upper-ontology tier (Cyc, SUMO, BFO), and
Wikidata's identifier space were **not** completed — they appear as provisional
rows and are listed explicitly under *Incomplete* below so a follow-up pass can
pick them up.

---

## Ranked nearest neighbours

Closeness is judged against SBL's full claim: *model-independent,
language-independent meaning representation with stable shared identifiers for
concepts and relations, consumed as an interface between language and models.*

| # | Name | What it is | Closeness to SBL | Active / dormant |
| --- | --- | --- | --- | --- |
| 1 | [UMR — Uniform Meaning Representation](https://umr4nlp.github.io/web/) | Cross-lingual graph meaning representation: one shared set of abstract concepts, relations and attributes, plus language-specific concrete concepts; sentence-level + document-level graphs | **Highest.** Same niche, minus the "interface to models" framing. Cross-lingual by design, stable shared relation/attribute inventory | **Active.** NSF-funded (IIS 1763926/1764048/1764091, CNS 2213804/2213805); summer schools 2024 and 2025; DMR workshop 2025; guidelines repo last pushed 2025-05-26 |
| 2 | [AMR — Abstract Meaning Representation](https://catalog.ldc.upenn.edu/LDC2020T02) | Single-sentence, rooted, labelled graph of predicate–argument structure over English text; the substrate UMR extends | **High in kind, not in scope.** Model-independent graph with shared relation labels, but English-only and sentence-scoped | **Active.** AMR 3.0 released 2020-01-15; parsers still shipping (below) |
| 3 | [Universal Dependencies](https://universaldependencies.org/) | Cross-linguistically consistent morphosyntax: a fixed universal POS/feature/relation inventory, applied per language, with ~all data public | **High on the "language-independent standard with stable shared inventory" half; structurally syntax, not semantics.** It is the existence proof that the SBL *governance* model works | **Active and growing.** 2.18 released 2026-05-15: 353 treebanks, 193 languages. Up from 130 languages in 2.12 (2022-05-15). Next release 2.19 on 2026-11-15 |
| 4 | [OntoLex-Lemon](https://www.w3.org/2016/05/ontolex/) | W3C community standard for publishing lexical entries and their senses as RDF, with `ontolex:LexicalSense` / `LexicalConcept` as stable URIs | **High on the ID-space half.** Gives stable dereferenceable identifiers for word senses and concepts, model-independent by construction | Provisional — not investigated |
| 5 | [ConceptNet](https://conceptnet.io/) | Commonsense knowledge graph of labelled natural-language assertions between concept nodes | **Medium.** Stable concept nodes plus typed relations, but untyped/loose edges and no compositional sentence semantics | Provisional. Code repo last pushed 2023-01-19, which suggests the *tooling* is static; data release cadence unverified |
| 6 | [Wikidata](https://www.wikidata.org/) | Collaborative knowledge base whose Q/P identifiers are stable, language-neutral, densely externalised across the web | **Medium-high on identifiers, low on composition.** Stable global IDs for entities and relations exist and are already model-independent; there is no sentence-meaning layer | Provisional — not investigated |
| 7 | [FrameNet](https://framenet.icsi.berkeley.edu/) | Frame-semantic lexicon: frames with typed frame elements, linked to annotated sentences | Medium. Shared semantics inventory, but lexical/frame-level, not a compositional whole-sentence interface | Provisional — not investigated |
| 8 | [PropBank](https://propbank.github.io/) | Predicate–argument annotation layer: frame files giving numbered argument roles per verb sense | Medium. Its rolesets are literally the `:ARG0/:ARG1` vocabulary AMR and UMR build on — a shared-identifier layer already in production inside AMR | Provisional — not investigated |
| 9 | [VerbNet](https://verbs.colorado.edu/verbnet/) | Verb classes with syntactic frames and thematic roles, mapped to PropBank and FrameNet | Medium-low. Class-based semantics; a lexical resource, not a language-independent meaning format | Provisional — not investigated |
| 10 | [SUMO](https://www.ontologyportal.org/) / Cyc / [BFO](https://basic-formal-ontology.org/) | Upper ontologies: a single formal top-level concept hierarchy intended to be reused across domains | **Low-medium.** They supply the `CAT --IS_A--> ANIMAL` inventory SBL's §9 sketches, but they are ontology-first, not language-to-model interfaces | Provisional — not investigated. SUMO homepage returned HTTP 403 to automated fetch; status unverified |
| 11 | [MCP — Model Context Protocol](https://modelcontextprotocol.io/introduction) | Open protocol standardising how AI models discover and call tools/resources, with declared schemas | **Low but strategically relevant.** The only one of these that is *actually* a shared model-facing interface with real adopters. It standardises the transport and tool schema, not meaning | Active |

---

## 1. What already exists

The core finding is that **the niche is occupied at the top of the list, and
occupied by a project with funding, users, and a decade of infrastructure.**

**UMR.** The project describes itself as designing "a meaning representation that
can be used to annotate the semantic content of a text in any language," explicitly
to "extend AMR to other languages, particularly morphologically complex,
low-resource languages," with a document-level companion graph
([homepage](https://umr4nlp.github.io/web/)). The first released dataset covers six
languages — Arapaho, Chinese, English, Kukama, Navajo, Sanapaná — and the paper
states that cross-linguistic comparability "is done through the use of a common set
of abstract concepts, relations, and attributes as well as concrete concepts
derived from words from individual languages"
([LREC 2024](https://aclanthology.org/2024.lrec-main.229/)). The formal
specification is [UMR 0.9, dated 2022-08-08](https://github.com/umr4nlp/umr-guidelines/blob/master/guidelines.md)
— a single versioned document defining the concept types, participant roles,
non-participant roles, attributes, aspect, and quantification. That is, functionally,
an SBL-style specification: a fixed relation/attribute inventory plus per-language
concept anchoring.

**AMR.** [AMR Annotation Release 3.0, LDC2020T02](https://catalog.ldc.upenn.edu/LDC2020T02),
released 2020-01-15, English only, produced under the US GALE/DEFT/BOLT/LORELEI
programmes, and its declared applications are coreference resolution, entity
extraction, information extraction and semantic role labelling. AMR is the
model-independent semantic notation SBL's §5 examples most resemble.

**Universal Dependencies.** [Release 2.18 (2026-05-15)](https://universaldependencies.org/download.html)
ships 353 treebanks across 193 languages, distributed through LINDAT/CLARIAH-CZ,
with a published release cadence and a frozen 2.19 date of 2026-11-15. This is the
strongest evidence in the whole census that a community will adopt a shared,
language-neutral annotation standard with a stable inventory — and its adoption
curve is still rising (130 languages in 2.12, 148 in 2.13, 193 in 2.18).

**Wikidata** is the de facto precedent for "one stable ID space that everyone else
points at" — but its IDs denote entities and properties, not compositional sentence
meaning.

---

## 2. Where each is actually used — verified entries only

- **AMR — deployed in tooling and research pipelines.** Two maintained parsers with
  real activity: [transition-amr-parser](https://github.com/IBM/transition-amr-parser)
  (IBM, Apache-2.0, last push 2026-09-13) and
  [amrlib](https://github.com/bjascob/amrlib) (MIT, last push 2026-03-10).
  Both are libraries, not hosted products. Deployment is downstream of LDC corpora;
  no commercial product shipping AMR was verified. **Verdict: active in research,
  unverified in industry.**
- **UMR — active, grant-funded, small.** NSF awards IIS 1763926, 1764048, 1764091
  and CNS 2213804, 2213805; collaboration across CU Boulder, Brandeis and UNM.
  Usage evidence is training and community: UMR summer schools (Boulder 2024,
  Brandeis 2025), a UMR parsing workshop at CU Boulder (2024), tutorials at
  Georgetown (Jan 2024), and the DMR workshop series (Torino 2024, Prague 2025),
  all listed on the [project homepage](https://umr4nlp.github.io/web/).
  The guidelines repo has 21 stars. **Verdict: growing but academic and small; no
  commercial adopter verified.**
- **UD — deployed as infrastructure.** Shipped through
  [LINDAT/CLARIAH-CZ](https://universaldependencies.org/download.html) with a
  release number and DOI handle; standard input to the CoNLL shared tasks; consumed
  by parsers, cross-lingual transfer work and Tamil/Telugu/Dravidian treebank
  projects. **Verdict: growing.**
- **ConceptNet — tooling looks dormant.** The [conceptnet5 repo](https://github.com/commonsense/conceptnet5)
  (2,959 stars) last received a push on 2023-01-19. Whether the *data* is still
  released on a cadence is unverified. **Verdict: possibly static/dormant —
  needs a follow-up check.**

A resource with no users is a fact worth reporting, and the pattern here is that
the *representation* projects (UMR, AMR, UD) have users while the general-purpose
commonsense graphs have not shown verifiable recent movement.

---

## 3. The closest single thing

**UMR.** It is SBL's claim with the words "for AI models" removed: one
language-independent representation, a shared inventory of concepts/relations/
attributes, document-level scope, cross-lingual alignment, a versioned
specification, and an NSF-funded maintainer community. SBL's §16 lists UD, semantic
parsing, knowledge graphs, and multilingual representation learning as *adjacent*;
UMR is not adjacent, it is the thing.

What SBL would add that UMR lacks:

1. **Model-consumption as the primary purpose.** UMR is an annotation format:
   humans and parsers *produce* it, and downstream models consume it as features or
   training signal. SBL's §7 pitch is that a model consumes SBL structures *instead
   of* raw surface text at inference time. This is a real distinction and I did not
   find it anywhere in the UMR material.
2. **A single normative global ID space.** UMR anchors concept identity through a
   common abstract-concept inventory plus per-language concrete concepts and word
   senses; SBL proposes one minted, governed, globally stable ID space. This is a
   governance difference more than a technical one — UD already shows the governance
   model can work at scale.
3. **Program semantics** (design doc §11). Not covered by UMR or AMR, but ASTs and
   compiler IRs are the obvious prior art there; not investigated.

---

## Does SBL's novelty claim survive?

**As stated — "the novelty is the combination" — no, it does not survive.**

The claim in [design doc §16](../../../semantic-base-layer-design-5.md) is that SBL
is novel because it *combines* several known areas into "a deliberately
standardized, model-independent semantic interface." UMR already is that
combination: a standardised, model-independent, cross-lingual semantic
representation with a shared inventory of concepts, relations and attributes, a
public versioned specification, published corpora, funded maintainers, and a
community large enough to run its own summer school and workshop series. UD
separately demonstrates that a language-neutral shared inventory can reach 193
languages on a published cadence. Anyone reviewing SBL on its own §16 wording will
conclude it is UMR with different vocabulary, and the doc's own hedge ("should
therefore be treated as a research hypothesis rather than claiming that the
underlying idea has never been explored") concedes the point.

**A narrower version does survive.** Not "a standardised language-independent
semantic interface" — that exists. But the specific combination of (a) a semantic
representation designed from the start as a *consumption interface for models at
inference time*, not as an annotation target for human annotators, plus (b) a
single globally governed ID space, plus (c) reuse of that same layer for program
semantics, was not found in any source I reached. If SBL's pitch is rewritten to
that narrower claim, the novelty question becomes an empirical one about (a) —
which is exactly what the [scientific-feasibility ticket](01-is-the-core-hypothesis-already-falsified.md)
is testing. **The strategic implication is that SBL's identity should be "the
consumption interface over representations like UMR," not "a new representation,"
because the latter is already built and funded.**

---

## Incomplete — not yet investigated

Research stopped at the time budget. Not reached, in priority order:

1. **The lexical-resource tier** — WordNet (and whether the maintained fork is
   [Open English WordNet](https://github.com/globalwordnet/english-wordnet) rather
   than Princeton's original), BabelNet (version, licence tiers, commercial users),
   ConceptNet (data release cadence — only the code-repo dormancy was verified),
   FrameNet (maintainer and funding status), PropBank, VerbNet, and
   [OntoLex-Lemon](https://www.w3.org/2016/05/ontolex/) deployments. I fetched the
   BabelNet, ConceptNet, FrameNet, VerbNet, PropBank and Lemon homepages but recorded
   no claims from them, so **nothing about them should be treated as sourced.**
2. **The upper-ontology tier** — Cyc/OpenCyc (including whether OpenCyc was
   officially retired), SUMO (its homepage returned HTTP 403 to automated fetch; use
   the Wayback Machine), BFO and its ISO/IEC 21838-2 status, and Wikidata's live item
   count and named non-Wikimedia consumers. All unverified; rows 4–10 in the table
   are provisional.
3. **Part of question 2 for the non-AMR/UMR/UD entries** — deployed usage,
   maintenance dates and growing/static/dormant verdicts are missing for every
   provisional row.
4. **Interlingua approaches in MT** (the classical interlingua line, e.g. KANT),
   **LLM-era shared semantic interface proposals** beyond MCP (tool/schema
   interlinguas, "semantic ID" proposals, agent-tooling schema standards), and the
   **AST/compiler-IR** prior art for design doc §11. MCP was only spot-checked; its
   adoption evidence was not gathered.
5. **UMR corpus sizes and LDC catalog numbers.** The LREC 2024 abstract confirms the
   six-language first release, but I did not obtain the LDC item number, the token
   counts, or whether a UMR 1.0+ corpus was released afterwards. A follow-up should
   also determine whether UMR has any non-academic consumers.

---

## Confidence

**Primary-source verified** (fetched from the owning site during this pass):

- UD release 2.18, 353 treebanks / 193 languages, 2026-05-15, and the 2.12→2.18
  growth curve and 2.19 date — [download.html](https://universaldependencies.org/download.html).
- AMR 3.0 = LDC2020T02, 2020-01-15, English, GALE/DEFT/BOLT/LORELEI, stated
  applications — [LDC catalog](https://catalog.ldc.upenn.edu/LDC2020T02).
- UMR's self-description, the six-language first release, the "common set of
  abstract concepts, relations, and attributes" design — [UMR homepage](https://umr4nlp.github.io/web/)
  and [LREC 2024 abstract](https://aclanthology.org/2024.lrec-main.229/).
- UMR 0.9 specification dated 2022-08-08 — [guidelines.md](https://github.com/umr4nlp/umr-guidelines/blob/master/guidelines.md).
- UMR NSF award numbers, summer schools 2024/2025, DMR 2025, Georgetown tutorial —
  [UMR homepage](https://umr4nlp.github.io/web/).
- Parser repo activity dates and licences for
  [transition-amr-parser](https://github.com/IBM/transition-amr-parser) and
  [amrlib](https://github.com/bjascob/amrlib); ConceptNet repo last-push 2023-01-19
  and star count — GitHub API metadata (fetched before that API's rate limit was hit).
- MCP is a published open protocol for model–tool integration —
  [modelcontextprotocol.io](https://modelcontextprotocol.io/introduction).

**Partially verified:** the UD Tamil treebank's provenance (Charles University,
via HamleDT) comes from the treebank README, but I did not verify Tamil's share of
2.18 or any Tamil-specific adoption.

**Inference, not sourced:** that UMR has no commercial adopters; that no
industry system ships AMR; that SBL's "inference-time consumption" framing is the
only genuinely unoccupied part of its claim; that UD's growth is evidence a shared
inventory gets adopted. These are my reading of the evidence above, not claims any
source makes.

**Explicitly unverified — do not cite:** every statement about WordNet, BabelNet,
ConceptNet's data cadence, FrameNet, PropBank, VerbNet, OntoLex-Lemon, Cyc,
OpenCyc, SUMO, BFO, Wikidata item counts and consumers, classical MT interlinguas,
and LLM-era semantic-ID proposals. Also: web search was unavailable for most of this
session (repeated upstream failures), so coverage relied on direct fetch of primary
URLs and is therefore narrower than the ticket asks for.
