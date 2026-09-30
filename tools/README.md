# tools/ — the repository graph index

`tools/sblgraph.py` builds a **nodes-and-edges index** of this repository into
`tools/sblgraph.sqlite`, so an agent (or a human) can find the one section,
ticket, or artifact that matters and read **only those lines** — instead of
pulling whole files into context.

Governed by [`AGENT.md`](../AGENT.md) §4. Design and verification contract:
[`plan.md`](../plan.md) §4.

No dependencies. Python 3.9 standard library only (`sqlite3`, `re`, `json`,
`hashlib`, `subprocess`). No build step, no package install, no server.

## Commands

Run everything from the repository root.

```bash
python3 tools/sblgraph.py build                     # (re)build the index
python3 tools/sblgraph.py stats                     # counts, build time, ticket table
python3 tools/sblgraph.py health                    # stale? broken links? tickets off the map?
python3 tools/sblgraph.py query "interlingua"       # keyword search -> path + line range
python3 tools/sblgraph.py node semantic-base-layer-design-5.md
python3 tools/sblgraph.py deps 07                   # upstream + downstream ticket closure
python3 tools/sblgraph.py raw <path> <start> <end>  # read ONLY lines start–end
python3 tools/sblgraph.py raw --grep "hierarchical softmax" -C 3
python3 tools/sblgraph.py sql "SELECT kind, COUNT(*) FROM nodes GROUP BY kind"
```

### Why this saves context

Measured on this repository (`plan.md` V7):

| Approach | Lines pulled into context |
| --- | --- |
| Read the whole design doc | **1100** |
| `query` → 8 matching sections | **18** |
| `raw` the one section the query found (§6, lines 335–397) | **64** |
| `raw --grep "…" -C 3` for one phrase | **55** |

The intended loop: `query` to locate → `raw` to read only that range → `grep` to
confirm against the real file.

## What the graph contains

**Nodes** (`nodes.kind`) — every node carries `repo_path`, `line_start`,
`line_end`, and an `attrs_json` blob:

| `kind` | Meaning |
| --- | --- |
| `repo` | the repository root |
| `file` | a git-visible file (tracked or untracked-not-ignored) |
| `section` | a markdown heading, with its line range and body text |
| `ticket` | an SBL decision ticket |
| `ticket_field` | one typed field of a ticket (`Type`, `Status`, `Blocked by`, …) |
| `map_version` | a versioned wayfinder map folder (`v01`) |
| `github_issue` | a row of the GitHub mirror TSV |
| `missing` | a reference target that does not exist — kept so `health` can report it |

**Edges** (`edges.relation`): `contains`, `blocked_by`, `cites_section`,
`links_to`, `artifact_of`, `mirrors`, `part_of`, `documents`, and the two
problem relations `missing_ref` / `missing_artifact`.

## Schema (v1)

The SQL in `SCHEMA_SQL` is the **port contract**: it is plain SQLite, and all
structured data lives in `attrs_json`, so a C# port targets the same tables.

```sql
nodes(rowid INTEGER PK, uid TEXT UNIQUE, kind, repo_path, name, body,
      line_start, line_end, attrs_json, content_hash)
edges(id, src_id, dst_id, relation, attrs_json)      -- src/dst hold nodes.uid
tickets(ticket_id, title, area, type, status, blocked_by, resolved, artifact,
        file_path, line_start)
nodes_fts USING fts5(name, body, content='nodes', content_rowid='rowid')
builds(id, started_at, finished_at, file_count, node_count, edge_count, git_rev,
       schema_version)
```

Two detail that matter if you extend this:

- **`uid` vs `rowid`.** Edges reference the readable `uid` (`ticket:07`).
  `nodes_fts` is an external-content FTS5 table and must join on the *integer*
  `rowid`, which is why `nodes` has `rowid INTEGER PRIMARY KEY` **and** a separate
  TEXT `uid`. Collapsing the two makes full-text search fail with
  `SQL logic error`.
- **FTS population** uses the special `INSERT INTO nodes_fts(nodes_fts)
  VALUES('rebuild')` command after nodes are inserted. A hand-written `INSERT`
  into an external-content FTS table does not work.

Convenience views: `v_blocked` (unresolved tickets with dependencies),
`v_frontier` (open, unblocked, unclaimed).

## Scope

The graph covers what **git sees**: tracked files plus untracked-but-not-ignored
files — currently 34 files. Gitignored bulk (the `research/` corpora and
`.sbl-*-scratch/`) is deliberately excluded; indexing it produced 559 files,
1489 nodes, and a 1.7 MB database of downloaded HTML that says nothing about
project structure. The build prints how many files it excluded.

External URLs are counted, not graphed (`external URLs referenced: 64`).

## Adding code later — no schema migration needed

There is no application code in this repository yet, so there are no `class`,
`method`, or `property` nodes. When code arrives, add **new node kinds** and a
parser that fills `line_start`/`line_end`:

| `kind` | `name` | `attrs_json` | edges to add |
| --- | --- | --- | --- |
| `class` | class name | `namespace`, `base`, `interfaces`, `modifiers` | `contains` (file→class), `inherits`, `implements` |
| `method` | method name | `signature`, `return_type`, `params`, `visibility` | `contains` (class→method), `calls`, `overrides` |
| `property` | property name | `type`, `accessors` | `contains` (class→property) |

The existing tables, the CLI, `query`, `raw`, and `deps` all keep working
unchanged — a new extractor only inserts more rows.

## Known limitations — read before trusting a number

- **Markdown parsing is regex-based**, not a real CommonMark parser. Fenced code
  blocks are blanked out before heading detection, so `#` inside a code sample is
  not treated as a heading. Setext headings (`Title` underlined with `===`) are
  **not** recognised. Nested list indentation is not modelled.
- **Staleness is detected, not automatic.** `health` compares source mtimes and
  the recorded `git_rev`. It warns; it does not rebuild. Rebuild before answering
  questions if it says `STALE`.
- **`missing_ref` edges are real findings, not noise.** They mean a markdown link
  points at a file that does not exist. Current known-good set: 8 broken links
  and 4 tickets claiming findings artifacts not yet written.
- **`ticket_field` nodes hold only the fields listed in `RE_FIELD`** (`Type`,
  `Status`, `Blocked by`, `Resolved`, `Artifact`, `Label`). A new field name in a
  ticket is silently ignored — add it to the regex.

## Build history

Every build appends one line to `tools/build_log.md`.
