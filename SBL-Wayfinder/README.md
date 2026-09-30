# SBL Wayfinder

The wayfinder map for the **Semantic Base Layer (SBL)** effort.

Tracker: **local markdown** (this folder). Source design doc: `../semantic-base-layer-design-5.md`.

## Versioning rule — read this first

**Nothing in this folder is ever overwritten or deleted.**

Every revision of the map is a new numbered version folder. When the map changes,
`v01/` is frozen and copying forward produces `v02/`, then `v03/`, and so on.
An issue file is copied into the new version at its current state and only then
appended to.

This means: to see how a decision evolved, diff two version folders. Earlier
versions are history, not stale copies — never clean them up.

## Versions

| Version | Opened | Status | Contents |
| --- | --- | --- | --- |
| `v01/` | 2025-10-01 | open | Map charted; 9 tickets created (01–05 frontier, 06–09 blocked) |

## Layout of a version

```
vNN/
├── map.md              the map: Destination, Notes, Decisions so far, Not yet specified, Out of scope
└── issues/
    ├── NN-<slug>.md    one decision ticket per file, numbered from 01
    └── NN-findings.md  the research artifact a ticket links to (never pasted into the ticket)
```

Ticket conventions (from the local-markdown tracker):

- `Type:` — `research` / `prototype` / `grilling` / `task`
- `Status:` — `open` / `claimed` / `resolved`
- `Blocked by: NN, NN` — unblocked when every listed ticket is `resolved`
- **Frontier** — open, unblocked, unclaimed; lowest number wins
- **Claim** — set `Status: claimed` before any work
- **Resolve** — answer under `## Answer`, set `Status: resolved`, then append the
  context pointer to the map's *Decisions so far*
