# AGENT.md — Rules for any AI agent working in this repository

**Read this file completely before doing any work in this repository.**
This applies to every agent, every tool, every session — code, docs, research,
file moves, dependency installs, and anything that touches git.

Canonical path: `AGENT.md` (this file). `AGENTS.md` is a symlink to this file so
agent harnesses that look for either name read the same rules. Edit only `AGENT.md`.

---

## 0. Who you are working for

The project owner is a **.NET developer**. Assume professional competence in
C#, .NET, SQL, HTTP, DI, testing, and build tooling. Do not explain those.

When the work involves a technology, language, or tool **outside** that
experience — Python, neural architectures, ontology standards such as RDF/OWL,
vector indexes, MCP, shell plumbing — explain it in **one or two plain-English
sentences before using it**, then proceed. Say what it is, why it is being used
here, and what it costs (dependency, build step, runtime). No lectures, no
tutorials, no walls of analogies. One or two sentences is the budget.

---

## 1. Do not assume. Establish.

Never state a fact about this repository that you have not read or run yourself.

- Read the file before claiming what it says. Run the command before claiming
  what it prints. Check the directory before claiming a file exists.
- When something is unknown, the correct move is to inspect it, not to infer it
  from the name, from a previous project, or from how such projects usually look.
- If a tool, credential, URL, or service might be unavailable, test it and report
  the actual result.
- Distinguish clearly, every time, between:
  - **Verified** — I read it / ran it, and here is the evidence.
  - **Inferred** — I am reasoning from the verified facts; here is the chain.
  - **Unknown** — I have not checked, and here is what checking would cost.

Presenting an inference as a verified fact is the single worst failure mode in
this repository. If you catch yourself having done it, say so immediately.

---

## 2. Plan before you act. Always.

No work starts without a current `plan.md`.

1. **Analyze** the request and the repository. Inspect first (section 1).
2. **Write or update `plan.md`** before writing code or changing any file.
3. **Prove the plan.** `plan.md` must contain *evidence* that the plan works:
   - a `Verified facts` table, each row citing the command or file read that
     establishes it;
   - a `Verification` section listing the exact commands that will prove the
     work succeeded, written **before** the work is done;
   - a `Risks` register with a mitigation for each risk.
   A plan without evidence is a wish. Do not execute a wish.
4. **Get the plan discussed.** Per the owner's standing rule, nothing goes into
   code without the owner's thought. The plan is discussed and agreed before
   execution. Use the question tool when a decision is genuinely the owner's.
5. **Then execute**, against the plan, with the plan's verification commands.

`plan.md` is a living document for the current work, not a historical record.
Completed work is compressed into its `Done` section.

### If the plan has to change once work is underway

Plans meet reality. That is expected — hiding it is not.

When the plan changes mid-execution, **stop and tell the owner**, in this order:

1. **What changed** — the concrete new fact that invalidated the plan.
2. **Why the original plan cannot hold** — the evidence, not a preference.
3. **What you propose instead** — the revised approach, with its cost.
4. **What it affects** — files, scope, risk, and anything already built.

Then record it in `plan.md` under `## Change log` as an appended entry, never a
silent rewrite:

```
### YYYY-MM-DD — <short title>
- Planned: <what plan.md said>
- Discovered: <the fact that broke it> (evidence: <command / file>)
- Changed to: <the new plan>
- Owner notified: yes — <where / when>
- Affects: <files, scope, risk>
```

Small mechanical corrections do not need a stop — but they do get a change-log
entry. Anything that changes scope, deliverables, interfaces, stored data, or
risk is a stop-and-ask.

---

## 3. Credentials and protected resources — ask before you touch

Treat every secret as a thing that requires explicit, specific permission.

**Do not access, read, print, transmit, or use any of the following without
telling the owner first and getting an explicit yes:**

- passwords, passphrases, API keys, tokens, or private keys;
- `.env` files, credential stores, keychains, secret managers, `~/.ssh`,
  `~/.aws`, `~/.config/gh`, or any file whose name suggests secrets;
- authenticated network resources, private repositories, paid APIs, cloud
  consoles, or third-party accounts that bill or expose private data;
- anything that would send repository content to an external service.

The notification must state, before the access happens:

- **what** is being accessed (exact path, host, or service),
- **why** it is needed for the task,
- **what** will be read or written,
- **what leaves the machine**, if anything.

"I am about to read `~/.aws/credentials` to list buckets — do you want that?"
is correct. Doing it silently and mentioning it afterwards is not.
If the owner declines, the answer is no, permanently, for this session — find a
different route or report the task as blocked. Never work around a refusal.

If a secret is ever needed in a *file you are writing*, write a placeholder and
name the environment variable instead. Never commit a secret. Never echo one
into a log, a plan, or a chat message.

---

## 4. Navigation — use the graph and SQLite, not bulk reads

Full-file reads of this repository into context are expensive and mostly
redundant. Navigate with the local index instead.

The index lives in `tools/sblgraph.sqlite` (see `tools/README.md`) and is built
from the repository's own artifacts:

| Table | Holds |
| --- | --- |
| `nodes` | every file, heading/section, ticket, ticket field, code construct |
| `edges` | containment, references, `blocked_by`, citations, links |
| `tickets` | flattened ticket metadata: type, status, blocked-by, artifact |
| `nodes_fts` | full-text index for keyword search |

Working order for any question about the repository:

1. **Query the index** — find the *node* (which section, which ticket, which
   class or method) that actually matters. `tools/sblgraph.py` is the entry point.
2. **Read only that node's range** — the index stores `line_start`/`line_end`,
   so read the specific slice you need, not the whole file.
3. **Grep to confirm** — `grep`/`rg` for the exact symbol, id, or phrase, to see
   the real line and its neighbours.
4. **Open the whole file only** when the file is small, or when the question
   genuinely spans it.

If the index is missing or older than the files it describes, rebuild it first
(one command; see `tools/README.md`) and say that you did.

### What the graph looks like out there in the world

"Code graph" is a general idea, not a format this repository invented. Outside
this repo the same shape appears as a *call graph* in compilers and profilers
(.NET: `dotnet-counters`/`dotnet-trace` flame graphs, Roslyn syntax trees), as a
*UML class diagram* in modelling tools (classes as nodes, inheritance and
association as edges), and as a *knowledge graph* in semantic tooling (RDF
triples: subject–predicate–object). All of them are the same thing — nodes with
named edges — so the vocabulary transfers directly. What differs here is that
this repository's primary artifacts are documents rather than compiled code, so
the nodes are sections and tickets as much as they are classes and methods.

---

## 5. Say what is going on

The owner wants the reasoning, not just the result. After any non-trivial step,
report briefly:

- **What I did** — the commands and files.
- **What I found** — the actual output, including surprising or bad results.
- **What it means** — your reading of it, labelled as inference (section 1).
- **What is next** — the next step, or the decision you need.

Report failures immediately and plainly. A blocked task reported early is cheap;
a blocked task discovered late is expensive. Never present partial work as
complete, and never let a confident summary paper over a failed command.

---

## 6. Do not touch existing content unless the change is required

This repository is **append-only by standing owner preference**, and its tracker
files are canonical and versioned.

- **Change existing files only when the task cannot be completed without it.**
  Prefer adding a new file, or appending, over rewriting what is there.
- `SBL-Wayfinder/vNN/` folders are **frozen history**. Never edit, reformat, or
  "clean up" a past version. A revision is a **new** `v(N+1)/` folder copied
  forward.
- `SBL-Wayfinder/README.md` states that the markdown tracker is canonical and the
  GitHub issues mirror it — never the reverse. Never push an issue-side edit back
  into the markdown as if it were canonical.
- Never delete or reorganize files to make something tidier. If you believe an
  existing file is wrong, **report it** with evidence and let the owner decide.
- Preserve the existing voice, heading style, and formatting of any document you
  append to.
- Report every incidental inconsistency you find (stale counts, contradictory
  status lines, broken links) even when fixing it is out of scope for the task.

---

## 7. Write for a reader who was not in the conversation

Files an agent writes here — findings, plans, reports — must stand alone.
No "as discussed above", no unstated context, no references to a chat the reader
cannot see. State the sources, cite the file and line, and make the reasoning
followable by someone reading the file cold in six months.

---

## Quick checklist before you act

- [ ] Read `AGENT.md` (this file) and the current `plan.md`.
- [ ] Inspected the repo rather than assuming it (section 1).
- [ ] plan.md updated, with verified facts, verification commands, and risks.
- [ ] Plan discussed with the owner; nothing in code without their thought.
- [ ] No secret, credential, or authenticated resource touched without an
      explicit, prior yes.
- [ ] Queried the graph/`sblgraph.sqlite` before bulk-reading files.
- [ ] Existing files untouched except where required; tracker versions frozen.
- [ ] Final report says what was done, what was found, and what is next.

## Quick checklist before you finish

- [ ] Plan's own verification commands actually run, and their output is reported.
- [ ] Any plan change is reported to the owner and appended to `## Change log`.
- [ ] Every claim in the summary is something you read or ran.
- [ ] Nothing was written outside this repository.
