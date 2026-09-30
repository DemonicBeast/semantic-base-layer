# SBL | Engineering | Can the first milestone be built with tools that exist?

**Status of this artifact: RECOVERED FROM TRANSCRIPT — PARTIAL, UNREVIEWED BY ITS AUTHOR.**
The research agent was stopped before it wrote this file. The contents below were
reconstructed by the orchestrator from the agent's session transcript and from the
evidence it had downloaded to `research/tamil_corpora/`. Numbers attributed to a
downloaded file were re-verified on disk by the orchestrator; numbers attributed to
a fetched web page were read by the agent during its session and are marked
**transcript-sourced, not re-verified**. Treat the verdict as directionally sound and
the specific figures as requiring a confirmation pass.

## Verdict

**Phase 1 (registry, graph, validation, JSON — no neural net): BUILD.** Trivially.
A small Python project. This was never in doubt and should not be where effort goes.

**Phase 2 (automatic English + Tamil parser → semantic pipeline): BUILDABLE BUT NOT
TO PUBLISHABLE STANDARD.** The components exist, but two independent facts each
undercut the design doc's §20 milestone:

1. **Accuracy.** Tamil dependency parsing tops out around **LAS 51–62** against
   English's **LAS 88–90**. §3 routes *all* meaning through the parser, so ~40% of
   Tamil dependency arcs are wrong before grammar-role mapping, concept alignment,
   or ontology-gap error is added.
2. **Licensing.** The one Tamil treebank with actual *training data* is
   **CC BY-NC-SA 3.0 — non-commercial**. The commercially-licensed Tamil treebank is
   test-only. This is not a tuning problem; it is a legal constraint on what can be
   shipped and published.

**§20's milestone therefore depends on which claim is being made.** "Two surface forms
can be converted into the same machine-readable representation" is **achievable on
hand-authored simple sentences** — which is what §20 literally asks, and which proves
little. It is **not achievable by an automatic parser at Tamil's current accuracy**
without accepting low fidelity. The gap between those two readings is the single most
important thing on this ticket.

## The English vs Tamil tooling gap

**Verified on disk** (`research/tamil_corpora/ttb_test.conllu`, `mwtt_test.conllu`,
`ud_ttb_license.txt`, `ud_ttb_readme.md`, `pmindia.v1.ta-en.tsv`):

| Fact | Value | Source |
| --- | --- | --- |
| UD_Tamil-TTB test split | 120 sentences, 2,303 tokens | counted on disk |
| UD_Tamil-MWTT test split | 534 sentences, 3,161 tokens | counted on disk |
| UD_Tamil-TTB licence | **CC BY-NC-SA 3.0 (non-commercial)** | `ud_ttb_license.txt`, `ud_ttb_readme.md` |
| UD_Tamil-MWTT licence | **CC BY-SA 4.0 (commercial OK)** | UD treebank page |
| MWTT training data | **none — test-only** | UD docs; only 1 `.conllu` downloaded |
| PMIndia EN–TA pairs | 39,526 lines | counted on disk |

**Transcript-sourced (read by the agent from official accuracy tables, not
re-verified here):**

| Tool / model | Metric | English | Tamil | Gap |
| --- | --- | --- | --- | --- |
| UDPipe 2 (UD 2.17), raw text | LAS | **89.91** (EWT) | **51.33** (TTB) | **−38.6** |
| UDPipe 2, raw text | UAS | 91.59 | 70.38 | −21.2 |
| UDPipe 2, raw text | UPOS | 96.75 | 83.94 | −12.8 |
| Stanza (UD 2.12) | LAS | **87.85** (Talbanken) | **50.97** (TTB) | **−36.9** |
| Stanza | UAS | 90.32 | 58.39 | −31.9 |
| Stanza | UPOS | — | 89.61 | — |

Published reference point: **ThamizhiUDp, LAS 62.39** — reported in
[Sarvabhotla et al. 2020](https://arxiv.org/abs/2012.13436) as "4 points higher than
the current best achieved for Tamil". So the best published Tamil result is ~62 LAS,
and general-purpose stacks land at ~51.

**spaCy has no Tamil model at all** (43rd of its 77 languages is not Tamil). Tamil is
served by Stanza, UDPipe 2, and the Thamizhi toolchain, not by the mainstream
English-first stack.

### The structural problem underneath the accuracy gap

Tamil's low score is not only a data-quantity issue. It is that **the Tamil treebank
with training data is the one that cannot be used commercially**:

- **UD_Tamil-TTB** — has train/dev/test, so a parser can actually be trained. Licensed
  **CC BY-NC-SA 3.0**.
- **UD_Tamil-MWTT** — permissive **CC BY-SA 4.0**, but **test-only**, so no training
  signal.

So an SBL that publishes or ships cannot train on the usable Tamil treebank, and the
treebank it *can* use cannot train a parser. That is a genuine dead end for the
automatic pipeline, independent of accuracy. `spaCy has no Tamil` compounds it: there
is no fallback to a permissively-licensed mainstream model.

## Parallel corpora

**Verified on disk:**

| Corpus | EN–TA size | Licence | Usable? |
| --- | --- | --- | --- |
| PMIndia v1 | **39,526 pairs** (government press releases) | **CC BY 4.0** | **Yes — commercial OK** |
| FLORES-200 | ~1,012 dev + ~1,012 devtest per language | CC BY-SA 4.0 (README); FLORES+ moved to OLDI, **gated** on HF | Yes, but small and gated |
| UD_Tamil-TTB | 120 test sentences | CC BY-NC-SA 3.0 | Non-commercial only |
| UD_Tamil-MWTT | 534 test sentences | CC BY-SA 4.0 | Test-only |

**Transcript-sourced (OPUS/Anuvaad figures read by the agent, not re-verified):**
Anuvaad ~1.4M alignment pairs, CCAligned ~880K, CCMatrix ~7.2M for EN–TA. Samanantar
(AI4Bharat, ~49.6M Indic pairs) is **CC-BY-NC-4.0 — non-commercial**.

**The decisive point about corpora: they are parallel, not semantic.** 39,526 PMIndia
pairs give English sentences and their Tamil translations. They do **not** give
sentence–meaning pairs, which is what Phase 3 of the design doc actually needs. No
amount of parallel text removes the semantic annotation bottleneck. This is the
corpus-side confirmation of the cost finding in
[SBL \| Engineering \| What does it take to reach the final state?](04-what-does-it-take-to-reach-the-final-state.md).

## Build / no-build, component by component

| Stage | Verdict | Binding constraint |
| --- | --- | --- |
| Phase 1 registry / graph / validation / JSON | **Build** | None. Days of work. |
| English parsing | **Build** | None. UD EWT + Stanza/UDPipe at LAS ~88–90. |
| Tamil parsing | **Build with caveats** | LAS ~51–62; **spaCy has no Tamil**; training data is NC-licensed |
| Tamil *semantic* pipeline | **No-build at publishable standard** | Tamil parse error rate ~40%, before semantic mapping |
| Parallel corpus acquisition | **Build** | 39,526 PMIndia pairs under CC BY 4.0 — genuinely usable |
| Sentence–meaning corpus (Phase 3) | **Build is the wrong question** | No off-the-shelf source exists; it is annotation labour, not acquisition |
| Vector layer (Phase 4) | **Build** | None. |
| Small neural model (Phase 5) | **Unassessed** | The agent never reached this; see below. |

## Assumptions this rests on — stated because they are load-bearing

1. **That §20 requires automatic processing.** The design doc does not say the first
   experiment must use an automatic parser. If hand-authored parses are acceptable for
   the first experiment, the Tamil accuracy problem largely disappears from v0.1 and
   reappears as the blocker for scaling — a much better place for it to sit.
2. **That publishing matters.** If SBL is a private research effort,
   CC BY-NC-SA 3.0 on TTB is workable. If it publishes or ships, it is not.
3. **That LAS is the right proxy.** ~40% wrong arcs does not mean ~40% wrong meaning
   for the design doc's simple sentences; short simple sentences may parse much better
   than the treebank average. **This was not established and is the most important gap
   in this report.**

## Incomplete — not yet investigated

**Do not treat the above as a complete answer to this ticket.** Missing:

- **Tamil accuracy on *simple sentences* specifically.** The LAS 51–62 figures are
  treebank-wide averages over news and web text. The design doc's milestone uses
  simple sentences ("The dog eats food"), which may parse far better. **This single
  measurement decides whether Phase 2 is buildable, and nobody has run it yet.**
- **Phase 5 (small neural model) requirements** — never reached.
- **Serialization and graph tooling** — sub-research ran
  (`d4-jsonld-rdf-shacl`, `d4-linguistic-formats`, `d4-ontology-registries` dumps
  exist) but the parent never integrated it.
- **UD → semantics path** — sub-research ran (`d3-ud-to-semantics`) but was not
  integrated. Reported direction: UD→AMR and UD→UCCA tooling exists.
- **ThamizhiMorph / ThamizhiPOSt runnability** — licence and last-commit data were
  being collected from GitHub when the agent stopped. ThamizhiPOSt reported **95.20%
  accuracy** on TTB (ThamizhiPOSt repo, Sept 2020); `thamizhi-udp` had **no LICENSE
  file**, with the GitHub API reporting Apache-2.0 — unresolved.
- **The English–Tamil gap for *pure* English tooling** (e.g. spaCy/Trankit English
  numbers) to complete the comparison table.
- **Whether any Tamil semantic-annotated corpus exists at all** — no source was found,
  but the search was incomplete.

## Confidence

- **Verified on disk by the orchestrator:** all treebank counts, the TTB licence text,
  the PMIndia pair count.
- **Transcript-sourced, not re-verified:** the UDPipe 2 and Stanza accuracy tables, the
  OPUS/Anuvaad/CCAligned/CCMatrix/Samanantar figures, the ThamizhiPOSt 95.20% figure,
  the spaCy-has-no-Tamil claim.
- **Inference, not sourced:** the reading that the accuracy and licensing constraints
  are *independent* blockers; the judgement that parallel corpora do not address the
  semantic annotation bottleneck; the forecast that simple sentences may parse better
  than the treebank average.
- **Absence of evidence, not proof of absence:** "no Tamil semantic-annotated corpus
  exists" rests on an incomplete search.
