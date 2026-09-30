# D2 — First experiment: does an SBL layer beat an AST baseline?

**Status:** proposed. Awaiting owner approval before any code is written
(`AGENT.md` §2). Governed by [`plan.md`](../../../plan.md) §12.

**Scope decisions fixed by the owner on 2026-10-01:**
SBL-for-code captures **syntax/structure only** — declarations, calls, control flow,
expressions. The first language pair is **C# + Python**.

---

## 1. The question

SBL's claim, applied to code, is that a compact language-independent representation can
sit between source languages and AI models and expose equivalences that raw syntax hides.

The honest way to test that is **not** against an LLM. Modern models already handle
cross-language code reasonably well, so beating them proves little and losing to them
proves less. The right opponent is the thing compilers have always had: **the AST.**

If plain syntax trees already surface the same cross-language equivalences, then an SBL
layer is a re-encoding of an AST with extra steps, and the hypothesis is false. That is
a result worth having, and this design is built so it can arrive.

## 2. Hypothesis

> **H1.** Normalizing C# and Python programs into SBL surfaces structural equivalences
> between them that an AST-level comparison does not surface at comparable cost.

**H1 is false if** the AST baseline surfaces the same equivalences at comparable cost.

## 3. The corpus — and why it's built the way it is

A set of **matched triples**, hand-authored, no crowd annotation:

| Field | Meaning |
| --- | --- |
| `pair_id` | stable id |
| `csharp` | a C# snippet |
| `python` | a Python snippet |
| `equivalent` | `true` / `false` — do these two compute the same thing? |
| `construct_kind` | which construct the pair exercises (see §3.2) |
| `author_confidence` | how sure the author is that the pair really is equivalent |

### 3.1 Equivalence is computable here — that is the whole advantage

Because the scope is **structure only**, "equivalent" is not a judgement call. Two
snippets are equivalent iff they have the same structural shape after normalizing the
syntax that differs between the languages. That makes the ground truth objective, which
is exactly what the natural-language version of this experiment could not achieve.

### 3.2 Three construct tiers

The tiers exist because the interesting question is *where* SBL stops working.

- **Tier 1 — near-isomorphic.** `if/else`, `while`, assignment, function declaration,
  arithmetic, return. C# and Python have almost the same shapes. **Expected: both SBL
  and the AST baseline succeed.** A system that fails here is simply broken.
- **Tier 2 — same semantics, different shape.** C# `foreach` vs Python `for … in`;
  C# `string.Format`/interpolation vs Python f-strings; C# `List<T>.Add` vs Python
  `list.append`; ternary spellings; `switch` vs `match`. **This is the discriminating
  tier.** An AST baseline should struggle because the node types genuinely differ.
- **Tier 3 — idiomatic divergence.** C# LINQ vs Python comprehensions; `using`/`IDisposable`
  vs `with`; properties vs `@property`; expression-bodied members; `null`-conditional
  operators vs `None` checks. **Expected: SBL needs ontology concepts it will not have.**
  This tier measures the *cost* of a fixed ontology — the thing that killed UMR-style
  approaches at scale, and the thing `03-findings.md` predicts will bite.

### 3.3 Size

Start at **~30 pairs**: 10 per tier, half `equivalent: true` and half deliberately
`false` (matched syntactically but not semantically, so a system cannot win by calling
everything equivalent). Thirty is enough to see the shape of the result; it is not
enough to publish. Growing the corpus is a later decision, made *after* the tiers show
where the interesting failure lives.

## 4. The systems under test

| System | What it does |
| --- | --- |
| **B1 — AST baseline** | Parse C# with Roslyn (or `tree-sitter-c-sharp`), Python with the stdlib `ast` module. Normalize node names to a common vocabulary with a **small, hand-written mapping** — the cheapest thing that could possibly work. Compare with tree edit distance. |
| **B2 — token baseline** | Compare raw source via token overlap / a code embedding. Included only to sanity-check the corpus: if B2 beats B1, the corpus is testing surface form, not structure. |
| **S — SBL** | Parse the same snippets, normalize into **SBL-C** (the code ontology, §5), compare structurally. |

**B1 is the system that matters.** B2 is a control on the corpus, not a competitor.
No LLM is used, so none of the traditional "a big model would do better" objection
applies — and if a big model *is* needed to make SBL work, that is itself a finding.

## 5. SBL-C, deliberately minimal

The ontology is the variable under test, so it starts as small as it can while covering
Tier 1. Roughly two dozen concepts:

- **Declarations:** `DECLARE_VARIABLE`, `DECLARE_FUNCTION`, `DECLARE_CLASS`
- **Control:** `IF`, `ELSE`, `WHILE`, `FOR_EACH`, `FOR_RANGE`, `RETURN`, `BREAK`, `CONTINUE`
- **Expressions:** `ASSIGN`, `CALL`, `BINARY_OP`, `UNARY_OP`, `COMPARE`, `LITERAL`
- **Data:** `SEQUENCE`, `MEMBER_ACCESS`, `INDEX`, `PARAMETER`, `ARGUMENT`
- **Relations:** `AGENT_OF`, `OBJECT_OF`, `HAS`, `PART_OF`, `PRECEDES`

**The rule:** a construct that SBL-C cannot express is recorded as an `UNKNOWN` node,
**not** quietly given a new concept. The unknown rate per tier is a first-class result —
it is the direct measurement of the coverage cost that a fixed ontology imposes.

## 6. Metrics

| Metric | Why |
| --- | --- |
| **Match accuracy** on `equivalent` pairs, per tier, per system | the headline |
| **Unknown-node rate**, per tier | the cost of the fixed ontology — the number the design doc's §8 assumption lives or dies on |
| **Concept count** needed to reach a given accuracy | SBL's pitch is that it is *small*; if it needs 400 concepts to match an AST, the pitch fails |
| **Authoring cost** — concepts added, mapping rules written, hours | compared against B1's mapping cost |
| **Tier boundary** — the tier where SBL's accuracy drops to B1's | locates the ceiling |

## 7. Pre-registered falsification conditions

Written **before** measuring, per `plan.md` V3. Any one of these kills H1:

1. **The baseline matches SBL.** B1 achieves accuracy equal to or better than S on
   Tier 2, at comparable authoring cost. → SBL is an AST re-encoding; stop.
2. **The ontology doesn't stay small.** Matching B1's Tier-2 accuracy requires SBL-C to
   grow past ~100 concepts. → SBL's smallness claim (design doc §8) fails.
3. **Unknowns dominate.** SBL's unknown-node rate exceeds ~30% on Tier 2 — the tier SBL
   is supposed to win. → coverage cost exceeds the benefit.
4. **The corpus is testing surface form.** B2 (tokens) matches or beats B1 (AST). → the
   corpus is broken and the experiment must be redesigned before any conclusion is drawn.

**A negative result here is a good outcome.** It costs days, not the months the
natural-language route would have cost, and it settles the direction.

## 8. What would make this a *positive* result

To be clear about the bar, so success is not claimed on a technicality: S is a positive
result only if it beats B1 on **Tier 2** by a margin that survives the small corpus
size, **while** SBL-C stays under ~100 concepts. Beating B1 on Tier 1 proves nothing
(Tier 1 is near-isomorphic by construction). Winning only on Tier 3 is interesting but
must be reported as "SBL handles idiomatic divergence at the cost of N new concepts",
not as general superiority.

## 9. Cost estimate

| Item | Estimate | Basis |
| --- | --- | --- |
| Corpus authoring, 30 pairs | a few hours | authored by hand; both languages known to the owner |
| Roslyn or tree-sitter parse harness | under a day | Roslyn is a maintained C# parser with a public syntax-tree API |
| Python `ast` harness | well under a day | standard library |
| Tree edit distance | under a day | small, well-understood algorithm |
| SBL-C ontology + writer | 1–2 days | ~24 concepts, JSON + a serializer |

**Total: days, not weeks.** Compared with the natural-language route — Tamil annotation
at $2.5k–15k for 1,000 pairs (`04-findings.md`) — this is the cheapest experiment on the
board, and the only one currently designed to be able to fail.

## 10. Open questions before execution

1. **D1 is unresolved.** `12-findings.md` is in flight: if SCIP/LSIF/Glean/Kythe already
   provides a compact structural interlingua for multiple languages, then B1 should
   arguably *be* that tool rather than a hand-written AST mapping — and the experiment
   gets sharper for free. **Do not finalise B1 until D1 lands.**
2. **Roslyn vs tree-sitter for C#.** Roslyn is the real compiler front end and gives
   semantic info; tree-sitter is lighter and gives structure only. Since the scope is
   structure-only, tree-sitter may be sufficient — but Roslyn is the owner's stack.
   Owner's call.
3. **Which side of a pair counts as "the same shape"** when one language genuinely lacks
   a construct. The corpus must state the normalization rule per Tier-3 pair, or the
   ground truth becomes contestable and the experiment loses its main advantage.
