# PHASE3_SPEC — Frozen research preregistration v001

## Provenance / scope
Phase 2C verdict: `OPEN_NOT_DERIVED`; proto-closure with freely selected observation map does not force orthogonal additivity. Preserve exactly the supplied JSON; checksum is pinned in `config/PHASE3_LOCK.json`. The prior source document describes proto-closure as nontrivial structural recurrence, not a physical probability law. Operator XVI Fold-2 and a separate XVI Closure implementation remain unreconciled: no canonical XVI is used here.

## Substantially different target
Let `M` be a proto-closed mechanism and `E(M)` an *as-yet-unspecified* quotient of observable events. A measurement context `C` is a finite set of exclusive, exhaustive events. Seek a map

    mu_M : E(M) -> [0,1]

with (R1) total normalization `sum_{e in C} mu_M(e)=1`, (R2) context independence for the same event `e` appearing in distinct contexts, (R3) additivity under disjoint coarse-graining, and (R4) compatibility with independently generated systems. Crucially, R1–R4 are candidate representation assumptions, NOT results of proto-closure. Define event identity/embedding in terms of actual UNNS mechanics before claiming a derivation.

**Conditional representation question:** If observable events are identified with all orthogonal projections on a real or complex Hilbert space of dimension >= 3, and mu is nonnegative, normalized and countably additive on orthogonal projections, what form must mu have? The standard Gleason theorem gives mu(P)=Tr(rho P) with rho a positive trace-one operator (appropriate field and dimension). This is a known theorem imported as a conditional reference. Its hypotheses, particularly Hilbert projection structure and noncontextual additivity, are *not* proved for UNNS. The original rebit/single-qubit two-dimensional project does not satisfy the dimensional prerequisite of the standard theorem. Tensor/network generalization is a separate future stage.

## Preregistered gates
- R0: SHA-256 byte equality for frozen Phase 2C and matching active report (if present); on mismatch abort, not merely warn.
- R1: a deterministic two-context countermodel satisfies normalization, yet assigns different probabilities to a common event; establishes normalization does NOT imply noncontextuality.
- R2: a two-dimensional nonquadratic frame assignment is normalized on every orthogonal pair; establishes 2D frame sums do NOT force Born rule.
- R3: finite 3D orthonormal frame checks distinguish radial power q=2 from q=1 and q=3; finite numerical checks are *not* a representation theorem.
- R4: explicitly label Hilbert-space event mapping, noncontextuality and additivity as unproved UNNS bridge assumptions.
- R5: primary UNNS representation theorem: BLOCKED until R4 is independently derived, never marked PASS solely from R0–R3.

## Acceptance / falsification policy
PASS of R0–R3 validates integrity and counterexamples only. A proof of R5 must define generative events and a context-independent composition operation without using Hilbert/Born premises as substrate axioms. Find one proto-closed mechanism with incompatible projections and it falsifies any universal proto-closure -> probability-representation claim. The R1/R2 countermodels already bar such a universal claim with unspecified event structure. No fitted q window, no CHSH reproduction accepted as an original derivation.
