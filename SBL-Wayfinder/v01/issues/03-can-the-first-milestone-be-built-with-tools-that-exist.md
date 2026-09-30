# SBL | Engineering | Can the first milestone be built with tools that exist?

Type: research
Status: resolved
Blocked by: —

## Question

Assume the science is worth pursuing. Is the design doc's §20 milestone and Phase 1
buildable *now*, with off-the-shelf components, and what exactly is missing?

Establish feasibility for each pipeline stage independently, because a single weak
stage is what decides the answer:

1. **Tokenization, POS tagging, and dependency parsing for Tamil.** This is the
   design doc's highest-risk engineering assumption — Tamil is agglutinative,
   morphologically rich, and lower-resource than English. What production-quality or
   research-grade Tamil taggers, parsers, and morphological analysers exist today?
   Name them, give their reported accuracies, their licences, and whether they are
   actually maintained and runnable. Compare against the equivalent English tooling.
   If Tamil parsing accuracy is materially worse than English, quantify the gap —
   that number is load-bearing for the whole milestone.
2. **Semantic parsing from UD to a structured representation.** Is there a
   well-trodden path from UD trees to a semantic representation (UD→AMR, UD→UCCA,
   UD→logical forms)? What tooling exists, and what accuracy does it reach?
3. **Available aligned corpora.** What parallel English–Tamil resources exist —
   PMIndia, Samanantar, IndicCorp, UD Tamil treebanks, FLORES-200, and any
   semantic-annotated multilingual corpora? For each: size, domain, licence, and
   whether it is actually downloadable. State the licence plainly; a corpus that
   cannot be used is not a resource.
4. **Serialization and graph tooling.** What already exists for the wire format
   (JSON-LD, RDF, CoNLL-U, AMR's PENMAN notation, protobuf) and what
   graph/validation libraries are available?

Conclude with a component-by-component build/no-build verdict and the specific
missing pieces. Name tools and versions rather than describing categories of tools.

## Artifact

`03-findings.md` — link it here when resolved; do not paste findings into this ticket.
