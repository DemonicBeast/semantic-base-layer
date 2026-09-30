# SBL | Research | Does this already exist, and where is it used?

Type: research
Status: resolved
Blocked by: —

## Question

The design doc §16 lists related areas but asserts, without evidence, that the
novelty is "the combination." That assertion needs testing against an actual census.

Answer three things:

1. **What already exists.** Produce a census of systems, standards, and resources
   that occupy SBL's claimed niche — a model-independent, language-independent
   semantic representation with stable shared identifiers. Cover at minimum:
   Interlingua and the interlingua approach in MT; AMR (Abstract Meaning
   Representation) and its corpora; Universal Dependencies; WordNet, BabelNet,
   ConceptNet, FrameNet, PropBank, VerbNet; OntoLex-Lemon and other lexical-model
   standards; Cyc and OpenCyc; Wikidata's identifier space; SUMO and upper ontologies;
   UMR (Uniform Meaning Representation); and any recent LLM-era proposals for shared
   semantic interfaces (for example tool/schema interlinguas, MCP-style protocol work,
   or "semantic ID" proposals). For each: one line on what it is, one line on how
   close it gets to SBL's claim.
2. **Where each is actually used.** Not where it is published — where it is *deployed*.
   Which systems ship with it, which companies or research groups maintain it, what
   downstream tasks consume it (search, MT, QA, knowledge graphs, compliance,
   agent tooling), and whether that use is growing, static, or dormant. Cite
   adopters and, where findable, usage evidence.
3. **The closest single thing.** Of everything found, name the one system that is
   nearest to SBL and state precisely what SBL would add that it lacks. If nothing
   is meaningfully close, say that too — but only after checking UMR and AMR, which
   are the strongest candidates.

Deliver a ranked table of nearest neighbours, not an undifferentiated literature dump.

## Artifact

`02-findings.md` — link it here when resolved; do not paste findings into this ticket.
