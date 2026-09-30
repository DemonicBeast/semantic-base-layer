# T01 — Scientific feasibility: is SBL's hypothesis already falsified?

**Status of this artifact: PARTIAL.** Research was cut short by time budget. Questions 1, 3
and 4 were investigated substantially; Question 2 only partially. See
"Incomplete — not yet investigated" at the end for exactly what is missing.

**Verdict.** SBL is not falsified as a *representation* — a compact shared semantic
address space with language-independent IDs demonstrably exists in published, funded,
multi-year work (Uniform Meaning Representation, [UMR](https://arxiv.org/abs/2502.11968)),
so the design doc's §5/§12/§20 claim that two surface languages can resolve to one shared
structure is **not** speculative. What the evidence *does* contradict is narrower and more
damaging: the two claimed *mechanisms* — that a fixed symbolic ontology delivers
compositional generalization (§13), and that hierarchical category→concept prediction
saves computation (§6) — are each undercut by primary sources. Compositional
generalization in this exact setting has been shown to be a property of the *training
distribution* and the *surface form of the meaning representation*, not of whether the
representation is symbolic or compositional, and the benchmark that the design doc's §13
experiment is modelled on (COGS) was itself shown to be measuring incidental
representation details rather than semantic interpretation. Separately, the pipeline's
grammar layer has a hard published accuracy ceiling that compounds: Tamil's
state-of-the-art UDParser reports **LAS 62.39**, which alone caps end-to-end semantic
fidelity well below what §20's first milestone needs. Confidence in the verdict:
**medium-high** on Q1, **medium** on Q3, **medium-high** on Q4, **low** on Q2.

---

## Findings that contradict the design doc

**1. The COGS result — the benchmark §13's experiment mirrors — was substantially retracted
in effect.** COGS reported that in-distribution accuracy was near-perfect (96–99%) while
generalization accuracy was 16–35% with ±6–8% seed sensitivity, which is the canonical
"symbolic structure does not save you" result ([Kim & Linzen 2020](https://arxiv.org/abs/2010.05465)).
But [Wu, Manning & Potts, "ReCOGS" (TACL 2023)](https://arxiv.org/abs/2303.13716) showed
that "the negative results trace to incidental features of COGS LFs" — i.e. the models were
failing on semantically irrelevant formatting details of the logical form, not on
compositional semantics. After converting to semantically equivalent LFs and factoring out
non-semantic capabilities, "even baseline models get traction." ReCOGS is a *correction to
the strength of the COGS claim*, and it cuts both ways for SBL: it means the famous
failure is less damning than it looks, **but it also means a result on a hand-built
logical form is a measure of that logical form's incidental design choices as much as of
compositional ability.** A COGS-style experiment built on SBL's own ontology would have the
same exposure — SBL would be measuring its own serialization as much as its semantics.

**2. Whether a symbolic/structured route helps is a data-distribution question, not an
architecture question.** [Akyürek et al. 2022, "Revisiting the Compositional Generalization
Abilities of Neural Sequence Models"](https://arxiv.org/abs/2203.07402) found that
"modifying the training distribution in simple and intuitive ways enables standard
seq-to-seq models to achieve near-perfect generalization performance," concluding the
models' ability "was previously underestimated" and that results are "highly sensitive to
the characteristics of the training data." This directly weakens the implication in §13
that a genuinely compositional *representation* is what produces EAT(DOG, MILK) from
unseen combinations — the observed effect is achievable by changing the data.

**3. The signal does not transfer upward.** [Alajrami & Aletras 2021](https://arxiv.org/abs/2107.01366)
built Transformers that are SCAN-capable and found that "improvements of a SCAN-capable
model do not directly transfer to the resource-rich MT setup," with gains only in
low-resource and distribution-shifted settings. So even a *successful* SBL compositional
result at v0.1 scale is not evidence of benefit at the scale where the design doc's later
phases live.

**4. Symbolic intermediate representations help compositional generalization only
conditionally, and the conditions are the expensive part.** [Herzig & Berant 2021,
"Unlocking Compositional Generalization in Pre-trained Models Using Intermediate
Representations"](https://arxiv.org/abs/2104.07478) found large gains (CFQ +14.8 accuracy
points; text-to-SQL template splits +15.0 to +19.4) — but explicitly from intermediate
representations "that [have] stronger structural correspondence with natural language,"
with the key design aspects identified as critical. This is evidence *for* the mechanism
and *against* the assumption that any symbolic layer works. It also shows the gain is
attributable to representation *design*, which SBL has not yet specified (map: "Not yet
specified — neural architecture for §6").

**5. §6's computational claim has no located support at inference time.** The classic
efficiency result is **training-time**, and the modern lineage is explicitly framed that
way: [Grave et al. 2017, "Efficient softmax approximation for GPUs"](https://arxiv.org/abs/1609.04309)
describes an approach to "efficiently **train** neural network based language models over
very large vocabularies." [Prabhu et al. 2018](https://arxiv.org/abs/1810.11671) prove that
"the pick-one-label heuristic — a reduction technique from multi-label to multi-class that is
routinely used along with HSM — is not consistent in general," and note hierarchical
methods' advantages are expressed in "model size and prediction time" for
*extreme-multi-label* settings, not for next-token generation. And [Ghosh et al. 2018](https://arxiv.org/abs/1812.05737)
report plainly that "the performance of Hierarchical Softmax degrades as the number of
classes increase." **No source was located showing that predicting through a semantic
category hierarchy reduces inference computation versus flat next-token prediction while
holding accuracy.** Design doc §6 hedges this itself ("not yet a proven computational
advantage"), so §6 is an open hypothesis, not a supported claim — but the literature's
framing (training-time efficiency) means the burden of proof is on SBL, and the natural
reading of hierarchical softmax does not transfer to inference.

**6. The Tamil grammar layer is the hard bound, and it is severe.** [Sarvabhotla et al.
2020, "ThamizhiUDp: A Dependency Parser for Tamil"](https://arxiv.org/abs/2012.13436)
report the state of the art for Tamil UD parsing as **LAS 62.39** — "4 points higher than
the current best achieved for Tamil." For comparison, low-resource UD parsers sit far lower
still: the [Odia UD treebank paper](https://arxiv.org/abs/2205.11976) reports **21.34% LAS**.
The design doc's pipeline routes *all* meaning through parser → grammar → semantics
(§3, §14 Model B); ~38% of Tamil dependency arcs are wrong at the first hop, before any
grammar-role mapping, concept alignment, or ontology gap error is added.

**7. Multilingual AMR parsing shows the cost of the interlingua route is paid in accuracy.**
[Lee et al. 2021](https://arxiv.org/abs/2109.15196) had to use noisy knowledge distillation
from an English teacher to get a *single* multilingual AMR parser, reporting gains "up to
18.8 Smatch points on Chinese." A large gain of that size implies the pre-existing
multilingual baseline was very low — the shared-graph route across languages is not
free.

**8. The strongest published argument against the interlingua thesis is about form vs.
meaning, and it applies to SBL's architecture as written.** [Bender & Koller, "Climbing
towards NLU" (ACL 2020)](https://aclanthology.org/2020.acl-main.463/) argue "a system
trained only on form has a priori no way to learn meaning," because meaning is the relation
between form and communicative intent, not a property of form. SBL's §4.4 and §15 partially
concede this by leaving ambiguity, nuance and world knowledge to the neural layer — but §5
and §20 assert that the semantic representation "does not" change between English and
Tamil. Those two positions are in tension: if meaning requires non-linguistic context, a
language-independent form-derived graph cannot be the meaning, only a normalised notation
for it.

**9. The interlingua BLEU evidence is mixed, not supportive.** [Vázquez et al. 2019](https://arxiv.org/abs/1905.06831)
report a neural interlingua gives "BLEU improvements up to 2.8" on low-resource pairs but
"results on a larger dataset ... show BLEU loses if the same amount." [Gu et al. 2018](https://arxiv.org/abs/1804.08198)
claim zero-shot direct translation and "comparable" (not better) BLEU. The honest reading:
shared intermediate representations buy *architecture* properties (linear rather than
quadratic language-pair count), not quality.

---

## Q1 — Compositional generalization over a fixed symbolic ontology

Primary sources verified (abstract-level; see Confidence):

- [Lake & Baroni 2018, SCAN, arXiv:1711.00350](https://arxiv.org/abs/1711.00350) — RNNs
  succeed on "mix-and-match" splits but where "generalization requires systematic
  compositional skills ... RNNs fail spectacularly."
- [Kim & Linzen 2020, COGS, arXiv:2010.05465](https://arxiv.org/abs/2010.05465) — 96–99%
  in-distribution vs 16–35% generalization, ±6–8% seed sensitivity.
- [Keysers et al. 2020, CFQ, arXiv:1912.09713](https://arxiv.org/abs/1912.09713) — three
  architectures "fail to generalize compositionally," with "a surprisingly strong negative
  correlation between compound divergence and accuracy."
- Critique/replication: [Akyürek et al. 2022](https://arxiv.org/abs/2203.07402) (training
  distribution sufficient), [Wu et al. 2023 ReCOGS](https://arxiv.org/abs/2303.13716)
  (LF-incidental details caused COGS failures), [Alajrami & Aletras 2021](https://arxiv.org/abs/2107.01366)
  (no transfer to resource-rich MT).
- Mechanism-positive: [Herzig & Berant 2021](https://arxiv.org/abs/2104.07478) (intermediate
  representations, CFQ +14.8), [Gao et al. 2023](https://arxiv.org/abs/2305.16954) (multiset
  tagging + latent permutations, no trees, high accuracy on deeper recursion),
  [Huang et al. 2023](https://arxiv.org/abs/2310.14124) (supertagging + valency constraints
  as an ILP improves COGS structural generalization; "structural constraints are important").
- LLM-era: [Chen et al. 2025, LCS/CompSub](https://arxiv.org/abs/2502.20834) — LLMs remain
  deficient; their method's gains are largest on SCAN (+66.5%) and much smaller on COGS
  (+10.3%) and GeoQuery (+1.4%), i.e. the more realistic the benchmark the smaller the fix.

**Answer: it is shown to require specific architectural or training commitments, not to be
free with a symbolic ontology, and not to fail permanently.** COGS was the strongest
"persistently fails" evidence and it has been partially walked back. SBL's §13 test as
written — construct EAT(DOG, MILK) from separately-seen concepts — is a *mix-and-match*
split of the kind SCAN found RNNs can already pass, so it is **not a discriminating
experiment**. This is a direct hit on §13.

## Q3 — The symbolic interlingua thesis

Sources: [Bender & Koller 2020](https://aclanthology.org/2020.acl-main.463/), the neural
interlingua papers above, and **UMR as the closest existing realization**:
[UMR is described as a graph-based semantic representation "expanding on Abstract Meaning
Representation ... through the inclusion of document-level information and multilingual
flexibility," with an automatic parser, SETUP, reaching SMATCH++ 91](https://arxiv.org/abs/2502.11968);
[UMR in prompts produced statistically significant translation gains for Navajo, Arapaho
and Kukama](https://arxiv.org/abs/2502.08900); [UMR-to-text generation reaches multi-reference
BERTScore 0.825 English / 0.882 Chinese](https://arxiv.org/abs/2502.11973). UMR's own
framing is decisive: it builds "flexibility ... into the annotation schema such that the
breadth of the world's languages can be annotated." That is a *multilingual* schema, not a
*language-independent* one — precisely the compromise the interlingua debates converged on,
and a challenge to §5's claim that the representation "does not" change.

**Answer: a compact hand-specified ontology demonstrably can carry real meaning for
simple sentences across languages (UMR exists and works), so there is no proven general
ceiling. But the published exemplars compromise on language-independence rather than
achieving it, and the classical interlingua arguments (ambiguity, sense enumeration,
context-dependence) are consistent with that compromise.**

## Q2 — Hierarchical / factored prediction (§6) — PARTIAL

See contradicting finding 5. What was verified: hierarchical softmax descendants are framed
as *training*-efficiency methods ([Grave et al. 2017](https://arxiv.org/abs/1609.04309),
[Prabhu et al. 2018](https://arxiv.org/abs/1810.11671)); one paper reports accuracy
*degrading* as classes grow ([Ghosh et al. 2018](https://arxiv.org/abs/1812.05737)); one
recent paper reports hierarchical softmax improving macro-F1 on four text-classification
datasets ([Han et al. 2023](https://arxiv.org/abs/2308.01210)). **Not verified:** the
classic Morin & Bengio (2005) and Mnih & Hinton (2009) hierarchical-softmax papers, factored
language models (Bilmes & Kirchhoff), and any explicit inference-cost analysis. Treat Q2 as
open, leaning negative.

## Q4 — Parsing accuracy as an upstream bound

- Tamil UD parsing: **LAS 62.39** ([Sarvabhotla et al. 2020](https://arxiv.org/abs/2012.13436));
  Tamil POS tagging F1 93.27 with a *rule-based* morphological analyser.
- Low-resource UD floor: **21.34% LAS** for Odia ([2205.11976](https://arxiv.org/abs/2205.11976)).
- AMR parsing (Smatch F1, AMR 3.0 / LDC2020T02): **Graphene 0.854**, APT+Silver 0.804,
  fine-tuned LLaMA 3.2 0.804 ([Opitz et al. 2025](https://arxiv.org/abs/2508.05028)).
  Earlier reference points: [Zhang et al. 2019](https://arxiv.org/abs/1905.08704) 76.3% F1
  on AMR 2.0; [Wang et al. 2015](https://arxiv.org/abs/1504.06665) improved SOTA by 7
  Smatch points. AMR parsing is now **LLM-comparable**, which is itself notable for the
  design doc's §14 baseline: a conventional model fine-tuned to emit a structured semantic
  graph matches purpose-built symbolic-stack parsers.
- **Smatch is itself contested**: [Shen et al. 2019](https://arxiv.org/abs/1905.10726)
  argue Smatch's greedy hill-climbing "leads to search errors" and that a later evaluation
  [criticizes the node-matching criterion as rewarding unintentional similarity](https://arxiv.org/abs/2603.26401).
  So even the metric that certifies AMR quality is not stable ground.

**Answer: error compounding is the strongest single quantitative argument against §6/§14/
§20's pipeline.** Even taking the *best published* AMR number (0.854 Smatch) as the
*semantic* ceiling, and the best Tamil LAS (0.6239) as the *grammar* ceiling, an
SBL-shaped pipeline on Tamil would have ~37.6% of dependency arcs wrong before semantic
mapping begins. §20's first milestone ("can two surface forms be converted into the same
machine-readable representation") is achievable on hand-curated simple sentences; it is
not achievable by an automatic parser at Tamil LAS 62.39 without either accepting low
fidelity or hand-authoring the parse.

---

## What the literature is silent on

1. **Inference-time compute of hierarchical semantic prediction versus flat next-token
   prediction, at matched accuracy.** Nothing located. This is the core of §6 and it is
   genuinely open — but the burden is on SBL, since the classic literature optimises
   training.
2. **Whether a single *language-independent* (not merely multilingual) semantic ID space
   can reach high accuracy for a language like Tamil.** UMR sidesteps this by building
   flexibility into the schema. No source located that tests strict language-independence.
3. **The compositional-generalization behaviour of a *fixed, small, hand-specified*
   ontology (~100 concepts, §8) as opposed to a large induced one.** The benchmarks all sit
   at much larger concept inventories; the small-ontology regime is untested either way.
4. **Serialization-format sensitivity** — ReCOGS shows LF-format choices dominate results,
   but no source predicts which serialization choices are safe.
5. **Cost of ontology coverage gaps** at SBL scale: UMR/AMR parsers use large concept
   inventories; the failure mode of a 100-concept ceiling (unknown-concept rate) is not
   evaluated in the located literature.

## Confidence

- **Primary-source verified** (abstract or body text read at the owned URL): SCAN, COGS,
  CFQ, ReCOGS, Akyürek et al. 2022, Alajrami & Aletras 2021, Herzig & Berant 2021,
  LCS/CompSub 2025, Grave et al. 2017, Prabhu et al. 2018, Ghosh et al. 2018, Han et al.
  2023, Bender & Koller 2020, Vázquez et al. 2019, Gu et al. 2018, UMR papers (2502.11968,
  2502.08900, 2502.11973), ThamizhiUDp, Odia UD, AMR Smatch papers (2508.05028, 1905.08704,
  1504.06665, 1905.10726), Gao et al. 2023, Huang et al. 2023.
- **Partially verified / abstract-only, not confirmed in the paper body**: the specific
  numeric splits read from abstracts; UMR's "multilingual flexibility" framing; the claim
  that no inference-time-savings result exists — this is an *absence of evidence* from a
  short search, not a proof of absence.
- **My inference, not sourced**: the compounded-fidelity arithmetic in Q4 (it is my
  multiplication of two independently published ceilings, not a published result); the
  reading that §13's test is a mix-and-match split; the tension noted in contradicting
  finding 8 between §4.4/§15 and §5/§20.
- **Unverified — I did not reach a source**: the classical interlingua debate literature
  itself (Bar-Hillel's 1960 argument against fully automatic high-quality translation, the
  1966 ALPAC report, Dorr's interlingua/transfer survey in *Computational Linguistics*)
  and the class-based n-gram / factored-LM line (Brown et al. 1992; Bilmes & Kirchhoff
  2003; Morin & Bengio 2005; Mnih & Hinton 2009). Q3 and Q2 below rest on modern sources
  only and should be re-checked against this older literature, which is where the strongest
  arguments against the interlingua thesis are known to live.

## Incomplete — not yet investigated

- **Q2 (hierarchical prediction) is only partially done.** Missing: Morin & Bengio (2005),
  Mnih & Hinton (2009), Brown et al. (1992) class-based n-grams, Bilmes & Kirchhoff (2003)
  factored LMs, and any source that explicitly measures *inference* cost of a hierarchy at
  matched accuracy. The specific sub-question — "does §6's claim hold only at training
  time?" — is answered *indicatively* yes (the literature is framed on training) but not
  *conclusively*, because no source located states it as a limitation in those words.
- **Q3 (interlingua) is missing the classical debate.** Missing primaries: Bar-Hillel
  (1960), ALPAC (1966), Dorr (1993), Hutchins' surveys, Nirenburg & Carbonell (1992), and
  any formal statement of the ambiguity/coverage ceiling. The modern sources suffice to say
  "no proven general ceiling, but exemplars compromise," not to state the classical
  counterarguments in their own terms.
- **Q1 is missing full-text verification** of the CFQ and SCAN split-level numbers, and
  missing a systematic sweep of the post-2023 LLM-era COGS literature beyond one paper.
- **Q4 is missing UD baseline numbers for English** (to quantify the English/Tamil gap) and
  any semantic-parsing number outside AMR (e.g. GeoQuery, Spider, COGS-QL) that would test
  the design doc's stated target scale more directly.
- **Not attempted at all:** whether SBL's *specific* choice of ~100 concepts and ~30
  relationships (§8) has been tested; the `ismatch`/serialization question; and whether the
  "IDs stable, vectors not" claim (§7) is already realised by any existing standard.

A follow-up pass should start with Bar-Hillel/ALPAC/Dorr (Q3) and Morin & Bengio /
Mnih & Hinton (Q2), since those are the two places the design doc's claims are most likely
to be directly contradicted in the authors' own words.
