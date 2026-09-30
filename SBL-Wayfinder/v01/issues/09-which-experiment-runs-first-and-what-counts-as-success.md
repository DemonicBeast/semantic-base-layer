# SBL | Decision | Which experiment runs first, and what counts as success?

Type: grilling
Status: open
Blocked by: 06, 08

## Question

Design doc §14 says SBL "should only be considered successful if experiments
demonstrate measurable benefits," §20 names a first measurable goal, and §13 calls
compositional generalization "one of the most important experiments." These are in
tension: §20's goal is a *representation* test (do two surface forms map to the same
structure?), while §13 and §6 are *capability* tests (does the structure buy
generalization or compute?). The first one is cheap and nearly certain to pass; the
second can fail.

Settle with the user:

- **Which experiment runs first**, and what it is allowed to conclude. A §20 mapping
  success proves the representation is expressible — it does not prove it is useful,
  and the write-up must not let it imply otherwise.
- **The baseline.** §14 proposes a conventional architecture to compare against. What
  specifically is the baseline — an off-the-shelf multilingual model, a rule-based
  system, a small trained model? What makes the comparison fair rather than rigged?
- **The metrics and their thresholds.** §14 lists accuracy, RAM, parameters, training
  and inference time, compositional generalization, multilingual transfer, and
  interpretability. Which are primary, which are reported-only, and what numbers
  count as success versus failure versus inconclusive? Fix these *before* seeing
  results.
- **The falsification condition.** State in advance what result would mean SBL's
  hypothesis is wrong and the project should stop. A plan without this is not an
  experiment.
- **Scope of the first milestone.** Where the first experiment ends and Phase 2–5 begins.

HITL: resolves only in live conversation with the user. The agent must not answer the
user's side.

## Artifact

None — the resolution is the answer itself.
