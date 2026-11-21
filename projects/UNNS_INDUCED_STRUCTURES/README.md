# UNNS Substrate — Induced Structures

**Research-source collection**  
**Status:** consolidation / reference freeze at FUG-I v005, MUG-I v009, CIB-I v001, QTI-I v003, SIB-I v005  
**Destination:** `ukbbi/UNNS/projects/UNNS_INDUCED_STRUCTURES/`  

## Scope

Study **structures induced by a specified correspondence** between independently generated systems (integer sequences, recurrence states, Maxwell fields, or detector records) and explicitly defined UNNS Substrate grammars. This collection primarily analyzes the **integer self-substitution** SELECT-II grammar

\[
T_N(x)=x\frac{(N+1)^2}{N},\qquad N\mid x,\quad x,N\in\mathbb N_{>0}.
\]

The underlying occurrence primitive `M ⟂ N = M (N+1)²/N` also admits rational outputs; integer self-substitution is a **selected continuation grammar**, not the definition of every UNNS grammar. Other UNNS grammars are legitimate independently defined constructions. Cross-grammar equivalences require a specified map and proof, not rhetorical identification.

Induced structure means **more than attaching ancestry to individual integers**. It includes ordering, recurrence relations, transport, overlap, mergers, state-level compatibility, and controlled obstructions. External physical correlations are not automatically substrate-specific.

## Navigation

- **[RELEASE_INDEX.md](RELEASE_INDEX.md)** — complete citable release map (FUG, SIB, MUG, CIB, QTI), with scope and caveats.
- **[THEOREM_INDEX.md](THEOREM_INDEX.md)** — monograph-facing theorem identifiers and primary sources; do not cite this summary as a substitute for the source theorem.
- **[CLAIM_BOUNDARIES.md](CLAIM_BOUNDARIES.md)** — interpretation and correction requirements, negative results and limits.
- **[SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md)** — source/data references and relation to frozen mathematics elsewhere in the repository.
- **[CURATION_AUDIT.md](CURATION_AUDIT.md)** — pruning decisions, inherited issues and exact provenance.
- **[PROVENANCE/SOURCE_FILE_LEDGER.csv](PROVENANCE/SOURCE_FILE_LEDGER.csv)** — each original archive file, original SHA-256, action and rationale.
- **[tools/VERIFY.md](tools/VERIFY.md)** — integrity verification and selected WSL commands.

## Research families

| Folder | Releases | What it establishes |
|---|---|---|
| [FIBONACCI](investigations/FIBONACCI/) | FUG-I v001–v005 | Exact Fibonacci ancestry, index activation and infinite merger families |
| [SEQUENCES](investigations/SEQUENCES/) | SIB-I v001–v005 | Arithmetic controls, recursive architecture, sequence-conditioned exclusions, transport and recurrence-state compatibility |
| [MAXWELL](investigations/MAXWELL/) | MUG-I v001–v009; CIB-I v001 | Maxwell solution mappings, exact fixed-medium obstruction, driven field coupling and alternative-grammar controls |
| [QUANTUM_TELEPORTATION](investigations/QUANTUM_TELEPORTATION/) | QTI-I v001–v003; QTI audit | Time-tag/channel relationships and exact representation/clock-dependent negative specificity results |


