# SBL | Decision | How deep should the ontology be, and what is context?

Type: grilling
Status: open
Blocked by: 01, 02, 06

## Question

Design doc §9 proposes an ontology of entities, actions, properties, relationships,
and logic, and §4.4 insists context is not eliminated. But it leaves two things open
that determine whether the layer can carry meaning at all:

- **How deep does the hierarchy go?** §6's prediction story needs a category tree
  (PROPERTY → PHYSICAL_PROPERTY → COLOR → BLACK), while §9's list is nearly flat. A
  deep tree buys the §6 hypothesis and costs annotation effort and disagreement; a
  flat list is cheap but may not support §6 at all. Where does v0.1 sit?
- **How is context represented?** §4.4's `bank` example gives a stable identity plus
  context but never says what "context" is — a disambiguation tag, a frame, a
  probabilistic distribution over senses, an embedding offset? This is unaddressed in
  the design doc and it is load-bearing for §7.

Settle with the user:

- The depth of the v0.1 ontology, and the test that would tell them it is wrong.
- What a "concept" is at v0.1 granularity — a word sense, a basic-level category, or
  a cluster of senses — with the reasoning that decides it.
- How context attaches to a concept identity, and what the serialized form of a
  context-qualified meaning looks like.
- Which of §9's entries survive the first cut, and which move to v0.2.

HITL: resolves only in live conversation with the user. The agent must not answer the
user's side.

## Artifact

None — the resolution is the answer itself.
