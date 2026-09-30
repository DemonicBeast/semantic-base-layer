# Issue 12 — Prior art: is a front-end semantic interlingua for code already built?

**Question.** Is SBL's core claim, for programming languages specifically, already delivered by existing
interlinguas — and if not, what precisely is left for SBL to contribute?

**Verdict.** The *front-end, analysis-facing* interlingua that §11 proposes already exists, is mature, and
already ships a C#/VB indexer built on Roslyn. [Kythe](https://kythe.io/docs/kythe-overview.html) is a
"language-agnostic" graph capturing "usages, type information, and cross-language associations";
[SCIP](https://github.com/sourcegraph/scip/blob/main/README.md) is "a language-agnostic protocol for indexing
source code" with indexers for ~10 language families, including
[scip-dotnet](https://github.com/sourcegraph/scip-dotnet) — "SCIP indexer for the C# and Visual basic
programming languages", built on Roslyn; [Glean](https://glean.software/docs/introduction/) stores facts over
per-language schemas and *derives* language-neutral abstractions in a Datalog-like query language. SBL's
`DECLARE(VARIABLE=result, VALUE=CALL(...))` is a lossy restatement of what Kythe's edges and SCIP's symbols
already encode at higher fidelity. On the narrow claim — *many source languages normalise into one structure
so a tool can reason across them without compiling or executing* — the answer is **yes, it is delivered**.
Only two things are uncovered: nothing targets an *AI model* as consumer, and nothing captures *intent or
behaviour* rather than structure. **Recommendation: do not build a new code interlingua; contribute on top
of SCIP or Kythe.**

---

## §1 — The existing interlinguas

| System | Level | Genuinely language-agnostic *front end*? | Consumer |
|---|---|---|---|
| [CIL/MSIL](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process) | Bytecode, "a CPU-independent set of instructions" | Yes *for compiled code* (C#, VB, F#), but post-lowering | CLR: JIT |
| [LLVM IR](https://llvm.org/docs/LangRef.html) | SSA IR, below source semantics | Back end only — clang/rustc/swiftc are separate front ends | `opt`, JIT |
| [GraalVM/Truffle](https://www.graalvm.org/latest/graalvm-as-a-platform/language-implementation-framework/) | Per-language "interpreters for self-modifying Abstract Syntax Trees" | **No** — each language writes its own AST/interpreter; only compiler and tooling API are shared | Implementers |
| [MLIR](https://mlir.llvm.org/docs/LangRef/) | Extensible multi-level SSA IR | Yes — closest analogue of "dialects as shared semantics", but source languages *lower into* it | Compilers |
| [tree-sitter](https://tree-sitter.github.io/tree-sitter/) | "a concrete syntax tree", per-language grammar | No — one grammar per language, no shared node vocabulary, syntax not semantics | Editors |
| [LSP](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/) | Protocol only: URIs, positions, JSON-RPC | Deliberately no: its types "are not at the level of a programming language domain model which would usually provide abstract syntax trees and compiler symbols" | Editors |
| [RPython/PyPy](https://doc.pypy.org/en/latest/translation.html) | Restricted dialect used to *implement* a runtime | No — one dialect, translated ahead of time; not a cross-language interlingua | PyPy |
| [WebAssembly](https://webassembly.org/docs/high-level-goals/) | Stack machine, "a compilation target" | Back end; source features compiled away | Browsers |
| **[SCIP](https://github.com/sourcegraph/scip/blob/main/docs/DESIGN.md)** | Symbol index: definitions, references, implementations, docs, monikers | **Yes — this is the front-end interlingua.** "Not meant as a storage format for querying": a transmission format from indexers to consumers | Sourcegraph |
| **[LSIF](https://github.com/microsoft/language-server-protocol/blob/main/indexFormat/specification.md)** | Same level, prior generation | Yes, but pointedly "doesn't define any symbol semantics ... doesn't define a symbol database" | Deprecated |
| **[Kythe](https://kythe.io/docs/kythe-overview.html)** | Language-agnostic graph, "liberal and extensible" schema | **Yes — the most explicit front-end claim**: a "language-agnostic graph structure" for "usages, type information, and cross-language associations" | Google |
| **[Glean](https://glean.software/docs/introduction/)** | Immutable facts queried with Angle (Datalog-like) | Yes, but neutrality is *derived*: "doesn't force all the data into a single schema... Language-neutral abstractions can be built by deriving facts using Angle" | Meta |
| **[CodeQL](https://codeql.github.com/docs/codeql-overview/about-codeql/)** | Per-language DB + shared query language (QL); [8 languages](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/) incl. C# | Partly — the *query* structure is shared, each language keeps its own schema | Security |

---

## §2 — Is the distinction real, and does the front-end direction already exist?

**The distinction is real.** CIL, LLVM IR and Wasm are places many languages go *down* into so one runtime
executes the result, abandoning source semantics. SCIP, LSIF, Kythe and Glean are places many languages
normalise *sideways* into so tools reason over them without compiling or executing. §11's framing is sound —
**but the front-end direction already exists, and the four flagged tools *are* it, not neighbours of it.**

- **SCIP** already indexes **C#/VB** through Roslyn — `dotnet tool install --global scip-dotnet` — so the
  planned starting stack is the *least* novel part of the plan.
- **LSIF** *explicitly refused* to define symbol semantics — exactly the gap SBL claims to fill. Deprecated.
- **Kythe** is the closest match to §11's wording, and its overview is candid the graph targets post-build
  structure, not "writing a compiler or optimizer".
- **Glean** is closest to a *semantic* layer, and reaches neutrality by *deriving over* per-language schemas
  rather than imposing one universal schema — the opposite of SBL's choice, and the one Meta shipped.

No gap is left in the "cross-language program-semantics representation" space for a new format to occupy.

---

## §3 — What is actually left

| Candidate | Verdict | Evidence |
|---|---|---|
| **(a) ~100-concept ontology vs. real grammars** | **A regression, not a contribution.** | The big grammars exist because the languages are big; SCIP gets C#/VB from Roslyn's full *semantic* model. A 100-concept ontology cannot express overload resolution, generics, `async` states or LINQ. C# and Python `Add` are "the same" only if they resolve alike — the claim to be proven, not assumed. |
| **(b) AI-model-facing vs. tool-facing** | **Real but thin.** | SCIP optimises for producers, not querying; Kythe is a post-build graph dump. Neither targets an LLM, so an LLM-friendly projection of an existing index is a genuine small gap — but a *renderer*, not a new semantic layer. |
| **(c) Semantics/behaviour vs. syntax** | **Real gap — SBL does not deliver it either.** | SCIP is navigation; LSIF defined no symbol semantics; Kythe captures structural/type facts; CodeQL queries structure. Glean alone has a designed extension point, and its docs name this: "you could store test coverage data or profiling data". Capturing *intent* is the surviving opportunity — with no mechanism proposed. |
| **(d) Nothing — niche covered** | **True for §11 as written.** | Phase 6's question ("can different languages map into a shared semantic/program representation?") is answered *yes* by four shipped systems; the remainder is re-implementation with fewer features. |

**A direct objection to SBL's chosen representation.** §11 proposes explicit nodes-and-relationships. SCIP's
design doc [rejected that shape on purpose](https://github.com/sourcegraph/scip/blob/main/docs/DESIGN.md) —
"Avoid direct encoding of graphs" — because adjacency-list graphs "encourage a wholesale approach to writing
indexers", hurt parallelism, and blow up index-time memory.

---

## §4 — The strongest counter-case

**Best argument for a new layer.** (i) Every tool above needs a per-language front end (Roslyn, a real build,
a JDK), so cross-language reasoning costs N integrations; a syntax-level ontology could be produced cheaply
per language. (ii) None represent *behaviour or intent*, so none answers "do these two programs do the same
thing?". (iii) All are tool-facing, not model-facing. (iv) Nobody has *shipped* a fixed shared vocabulary.

**Does it convince me? Partly — not enough to build a new interlingua.** (i) is an *indexer-cost* argument:
it favours cheaper SCIP indexers, not a new format, and SBL's ontology would hit the same per-language wall
past trivial expressions. (ii) is the real gap and I find it genuine — but §11's example does not address it:
`DECLARE`/`CALL` restates syntax in new words and carries *less* information than Roslyn's own syntax tree.
(iii) is worth a small tool on an existing index. (iv) is instructive: Meta, Google and Sourcegraph each
tried a shared vocabulary and each landed on "per-language schemas with derived neutrality".

**Conclusion.** §11's premise for code is falsified as stated. The one defensible direction is (c) —
behaviour and intent rather than structure, consumed by a model. That is a different project and should be
re-scoped before any Roslyn work begins.

---

## Confidence

**Primary-source verified** — every quotation in §1–§3 was read directly this session from SCIP's
[README](https://github.com/sourcegraph/scip/blob/main/README.md) and
[DESIGN.md](https://github.com/sourcegraph/scip/blob/main/docs/DESIGN.md),
[scip-dotnet](https://github.com/sourcegraph/scip-dotnet), the
[LSIF spec](https://github.com/microsoft/language-server-protocol/blob/main/indexFormat/specification.md), the
[Kythe overview](https://kythe.io/docs/kythe-overview.html),
[Glean](https://glean.software/docs/introduction/), the
[LSP overview](https://microsoft.github.io/language-server-protocol/overviews/lsp/overview/), the
[.NET docs](https://learn.microsoft.com/en-us/dotnet/standard/managed-execution-process),
[LLVM](https://llvm.org/docs/LangRef.html)/[MLIR](https://mlir.llvm.org/docs/LangRef/) LangRefs,
[WebAssembly](https://webassembly.org/docs/high-level-goals/) and
[CodeQL](https://codeql.github.com/docs/codeql-overview/supported-languages-and-frameworks/) — all via `curl`.

**Partial** — characterisation verified, cross-language generalisation inferred: CodeQL's per-language schema
(from its library guides, not one page); Truffle ("interpreters for self-modifying Abstract Syntax Trees"
verified, "not a shared representation" inferred); tree-sitter ("concrete syntax tree" verified, "no shared
node vocabulary" inferred); RPython (from [PyPy](https://doc.pypy.org/en/latest/translation.html) and
[RPython](https://rpython.readthedocs.io/en/latest/translation.html) docs, not a paper).

**Inference** — "no front-end tool captures intent or behaviour" (Glean's coverage/profiling extensibility is
the counterexample); §11's example is *lossy* relative to Roslyn's syntax tree, reasoning from
`semantic-base-layer-design-5.md` lines 594–631. **Unverified** — Glean's exact per-language indexer list;
whether a cross-language program-semantics representation exists outside SCIP/LSIF/Glean/Kythe/CodeQL/MLIR.

*`web_search` failed on every call this session; all findings come from `curl` against the primary sources
cited.*
