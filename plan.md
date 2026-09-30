# plan.md — Active work plan

> Governed by `AGENT.md`. Every claim below is either **verified** (with the
> command that proves it) or explicitly labelled **inferred**.
> Read this file before acting; update it before executing.

- **Status:** awaiting owner approval to execute step 4
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
3. ⏸ Owner reviews `AGENT.md` and this plan; answers Q1–Q3.
4. ⏸ Build `tools/sblgraph.py` (D4) exactly to the §4.3 schema.
5. ⏸ Write `tools/README.md` (D6) and `tools/build_log.md` (D7).
6. ⏸ Run V1–V10 and report the real output, including anything that fails.
7. ⏸ Create the `AGENTS.md` symlink (D2) if Q1 is yes.

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
