# SBL — Research Recovery Report

**Written:** 2025-10-01 by the orchestrator, after stopping all research agents at the
user's request.

**What happened.** Five research subagents were dispatched in parallel to resolve tickets
01–05. Each spawned its own sub-teams, cascading to **24 agents in total**. They were
interrupted mid-flight. Four of the five parents wrote their `NN-findings.md` before
stopping; ticket 03 did not, and its findings survived only in its session transcript.

**This report is the index to what was recovered.** The detailed findings live in the
files it links. Nothing here replaces them.

---

## 1. What was recovered

| Ticket | Artifact | State | Reliable? |
| --- | --- | --- | --- |
| [SBL \| Research \| Is the core hypothesis already falsified?](01-is-the-core-hypothesis-already-falsified.md) | `01-findings.md` (20 KB) | **Substantially complete.** Q1/Q3/Q4 done; Q2 partial. Written by its author. | **Yes** — 20+ primary sources cited at owned URLs |
| [SBL \| Research \| Does this already exist, and where is it used?](02-does-this-already-exist.md) | `02-findings.md` (17 KB) | **Partial.** Top-tier systems verified; lexical/upper-ontology tiers provisional. Written by its author. | **Yes** for UMR/AMR/UD; provisional rows are labelled |
| [SBL \| Engineering \| Can the first milestone be built with tools that exist?](03-can-the-first-milestone-be-built-with-tools-that-exist.md) | `03-findings.md` | **RECOVERED FROM TRANSCRIPT.** Never written by its author. Reconstructed by the orchestrator. | **Directionally sound; figures need a confirmation pass** — see the file's own caveats |
| [SBL \| Engineering \| What does it take to reach the final state?](04-what-does-it-take-to-reach-the-final-state.md) | `04-findings.md` (13 KB) | **Partial.** Items 1, 2, 4 done; item 3 and the human-cost half of item 5 unsourced. Written by its author. | **Yes** — every number cited or labelled *estimate* |
| [SBL \| Research \| Would anyone adopt a shared semantic ID space?](05-would-anyone-adopt-a-shared-semantic-id-space.md) | `05-findings.md` (20 KB) | **Partial.** Q1/Q2 strong with primary sources; Q3 vendor side unmined. Written by its author. | **Yes** — 9 standards researched at source |

**Raw transcript evidence** (gitignored, local only): `research/agent-dumps/*.md` holds
23 section-tagged transcript dumps; `research/extract_agent_sessions.py` regenerates
them; `research/tamil_corpora/` and `.sbl-05-scratch/` hold the actual downloaded
evidence (corpus files, licence texts, saved standard histories) behind the figures.

---

## 2. The five findings that matter

### 2.1 Prior art is occupied — by UMR, and it is funded and active

[SBL \| Research \| Does this already exist](02-does-this-already-exist.md) ranks
**UMR (Uniform Meaning Representation)** as the nearest neighbour, and the case is
strong: UMR is a cross-lingual graph meaning representation with one shared set of
abstract concepts, relations and attributes plus language-specific concrete concepts;
sentence- and document-level; six languages annotated; an automatic parser (SETUP)
reported at SMATCH++ 91; NSF-funded across five grants; summer schools in 2024 and
2025; guidelines actively pushed in 2025.

No single ranking row on the map at `v01` is more consequential than this one. SBL's
contribution cannot be "a model-independent multilingual semantic representation with
stable shared identifiers" — **that exists**. The surviving candidate contributions are
the model-interoperability framing (§7) and the hierarchical-prediction hypothesis (§6),
and the second is undercut (below).

**Universal Dependencies is the existence proof that SBL's governance model works** —
353 treebanks, 193 languages, a fixed shared inventory applied per language, all data
public. That is the encouraging half of this finding: a shared semantic inventory *can*
be built and adopted. It is also the discouraging half: UD did it for syntax, over
decades, with a community.

### 2.2 The compositional-generalization claim is weaker than the design doc assumes

[SBL \| Research \| Is the core hypothesis already falsified](01-is-the-core-hypothesis-already-falsified.md)
delivers the sharpest technical result recovered:

- **COGS's famous negative result was substantially walked back.** Wu, Manning & Potts
  (TACL 2023, [ReCOGS](https://arxiv.org/abs/2303.13716)) showed the failures "trace to
  incidental features of COGS LFs" — models were failing on semantically irrelevant
  formatting, not compositional semantics. This cuts both ways: the canonical
  "structure doesn't save you" evidence is weaker than it looks, **but a COGS-style
  experiment built on SBL's own ontology would measure SBL's serialization as much as
  its semantics.**
- **The effect is achievable by changing the data, not the representation.**
  [Akyürek et al. 2022](https://arxiv.org/abs/2203.07402) found that simply modifying
  the training distribution lets standard seq-to-seq models reach near-perfect
  compositional generalization.
- **§13's proposed test is not a discriminating experiment.** Constructing
  `EAT(DOG, MILK)` from separately-seen concepts is a *mix-and-match* split — the kind
  SCAN found RNNs can already pass.

This is a direct hit on the experiment the design doc calls "one of the most important."

### 2.3 §6's computational claim has no located support at inference time

The efficiency literature for hierarchy is framed around **training**. No source was
located showing that predicting through a semantic category hierarchy reduces
*inference* computation versus flat next-token prediction at matched accuracy. One paper
reports hierarchical softmax *degrading* as classes grow
([Ghosh et al. 2018](https://arxiv.org/abs/1812.05737)). The design doc hedges §6
itself, so it is an open hypothesis rather than a false claim — but the burden of proof
sits with SBL, and the natural reading of the literature does not transfer.

### 2.4 The Tamil pipeline has two independent blockers — accuracy and licensing

From the recovered [ticket 03](03-can-the-first-milestone-be-built-with-tools-that-exist.md):

- **Accuracy gap.** Tamil dependency parsing tops out at **LAS ~51–62** against
  English's **~88–90** (−37 to −39 points). The best published Tamil result
  ([ThamizhiUDp](https://arxiv.org/abs/2012.13436)) is LAS **62.39**, described in its
  own paper as "4 points higher than the current best achieved for Tamil".
  **spaCy has no Tamil model at all.**
- **Licensing dead end.** The one Tamil treebank with *training data* — UD_Tamil-TTB —
  is **CC BY-NC-SA 3.0 (non-commercial)**, verified from the downloaded licence text.
  The permissively-licensed treebank (UD_Tamil-MWTT, CC BY-SA 4.0) is **test-only**.
  So a SBL that publishes cannot train on the usable treebank, and the treebank it *can*
  use cannot train a parser.
- **Corpora are parallel, not semantic.** 39,526 PMIndia EN–TA pairs under CC BY 4.0 are
  genuinely usable — but they give translations, not sentence–meaning pairs. They do not
  relieve Phase 3's annotation bottleneck.

**The most important unmeasured quantity on the whole map:** these LAS figures are
treebank-wide averages over news and web text. The design doc's milestone uses *simple
sentences*. Simple sentences may parse far better. **Nobody has measured this, and it
decides whether Phase 2 is buildable.**

### 2.5 The interoperability claim is unfalsifiable at the design doc's own scale

[SBL \| Research \| Would anyone adopt a shared semantic ID space](05-would-anyone-adopt-a-shared-semantic-id-space.md)
answers this more decisively than expected. The claim is not merely untested — it is
**unfalsifiable in principle at §20's scale**, because it is a property of *independent
adopters* and at 100 concepts the only emitter is SBL itself. One party emitting a
format is a serialization choice, not interoperability. Any v0.1 result, success or
failure, is **silent** on §7.

Six minimum conditions are stated in that artifact. The research also produced the
outcome that matters most for design: **every verified standard adoption succeeded
because the adopter was paid at the point of use** (search ranking, retail checkout,
rendering text), and the closest negative precedent — the W3C Semantic Web Activity,
whose rationale was almost exactly SBL's — **ended after ~12 years without becoming the
interchange medium.** ONNX, the closest genuine success, won where it was *narrow*
(inference graphs only), which argues for narrowing SBL's scope rather than §19's
universal framing.

---

## 3. What each finding does to the map

| Ticket | Effect |
| --- | --- |
| [SBL \| Research \| Is the core hypothesis already falsified?](01-is-the-core-hypothesis-already-falsified.md) | §13's first experiment is **not discriminating** and must be redesigned. Feeds directly into ticket 09. |
| [SBL \| Research \| Does this already exist, and where is it used?](02-does-this-already-exist.md) | **Novelty claim does not survive as written.** Must be narrowed to model-interoperability + hierarchical prediction. Feeds ticket 07 (ID space) directly: UMR/UD are the alignment candidates. |
| [SBL \| Engineering \| Can the first milestone be built with tools that exist?](03-can-the-first-milestone-be-built-with-tools-that-exist.md) | Phase 1 buildable; Phase 2 automatic Tamil pipeline blocked on licensing and accuracy. **Unblocks ticket 06** and gates ticket 07. |
| [SBL \| Engineering \| What does it take to reach the final state?](04-what-does-it-take-to-reach-the-final-state.md) | Answer to the user's requirements question. Compute is cheap; **annotation dominates**. Feeds ticket 06. |
| [SBL \| Research \| Would anyone adopt a shared semantic ID space?](05-would-anyone-adopt-a-shared-semantic-id-space.md) | §7's interoperability goal is **not testable at v0.1**. Confirms the map's decision to keep interoperability design-informing rather than gating. |

**Tickets 07, 08 and 09 are now unblocked** (07 on 01/02/03, 08 on 01/02/06). Ticket 06
is unblocked by 01 and 02 — the two findings that landed complete — so it can proceed
while 03's recovery is confirmed.

---

## 4. What was lost

Honest accounting of the gaps, so nothing is mistaken for a complete answer:

1. **Depth-3 agent syntheses.** 18 sub-teams researched Tamil tooling, corpora, UD→AMR,
   UMR, LLM parsing, serialization (JSON-LD/SHACL, PENMAN/CoNLL-U/binary), and ontology
   registries. Their raw evidence is in the scratch dirs and their reasoning is in
   `research/agent-dumps/`, but **no integrated reports were written.** The transcript
   dumps for those sessions are mostly planning and tool-call narration rather than
   conclusions.
2. **Ticket 03's author never reviewed its own findings.** The reconstruction is sound
   on the disk-verified numbers (treebank counts, TTB licence, PMIndia count) and
   transcript-sourced on the rest.
3. **The classical interlingua literature was never read.** Bar-Hillel (1960),
   ALPAC (1966), Dorr (1993) — where the strongest arguments against the interlingua
   thesis live — were explicitly listed as unread.
4. **Q2 (hierarchical prediction) is open, leaning negative** — the classic
   hierarchical-softmax papers (Morin & Bengio 2005, Mnih & Hinton 2009) were not read.
5. **The lexical-resource and upper-ontology tiers** (WordNet, BabelNet, ConceptNet,
   FrameNet, PropBank, VerbNet, OntoLex, Cyc, SUMO, BFO, Wikidata) are **provisional
   rows only.** SKOS, OWL 2, BFO ISO 21838-2 and Cyc's discontinuation were partially
   gathered in depth-3 scratch work but not integrated.
6. **Search tooling failed repeatedly.** `web_search` timed out or returned unparseable
   JSON for most agents; the GitHub API rate-limited at 60 req/hr. Agents worked around
   this with `curl` to primary sources, which is why the recovered citations are real —
   but coverage is uneven, and absence of evidence in this report is **not** evidence of
   absence.
7. **English-vs-Tamil gap needs a second source.** The Stanza/UDPipe figures are from
   official accuracy tables read during the session, not re-verified.

---

## 5. Recommended next steps

1. **Do not re-run five parallel research fleets.** The failure mode was fan-out without
   a write-back checkpoint. If research resumes, it should be one ticket at a time, with
   the findings file written incrementally.
2. **Measure the one thing that decides Phase 2:** Tamil LAS on the design doc's *simple
   sentences* specifically. It is a small, bounded task and it converts ticket 03 from
   "blocked" to "answered".
3. **Take ticket 07 (ID space) next.** Finding 2.1 changed its input materially: UMR and
   UD now look like the live alignment candidates rather than hypotheticals, and that
   choice determines the ontology's whole shape.
4. **Rewrite §13's experiment before running anything**, per finding 2.2 — as written it
   cannot come back negative, which is exactly ticket 09's concern.
