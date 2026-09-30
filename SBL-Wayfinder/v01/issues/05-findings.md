# T05 — Interoperability feasibility: findings (PARTIAL)

Artifact for [05-interoperability-feasibility.md](05-interoperability-feasibility.md).
**Status: partial — research budget expired mid-investigation.** Four of the
numbered questions are answered only in part; Q3's vendor side and the
failure cases are essentially unmined. See *Incomplete* and *Confidence*.

---

## Headline: minimum conditions for the interoperability claim

SBL's interoperability claim (§7: Model A → SBL → Model B) becomes credible
**only if all six hold simultaneously**:

1. **A second, independent party emits SBL structures.** Not consumes — *emits*.
   A spec plus a reference implementation is not adoption.
2. **That party gains something it cannot get from its own representation.**
   Every verified success below paid the adopter at the point of use
   (search ranking, retail checkout, rendering text). No verified success
   was adopted for the good of the commons.
3. **The semantic granularity is settled by an authority, not by measurement.**
   Where identity is contested, the standard must impose a decision and
   deprecate gracefully.
4. **Cost of adoption is lower than the cost of the dominant alternative** —
   including zero cost of doing nothing.
5. **An adopter with a distribution channel absorbs the cost** (§19's
   sponsor role) or **the standard is a precondition of a transaction**
   (a mandate, formal or de-facto).
6. **Emission is lossless enough** that round-tripping through SBL does not
   degrade the adopter's own product.

### Is the claim testable at target scale? **No — not as currently scoped.**

At §20's scale (100 concepts, 30 relationships, English + Tamil), the claim is
**unfalsifiable in principle, not merely untested.** The claim is a property of
*independent adopters*, and at 100 concepts the only emitter is the SBL project
itself. One party emitting a format is a serialization choice, not
interoperability. Condition 1 cannot be satisfied by anything SBL does at v0.1;
it requires an outside actor whose participation SBL cannot compel. This is the
circularity the ticket predicted: **the interoperability claim only becomes
observable at a scale SBL must reach before it can be tested.** Any v0.1 result
(success or failure on the 100-concept benchmark) is *silent* on §7.

---

## Q1 — Adoption mechanisms

### The adoption-mechanism table

| Standard | What actually drove adoption | Does SBL have an equivalent forcing function? |
|---|---|---|
| **schema.org** | Three of the largest search engines (Google, Bing, Yahoo!) jointly announced it on 2 Jun 2011 and folded their *competing* rich-snippet schemas into one vocabulary. The adopter's payoff was ranking/display in search results — a private, immediate, measurable benefit. As the announcement puts it: "adding markup is much harder if every search engine asks for data in a different way." ([archived founding announcement](https://web.archive.org/web/20110604000000/http://googleblog.blogspot.com/2011/06/introducing-schemaorg-search-engines.html)) | **No.** SBL has no distribution channel to withhold. schema.org worked because the consolidating sponsors *owned the market* the adopter wanted access to. |
| **Unicode** | Consolidation of many incompatible vendor encodings, driven by a small founding coalition (Xerox/Apple engineers from 1987) that then recruited competitors: Metaphor, RLG and Sun in early 1989; Microsoft in early 1990; IBM in mid-1990. Critically, they **absorbed the switching cost themselves** by writing mapping tables to every rival standard, and moved the encoding *toward* the incumbents' behaviour ("all existing ISO composite characters were added… ordering was changed to use ISO 8859 ordering where possible"). ([Unicode history summary](https://www.unicode.org/history/summary.html)) Formally incorporated 3 Jan 1991; synchronized code-for-code with ISO/IEC 10646 ([Unicode Consortium history](https://www.unicode.org/history/)) | **Partially — mechanism only, not the resource.** The mechanism (founder pays all mapping costs; concede to incumbents to reduce their cost to zero) *is* transferable to SBL. The resource — a decade of funded engineering plus an ISO committee to ratify into — is not. |
| **Wikidata** | Not network economics: **philanthropic funding** (Allen Institute for AI, Gordon and Betty Moore Foundation, Google; ~€1.3M) plus a Wikimedia chapter to operate it. Its initial job was not open data — it was **fixing a specific operational pain**: centralizing interlanguage links and infobox data that each Wikipedia was maintaining redundantly. Launched 29 Oct 2012, language links first, English Wikipedia switched 13 Feb 2013. ([Wikidata](https://en.wikipedia.org/wiki/Wikidata)) | **No.** SBL has neither a funder of that class nor an existing operational pain of comparable sharpness. |
| **GS1 / UPC barcode** | **Industry self-mandate.** The US retail industry formed the *Ad Hoc Committee for a Uniform Grocery Product Identification Code* in 1969; UPC was selected in 1973 and the Uniform Code Council founded in 1974 to administer it; the first scan was 26 Jun 1974. Adoption was compelled by the retail channel, not by the code's elegance. ([GS1](https://en.wikipedia.org/wiki/GS1)) | **No — the closest structural analogue and the least available.** UPC's forcing function was that retailers refused to buy unbarcoded goods. SBL has no transaction to gate. |
| **Dublin Core** | A 1995 invitational workshop (OCLC + NCSA, Dublin, Ohio), then a **long, slow path through formal standards bodies**: RFC 2413 (1998), ANSI/NISO Z39.85 (2001), ISO 15836-1:2017, ISO 15836-2:2019. Its design choice for adoptability was **deliberate lossiness** — the "Dumb-Down Principle": an application that does not understand a refinement ignores the qualifier and treats the value as the broader element. ([Dublin Core](https://en.wikipedia.org/wiki/Dublin_Core)) | **Partially — and this is the most transferable design lesson.** SBL's contested-granularity problem (Q2) is exactly what Dumb-Down solves: *permit* under-specification and require degradation to be safe. SBL's spec currently has no equivalent clause. |
| **ISO 639** | **Institutional drag, not adoption pull.** First approved 1967 as ISO/R 639 to regulate ISO's own vocabularies, countries and agencies — internal convenience. Grew through RFC 1766 into web infrastructure; the codesets are now maintained by third parties (Library of Congress for 639-2, SIL International for 639-3) rather than by ISO. ([ISO 639](https://en.wikipedia.org/wiki/ISO_639)) | **Weakly — the mirror image.** ISO 639 shows a standard surviving by being *cheap to use*, not by being enforced. Cheapness is a real SBL lever; it is not a forcing function. |
| **ONNX** | Two competitors (Facebook, Microsoft) co-founded it in Sept 2017, then recruited IBM, Huawei, Intel, AMD, Arm and Qualcomm; Microsoft added Cognitive Toolkit and Project Brainwave in Oct 2017. It won where it was **narrow**: the spec covers *inference* computation graphs only, "the capabilities needed for inferencing (scoring)". Governance was moved to an open structure and it is now an **LF AI graduate project** with SIGs, working groups and a steering committee. ([ONNX README](https://github.com/onnx/onnx), [onnx.ai](https://onnx.ai/), [ONNX](https://en.wikipedia.org/wiki/Open_Neural_Network_Exchange)) | **Partially — the closest genuine precedent, and it argues for narrowing, not for §19.** See Q3. |
| **safetensors** | Adopted on a **concrete, non-ideological defect**: pickle — the incumbent — executes arbitrary code on load. Value proposition is "safely (as opposed to pickle) and that is still fast (zero-copy)." Sponsored by one dominant distribution channel (Hugging Face). ([safetensors README](https://github.com/huggingface/safetensors)) | **Partially — the mechanism is available.** "The alternative is unsafe" is a forcing function SBL could borrow, but only if SBL's absence causes an *observable failure*, which at 100 concepts it does not. |
| **RDF / OWL / Semantic Web** | **Adoption failed at the layer that mattered.** The W3C Semantic Web Activity statement now reads: "October 2013 — Work conducted under the Semantic Web Activity has ended or is now nearing the end of its charter." Despite the W3C's own framing that "tomorrow's programs must be able to share and process data even when these programs have been designed totally independently." ([W3C Semantic Web Activity](https://www.w3.org/2001/sw/Activity)) | **No — and this is the negative precedent that most resembles SBL.** A well-funded, spec-complete, W3C-blessed, model-independent semantic layer with exactly SBL's stated rationale ended its activity after ~12 years without becoming the interchange medium. |

### Mechanisms, generalised

Four forcing functions appear in the successes: **distribution control**
(schema.org, GS1), **a defect in the incumbent** (safetensors), **a funder
paying the switching cost** (Unicode, Wikidata), and **internal operational
pain** (Wikidata's interlanguage links, ISO 639's own vocabulary). SBL has none
of them at v0.1. The unsuccessful end of the spectrum —
RDF/OWL's stalled Semantic Web — had the *strongest* technical case and no
forcing function, which is the single most instructive data point here.

---

## Q2 — Where the GPS analogy breaks

**What survives.** Only the weak half: a shared identifier permits a
representation produced by party A to be *parsed* by party B without a
negotiation between their internal vector spaces (design doc §7). That is real
and is exactly what ONNX demonstrates for computation graphs — a common
*container* meaning is genuinely portable.

**What breaks.** The analogy's load-bearing claim is that semantic identity is
like a coordinate: physical, measurable, lossless. It is none of those.

- GPS coordinates are **physical** — latitude is fixed by the geoid, not by
  committee. `CONCEPT:C0001` is fixed by whoever edits `ontology.json`.
- GPS is **lossless** — no information about a location is destroyed by
  recording it to arbitrary precision. Semantic identity destroys information
  at every level: is `CAT` the species, the domestic animal, the taxon, the
  colloquial pet, the Unicode emoji? No measurement adjudicates this.
- GPS adoption required **no coordination among adopters** — Receiver A and
  Receiver B each benefit from the frame *individually*. SBL only pays off
  when the *other* party has adopted it, which is the definition of a
  coordination game with a low-value equilibrium.
- GPS had a **forcing function SBL lacks**: government funded, deployed, and
  then mandated the constellation and made the signal a public good. The
  §1 claim that "GPS works because locations share a coordinate system" is
  therefore **inverted**: locations share a coordinate system because GPS was
  centrally imposed. The coordinate system is the *output* of the mandate,
  not its cause. **§1's analogy, stated as a causal claim, does not survive.**

**The precise surviving claim:** a shared *syntax* for semantic structures is
adoptable exactly as ONNX's shared syntax for computation graphs was. A shared
*semantics* — SBL's actual novelty (§16) — is contested at the level where
adoption decisions are made, and Dublin Core's Dumb-Down Principle is the only
verified precedent for handling that: require the standard to be *safe to
under-interpret*, rather than correct.

---

## Q3 — The interoperability incentive problem

**What was verified.** ONNX is the strongest precedent *for*: two direct
competitors co-founded a shared model-graph representation in Sept 2017 and
recruited five more silicon and platform vendors within a month, and it is
still governed as an LF AI graduate project with open governance, SIGs and
working groups ([ONNX README](https://github.com/onnx/onnx), [ONNX](https://en.wikipedia.org/wiki/Open_Neural_Network_Exchange)).
Note what ONNX was *not*: it was not a shared *meaning* space and it did not
touch model weights, tokenizers, or training. It standardized the boundary of
an artifact that vendors were already being forced to move between frameworks,
and it paid off for hardware vendors (ONNX's own [hardware-access pitch](https://onnx.ai/))
more than for model vendors.

**What was not established.** The adversarial half — vendors deliberately
defending proprietary representation as a moat — was **not researched to
primary sources.** I saved vendor embedding documentation (OpenAI, Gemini,
Mistral, Cohere) expecting to find explicit statements that embedding vectors
are not portable between models, but did not extract quotable claims before
budget expired, so **no moat claim is asserted here.** Treat "embeddings are a
moat" as an untested hypothesis. Likewise the "AI winter of the semantic web"
literature (Shirky et al.) and ONNX's governance charter text were not
retrieved; my ONNX governance facts come from the project's own README and
homepage, not from its charter.

**What the evidence supports without further research.** The one directly
analogous failure is documented: the W3C ran a Semantic Web Activity with
SBL's exact rationale and it ended in October 2013
([W3C](https://www.w3.org/2001/sw/Activity)). Any argument that SBL's
interoperability layer will be adopted must explain why it succeeds where a
decade of W3C-blessed, vendor-funded ontology work did not — and the
verifiable difference (ONNX-style narrow scope, a concrete incumbent defect,
or a channel owner paying) is not yet present in SBL.

---

## Q4 — Switching cost

**Verified structurally, not quantitatively.** The cost profile is asymmetric
and unfavourable at v0.1, by direct comparison with the precedents:

- An adopter emitting SBL structures pays a **translation cost in both
  directions** and gains a benefit only if a counterparty also emits SBL.
  Every verified success avoided this: schema.org adopters paid once for a
  ranking benefit they received that same day; UPC adopters were *told* to.
- SBL adds a hop between model and output. Unicode's history shows the
  generator of a format must **pay the mapping cost for everyone else**
  ([Unicode history](https://www.unicode.org/history/summary.html)); SBL as
  scoped has no mechanism to do so.
- At 100 concepts and 30 relationships, **no adopter with an independent
  representation exists.** A party whose whole concept inventory is 100 items
  has no interoperability problem worth solving, and a party with a real one
  (a frontier model vendor) has an inventory orders of magnitude larger and a
  mapping cost proportional to it. The §20 scale is *below the threshold at
  which the problem SBL solves exists*, and §19 scale is *above the threshold
  at which SBL can fund the mapping*. That gap, not any technical defect, is
  the central finding.

**Honest verdict on §20 scale:** the 100-concept experiment remains a valid
test of the *scientific* and *engineering* hypotheses (T01, T03). It cannot
test interoperability, and it should not be reported as if it did.

---

## Incomplete — not yet investigated

1. **Q1 failures.** No unsuccessful/abandoned standards were studied from
   primary sources. The most instructive data in the ticket is **missing**.
   Specifically unexamined: microformats vs. RDFa vs. JSON-LD competition
   under schema.org, FOAF/DOAP/SIOC abandonment, ISO 639-6 (withdrawn),
   ICD-9→ICD-10 migration lags, LOINC adoption friction in US labs.
2. **Q3 vendor side.** No primary evidence on vendors defending proprietary
   representation as a moat: model weights, tokenizers, embedding APIs
   (docs saved in `.sbl-05-scratch/`: `openai_emb_guide.html`,
   `gemini_emb.html`, `mistral_emb.html`, `cohere_emb.html` — **unmined**),
   or ranking signals.
3. **Q3 semantic-web critique literature.** Shirky's "Semantic Web, XML, and
   Web Services" and the surrounding "AI winter of the semantic web" debate
   were not retrieved. Only the W3C's own end-of-activity statement is cited.
4. **Q3 ONNX governance detail.** The ONNX governance charter, steering
   committee composition, and adoption/share numbers were not retrieved; two
   attempted URLs 404'd (`GOVERNANCE.md`, `community/steering-committee.md`).
5. **Q4 quantification.** No latency or fidelity measurements, and no
   §20-scale cost model. The argument above is structural.
6. **ICD, LOINC, GS1 primary documents.** ICD and LOINC pages were fetched
   but not mined to quotable claims; the GS1 history page returned HTTP 403
   and the facts cited come from Wikipedia, **not** from GS1 directly.

---

## Confidence

| Finding | Status |
|---|---|
| schema.org was driven by three search engines consolidating competing schemas for a ranking payoff; quoted text | **Primary-source verified** — archived 2011 founding announcement |
| Unicode absorbed rivals' switching costs by writing mapping tables and conceding to ISO 8859 ordering; recruited Microsoft/IBM; incorporated Jan 1991 | **Primary-source verified** — unicode.org history summary |
| W3C Semantic Web Activity ended ~October 2013; quoted "designed totally independently" framing | **Primary-source verified** — w3.org activity statement |
| Wikidata: ~€1.3M from AI2/Moore/Google; launched 29 Oct 2012; interlanguage links first; English Wikipedia 13 Feb 2013 | **Partially verified** — Wikipedia, which cites Wikidata-l and Wikimedia Deutschland primary sources; I did not open those |
| ONNX: Sept 2017 founding by Facebook + Microsoft; IBM/Huawei/Intel/AMD/Arm/Qualcomm support; inference-only scope; LF AI graduate project; open governance with SIGs/WGs | **Partially verified** — ONNX's own README and homepage (primary) for scope, governance and LF AI status; founding dates and vendor list from Wikipedia citing the 2017 Microsoft announcement, which itself 404'd |
| Dublin Core "Dumb-Down Principle"; 1995 OCLC/NCSA workshop; RFC 2413 → ISO 15836 | **Partially verified** — Wikipedia, citing DCMI documents; the DCMI JISC paper itself not retrieved |
| ISO 639: 1967 as ISO/R 639 for ISO's internal vocabulary; 639-2 held by LoC, 639-3 by SIL; 639-6 withdrawn | **Partially verified** — Wikipedia citing ISO and SIL |
| GS1/UPC: 1969 ad hoc committee, 1973 UPC selected, 1974 UCC founded, first scan 26 Jun 1974 | **Partially verified** — Wikipedia; gs1.org returned HTTP 403 |
| safetensors' value proposition is pickle's arbitrary-code-execution risk plus zero-copy | **Primary-source verified** — safetensors README |
| GPS analogy's causal claim is inverted (§1 does not survive as stated) | **My inference** — argued from the structures above; no GPS primary source was retrieved |
| The interoperability claim is unfalsifiable at 100-concept scale | **My inference**, but a logical one: it follows from "the claim is about independent adopters" plus "at v0.1 there is one party" |
| SBL has no forcing function equivalent to any verified success | **My inference** from the table above; would strengthen with the Q1 failure cases |
| Vendors defend embeddings as a moat | **UNVERIFIED — explicitly not asserted** |

## Method note

`web_search` timed out on every call this session and DuckDuckGo/Mojeek
returned bot challenges; sourcing was done by direct `curl` to known primary
URLs plus a Bing HTML scrape. Pages saved under
`.sbl-05-scratch/` (raw HTML plus `h2t.py`, an HTML-to-text helper) for
re-verification; that directory is working scratch, not part of the map.
