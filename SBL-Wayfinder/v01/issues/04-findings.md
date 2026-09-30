# T04 — System and software requirements: findings

Artifact for [`04-system-requirements.md`](04-system-requirements.md). **Status: PARTIAL.**
Research was stopped by time budget before items 3 (most of it) and the human-cost half of item 5
were sourced. Every cell I could not verify says **not established** rather than carrying a guess.
Prices checked **2026-09-30 (UTC)**.

## Requirements summary table

Phase 1's and Phase 5's hardware rows are the contrast the ticket asked for: Phase 1 is a laptop job,
Phase 5 is the only phase with a hard VRAM floor.

| Phase | Software | Hardware | Data | People | Rough cost |
| --- | --- | --- | --- | --- | --- |
| **0** Spec | Markdown + JSON Schema; no runtime | None (any laptop) | §9's seed lists: ~100 concepts, ~30 relationships in the design doc | Computational linguist | **$0 cash**; not established in hours |
| **1** Registry + graph | Python 3; [jsonschema] (schema validation) and [NetworkX] (graph); stdlib JSON. Licences: [jsonschema is MIT], [NetworkX is BSD-3-Clause] | Any laptop; "almost nothing" — no GPU, no dataset | The 100-concept / 30-relationship ontology only | 1 Python engineer (no linguist strictly required) | **~$0** (local CPU) |
| **2** EN + TA parser | [Stanza] (Apache-2.0) for UD parsing; [spaCy] (MIT); UD Tamil treebank for TA; [indic-nlp-library] (MIT), [indic-transliteration] (MIT) for TA normalization | **≥12 GB VRAM** if fine-tuning a BERT-base-class parser — [UDify] states 12+ GB GPU memory and 16+ GB RAM, halves with fp16; CPU-only inference is feasible but slow | UD Tamil TB (TTB): **600 sentences / 8,635 tokens** ([UD treebank page](https://universaldependencies.org/treebanks/ta_ttb/index.html)); UD English-EWT | 1 comp. linguist (EN+TA), 1 engineer | Compute **negligible**; the real cost here is TA linguistic labour with no sourceable rate (**not established**) |
| **3** Dataset 100 / 1k / 10k / 100k | Annotation tooling + the Phase 2 pipeline; [AMR-style] guidance rewritten as an SBL guideline | 100–1k: laptop. 10k–100k: a multi-core workstation; annotation is human-bound, not machine-bound | 100 → 1,000 → 10,000 → 100,000 sentence–meaning pairs; **Tamil must be annotated from scratch** (largest available TA treebank is 600 sentences) | Native/fluent Tamil annotators (plural — see IAA), 1 comp. linguist as adjudicator | **Dominant line item.** See "Where the real cost is" — **$2.5k–15k range estimate** for 1,000 pairs at double annotation |
| **4** Vector layer | [PyTorch] (`Apache-2.0 AND … MIT` per PyPI `license_expression`); [Transformers] (Apache-2.0) | Same GPU class as Phase 5; vectors for ~100 concepts are tiny | The Phase 3 pairs | 1 ML engineer | **< $10** at rented-GPU rates |
| **5** Small neural model | PyTorch + Transformers; baseline (Model A) and SBL (Model B) per design doc §14 | **8–24 GB VRAM.** Grounded floor: BERT-base-class training in [UDify] needed 12+ GB, so 24 GB (RTX 4090 / A10G 24 GB / A100 40 GB) is the safe single-GPU target. [Lambda] lists RTX 6000 24 GB at $0.69/hr and A100 40 GB at $1.99/hr; [RunPod] lists RTX 4090 from $0.34/hr and RTX 5090 from $0.69/hr; [AWS] g5.xlarge (1× A10G, 4 vCPU, 16 GiB) is $1.006/hr on-demand in us-east-1 | Phase 3 pairs at 10k+ before the hierarchy claim is testable | 1 ML engineer (+ comp. linguist for error analysis) | **Compute < $100**; elapsed time **not established** |

## 1. Software stack

| Stage | Recommended | Licence (verified source) | What it trades away |
| --- | --- | --- | --- |
| Parsing (EN) | [Stanza] | Apache-2.0 ([PyPI metadata](https://pypi.org/pypi/stanza/json)) | Neural UD parsers are per-language models; error compounding into the semantic stage (see ticket 01) |
| Parsing (TA) | Stanza's TA model over UD TTB | Apache-2.0; **but** the training data is UD TTB, which is only 600 sentences | Very low-resource: expect materially lower LAS than EN, and no UD treebank scale-up path exists for TA |
| Tokenization/normalization (TA) | [indic-nlp-library], [indic-transliteration] | Both MIT | Less maintained than spaCy; worst for code-mixed text |
| Ontology storage | Plain JSON + JSON Schema ([jsonschema], MIT) or SQLite; RDF/OWL via [rdflib] (BSD-3-Clause) or [owlready2] (licence not verified) if you need description logic | rdflib BSD-3-Clause verified; owlready2 **not established** | RDF buys you reasoners and standard query but imposes triple-store ceremony on a 100-concept ontology where JSON is sufficient — design doc §17 already assumes `ontology.json` |
| Graph | [NetworkX] | BSD-3-Clause | In-memory only; fine for 100 nodes, wrong at millions. A graph DB is unjustified at v0.1 |
| Validation | jsonschema + hand-written constraint tests | MIT | JSON Schema cannot express cross-graph semantic constraints; those need custom code |
| Neural layer | [PyTorch] + [Transformers] | PyTorch `license_expression` = `Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT`; Transformers Apache-2.0 | Nothing material. This is the permissive path; see the copyleft warning below |

**Licence flags for a project that wants to publish.** None of the recommended core components above is
copyleft or non-commercial. Two real cautions: (i) [jsonschema] and [NetworkX] are permissive, but the
widely-used **GPL-licensed** alternatives in ontology tooling (e.g. Protégé-adjacent plugins, some
reasoners) are not interchangeable — check before adopting; I did not verify individual reasoner
licences. (ii) **Data licences are the bigger trap, not code licences.** UD treebanks carry
per-treebank licences that are *not* uniformly CC-licensed, and the AMR sembanks are sold through
[LDC](https://catalog.ldc.upenn.edu/LDC2020T02) under a restrictive user agreement. Publishing an SBL
dataset derived from either needs per-resource licence review. I did not complete that review.

## 2. System requirements per phase

| Phase | CPU | RAM | GPU / VRAM | Disk |
| --- | --- | --- | --- | --- |
| 0–1 | Any (2 cores) — *estimate* | 4–8 GB — *estimate* | **None needed** | < 10 MB — *estimate* |
| 2 | 4+ cores ([AWS] g5.xlarge ships 4 vCPU / 16 GiB with 1× A10G at $1.006/hr) | **16+ GB** to fine-tune ([UDify]) | **12+ GB VRAM** to fine-tune BERT-base-class ([UDify]); CPU-only for inference | UD treebanks on disk: small (TTB is 600 sentences); Stanza model downloads are hundreds of MB — *estimate* |
| 3 (100–1,000) | Any laptop | 8–16 GB | None | < 100 MB of JSON — *estimate* |
| 3 (10k–100k) | 8+ cores | 16–32 GB | None | 100k sentence–meaning pairs as JSON: low GB — *estimate* |
| 4 | 4+ cores | 16 GB | 8–24 GB VRAM | Vector files for 100 concepts: trivial |
| 5 | 4+ cores | 16–32 GB | **8–24 GB VRAM; 24 GB is the safe target** | Checkpoints: GB-scale — *estimate* |

The strongest sourced anchor is [UDify]: fine-tuning multilingual BERT for UD needed **16+ GB RAM and
12+ GB GPU memory**, halving with fp16, and **20+ days for the full multilingual 80-epoch run** over
124 treebanks. SBL's single-treebank, single-domain case is far smaller — but this is the published
figure that sets the floor for "fine-tune a parser", and it is the reason not to specify less than
12 GB VRAM. The **elapsed-time** analogue for SBL's Phase 5 is **not established**.

## 3. Data requirements

Verified: [AMR 3.0](https://catalog.ldc.upenn.edu/LDC2020T02) contains **over 59,255 sentences** of
English semantic annotation — the field's scale reference for a semantic bank. [UD Tamil TTB] contains
**600 sentences / 8,635 tokens**, and its own README records that it was produced by a rule-based
parser **then manually corrected**, which is a directly relevant precedent for bootstrapping SBL's Tamil
side: pre-annotate automatically, correct by hand. *(Sourcing note: I verified the 600/8,635 figures
from the [UD treebank page]; the README quote was observed earlier in the session and I did not re-verify
the exact line — treat the quote as provisional.)*

Gaps: sentences needed for statistical meaning per experiment, person-hours per 1,000 pairs, and
**inter-annotator agreement figures for AMR/UD/PropBank are all not established.** I did not reach
the Smatch-based IAA primary source, so I make no IAA claim. This matters because it determines
annotator count: the field's practice of double-annotation plus adjudication (the AMR consensus
annotation programme is funded and documented at LDC) means **per-sentence cost is a multiple of one
annotator's time**, and I have not verified the multiplier.

## 4. Human and skill requirements

- **Computational linguist**: owns Phase 0 (ID/relationship/category design), the grammar-role mapping
  in Phase 2, the SBL annotation guideline in Phase 3, and adjudication at every phase.
- **Tamil annotator**: Phase 2 validation and all of Phase 3. This is the hard constraint — the Tamil
  data does not exist at scale ([UD Tamil TTB] is 600 sentences), so it must be created. Native or
  fluent speakers only; this is a hiring constraint, not a preference, and it gates schedule.
- **ML engineer**: Phases 1, 4, 5 (and the pipeline code in 2).

Per-phase hour loads: **not established.** I did not source a rate card or booking model for either role.

## 5. Cost and time — partial

Compute, based on the verified rates above: Phase 1 is ~$0 (laptop). Phases 2 and 5 on a rented single
GPU are **order $10–$100 total** — a Phase 5 experiment of ~20–60 GPU-hours is **$7–$42** at
[RunPod]'s RTX 4090 rate ($0.34–0.69/hr) or **$20–$120** at [Lambda]'s RTX 6000 rate ($0.69/hr).
*Those GPU-hour counts are my estimate; the rates are sourced.* Elapsed time: **not established.**

## Where the real cost is

**Human annotation, by two to three orders of magnitude.** Reaching §20 needs only ~100 sentence–meaning
pairs; Phase 3's ladder to 100,000 dominates everything else. My rough model: 15–30 minutes per
sentence–meaning pair under a 100-concept ontology with a written guideline — *estimate, unsourced* —
gives **250–500 annotator-hours per 1,000 pairs**, and **500–1,000 hours at double annotation**. Even at
a deliberately conservative $5–15/hour for a Tamil-speaking annotator, that is **$2,500–$15,000 for
1,000 pairs**, and roughly **$250–$1,500 for §20's 100 pairs**. The same 1,000 pairs cost under $5 of
GPU time. Every compute line in this document is a rounding error against annotation labour; if the
budget is real, spend it on guideline quality and annotator retention, not on GPUs.

**Rough total to reach §20 (100 concepts, ~30 relationships, EN+TA, simple sentences): ~$300–$1,600,
overwhelmingly annotation labour, with compute under $10.** *Range estimate built on one unsourced
pace assumption; the compute component is sourced.*

## Incomplete — not yet investigated

1. **Item 3, most of it**: statistically-meaningful sample sizes; sourced person-hours for 1,000 pairs;
   real AMR/UD/PropBank inter-annotator agreement figures (Smatch-based or otherwise) and what they imply
   for annotator count. I did not reach the IAA primary sources before the stop.
2. **Item 4**: per-phase hour loads and role cost. No rate source reached.
3. **Item 5**: elapsed time to §20 and to Phase 5; any annotation rate card; the LDC AMR licence fee
   (the catalogue page is paywalled and I did not retrieve the price).
4. **Item 1**: licence verification for `owlready2` and any OWL reasoner, and the per-treebank UD
   corpus licences.

## Confidence

| Number | Status |
| --- | --- |
| UDify 12+ GB VRAM / 16+ GB RAM / 20+ days | **Primary-source verified** ([UDify README](https://github.com/Hyperparticle/udify)) |
| AWS g5.xlarge $1.006/hr, g4dn.xlarge $0.526/hr, p3.2xlarge $3.16/hr, g6.xlarge $0.94288/hr | **Primary-source verified** (AWS EC2 pricing API, us-east-1, checked 2026-09-30) |
| Lambda A100 40 GB $1.99/hr, RTX 6000 24 GB $0.69/hr, A100 80 GB $2.79/hr, V100 16 GB $0.79/hr | **Primary-source verified** ([lambda.ai/pricing](https://lambda.ai/pricing)) |
| RunPod RTX 4090 $0.34/hr, RTX 5090 $0.69/hr, A6000 $0.33/hr, L40S $0.79/hr | **Primary-source verified** ([runpod.io/pricing](https://www.runpod.io/pricing)) |
| AMR 3.0 > 59,255 sentences | **Primary-source verified** ([LDC2020T02](https://catalog.ldc.upenn.edu/LDC2020T02)) |
| UD Tamil TTB 600 sentences / 8,635 tokens / 9,581 syntactic words | **Primary-source verified** ([UD](https://universaldependencies.org/treebanks/ta_ttb/index.html)) |
| All component licences in the table | **Primary-source verified** (PyPI JSON metadata, checked 2026-09-30) |
| GPU-hours for Phase 5 (20–60 h); disk sizes; CPU/RAM for Phases 0–1 | **Estimate** |
| Annotation pace 15–30 min/pair; $5–15/hr; double annotation | **Estimate, unsourced** — the weakest link in the cost model |
| 100–1,000 sentence counts per Phase 3 rung | **Cited as the design doc's own ladder**, not a statistical claim |
| Sample sizes; IAA figures; elapsed time; annotator count | **Not established — no claim made** |
