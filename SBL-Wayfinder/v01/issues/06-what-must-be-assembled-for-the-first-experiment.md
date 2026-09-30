# SBL | Engineering | What must be assembled for the first experiment?

Type: research
Status: open
Blocked by: 01, 02

## Question

T03 establishes what tooling exists and T04 sizes the general build. This ticket
narrows to the specific question the first experiment depends on: **what exactly
must be assembled to run §20's milestone, and what does assembly cost?**

1. **The ontology's starting content.** Given the census in T02 (prior art) and the
   scientific finding in T01, what should the first 100 concepts and 30 relationships
   actually be drawn from? Is there an existing ontology subset — WordNet's core
   synsets, ConceptNet's highest-degree concepts, a basic-level category inventory —
   that would be both defensible and cheaper than hand-authoring §9's list? What are
   the licensing and attribution consequences of each source?
2. **The grammar-role inventory.** §4.1 lists POS tags and §9 lists relations, but the
   mapping between grammar roles and semantic roles is unspecified. What existing
   role inventories are available to adopt rather than invent (UD's dependency labels,
   PropBank/VerbNet semantic roles, AMR's frame roles), and what does aligning to one
   commit the project to?
3. **The serialization schema.** What concrete schema options exist for the wire format,
   with real examples — an SBL JSON schema, CoNLL-U plus extensions, PENMAN/AMR,
   JSON-LD against an existing vocabulary, RDF with a custom namespace? What does each
   make easy and hard (validation, streaming, graph queries, human readability,
   versioning)?
4. **The assembly plan.** A concrete inventory: which components are adopted, which
   are written, in what order, and what each step depends on. Name the libraries and
   the specific existing resources being reused.

This is the resource plan the specification in the destination will cite. Requirements
must be specific enough that someone could start work from this ticket alone.

## Artifact

`06-findings.md` — link it here when resolved; do not paste findings into this ticket.
