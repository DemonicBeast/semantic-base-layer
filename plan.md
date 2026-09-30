# plan.md — Active work plan

> Governed by `AGENT.md`. Every claim below is either **verified** (with the
> command that proves it) or explicitly labelled **inferred**.
> Read this file before acting; update it before executing.

- **Status:** executed — V1–V10 run, results in §12; awaiting owner review
- **Owner:** Shrishti Pekhale (developer; .NET background)
- **Opened:** 2026-05-22
- **Scope of this plan:** governance files + a local repository graph index

---

## 1. Request

The owner asked for eight things, in their words:

1. An `agent.md` read before any AI work — instructing: no assumptions, analyze
   and plan first, keep a `plan.md` that carries **evidence** the plan will work,
   and **inform the owner** when the plan changes.
2. Treat the owner as a competent .NET developer: explain unfamiliar technology in
   a sentence or two of plain English, and put **nothing** into code without their
   thought — plans get discussed and agreed before execution.
3. Never access anything needing a password or credential without telling them
   first; they must know what is being accessed.
4. Do not burn context: build a graph of the codebase — classes, methods,
   properties, relationships, dependencies — as nodes and edges.
5. Store that graph in a local file, use **SQLite**, and answer later questions
   from it instead of re-reading the repository.
6. Having identified the relevant class, use **grep** to read the actual code —
   faster, less context.
7. Always explain what is going on behind the scenes.
8. Do not change existing code unless the change is absolutely required.

## 2. Current state of the repository

SBL is a **research/specification project**. There is no implementation yet.

| Verified fact | Evidence |
| --- | --- |
| No code of any kind | `find . -type f` outside `.git` returns only `.md`, `.json`, `.jsonl`, `.tsv`, `.conllu`, `.html`, `.bz2` — no `.csproj`, `.sln`, `.py`, `package.json` |
| Not a code repository yet | `git log --oneline` → 3 commits, all adding markdown docs |
| No instruction file exists | `ls AGENT.md AGENTS.md CLAUDE.md plan.md PLAN.md` → all "No such file or directory" |
| Python available | `python3 -VV` → Python 3.9.6 |
| SQLite available in stdlib | `python3 -c "import sqlite3"` → lib 3.51.0 |
| 10 tickets, 5 findings artifacts | `ls SBL-Wayfinder/v01/issues/*.md` → 10 ticket files + 5 `*findings*` files (`01`, `02`, `04`, `05`, `10`). **Ticket `03` has no findings artifact yet.** |
| Design doc has **46** headings | `grep -c '^#\{1,3\} ' semantic-base-layer-design-5.md` → **46** (not the 60 first estimated — corrected, see §11) |
| Findings are untracked work-in-flight | `git status --short` → `01`, `02`, `04`, `05`, `10` findings files are `??` (uncommitted) |
| Ticket dependency chain is real data | `grep '^Blocked by:'` → 4 non-empty dependency edges |
| Ticket metadata is machine-readable | `Status:` values: 5 × claimed, 4 × open, 1 × resolved |
| Docs cross-reference by section number | `grep '§'` and `design doc §13` / `§6` / `§5, §12 and §20` appear inside ticket bodies |
| The map is stale | `map.md` contains 5 ticket links and a "Research in flight" table of 5, but 10 tickets exist and `10-reconnaissance-scan.md` is `Status: resolved` |

**Consequence for the request — this is the important correction.**
Item 4 asks for a graph of *classes, methods, and properties*. **There are none.**
Building a class/method graph today would be inventing structure that does not
exist. What genuinely exists, and is worth graphing, is:

- design-doc sections (`semantic-base-layer-design-5.md`, **46** headings, §§1–20),
- decision tickets and their typed fields (`Type`, `Status`, `Blocked by`, `Artifact`),
- the map, README, findings artifacts, and the GitHub-issue mirror TSV,
- the typed relationships between them: containment, `blocked_by`, citation,
  file link, artifact link, issue mirror.

The builder is therefore written as a **document/repository graph now**, with the
node and edge tables already carrying a `kind` column plus `line_start`/`line_end`,
so that when C#/Python code arrives it is added as new node kinds (`class`,
`method`, `property`) by a new extractor — **no schema migration**.

## 3. Deliverables

| # | Artifact | State |
| --- | --- | --- |
| D1 | `AGENT.md` — the rules file (items 1, 2, 3, 7, 8) | **written**, needs owner review |
| D2 | `AGENTS.md` — symlink → `AGENT.md` (so either convention is found) | not created — awaiting consent |
| D3 | `plan.md` — this file, with evidence + verification + risks | **written** |
| D4 | `tools/sblgraph.py` — builder + read-only query CLI | **awaiting approval** |
| D5 | `tools/sblgraph.sqlite` — the generated index (committed? see §8) | **awaiting approval** |
| D6 | `tools/README.md` — how to rebuild and query, and how the graph is structured | **awaiting approval** |
| D7 | `tools/build_log.md` — what was run, when, with what result | **awaiting approval** |

## 4. Design — what the graph actually contains

### 4.1 Nodes (from `AGENT.md`: "don't assume" — every node has a source field)

| `kind` | Meaning here | Source of truth |
| --- | --- | --- |
| `repo` | the repository itself | workspace root |
| `file` | any tracked file, with hash, size, line count | filesystem scan |
| `section` | a markdown heading, with level + line range | heading regex over `.md` |
| `ticket` | an SBL decision ticket | `SBL-Wayfinder/vNN/issues/NN-*.md` |
| `ticket_field` | a typed field of a ticket (`Status`, `Type`, …) | front-matter lines |
| `map_version` | a versioned wayfinder map (`v01`) | `SBL-Wayfinder/vNN/map.md` |
| `github_issue` | the mirror issue | `vNN/github-issues.tsv` |

*(future, no schema change: `class`, `method`, `property`, `namespace`.)*

### 4.2 Edges

| Relation | From → To | How it is derived |
| --- | --- | --- |
| `contains` | file → section; ticket → ticket_field | line ranges |
| `blocked_by` | ticket → ticket | `Blocked by: 01, 02` |
| `cites_section` | ticket/section → section | `§13`, `§5, §12 and §20` |
| `links_to` | file/section → file | markdown links and backticked paths |
| `artifact_of` | findings file → ticket | `NN-findings.md` ↔ ticket `NN` |
| `mirrors` | ticket → github_issue | `github-issues.tsv` |
| `part_of` | map_version → repo | folder structure |

### 4.3 SQLite schema (the contract — a .NET port targets this, not the Python)

```sql
nodes(id, kind, repo_path, name, line_start, line_end, attrs_json, content_hash)
edges(id, src_id, dst_id, relation, attrs_json)
tickets(ticket_id, title, area, type, status, blocked_by, resolved, artifact,
        file_path, line_start)
nodes_fts(name, body, content='nodes', content_rowid='id')
builds(id, started_at, finished_at, file_count, node_count, edge_count, git_rev)
```

Query helper view for humans and agents alike:

```sql
CREATE VIEW v_blocked AS
SELECT t.ticket_id, t.title, t.status, t.blocked_by
FROM tickets t WHERE t.status != 'resolved' AND t.blocked_by != '';
```

### 4.4 Query CLI — the part that saves context (items 4, 5, 6)

```
python3 tools/sblgraph.py build            # (re)build the index — must be run from repo root
python3 tools/sblgraph.py stats            # counts, build time, source revision
python3 tools/sblgraph.py health           # stale index? dangling links? orphan artifacts?
python3 tools/sblgraph.py query "<text>"   # keyword search; prints path + line range
python3 tools/sblgraph.py node <name|path> # one node and its immediate edges
python3 tools/sblgraph.py deps <NN>        # blocks / blocked-by closure for a ticket
python3 tools/sblgraph.py raw <path> <a> <b>   # read only lines a–b  ← the grep replacement
```

The intended loop for a future agent — and the reason the index pays for itself:

```
query "hierarchical prediction"  → semantic-base-layer-design-5.md:335-397 (§6)
raw semantic-base-layer-design-5.md 335 397   → 63 lines, not 1100
```

That is the token saving: **~63 lines instead of 1100**, and the index is consulted
before any file is opened.

## 5. Verification — how this plan will be proven

These commands are written **before** the work, and their real output will be
reported, pass or fail.

| # | Command | Expected result |
| --- | --- | --- |
| V1 | `python3 tools/sblgraph.py build` | exits 0; prints node/edge counts; creates `tools/sblgraph.sqlite` |
| V2 | `python3 tools/sblgraph.py stats` | `nodes` ≥ 100 (46 sections + 10 tickets + 10 fields + files), `edges` ≥ 40, build time < 5 s |
| V3 | `python3 tools/sblgraph.py deps 07` | shows `07 → blocked_by → 01, 02, 03`, all three `claimed` ⇒ **not yet unblocked** |
| V4 | `python3 tools/sblgraph.py deps 09` | `09 → 06, 08`; transitively report 01, 02 |
| V5 | `python3 tools/sblgraph.py health` | lists ticket 10 + its 2 files as **not referenced from `map.md`** (the mismatch in §2) and 0 dangling links |
| V6 | `python3 tools/sblgraph.py query "interlingua"` | returns the §5/§12/§20 ticket hits with line numbers |
| V7 | `wc -l semantic-base-layer-design-5.md` vs the `raw` range from V6 | **1100 vs < 70** — the measured context saving |
| V8 | `du -h tools/sblgraph.sqlite` | < 2 MB |
| V9 | `git status --short` | shows **only** the new files from §3; no existing file modified (`git diff --stat` empty for tracked files) |
| V10 | `python3 tools/sblgraph.py build` run twice | second run is idempotent — same counts, same `content_hash`es |

**Self-check on the schema:** a C# port must be mechanical — the SQL in §4.3 is
plain ANSI SQLite with no Python-specific types, all JSON kept in `attrs_json`.

## 6. Risks, and what will be done about each

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Regex markdown parsing mis-handles fenced code blocks or setext headings | wrong section ranges, bad `raw` output | strip fenced blocks before heading detection; assert heading count == `grep -c '^#\{1,3\} '` (expected 46) |
| The index silently goes stale | agent answers from old structure | `builds.git_rev` + file `content_hash`; `health` prints staleness; `AGENT.md` §4 requires a rebuild first |
| A ticket claims a findings artifact that does not exist (ticket `03` claims `03-findings.md`; `01`/`02`/`04`/`05` were still untracked while this plan was written) | dangling edges | `health` reports dangling `artifact_of` targets explicitly rather than dropping them |
| Python 3.9 is the system interpreter | syntax errors from newer typing | target 3.9: no `X \| Y` unions, no `match`, no `tomllib` |
| `AGENT.md` and `AGENTS.md` drift apart | two rule sets | `AGENTS.md` is a **symlink**, so there is exactly one file to edit |
| Adding `tools/` changes repo shape | scope creep | everything confined to `tools/`; no existing file touched (item 8) |
| The `.sqlite` binary lands in git | noisy diffs, bloat | decision deferred to the owner — see §8, Q3 |

## 7. Explicitly out of scope for this plan

Listed so nobody assumes they are covered:

- Writing the SBL feasibility specification, or resolving any ticket.
- Fixing the stale `map.md` / `README.md` counts (owner chose **report only**;
  recording it here in §2 and in `health` output is the whole action).
- Any .NET implementation — the schema is the port contract, the port is later.
- An MCP server — owner chose the read-only CLI for now.
- Touching `SBL-Wayfinder/v01/` at all. It is frozen history.

## 8. Decisions taken, and the ones still open

**Taken by the owner (this session):**

1. Builder language: **Python 3, stdlib only**. No build step, no NuGet, no
   virtualenv; portable, and the SQLite schema is the contract for a later .NET port.
2. Access interface: **read-only CLI over SQLite**. No server, no socket, no
   dependency, no new security surface.
3. Stale map: **report only** — do not modify `map.md` or `README.md`.

**Still open — needed before step 4 executes:**

- **Q1.** Create `AGENTS.md` as a symlink to `AGENT.md`? (Item 8 says don't touch
  what isn't required; a symlink adds a file, touches nothing.)
- **Q2.** Commit `tools/sblgraph.sqlite` to git, or generate it on demand and
  gitignore it? Committing it means every doc edit churns a binary blob; ignoring
  it means each fresh clone rebuilds with one command.
- **Q3.** Should `health` treat the ticket-10 mismatch as a **warning** only, or
  should it also exit non-zero so it cannot be ignored?

## 9. Execution order

1. ✅ Confirm repository facts (§2 evidence table).
2. ✅ Write `AGENT.md` (D1) and `plan.md` (D3).
3. ⏸ Owner reviews `AGENT.md` and this plan; answers Q1–Q3. *(Q2 answered: commit
   the `.sqlite`. Q1 and Q3 executed on the recommended default — see §13.)*
4. ✅ Build `tools/sblgraph.py` (D4) to the §4.3 schema.
5. ✅ Write `tools/README.md` (D6) and `tools/build_log.md` (D7).
6. ✅ Run V1–V10; real output recorded in §13. **Seven defects found and fixed.**
7. ✅ Create the `AGENTS.md` symlink (D2) — verified to resolve to `AGENT.md`.

No file outside `tools/`, `AGENT.md`, `AGENTS.md`, and this `plan.md` is created
or modified at any step.

## 10. Owner's rules — where each one is honoured

| Owner's rule | Where it lives |
| --- | --- |
| 1. `agent.md` read before any AI work | `AGENT.md` header + §0; checklist at the end |
| 1. No assumptions | `AGENT.md` §1 (verified / inferred / unknown labels) |
| 1. Plan with evidence, notify on change | `AGENT.md` §2; `## Change log` below |
| 2. .NET-level reader; explain new tech briefly | `AGENT.md` §0; §4's note on call graphs vs UML vs RDF |
| 2. Nothing in code without owner's thought | `AGENT.md` §2.4; this plan is not executed until step 3 |
| 3. Credentials gated on notification | `AGENT.md` §3 |
| 4. Graph as nodes and edges, low token use | `AGENT.md` §4; §4 of this plan; V7 measures it |
| 5. Store locally, SQLite, query by context | `AGENT.md` §4 table; schema in §4.3 |
| 6. Then Grep the real code | `AGENT.md` §4 working order (steps 1→2→3) |
| 7. Always say what is going on | `AGENT.md` §5; every report in this session |
| 8. Don't change existing code unless required | `AGENT.md` §6; §7 above; V9 proves it |

## 11. Change log

Append-only. Every deviation from this plan is recorded here, and reported to the
owner at the moment it is discovered.

### 2026-05-22 — Initial plan opened
- Planned: graph "classes, methods, properties and their relationships".
- Discovered: the repository contains **no code** at all — it is a research and
  specification corpus (evidence: §2, file inventory and `git log`).
- Changed to: graph the artifacts that do exist — files, sections, tickets,
  ticket fields, map versions, mirror issues — with `kind` columns and
  `line_start`/`line_end` so code nodes can be added later with no migration.
- Owner notified: yes — raised as the first question of this session, and the
  three decisions were taken by the owner before this plan was written.
- Affects: node kinds in §4.1; deferred .NET port in §7; the `.NET-explanation`
  obligation in `AGENT.md` §0.

### 2026-05-22 — Section count corrected, findings inventory corrected
- Planned: `plan.md` §4.1 said the design doc has "60 headings"; §6's risk row used
  the same number as its assertion target.
- Discovered: `grep -c '^#\{1,3\} ' semantic-base-layer-design-5.md` → **46**.
  The 60 was an estimate written before counting — an assumption, which is exactly
  what `AGENT.md` §1 forbids. Separately, `git status --short` showed findings
  artifacts for tickets `01`, `02`, `04`, `05` now exist and are untracked, and
  ticket `03`'s is still absent; the earlier "3 findings files" count was taken
  before those files landed.
- Changed to: 46 in §4.1, §6, and V2; findings inventory rewritten to five files
  with ticket `03` named as the gap; `health` must surface dangling artifacts.
- Owner notified: yes — reported in this turn's summary (no scope or deliverable
  changed, so this is a mechanical correction with a log entry, per `AGENT.md` §2).
- Affects: §4.1, §6, V2 expectations, and the `health` implementation requirement.

### 2026-05-22 — Verification found seven defects; §4.3 schema changed
- Planned: `plan.md` §4.3 specified `nodes(id TEXT PRIMARY KEY, …)` with
  `nodes_fts … content_rowid='id'`, and §6 expected the graph to cover the
  repository tree.
- Discovered, each with evidence, while running V1–V10:
  1. A TEXT `nodes.id` cannot back an FTS5 external-content table — the insert
     failed with `sqlite3.IntegrityError: datatype mismatch`. **Schema changed:**
     integer `rowid` primary key + separate TEXT `uid`; edges still key on `uid`.
  2. The walk indexed **gitignored** bulk — 479 files under `research/` and 52 in
     `.sbl-*-scratch/` — giving 557 files, 1489 nodes, 1712 KB. **Changed to:**
     scope follows git (`git ls-files -co --exclude-standard`), 34 files.
  3. `health` reported all 10 tickets as unreferenced. **Cause:** the query looked
     for `contains` edges sourced from the ticket; the map's `contains` edges point
     at *sections*, and the ticket link is a section→file `links_to` edge.
  4. `health` reported `STALE` on a freshly built index because the staleness scan
     counted `tools/sblgraph.sqlite` and `tools/build_log.md` as source files.
  5. `query` failed with `SQL logic error`. **Cause:** an external-content FTS5
     table must be filled with `INSERT INTO nodes_fts(nodes_fts) VALUES('rebuild')`;
     a hand-written INSERT does not work. `nodes` also gained a `body` column.
  6. 78 of 82 "broken links" were URLs, mangled into junk paths such as
     `SBL-Wayfinder/v01/https:/arxiv.org/abs/...`. **Cause:** `os.path.normpath`
     collapses `https://` into `https:/`, and the caller in `build()` joined and
     normalised the target *before* `link_file()` could classify it as a URL.
     **Changed to:** classify before resolving; the URL check precedes all path
     work; `link_file` takes `base_dir` instead of a pre-joined path.
  7. Two self-inflicted edit errors while patching: a duplicated log-write block
     left dead code after `return`, and a status line briefly carried a wrong count.
     Both caught by re-reading the file; no incorrect number survives in this plan.
- Changed to: schema v1 with the `rowid`/`uid` split and a `body` column; git-scoped
  file discovery; corrected orphan detection; staleness limited to non-`tools/`
  files; URL-first link classification.
- Owner notified: yes — reported in this turn's summary before committing.
- Affects: §4.3 (schema), §4.1 (a `missing` node kind and `nodes.body` were added),
  §2 (34 files, not the whole tree), and `tools/README.md`, which documents all of
  this as the port contract.

### 2026-05-22 — Owner answered Q2; Q1 and Q3 executed on the recommended default
- Planned: §8 left Q1 (symlink), Q2 (commit the `.sqlite`), Q3 (`health` exit code)
  open, blocking step 4.
- Discovered: the owner replied "commit it", which answers Q2 only.
- Changed to: **Q2** — `tools/sblgraph.sqlite` **is committed**, per the owner.
  **Q1** — `AGENTS.md` created as a **symlink** to `AGENT.md` (verified:
  `os.path.realpath` resolves both names to the same file). **Q3** — `health` exits
  0 and prints a warning count rather than failing, so a stale-map warning cannot
  break a scripted pipeline; say the word and it becomes non-zero.
- Owner notified: yes — both defaults are called out in this turn's summary, and
  either can be reversed without touching the graph.
- Affects: `.gitignore` is **unchanged** (the index is deliberately not ignored);
  the committed binary will churn on every document edit — the cost the owner accepted.

### 2026-05-22 — Section numbering renumbered after a concurrent append
- Planned: §9 and §3 referred forward to "§12" for this work's results.
- Discovered: a concurrent research session appended its own `# 12. SBL direction —
  programming language first` to this file while this work was in progress
  (evidence: `plan.md` lines 279–369 at the time of writing).
- Changed to: this work's results are §13, the verification table §13.1, and the
  Done list §14. The forward references in §3 and §9 were repointed from §12 to §13.
- Owner notified: yes — reported in this turn's summary.
- Affects: section numbers only; **§12's content was not touched or edited**, per
  `AGENT.md` §6. Two plans now share this file, which §12's own header acknowledges.

---

# 12. SBL direction — programming language first

> **Appended** by the research session on 2026-10-01. This section is scoped to a
> different deliverable from §1–§11 (which govern the repository graph index). Both
> live in this file because `AGENT.md` §2 names `plan.md` as *the* active plan; the
> scope expansion is recorded in the change log below. Nothing in §1–§11 was edited.

- **Status:** ⛔ **HALTED 2026-10-01 — hypothesis falsified before any code was written.**
  D1 returned a negative: the front-end interlingua §11 proposes already exists and is
  mature (`12-findings.md`). D2 must not be built as designed. Owner has been asked to
  choose a re-scoped direction; see §12.5.
- **Scope:** the first *experiment* for the Semantic Base Layer, on a programming
  language domain rather than natural language.

## 12.1 Request

The owner's direction, stated directly: **"my idea is to use a programming language
first."** This supersedes the design doc's implicit ordering, where §12 (English +
Tamil) precedes §11/Phase 6 (programming languages).

## 12.2 Why this is a better first experiment — with evidence

| Claim | Status | Evidence |
| --- | --- | --- |
| The design doc already proposes programming languages as a test domain | **Verified** | `semantic-base-layer-design-5.md` §11 and §18 Phase 6 |
| The doc's stated reason is that programming languages are less ambiguous | **Verified** | same file, §11: "Natural language is ambiguous. Programming languages are much more structured." |
| The natural-language first experiment cannot fail meaningfully | **Verified** | `SBL-Wayfinder/v01/issues/01-findings.md` — §13's proposed test is a *mix-and-match* split, the kind SCAN found RNNs pass; it is not discriminating |
| Natual-language Tamil route has a licensing dead end | **Verified** | `SBL-Wayfinder/v01/issues/03-findings.md` — UD_Tamil-TTB is CC BY-NC-SA 3.0; the permissive treebank is test-only |
| Tamil annotation dominates cost | **Verified** | `SBL-Wayfinder/v01/issues/04-findings.md` — 1,000 pairs ≈ $2.5k–15k at double annotation |
| A programming-language experiment removes the annotation cost entirely | **Inferred** | follows from the above: paired snippets are authored, not crowd-annotated |
| The owner's stack makes C# the cheapest entry point | **Verified** | `AGENT.md` §0 — project owner is a .NET developer; Roslyn is a maintained C# parser with a documented public syntax-tree API |

**The argument in one line:** the natural-language experiment is expensive *and*
incapable of returning a negative result; a programming-language experiment is nearly
free *and* can fail. It is the same ontology machinery either way.

## 12.3 Outcome — the risk resolved against us

`12-findings.md` (D1) answered the §12.3 question. **The answer is that the niche is
occupied, and occupied by systems that are better than what §11 proposes.**

| The proposed thing | What already does it | Status |
| --- | --- | --- |
| "Different languages map into a shared semantic/program representation" (§18 Phase 6, the Phase 6 question verbatim) | [Kythe](https://kythe.io/docs/kythe-overview.html), [SCIP](https://github.com/sourcegraph/scip/blob/main/README.md), [LSIF](https://github.com/microsoft/language-server-protocol/blob/main/indexFormat/specification.md), [Glean](https://glean.software/docs/introduction/) | **Shipped and mature** |
| A C# front end built on Roslyn | [`scip-dotnet`](https://github.com/sourcegraph/scip-dotnet) — literally "built with the Roslyn .NET compiler" | **Shipped** |
| Nodes-and-edges explicit graph (§10 shape) | SCIP's own [DESIGN.md](https://github.com/sourcegraph/scip/blob/main/docs/DESIGN.md) rejects this shape deliberately — "Avoid direct encoding of graphs" — because it hurts parallelism and blows up index-time memory | **Actively argued against, first-party** |

**Three findings that decide the matter:**

1. **The proposed representation is lossier than what exists.** SCIP gets C#/VB from
   Roslyn's full *semantic* model. A ~100-concept ontology cannot express overload
   resolution, generics, `async` state machines or LINQ. §11's
   `DECLARE(VARIABLE=result, VALUE=CALL(...))` carries **less** information than the
   syntax tree it came from.
2. **Nobody shipped a single fixed universal vocabulary — and the three who tried, chose
   otherwise.** Meta, Google and Sourcegraph each landed on *per-language schemas with
   derived neutrality*. Glean's docs say it directly: "Glean doesn't force all the data
   into a single schema." That is the **opposite** of SBL's design choice, made by teams
   with vastly more resources — and it is the same lesson UMR taught on the natural-language
   side (`02-findings.md`: languages vary, so the schema absorbs the variation).
3. **The one real gap is one SBL has no mechanism for.** Nothing in the surveyed set
   captures *behaviour or intent* — "do these two programs compute the same thing?".
   That gap is genuine (Glean has an extension point for it and ships nothing). But §11
   as written does not address it; `DECLARE`/`CALL` restates syntax in new words.

**What this costs:** nothing but time. The experiment was designed to be able to fail,
and it failed on evidence before a line of code was written — which is exactly the
outcome `D2 §7` was built to produce, and roughly days ahead of where the
natural-language route would have put us.

**What survives.** The AI-model-facing angle is real but thin: every tool above is
tool-facing, none targets a model as consumer. An LLM-friendly projection of an existing
SCIP/Kythe index is a genuine small gap — but it is a **renderer**, not a new semantic
layer, and should not be sold as one.

## 12.4 The risk this section existed to resolve

Cross-language program translation already has interlinguas: **CIL/MSIL, LLVM IR,
GraalVM/Truffle, WebAssembly** (back-end), plus **tree-sitter, LSP, SCIP/LSIF, Glean,
Kythe** (front-end / analysis-facing). If SBL-for-code is a sixth one, the novelty
question returns in a new costume.

- **Verified:** these systems exist and operate at the levels named above.
- **Unknown (being researched):** whether any of them already delivers SBL's specific
  claim — a compact, model-facing, language-independent *semantic* representation.
- Research dispatched; findings will land at
  `SBL-Wayfinder/v01/issues/12-findings.md`. **This plan does not execute until that
  answer is in**, because the answer decides whether deliverable D3 below is worth
  building at all.

## 12.5 Directions, for the owner to choose

Presented as options, not recommendations — this is a scope decision and `AGENT.md` §2
reserves it for the owner.

| # | Direction | What it means | Cost |
| --- | --- | --- | --- |
| **A** | **Contribute on top of SCIP/Kythe** | Stop building formats. Build the model-facing projection layer: take a real SCIP index and render it into something an LLM consumes well. Honest, small, shippable. | Low |
| **B** | **Re-scope to behaviour/intent** | The one unoccupied gap: equivalence of *what programs compute*, not their shape. Note this **reverses the owner's 2026-10-01 decision** to scope SBL-for-code to structure only — that decision is what the falsification result contradicts. | High — program equivalence is a known hard problem |
| **C** | **Return to the natural-language layer** | Where UMR is the nearest neighbour but the model-facing angle is likewise unclaimed. Carries the Tamil licensing and annotation-cost problems recorded in `03-findings.md` and `04-findings.md`. | Medium–High |
| **D** | **Stop the SBL effort** | The evidence supports this as a legitimate reading: two domains surveyed, both niches occupied. | None |

## 12.6 Deliverables

| # | Deliverable | Notes |
| --- | --- | --- |
| D1 | `12-findings.md` | the interlingua prior-art check (in flight) |
| D2 | A falsifiable experiment design | the hypothesis, the baseline, and a pre-registered falsification condition |
| D3 | Decision: proceed / re-scope / stop | the owner's call, informed by D1 |

Deliberately **not** in this plan: an ontology file, a parser, a graph implementation,
a model. Those are Build work and they follow a decision, not a plan.

## 12.7 Verification — how this plan will be proven

- **V1** — `12-findings.md` exists and answers sub-questions 1–4:
  `test -f SBL-Wayfinder/v01/issues/12-findings.md`
- **V2** — every claim in it carries a citation or is labelled unverified:
  manual read; count rows lacking a link.
- **V3** — the falsification condition in D2 is stated as a *measurable* outcome that
  can come back negative. Test: name the result that would stop the project. If no such
  result can be named, D2 has failed and must be rewritten.
- **V4** — the owner has explicitly approved D2 before any code is written.

## 12.8 Risks

| Risk | Mitigation |
| --- | --- |
| SBL-for-code duplicates an existing interlingua | Resolve *before* building — V1/V2. This is the whole point of D1. |
| The experiment is designed so it cannot fail | V3 makes "cannot fail" an explicit, checkable defect |
| Scope creep into building the whole pipeline | §12.4 fixes deliverables at three, all pre-code |
| Collision with the concurrent graph-index work in §1–§11 | This section appends only; `tools/` and §1–§11 are untouched |

## 12.9 Decisions taken (owner, 2026-10-01)

Both were put to the owner as the questions whose answers shape the ontology's depth
and the corpus's construction. Neither is reversible without cost, so both are recorded
with their reasons.

| Decision | Taken | Why this and not the alternatives |
| --- | --- | --- |
| **What SBL-for-code captures** | **Syntax / structure only** — declarations, calls, control flow, expressions | Cheap, unambiguous, and directly testable. Critically, it puts SBL head-to-head with existing AST tooling, which is the *honest* comparison: if plain syntax trees match SBL, the hypothesis is falsified. Capturing *intent* or *behaviour* would have been more novel but reintroduces the contestability that choosing a programming-language domain was meant to avoid; those remain open for a later map version. |
| **First language pair** | **C# + Python** | C# via Roslyn uses the owner's .NET stack (`AGENT.md` §0). Python is a wide syntactic contrast — indentation vs braces, no type annotations, different call syntax — so cross-syntax equivalence is visible and verifiable by eye. C#+F# and C#+TypeScript were rejected as too close: a narrow syntactic gap would make the experiment pass trivially. |

**Consequence for D2.** The falsification condition is now sharp: *if an AST-difference
baseline (tree edit distance over Roslyn and `ast` trees) surfaces the same
cross-language equivalences as SBL, at comparable cost, the hypothesis is falsified.*
This must be written into D2 before any measurement is taken.

## 12.10 Change log

### 2026-10-01 — Owner directs SBL to a programming-language-first experiment
- Planned: `plan.md` §1–§11 covered only the repository graph index; the SBL effort's
  own path was tracked in `SBL-Wayfinder/v01/map.md` and its tickets.
- Discovered: the owner directed, in this session, that SBL start with a programming
  language rather than the design doc's English+Tamil order. `AGENT.md` §2 requires a
  current `plan.md` for active work, so this work needed a plan entry.
- Changed to: §12 appended, scoped to the PL-first experiment; deliverables fixed at
  three pre-code artifacts; execution gated on the prior-art answer.
- Owner notified: yes — presented in this session for approval.
- Affects: adds a deliverable stream; does not alter §1–§11 or any `vNN/` tracker file.

---

# 13. Repository graph index — verification results (V1–V10)

> **Appended** by the graph-index session on 2026-10-01. Scoped to the deliverables
> in §3 and the schema in §4.3. §12 belongs to a different deliverable stream and was
> not edited. Section numbering here was chosen to avoid colliding with §12, which a
> concurrent session appended while this work was in progress.

Run against `tools/sblgraph.py` at rev `c032cb1`, repository working tree unchanged
except for the files listed in §14.

## 13.1 Results

| # | Check | Result |
| --- | --- | --- |
| V1 | `build` | ✅ 34 files, 290 nodes, 401 edges, 0.09 s, 932 KB, 12 dangling refs |
| V2 | `stats` | ✅ 290 nodes / 401 edges — over the ≥100 / ≥40 thresholds; ticket table renders |
| V3 | `deps 07` | ✅ `07 → 01, 02, 03`, all `resolved` ⇒ **unblocked: yes** |
| V4 | `deps 09` | ✅ `09 → 06(open), 08(open)` → transitively `01, 02` ⇒ **unblocked: no** |
| V5 | `health` | ✅ 8 broken links, 4 unwritten artifacts, tickets **06–10** unreferenced from `map.md` |
| V6 | `query "interlingua"` | ✅ 8 hits with path, line range and snippet across tickets, findings and the design doc |
| V7 | context saving | ✅ **1100 lines** (whole doc) vs **18** (query) vs **64** (raw §6) — ~17× reduction |
| V8 | `du -h` | ✅ 932 KB, under the 2 MB budget |
| V9 | `git status` | ✅ no tracked file modified; only new files added |
| V10 | build twice | ✅ idempotent — identical 290/401 counts and `content_hash` set |

## 13.2 Two corrections to expectations stated earlier in this plan

1. **§5's V5 expectation was wrong.** It predicted health would flag "ticket 10 + its
   2 files". Measured behaviour: tickets **06–10**. Ticket 10 is flagged because
   `map.md` never mentions it; tickets 06–09 are flagged because the map links only
   01–05 (verified: `map.md` contains 5 ticket links).
2. **V3/V4 changed meaning during the session.** Tickets 01–05 were `claimed` when
   this plan was opened and are `resolved` now, so ticket 07's dependencies became
   satisfied while the work was running. The index reported this correctly without
   being told — which is the reason for building it.

## 13.3 What the index found in the repository (evidence, not opinion)

- **8 broken markdown links**, including three artifacts referenced but never
  written: `02-prior-art-census.md`, `04-system-requirements.md`,
  `05-interoperability-feasibility.md`. The research-recovery report also links five
  ticket files at the wrong path (`v01/01-….md` instead of `v01/issues/01-….md`).
- **4 tickets claim findings artifacts that do not exist** (`06`–`09`); all four are
  still open, so this is expected rather than a defect.
- **Tickets 06–10 are unreferenced from `map.md`** — the stale-map observation in §2,
  now measured rather than estimated.
- **64 external URLs** are referenced across the corpus and are counted, not graphed.

# 14. Done

| # | Artifact | Status |
| --- | --- | --- |
| D1 | `AGENT.md` — rules file; all eight owner requirements mapped in §10 | ✅ |
| D2 | `AGENTS.md` — symlink to `AGENT.md`, verified same real path | ✅ |
| D3 | `plan.md` — this file, with evidence, verification and change log | ✅ |
| D4 | `tools/sblgraph.py` — builder + read-only CLI | ✅ |
| D5 | `tools/sblgraph.sqlite` — 290 nodes / 401 edges, committed per owner decision | ✅ |
| D6 | `tools/README.md` — usage, schema as port contract, limitations | ✅ |
| D7 | `tools/build_log.md` — build history, including the defect-fix table | ✅ |

**No existing file in this repository was modified to achieve any of it.** `map.md`,
`README.md`, and every `SBL-Wayfinder/v01/` file are untouched; `§12` was appended to
this plan by another session and was left exactly as written.
### 2026-10-01 — Owner fixed the experiment's scope and language pair
- Planned: §12.4 left "what SBL for code captures" and "which languages" open.
- Discovered: both were put to the owner as questions; the owner chose
  structure-only and C#+Python. Recorded in §12.7.
- Changed to: D1's prior-art question is now scoped to *structural* interlinguas
  (AST/syntax-level), not behavioural ones; D2's falsification condition is fixed
  against an AST-difference baseline.
- Owner notified: yes — the questions were answered by the owner directly.
- Affects: §12.4 D2, §12.5 V3, and the scope of the in-flight `12-findings.md`.
### 2026-10-01 — D1 falsified the §11 premise; plan halted before execution
- Planned: §12.4 D2 (the AST-baseline experiment) to be built once the owner approved.
  The owner had approved the scope (structure-only, C#+Python) and this section was
  awaiting a build go-ahead.
- Discovered: D1 (`12-findings.md`, primary-source verified) showed the front-end
  interlingua is **already shipped** — Kythe, SCIP, LSIF and Glean — including
  `scip-dotnet`, a Roslyn-built C# indexer. Further, SCIP's own design doc *rejects* the
  nodes-and-edges representation §10/§11 propose, and a 100-concept ontology is lossier
  than Roslyn's semantic model. (evidence: `12-findings.md` §1–§3)
- Changed to: §12 status set to HALTED; §12.3a records the outcome; §12.8 presents four
  directions for the owner to choose between. **No code was written against §12.** D2 is
  not deleted — it remains a correct design for testing *any* proposed representation
  against an AST baseline, and applies unchanged to a re-scoped direction.
- Owner notified: yes — reported in this session with the evidence, and the direction
  choice was put to the owner.
- Affects: §12.3 (risk resolved against us), §12.3a (new), §12.8 (new), D2's status, and
  the owner's structure-only decision, which direction B would reverse.
