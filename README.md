# Semantic Base Layer (SBL)

A universal semantic "GPS" for AI — a model-independent, language-independent
semantic representation that sits between language and AI models.

- **`semantic-base-layer-design-5.md`** — the SBL v0.1 design doc (research concept).

## Wayfinding

The route from this concept to a buildable specification is charted in
**`SBL-Wayfinder/`**. That folder is a versioned wayfinder map: a destination, a set
of decision tickets, and the research artifacts that resolve them.

Start at [`SBL-Wayfinder/README.md`](SBL-Wayfinder/README.md) for the versioning rule,
then read the current map at [`SBL-Wayfinder/v01/map.md`](SBL-Wayfinder/v01/map.md).

### How to read a ticket

Ticket titles follow `SBL | <area> | <question>`, where area is one of:

| Area | Meaning |
| --- | --- |
| `Research` | An open question answered from primary sources. Findings land in a sibling `NN-findings.md`. |
| `Engineering` | A question about buildability, tooling, or requirements. |
| `Decision` | A choice only the project owner can make. Resolved in conversation, not by research. |
| `Delivery` | Work that must happen before a decision can be made. |

Tickets state their dependencies in a `Blocked by:` line and their state in a
`Status:` line. The frontier — open, unblocked, unclaimed — is where work starts.
