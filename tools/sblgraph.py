#!/usr/bin/env python3
"""sblgraph - repository graph builder and read-only query CLI for the SBL project.

Builds a nodes/edges index of this repository into tools/sblgraph.sqlite so that an
agent or a human can locate the one section, ticket or artifact that matters, and
then read only those lines - instead of pulling whole files into context.

Governed by AGENT.md. Design and schema contract: plan.md section 4.
Targets Python 3.9 (system interpreter on this machine): no `X | Y` unions, no match.

Usage (run from the repository root):
    python3 tools/sblgraph.py build
    python3 tools/sblgraph.py stats
    python3 tools/sblgraph.py health
    python3 tools/sblgraph.py query "hierarchical prediction"
    python3 tools/sblgraph.py node semantic-base-layer-design-5.md
    python3 tools/sblgraph.py deps 07
    python3 tools/sblgraph.py raw semantic-base-layer-design-5.md 335 397
    python3 tools/sblgraph.py raw --grep "hierarchical softmax" -C 3
"""

import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB_PATH = os.path.join(HERE, "sblgraph.sqlite")
LOG_PATH = os.path.join(HERE, "build_log.md")
SCHEMA_VERSION = 1

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".idea", ".vscode"}
SKIP_SUFFIX = (".sqlite", ".sqlite-journal", ".sqlite-wal", ".sqlite.tmp", ".pyc")
TEXT_SUFFIX = (
    ".md", ".tsv", ".json", ".jsonl", ".txt", ".conllu", ".py", ".cs",
    ".csproj", ".sln", ".html", ".css", ".js", ".ts", ".yml", ".yaml",
)

RE_FENCE = re.compile(r"^\s*(```|~~~)")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
RE_MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
RE_TICKET_REF = re.compile(r"\b(\d{2})-findings\.md\b")
RE_ISSUES_LINK = re.compile(r"(?:^|/)issues/(\d{2})-[a-z0-9-]+\.md")
RE_FIELD = re.compile(r"^(Type|Status|Blocked by|Resolved|Artifact|Label):\s*(.*?)\s*$")
RE_SEC_REF = re.compile(r"§\s*(\d{1,2})")
RE_WORD = re.compile(r"[A-Za-z0-9_.\-/]+")


# --------------------------------------------------------------------------- util

def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def sha1(text):
    return hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()


def git_rev():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        )
        return out.stdout.decode().strip() or "unknown"
    except OSError:
        return "unknown"


def strip_fences(text):
    """Blank out fenced code blocks (keeping line numbering) so headings inside
    code samples are never mistaken for real markdown headings."""
    lines = text.splitlines()
    out = []
    inside = False
    for line in lines:
        if RE_FENCE.match(line):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    return out


def make_id(kind, key):
    return "%s:%s" % (kind, key)


# --------------------------------------------------------------------------- scan

def scan_files():
    found = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(SKIP_SUFFIX):
                continue
            path = os.path.join(dirpath, name)
            if name == os.path.basename(DB_PATH):
                continue
            if os.path.islink(path) and not os.path.exists(path):
                continue
            found.append(rel(path))
    return sorted(found)


# --------------------------------------------------------------------------- build

class Graph(object):
    def __init__(self, conn):
        self.conn = conn
        self.nodes = {}          # node id -> dict
        self.edges = []          # (src_id, dst_id, relation, attrs)
        self.sec_index = {}      # (file, section_number) -> node id
        self.tickets = {}        # "01" -> dict
        self.dangling = []

    def add_node(self, kind, key, repo_path="", name="", line_start=None,
                 line_end=None, attrs=None):
        nid = make_id(kind, key)
        if nid in self.nodes:
            return nid
        self.nodes[nid] = {
            "kind": kind, "repo_path": repo_path, "name": name,
            "line_start": line_start, "line_end": line_end,
            "attrs": attrs or {},
        }
        return nid

    def add_edge(self, src, dst, relation, attrs=None):
        if src is None or dst is None:
            return
        self.edges.append((src, dst, relation, attrs or {}))

    def link_file(self, target, src_id, relation, attrs=None):
        """Add an edge to `target` (repo-relative path) if it exists on disk.

        If it does not exist, still add the edge - pointing at a `missing` marker
        node - so `health` can report it instead of the reference vanishing."""
        target = target.strip().lstrip("./")
        if not target or target.startswith(("http://", "https://", "#", "mailto:")):
            return False
        target = os.path.normpath(target).replace(os.sep, "/")
        nid = make_id("file", target)
        if nid not in self.nodes:
            self.dangling.append((src_id, relation, target))
            marker = self.add_node("missing", target, repo_path="", name=target,
                                   attrs={"target": target, "relation": relation})
            self.add_edge(src_id, marker, "missing_ref", attrs or {"target": target})
            return False
        self.add_edge(src_id, nid, relation, attrs)
        return True


def parse_markdown(g, path, text):
    """Create `section` nodes for a markdown file and register §N lookups."""
    lines = strip_fences(text)
    raw_lines = text.splitlines()
    fid = make_id("file", path)
    headings = []
    for i, line in enumerate(lines, start=1):
        m = RE_HEADING.match(line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2)))

    for idx, (start, level, title) in enumerate(headings):
        end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(raw_lines)
        num = None
        m = re.match(r"^(\d{1,2})(?:\.(\d{1,2}))?\b", title)
        if m and level <= 3:
            num = m.group(1)
        sid = g.add_node(
            "section", "%s#L%d" % (path, start), repo_path=path, name=title,
            line_start=start, line_end=end,
            attrs={"level": level, "section_number": num,
                   "body": "\n".join(raw_lines[start - 1:end])},
        )
        g.add_edge(fid, sid, "contains", {"level": level})
        if num is not None and num not in g.sec_index:
            g.sec_index[num] = sid
    return headings


def parse_ticket(g, path, text):
    """Parse an SBL decision ticket. Returns the ticket id ('01'...) or None."""
    base = os.path.basename(path)
    m = re.match(r"^(\d{2})-", base)
    if not m or base.endswith("-findings.md"):
        return None
    tid = m.group(1)
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip() if lines else base
    fields = {}
    for line in lines[:16]:
        fm = RE_FIELD.match(line)
        if fm:
            fields.setdefault(fm.group(1), fm.group(2))
    blocked_raw = fields.get("Blocked by", "")
    blocked = re.findall(r"\d{1,2}", blocked_raw) if blocked_raw not in ("", "—", "-") else []
    area = ""
    am = re.match(r"^SBL \|\s*([A-Za-z]+)\s*\|", title)
    if am:
        area = am.group(1).lower()

    attrs = {
        "title": title, "area": area,
        "type": (fields.get("Type", "") or "").lower(),
        "status": (fields.get("Status", "") or "").lower(),
        "blocked_by": ",".join(blocked),
        "resolved": fields.get("Resolved", ""),
        "artifact": fields.get("Artifact", ""),
        "body": text,
    }
    g.tickets[tid] = dict(attrs, file_path=path, ticket_id=tid)
    fid = make_id("file", path)
    tid_node = g.add_node("ticket", tid, repo_path=path, name=title,
                          line_start=1, line_end=len(lines), attrs=attrs)
    g.add_edge(fid, tid_node, "contains")

    for key in ("Type", "Status", "Blocked by", "Resolved", "Artifact"):
        if key in fields:
            g.add_node("ticket_field", "%s@%s" % (tid, key), repo_path=path,
                       name=key, line_start=1, line_end=len(lines),
                       attrs={"ticket": tid, "value": fields[key]})
            g.add_edge(tid_node, make_id("ticket_field", "%s@%s" % (tid, key)),
                       "contains", {"field": key, "value": fields[key]})

    # artifact claim: "NN-findings.md"
    for art in set(RE_TICKET_REF.findall(text)):
        if art == tid:
            g.add_edge(tid_node, make_id("file", os.path.join(os.path.dirname(path), art)),
                       "artifact_claim", {"artifact": art})
    return tid


def parse_github_tsv(g, path, text):
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return
    header = lines[0].split("\t")
    fid = make_id("file", path)
    for row in lines[1:]:
        cells = row.split("\t")
        if len(cells) < 5:
            continue
        rec = dict(zip(header, cells))
        num = rec.get("ticket", "?")
        key = "%s/%s" % (rec.get("issue", "?"), num)
        nid = g.add_node("github_issue", key, repo_path=path, name=rec.get("title", ""),
                         attrs=rec)
        g.add_edge(fid, nid, "contains")
        t = g.tickets.get(num)
        if t:
            g.add_edge(make_id("ticket", num), nid, "mirrors",
                       {"url": rec.get("url", "")})


def build():
    if not os.path.isdir(os.path.join(ROOT, ".git")):
        print("ERROR: run me from inside the repository (no .git found at %s)" % ROOT)
        return 2

    started = time.time()
    files = scan_files()
    g = Graph(None)

    g.add_node("repo", ".", name=os.path.basename(ROOT), attrs={"root": ROOT})

    texts = {}
    for path in files:
        full = os.path.join(ROOT, path)
        if not path.endswith(TEXT_SUFFIX):
            g.add_node("file", path, repo_path=path, name=os.path.basename(path),
                       attrs={"binary_or_unknown": True})
            continue
        text = read_text(full)
        if text is None:
            continue
        texts[path] = text
        nlines = text.count("\n") + 1
        g.add_node("file", path, repo_path=path, name=os.path.basename(path),
                   line_start=1, line_end=nlines,
                   attrs={"lines": nlines, "bytes": len(text.encode("utf-8")),
                          "sha1": sha1(text)})

    # --- markdown: sections, links, section citations
    for path in sorted(p for p in texts if p.endswith(".md")):
        text = texts[path]
        parse_markdown(g, path, text)
        fid = make_id("file", path)
        for target in set(RE_MD_LINK.findall(text)):
            if target.endswith(".md") or "/" in target:
                resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
                g.link_file(resolved, fid, "links_to", {"raw": target})
        m = RE_ISSUES_LINK.search(path)
        if m:
            g.add_edge(fid, make_id("map_version", os.path.basename(os.path.dirname(os.path.dirname(path)))),
                       "part_of")

    # --- tickets
    ticket_paths = [p for p in sorted(texts) if RE_ISSUES_LINK.search(p)]
    for path in ticket_paths:
        parse_ticket(g, path, texts[path])

    # --- blocked_by edges (second pass: every ticket node now exists)
    for tid, t in g.tickets.items():
        for dep in [d for d in t["blocked_by"].split(",") if d]:
            dep_nid = make_id("ticket", dep)
            if dep_nid in g.nodes:
                g.add_edge(make_id("ticket", tid), dep_nid, "blocked_by",
                           {"resolved": g.tickets.get(dep, {}).get("status") == "resolved"})
            else:
                g.dangling.append((make_id("ticket", tid), "blocked_by", dep))

    # --- artifact edges: findings file -> ticket, and ticket -> findings file
    for tid, t in g.tickets.items():
        for cand in ("%s-findings.md" % tid,):
            art = os.path.join(os.path.dirname(t["file_path"]), cand)
            if make_id("file", art) in g.nodes:
                g.add_edge(make_id("file", art), make_id("ticket", tid), "artifact_of")
            else:
                marker = g.add_node("missing", art, repo_path="", name=cand,
                                    attrs={"ticket": tid, "artifact": cand})
                g.add_edge(make_id("ticket", tid), marker, "missing_artifact",
                           {"artifact": cand, "note": "claimed by the ticket but not written yet"})
                g.dangling.append((make_id("ticket", tid), "artifact", cand))

    # --- section citations: §N inside any markdown file
    for path in sorted(p for p in texts if p.endswith(".md")):
        src = make_id("ticket", os.path.basename(path)[:2]) \
            if RE_ISSUES_LINK.search(path) else make_id("file", path)
        if src not in g.nodes:
            continue
        for num in sorted(set(RE_SEC_REF.findall(texts[path]))):
            dst = g.sec_index.get(num)
            if dst:
                g.add_edge(src, dst, "cites_section", {"section": num})

    # --- map versions and the github mirror
    for path in sorted(p for p in texts if p.endswith("map.md")):
        ver = os.path.basename(os.path.dirname(path))
        g.add_node("map_version", ver, repo_path=path, name="Wayfinder %s" % ver,
                   attrs={"version": ver})
        g.add_edge(make_id("map_version", ver), make_id("repo", "."), "part_of")
        g.add_edge(make_id("file", path), make_id("map_version", ver), "documents")
    for path in sorted(p for p in texts if p.endswith("github-issues.tsv")):
        parse_github_tsv(g, path, texts[path])

    # --- write
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    tmp = DB_PATH + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    conn = sqlite3.connect(tmp)
    conn.executescript(SCHEMA_SQL)
    for uid, n in g.nodes.items():
        conn.execute(
            "INSERT INTO nodes(uid,kind,repo_path,name,line_start,line_end,attrs_json,content_hash)"
            " VALUES(?,?,?,?,?,?,?,?)",
            (uid, n["kind"], n["repo_path"], n["name"], n["line_start"], n["line_end"],
             json.dumps(n["attrs"], ensure_ascii=False),
             sha1(n["attrs"].get("body", n["name"]))),
        )
    seen = set()
    for src, dst, relation, attrs in g.edges:
        if src not in g.nodes or dst not in g.nodes:
            continue
        key = (src, dst, relation)
        if key in seen:
            continue
        seen.add(key)
        conn.execute("INSERT INTO edges(src_id,dst_id,relation,attrs_json) VALUES(?,?,?,?)",
                     (src, dst, relation, json.dumps(attrs, ensure_ascii=False)))
    for tid, t in sorted(g.tickets.items()):
        conn.execute(
            "INSERT INTO tickets(ticket_id,title,area,type,status,blocked_by,resolved,"
            "artifact,file_path,line_start) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (tid, t["title"], t["area"], t["type"], t["status"], t["blocked_by"],
             t["resolved"], t["artifact"], t["file_path"], 1),
        )
    for tid, t in sorted(g.tickets.items()):
        body = t.get("body", "")
        if body:
            row = conn.execute("SELECT rowid FROM nodes WHERE uid=?", (make_id("ticket", tid),)).fetchone()
            if row:
                conn.execute("INSERT INTO nodes_fts(rowid,name,body) VALUES(?,?,?)",
                             (row[0], t["title"], body))
    rev = git_rev()
    conn.execute(
        "INSERT INTO builds(started_at,finished_at,file_count,node_count,edge_count,"
        "git_rev,schema_version) VALUES(?,?,?,?,?,?,?)",
        (started, time.time(), len(files), len(g.nodes), len(seen), rev, SCHEMA_VERSION),
    )
    conn.commit()
    conn.close()
    os.replace(tmp, DB_PATH)

    elapsed = time.time() - started
    size = os.path.getsize(DB_PATH)
    print("built %s" % rel(DB_PATH))
    print("  files  %d" % len(files))
    print("  nodes  %d" % len(g.nodes))
    print("  edges  %d" % len(seen))
    print("  rev    %s" % rev)
    print("  time   %.2fs   size %.0f KB" % (elapsed, size / 1024.0))
    if g.dangling:
        print("  dangling refs: %d (see `health`)" % len(g.dangling))
    with open(LOG_PATH, "a", encoding="utf-8") as fh:
        fh.write("- %s  rev=%s files=%d nodes=%d edges=%d %.2fs %dKB%s\n" % (
            time.strftime("%Y-%m-%d %H:%M:%S"), rev, len(files), len(g.nodes),
            len(seen), elapsed, size // 1024,
            "  dangling=%d" % len(g.dangling) if g.dangling else ""))
    return 0


SCHEMA_SQL = """
PRAGMA journal_mode=DELETE;
CREATE TABLE nodes(
  rowid INTEGER PRIMARY KEY, uid TEXT NOT NULL UNIQUE, kind TEXT NOT NULL,
  repo_path TEXT, name TEXT, line_start INTEGER, line_end INTEGER,
  attrs_json TEXT, content_hash TEXT);
CREATE TABLE edges(
  id INTEGER PRIMARY KEY AUTOINCREMENT, src_id TEXT NOT NULL, dst_id TEXT NOT NULL,
  relation TEXT NOT NULL, attrs_json TEXT);
CREATE TABLE tickets(
  ticket_id TEXT PRIMARY KEY, title TEXT, area TEXT, type TEXT, status TEXT,
  blocked_by TEXT, resolved TEXT, artifact TEXT, file_path TEXT, line_start INTEGER);
CREATE VIRTUAL TABLE nodes_fts USING fts5(
  name, body, content='nodes', content_rowid='rowid');
CREATE TABLE builds(
  id INTEGER PRIMARY KEY AUTOINCREMENT, started_at REAL, finished_at REAL,
  file_count INTEGER, node_count INTEGER, edge_count INTEGER, git_rev TEXT,
  schema_version INTEGER);
CREATE INDEX idx_nodes_kind ON nodes(kind);
CREATE INDEX idx_nodes_path ON nodes(repo_path);
CREATE INDEX idx_edges_src ON edges(src_id);
CREATE INDEX idx_edges_dst ON edges(dst_id);
CREATE INDEX idx_edges_rel ON edges(relation);
CREATE VIEW v_blocked AS
  SELECT t.ticket_id, t.title, t.status, t.blocked_by
  FROM tickets t WHERE t.status <> 'resolved' AND t.blocked_by <> '';
CREATE VIEW v_frontier AS
  SELECT t.ticket_id, t.title, t.status FROM tickets t
  WHERE t.status = 'open' AND t.blocked_by = '';
"""


# --------------------------------------------------------------------------- query

def connect():
    if not os.path.exists(DB_PATH):
        print("no index at %s - run: python3 tools/sblgraph.py build" % rel(DB_PATH))
        return None
    conn = sqlite3.connect("file:%s?mode=ro" % DB_PATH, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def last_build(conn):
    row = conn.execute("SELECT * FROM builds ORDER BY id DESC LIMIT 1").fetchone()
    return row


def cmd_stats(conn):
    row = last_build(conn)
    if row is None:
        print("index is empty - run build")
        return 1
    print("index      %s" % rel(DB_PATH))
    print("built      %s (%.2fs)  rev=%s  schema=v%s" % (
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row["finished_at"])),
        row["finished_at"] - row["started_at"], row["git_rev"], row["schema_version"]))
    print("files      %d" % row["file_count"])
    print("nodes      %d" % conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0])
    print("edges      %d" % conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0])
    print("tickets    %d" % conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0])
    print("\nnodes by kind")
    for r in conn.execute("SELECT kind, COUNT(*) c FROM nodes GROUP BY kind ORDER BY c DESC"):
        print("  %-14s %d" % (r["kind"], r["c"]))
    print("\nedges by relation")
    for r in conn.execute("SELECT relation, COUNT(*) c FROM edges GROUP BY relation ORDER BY c DESC"):
        print("  %-16s %d" % (r["relation"], r["c"]))
    print("\ntickets")
    for r in conn.execute("SELECT ticket_id,area,type,status,blocked_by FROM tickets ORDER BY ticket_id"):
        print("  %s  %-11s %-9s %-8s blocked_by=[%s]" % (
            r["ticket_id"], r["area"], r["type"], r["status"], r["blocked_by"]))
    return 0


def cmd_health(conn):
    problems = 0
    row = last_build(conn)
    newest_src = 0.0
    for r in conn.execute("SELECT repo_path FROM nodes WHERE kind='file' AND repo_path <> ''"):
        p = os.path.join(ROOT, r["repo_path"])
        if os.path.exists(p):
            newest_src = max(newest_src, os.path.getmtime(p))
    if row and newest_src > row["finished_at"]:
        print("STALE      a source file changed after the build - rerun build")
        problems += 1
    rev = git_rev()
    if row and row["git_rev"] != rev and rev != "unknown":
        print("STALE      index built at rev %s, working tree at %s" % (row["git_rev"], rev))
        problems += 1

    print("dangling references")
    n = 0
    for r in conn.execute(
            "SELECT e.relation, e.src_id, e.attrs_json, n.name FROM edges e "
            "JOIN nodes n ON n.id = e.dst_id "
            "WHERE e.relation IN ('missing_ref','missing_artifact') ORDER BY e.relation"):
        label = "BROKEN LINK " if r["relation"] == "missing_ref" else "NO ARTIFACT "
        print("  %s %s -> %s" % (label, r["src_id"], r["name"]))
        n += 1
    if not n:
        print("  none")
    problems += 1 if n else 0

    print("\ntickets not referenced from any map")
    n = 0
    for r in conn.execute(
            "SELECT t.ticket_id, t.status, t.file_path, t.title FROM tickets t "
            "WHERE t.ticket_id NOT IN ("
            "  SELECT substr(e.src_id, 8) FROM edges e WHERE e.relation='contains' "
            "  AND e.dst_id IN (SELECT id FROM nodes WHERE kind='file' AND repo_path LIKE '%/map.md'))"):
        print("  ORPHAN   ticket %s (%s) - %s" % (r["ticket_id"], r["status"], r["file_path"]))
        print("           %s" % r["title"])
        n += 1
    if not n:
        print("  none")
    problems += 1 if n else 0

    print("\nticket state")
    unresolved = {}
    for r in conn.execute("SELECT ticket_id,status,blocked_by FROM tickets"):
        unresolved[r["ticket_id"]] = r
    for tid, r in sorted(unresolved.items()):
        deps = [d for d in r["blocked_by"].split(",") if d]
        open_deps = [d for d in deps if unresolved.get(d) and unresolved[d]["status"] != "resolved"]
        state = "unblocked" if not open_deps else "blocked by %s" % ",".join(open_deps)
        flag = ""
        if r["status"] == "claimed" and not open_deps:
            flag = "   <- claimed but unblocked: work may be finished, status not updated"
        print("  %s %-10s %s%s" % (tid, r["status"], state, flag))
    print("\n%d problem group(s)" % problems)
    return 0


def cmd_query(conn, text, limit):
    words = RE_WORD.findall(text.lower())
    if not words:
        print("empty query")
        return 1
    expr = " OR ".join('"%s"' % w for w in words)
    sql = """
      SELECT n.id, n.kind, n.repo_path, n.name, n.line_start, n.line_end,
             snippet(nodes_fts, 1, '', '', ' ... ', 12) AS snip,
             bm25(nodes_fts) AS score
      FROM nodes_fts JOIN nodes n ON n.id = nodes_fts.rowid
      WHERE nodes_fts MATCH ?
      ORDER BY score LIMIT ?"""
    rows = conn.execute(sql, (expr, limit)).fetchall()
    if not rows:
        print("no hits for %r" % text)
        return 0
    for r in rows:
        loc = "%s:%s-%s" % (r["repo_path"], r["line_start"], r["line_end"])
        print("%-9s %s  %s" % (r["kind"], loc, (r["name"] or "")[:70]))
        if r["snip"]:
            print("          %s" % " ".join(r["snip"].split())[:180])
    print("\n%d hit(s). Next: python3 tools/sblgraph.py raw <path> <start> <end>" % len(rows))
    return 0


def cmd_node(conn, key):
    rows = conn.execute(
        "SELECT * FROM nodes WHERE repo_path = ? OR id = ? OR name LIKE ? "
        "OR repo_path LIKE ? ORDER BY kind LIMIT 20", (key, key, "%" + key + "%", "%" + key + "%")
    ).fetchall()
    if not rows:
        print("no node matching %r" % key)
        return 1
    for r in rows:
        print("%s  %s  %s:%s-%s" % (r["kind"], r["id"], r["repo_path"], r["line_start"], r["line_end"]))
        for e in conn.execute(
                "SELECT relation, dst_id, attrs_json FROM edges WHERE src_id=? LIMIT 12", (r["id"],)):
            print("    -> %-16s %s %s" % (e["relation"], e["dst_id"], e["attrs_json"] or ""))
        for e in conn.execute(
                "SELECT relation, src_id, attrs_json FROM edges WHERE dst_id=? LIMIT 12", (r["id"],)):
            print("    <- %-16s %s %s" % (e["relation"], e["src_id"], e["attrs_json"] or ""))
    return 0


def cmd_deps(conn, tid):
    tid = tid.zfill(2)
    row = conn.execute("SELECT * FROM tickets WHERE ticket_id=?", (tid,)).fetchone()
    if row is None:
        print("no ticket %s" % tid)
        return 1
    print("ticket %s  %s" % (tid, row["title"]))
    print("  type=%s status=%s blocked_by=[%s]" % (row["type"], row["status"], row["blocked_by"]))
    direct = [d for d in row["blocked_by"].split(",") if d]
    if not direct:
        print("  no upstream dependencies")
    seen = set()
    frontier = list(direct)
    depth = 1
    while frontier:
        line = []
        for d in sorted(set(frontier)):
            if d in seen:
                continue
            seen.add(d)
            r = conn.execute("SELECT status,title FROM tickets WHERE ticket_id=?", (d,)).fetchone()
            if r:
                line.append("%s(%s)" % (d, r["status"]))
            else:
                line.append("%s(MISSING)" % d)
        if line:
            print("  %s %s" % ("  " * depth + "->", " ".join(line)))
        nxt = []
        for d in set(frontier):
            r = conn.execute("SELECT blocked_by FROM tickets WHERE ticket_id=?", (d,)).fetchone()
            if r and r["blocked_by"]:
                nxt.extend(x for x in r["blocked_by"].split(",") if x)
        frontier = [x for x in nxt if x not in seen]
        depth += 1
    open_deps = []
    for d in seen | set(direct):
        r = conn.execute("SELECT status FROM tickets WHERE ticket_id=?", (d,)).fetchone()
        if r and r["status"] != "resolved":
            open_deps.append(d)
    print("  unblocked: %s" % ("yes" if not open_deps else
                               "no - waiting on %s" % ",".join(sorted(open_deps))))
    print("  downstream (what this blocks)")
    for r in conn.execute(
            "SELECT src_id FROM edges WHERE relation='blocked_by' AND dst_id=?",
            (make_id("ticket", tid),)):
        print("    %s" % r["src_id"][len("ticket:"):])
    return 0


def cmd_raw(args):
    """Read only part of a file: an explicit range, or grep -C context."""
    if args and args[0] == "--grep":
        rest = args[1:]
        ctx = 0
        if "-C" in rest:
            i = rest.index("-C")
            ctx = int(rest[i + 1])
            del rest[i:i + 2]
        if not rest:
            print("usage: raw --grep \"text\" [-C n] [path]")
            return 1
        pattern = rest[0]
        paths = rest[1:]
        if not paths:
            paths = [p for p in scan_files() if p.endswith(TEXT_SUFFIX)]
        rx = re.compile(pattern, re.IGNORECASE)
        hits = 0
        for p in paths:
            text = read_text(os.path.join(ROOT, p))
            if text is None:
                continue
            lines = text.splitlines()
            shown = set()
            for i, line in enumerate(lines):
                if rx.search(line):
                    hits += 1
                    lo, hi = max(0, i - ctx), min(len(lines), i + ctx + 1)
                    for j in range(lo, hi):
                        if j in shown:
                            continue
                        shown.add(j)
                        mark = ":" if j == i else "-"
                        print("%s%s%s:%d%s %s" % (p, mark, "", j + 1, mark, lines[j]))
        print("\n%d match(es)" % hits)
        return 0
    if len(args) != 3:
        print("usage: raw <path> <start> <end>   |   raw --grep \"text\" [-C n] [path]")
        return 1
    path, start, end = args[0], int(args[1]), int(args[2])
    text = read_text(os.path.join(ROOT, path))
    if text is None:
        print("cannot read %s" % path)
        return 1
    lines = text.splitlines()
    print("# %s lines %d-%d of %d" % (path, start, end, len(lines)))
    for i in range(max(1, start), min(len(lines), end) + 1):
        print("%5d  %s" % (i, lines[i - 1]))
    return 0


# --------------------------------------------------------------------------- main

USAGE = __doc__


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[1], argv[2:]
    if cmd == "build":
        return build()
    if cmd == "raw":
        return cmd_raw(rest)
    conn = connect()
    if conn is None:
        return 1
    try:
        if cmd == "stats":
            return cmd_stats(conn)
        if cmd == "health":
            return cmd_health(conn)
        if cmd == "query":
            return cmd_query(conn, " ".join(rest), 8)
        if cmd == "node":
            return cmd_node(conn, " ".join(rest))
        if cmd == "deps":
            if not rest:
                print("usage: deps <ticket-id>")
                return 1
            return cmd_deps(conn, rest[0])
        if cmd == "sql":
            for r in conn.execute(" ".join(rest)):
                print(tuple(r))
            return 0
        print("unknown command %r\n" % cmd)
        print(USAGE)
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
