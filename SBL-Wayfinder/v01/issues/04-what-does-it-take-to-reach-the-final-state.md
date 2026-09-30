# SBL | Engineering | What does it take to reach the final state?

Type: research
Status: resolved
Blocked by: —

## Question

What does it actually take to build and run the design doc's §20 milestone and the
Phase 0–4 sequence? This is the requirements gathering the user asked for — an
inventory, not an opinion. Produce it as concrete, checkable requirements.

1. **Software stack.** What languages, libraries, and frameworks are the realistic
   choices for each stage (parsing, ontology storage, graph, validation, neural
   layer)? What are the alternatives and what does each choice trade away? Prefer
   components with permissive licences and state licence terms — this project may
   want to publish.
2. **System requirements.** For each phase (Phase 1 registry + graph; Phase 2 EN+TA
   parser pipeline; Phase 3 datasets at 100 / 1,000 / 10,000 / 100,000 sentences;
   Phase 4 vector layer; Phase 5 small model): what CPU, RAM, GPU/VRAM, and disk is
   actually needed? Ground this in comparable published work — training a small
   transformer, fine-tuning a parser, running a UD-based pipeline — rather than
   guessing. Give per-phase numbers and say what they are based on.
3. **Data requirements.** How many annotated sentences are needed before each
   experiment is statistically meaningful? What annotation effort does 1,000
   sentence–meaning pairs represent in person-hours? What inter-annotator agreement
   does the field expect for semantic annotation, and what does that imply about how
   many annotators this needs?
4. **Human and skill requirements.** What roles does this need (computational
   linguist, Tamil speaker annotator, ML engineer), and what does each phase require
   of them?
5. **Cost and time.** Rough order-of-magnitude for compute spend and elapsed time to
   reach §20's milestone, then to Phase 5, with assumptions stated.

Give numbers and ranges with sources. Where a number is an estimate rather than a
sourced figure, label it as an estimate.

## Artifact

`04-findings.md` — link it here when resolved; do not paste findings into this ticket.
