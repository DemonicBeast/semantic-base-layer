# SBL — High-Level Reconnaissance Scan

**Status: preliminary.** Written from model knowledge on 2025-10-01, in parallel with
the five deep investigations. **Nothing here is primary-source verified.** Treat every
claim as a hypothesis with an owner ticket that will confirm, sharpen, or overturn it.
Where a claim is uncertain I say so; where I am confident from well-established
literature I say that too, so you can calibrate which parts to trust before the deep
research lands.

---

## 1. The one-page version

| Axis | Read | Confidence |
| --- | --- | --- |
| **Engineering feasibility** | High. Every component exists today. Nothing needs inventing. | High |
| **Scientific novelty** | Low to moderate. A recombination of existing parts, not a new mechanism. | High |
| **Scientific validity of the core claim** | Mixed. One claim is nearly certain to "pass" and prove nothing; the interesting claim is untested. | Medium |
| **Adoption / interoperability** | Very low. Unfalsifiable at the design doc's own target scale. | High |
| **Cost driver** | Human semantic annotation, not compute. | High |
| **Biggest risk** | Not technical. It is that the milestone succeeds and nothing follows. | High |

**Blunt summary:** SBL is a well-formed research concept whose central architectural
insight — separate stable semantic identity from unstable learned vectors — is
genuinely sound, already standard practice in parts of the field, and *not* the part
that is hard. The hard part is coverage, and the design doc's target scale is three
orders of magnitude below where coverage starts to matter. The proposal is buildable;
the open question is whether it is *useful*, and the design doc's own first milestone
is not designed to answer that.

---

## 2. Feasibility, on the three axes you ranked

### (b) Scientific — mixed, and this is where the project lives or dies

- **Compositional generalization (design doc §13).** The literature here is large and
  I am confident in its shape: neural sequence models systematically fail at
  compositional generalization on SCAN and COGS, while systems with explicit
  compositional structure tend to do much better on those specific benchmarks. So
  §13's hypothesis is plausible — but that cuts *against* the novelty claim. If
  explicit structure helps, that is already known and already exploited by
  grammar-based and AMR-based systems.
- **Hierarchical prediction (§6).** This is the weakest claim in the document.
  Hierarchical softmax is a classic technique and its benefit is primarily at
  **training** time; at inference you still have to score candidates, and a
  category→concept→token cascade can cost *more* if the hierarchy is mispredicted
  early. The design doc itself hedges ("a research hypothesis, not yet a proven
  computational advantage"), which is honest — but it means the efficiency story
  should not be relied on to justify the project.
- **Symbolic interlingua (§5, §12, §20).** The interlingua debate in machine
  translation is decades old, and the historical verdict is that fully symbolic
  interlinguas were abandoned in favour of statistical and then neural methods —
  largely for coverage reasons, not for lack of elegance. SBL is proposing a
  *bounded* interlingua rather than a universal one, which is the defensible version,
  but the design doc's framing (§19's universal grammar) reaches past what the
  evidence supports.
- **Error compounding.** SBL routes all meaning through a parser. Published AMR and
  UD parsing accuracies mean the layer inherits a substantial error floor before any
  of its own machinery runs. Whether that floor is acceptable at 100 concepts is
  exactly what deep ticket
  [SBL \| Engineering \| Can the first milestone be built with tools that exist?](03-can-the-first-milestone-be-built-with-tools-that-exist.md)
  must quantify.

### (a) Engineering — high, and this is the least interesting axis

Every stage has an existing component: UD and stanza/spaCy/UDPipe for parsing,
existing treebanks and parallel corpora for data, networkx or an RDF store for the
graph, JSON Schema or JSON-LD for the wire format, standard tooling for the vector
layer. Phase 1 (registry, graph, validation, JSON) is a small Python project measured
in days, not months. **Nothing in the pipeline needs to be invented**, which means
engineering feasibility will not be the reason this project fails. Do not spend much
more time on this axis.

The one genuine engineering gap: the design doc assumes parser → grammar → semantics
is a clean cascade, but the **syntactic-to-semantic mapping is the hard part** and is
barely specified. §4.1 lists POS tags; §9 lists relations; nothing maps between them.
That is where the real work is, and it is currently a blank in the document.

### (c) Interoperability — very low, and structurally unfalsifiable

Model A → SBL → Model B only has value if independent parties emit SBL. The design
doc's target is 100 concepts. No vendor emits a 100-concept ontology, and the
incentive to adopt a shared semantic space is *negative* for anyone whose proprietary
representation is a moat. Two further structural problems:

1. **Two-hop translation is lossy.** Going A → SBL → B loses whatever A encoded that
   SBL cannot express. The narrower the ontology, the more is lost. This is the
   interlingua coverage problem in a different costume.
2. **Modern models may make it unnecessary.** Capable LLMs already map between natural
   languages and between representations directly and reasonably well. SBL's pitch is
   partly that this is hard and needs a structural fix; for a growing set of tasks,
   it demonstrably is not that hard anymore. Your deep ticket
   [SBL \| Research \| Would anyone adopt a shared semantic ID space?](05-would-anyone-adopt-a-shared-semantic-id-space.md)
   should test whether the layering buys anything a good multilingual model does not
   already do.

Per the map's own scope decision, this axis only *informs design*. Confirmed: it does
not gate anything at v0.1 — which also means it cannot be the thing that makes v0.1
worth doing.

---

## 3. Prior art: the landscape at a glance

Full census is in
[SBL \| Research \| Does this already exist, and where is it used?](02-does-this-already-exist.md).
The shape, at high level — the pieces of SBL all exist separately:

| Piece of SBL | What already owns it |
| --- | --- |
| Grammar layer (§4.1) | Universal Dependencies, Penn Treebank tags |
| Semantic graph (§10) | AMR, UMR, UCCA |
| Concept identity + hierarchy (§4.2) | WordNet, BabelNet, SUMO, Wikidata |
| Relationship inventory (§4.3) | ConceptNet, FrameNet, PropBank, VerbNet |
| Context/disambiguation (§4.4) | Word-sense disambiguation, AMR sense annotation |
| Cross-lingual alignment (§12) | UMR explicitly, multilingual WordNet, BabelNet |
| Program semantics (§11) | ASTs, IRs, LLVM IR, language servers |
| Model interchange (§7) | ONNX (for graphs), tool/schema protocols |

**The novelty is the combination, and §16 admits this.** The interesting question is
therefore not "is this new?" but "does the combination produce a capability none of
the parts has?" — and that is exactly what the first experiment should test, which is
why ticket
[SBL \| Decision \| Which experiment runs first, and what counts as success?](09-which-experiment-runs-first-and-what-counts-as-success.md)
is the highest-leverage decision on the board.

The single most direct threat to novelty is **UMR (Uniform Meaning Representation)**:
multilingual, cross-lingual, semantically explicit, with an existing annotation
vocabulary. If UMR already occupies the niche, SBL's contribution collapses to a
format choice. Your deep research must establish this precisely.

---

## 4. Requirements, at high level

Full inventory in
[SBL \| Engineering \| What does it take to reach the final state?](04-what-does-it-take-to-reach-the-final-state.md).

- **Software:** unremarkable. Python, an existing parser stack, a graph library, JSON
  Schema. Permissive licences are available throughout; the risk is corpus licences,
  not library licences.
- **System:** Phase 1 is a laptop. Phase 2 is a laptop. Phase 5 (a small trained
  model) wants a single GPU. Compute is *not* the constraint at this scale.
- **People:** this is the real constraint. Tamil annotation requires native or fluent
  speakers, and semantic annotation is skilled work.
- **Cost driver:** annotation. Order-of-magnitude, a 1,000-sentence
  sentence–meaning-pair set is plausibly weeks of skilled annotator time, and the
  design doc's roadmap runs to 100,000. Naively extrapolated that is a multi
  person-year annotation program — plausible for a funded lab, not for a solo effort.
- **The gap that matters:** building the *representation* is cheap. Filling it with
  *content* is not, and coverage is what decides whether the layer is useful.

---

## 5. The three fatal risks

1. **Coverage collapse.** 100 concepts covers a toy slice of language. At that scale
   SBL cannot demonstrate usefulness, and at the scale where it could, annotation cost
   is prohibitive. This is the central unsolved problem, and it is a *cost* problem,
   not a design problem — no architectural improvement makes annotation cheap.
2. **The milestone proves nothing.** §20 asks whether two surface forms can map to one
   structure. Given a hand-built ontology and simple sentences, the answer is
   essentially certain to be yes. Success will feel like validation while
   demonstrating almost nothing about whether the layer is *useful*. This is the
   project's biggest risk precisely because it looks like progress.
3. **Wrong problem, or a problem that shrank.** The value proposition is
   interoperability between models that do not share representations. Modern
   multilingual and multimodal models have been steadily eroding the need for a
   hand-specified layer between them. The project could be building a bridge to an
   island that is being connected by other means.

---

## 6. What I would do next (a reframe, offered as a decision input)

The design doc's scope is the source of most of its risk. Narrowing it would raise the
information gained per unit of effort sharply:

1. **Drop §19's universal framing from the map's destination.** It is fog, correctly
   parked on the map. Requirements should target §20 only, as the map's Notes already
   say.
2. **Replace §20's first experiment with a falsifiable one.** The question worth
   answering is not "can two sentences map to one structure?" but something like:
   *"does a fixed 100-concept ontology improve cross-lingual compositional
   generalization over a small multilingual baseline, at equal or lower compute?"*
   That experiment can fail, which is what makes it worth running.
3. **Fix the falsification condition before running anything**, which is exactly what
   ticket
   [SBL \| Decision \| Which experiment runs first, and what counts as success?](09-which-experiment-runs-first-and-what-counts-as-success.md)
   exists to do.
4. **If interoperability is the real goal, bootstrap it on a controlled domain** —
   agent tool schemas, a DSL, a compliance rulebook — where the ontology can be
   complete by construction and adoption does not require the world to agree on
   semantics. Universal scope is what makes the adoption problem unsolvable;
   domain scope makes it tractable.
5. **Consider that the most publishable output may be the negative or bounded
   result** — "here is precisely how far a 100-concept semantic layer gets you, and
   where it breaks." That is real knowledge and it is achievable.

None of this is a reason to stop. It is a reason to aim the first experiment at
something that can come back negative.
