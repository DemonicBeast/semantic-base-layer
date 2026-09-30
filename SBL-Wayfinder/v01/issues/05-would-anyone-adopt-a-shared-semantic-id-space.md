# SBL | Research | Would anyone adopt a shared semantic ID space?

Type: research
Status: claimed
Blocked by: —

## Question

The design doc's GPS analogy (§1) rests on an assumption that is social, not
technical: that independent parties would converge on one semantic coordinate
system. GPS works because it was mandated and because the alternative was
incompatible hardware. Semantics has no such forcing function. Test the analogy.

1. **What actually drives adoption of identifier standards?** Study the real
   history of shared identifier and vocabulary systems and extract the mechanism:
   schema.org, Unicode, Wikidata, ICD codes, ISO 639 language codes, GS1 barcodes,
   Dublin Core, LOINC, RDF/OWL vocabularies. For each, what made adoption happen —
   mandate, killer app, single dominant sponsor, network economics, funding? What
   made others fail or stall?
2. **Where is the GPS analogy load-bearing and where does it break?** A coordinate
   system is adopted when it is *lossless and physical*. Semantic identity is lossy
   and contested — reasonable people disagree about whether concepts split. State
   precisely which part of the analogy survives contact.
3. **The interoperability incentive problem.** SBL's value proposition (§7) requires
   two model vendors to route through a shared layer. What published evidence exists
   on whether vendors adopt shared semantic interfaces, and under what conditions?
   Find precedents both ways — including cases where interoperability was achieved
   (ONNX for model graphs is a candidate worth examining) and cases where proprietary
   representation was deliberately defended as a moat.
4. **Switching cost.** For a would-be adopter, what does it cost to emit SBL
   structures instead of a model-native representation? Does SBL add a hop that costs
   latency or fidelity without a corresponding benefit at v0.1 scale? Be honest about
   whether any adopter exists at 100 concepts.

The output that matters: the **minimum conditions** under which SBL's interoperability
claim becomes credible, and whether those conditions are reachable at the design
doc's target scale or only at a scale SBL cannot bootstrap alone.

## Artifact

`05-findings.md` — link it here when resolved; do not paste findings into this ticket.
