# SBL | Research | Is the core hypothesis already falsified?

Type: research
Status: resolved
Blocked by: —

## Question

Before any engineering is planned, does published evidence already falsify the
hypothesis SBL rests on? Specifically:

1. **Compositional generalization over a fixed symbolic ontology.** Design doc §13
   claims a good system should construct `EAT(DOG, MILK)` from sentences never seen
   together. What does the published record actually show about compositional
   generalization — over symbolic or structured intermediate representations, and
   over end-to-end neural models? Key work to find and read at source: SCAN (Lake &
   Baroni), COGS (Kim & Linzen), CFQ, and whatever replication or critique literature
   exists on them. Has compositional generalization in this setting been shown
   achievable, shown to require specific architectural commitments, or shown
   persistently to fail?
2. **Hierarchical / factored prediction (design doc §6).** Is there published
   evidence that predicting through a semantic category hierarchy (category →
   subcategory → concept → surface token) reduces computation versus flat
   next-token prediction while holding or improving accuracy? Look for class-hierarchy
   softmax, hierarchical softmax, factored language models, and any modern revival.
   Note that hierarchical softmax is usually *training-time* efficient while
   inference still touches many leaves — establish whether that undercuts §6's claim.
3. **The symbolic interlingua thesis.** Design docs §5, §12 and §20 claim different
   surface languages can resolve to one shared representation. Is there evidence that
   a compact hand-specified ontology can carry real natural-language meaning, or is
   there a documented ceiling? Find the strongest published arguments *against* this
   thesis as well as for it — the interlingua debates in machine translation are the
   place to start.
4. **Parsing accuracy as an upstream bound.** SBL's pipeline routes all meaning
   through a parser (grammar layer → semantic layer). What does published evaluation
   say about the accuracy attainable on semantic parsing / AMR parsing / UD parsing,
   and what does error compounding imply for end-to-end semantic fidelity at the
   design doc's target scale?

Report what the evidence supports, what it contradicts, and where it is genuinely
silent. Be explicit about which SBL claims survive and which do not. Do not
editorialize beyond what sources support, and do not soften a negative finding.

## Artifact

`01-findings.md` — link it here when resolved; do not paste findings into this ticket.
