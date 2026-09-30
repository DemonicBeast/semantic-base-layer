# SBL | Decision | Mint a new ID space, or align to an existing one?

Type: grilling
Status: open
Blocked by: 01, 02, 03

## Question

The design doc's §7 says "IDs are stable. Vectors are not," and §4.2 mints its own
identifiers (`C0001 = CAT`, `A0001 = EAT`). But every existing semantic resource
already has an identifier space — WordNet synsets, BabelNet ids, ConceptNet URIs,
Wikidata QIDs, UD's lemma-plus-feature conventions, AMR's frame names.

For SBL, "stable" then has two incompatible readings: stable *within this project*,
or stable *across the ecosystem*. Only the second delivers the GPS analogy, and it
cannot be achieved by minting `C0001`.

The decision to settle with the user:

- Does SBL mint its own canonical space and treat existing spaces as mappings, or
  adopt an existing space as canonical and mint only where nothing covers the concept?
- If owned: what happens when an existing standard changes, and who arbitrates splits?
- If aligned: which space, and what does the project lose by inheriting that space's
  granularity decisions and licence terms?
- What is the migration path if the first choice turns out wrong? (§7's claim depends
  on the answer — an ID space that must be re-minted invalidates everything keyed to it.)

This ticket is HITL: it resolves only in live conversation with the user. The agent
must not answer on the user's behalf. Come armed with the T01/T02/T03 findings.

## Artifact

None — the resolution is the answer itself.
