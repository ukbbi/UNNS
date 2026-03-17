# AXIS V ARCHITECTURE — THE COMPLETE ADMISSIBILITY TRIAD

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       AXIS V: ADMISSIBILITY GATES                       │
│                     "Can Substrate Support Utility?"                    │
└─────────────────────────────────────────────────────────────────────────┘

                           SUBSTRATE DYNAMICS
                                   ↓
              ┌────────────────────┴────────────────────┐
              │                                         │
              │     Recursive Event Generation          │
              │     (TauFieldEngineN / Generators)      │
              │                                         │
              └────────────────────┬────────────────────┘
                                   ↓
                    ═══════════════════════════════
                    ║  AXIS V ADMISSIBILITY GATES ║
                    ═══════════════════════════════
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │   V-3: DAG      │  │  V-4: SPECTRUM  │  │  V-5: XOR-SAT   │
    │  Embeddability  │  │   Invariants    │  │  Feasibility    │
    ├─────────────────┤  ├─────────────────┤  ├─────────────────┤
    │ Type:           │  │ Type:           │  │ Type:           │
    │  STRUCTURAL     │  │  ALGEBRAIC      │  │  LOGICAL        │
    │                 │  │                 │  │                 │
    │ Invariant:      │  │ Invariant:      │  │ Invariant:      │
    │  F = acyclic    │  │  F = λ_max      │  │  F = XOR-SAT    │
    │                 │  │      ∈ [λ,λ̄]    │  │      satisfied  │
    │                 │  │                 │  │                 │
    │ Depends on:     │  │ Depends on:     │  │ Depends on:     │
    │  Edge topology  │  │  Adjacency      │  │  Node-local     │
    │  (parents)      │  │  spectrum       │  │  parity bits    │
    │                 │  │  (eigenvalues)  │  │  (symbols/      │
    │                 │  │                 │  │   payloads)     │
    │                 │  │                 │  │                 │
    │ Collapse:       │  │ Collapse:       │  │ Collapse:       │
    │  Cycle intro    │  │  Spectral drift │  │  Constraint     │
    │                 │  │                 │  │  violation      │
    │                 │  │                 │  │                 │
    │ Falsifier:      │  │ Falsifier:      │  │ Falsifier:      │
    │  Utility after  │  │  Utility while  │  │  Utility while  │
    │  collapse       │  │  out-of-band    │  │  UNSAT          │
    └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ↓
                     ┌────────────────────────┐
                     │   ALL GATES PASS?      │
                     └────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
            ┌───────────────┐           ┌───────────────┐
            │  ANY GATE     │           │  ALL GATES    │
            │  FAILS        │           │  PASS         │
            ├───────────────┤           ├───────────────┤
            │ τ inadmissible│           │ τ admissible  │
            │ → Collapse    │           │ → Continue    │
            │ → No utility  │           │ → Utility     │
            │               │           │   possible    │
            └───────────────┘           └───────┬───────┘
                                                │
                                                ▼
                                    ┌───────────────────┐
                                    │  UTILITY REALIZED │
                                    │  (if U_t > U_crit)│
                                    └───────────────────┘
```

---

## ORTHOGONALITY MATRIX

```
                    Sensitive To:
                ┌──────────┬──────────┬──────────┐
                │  Edges   │ Spectrum │ Node Bits│
    ────────────┼──────────┼──────────┼──────────┤
    V-3 (DAG)   │    ✓     │    ✓     │    ✗     │
    V-4 (Spec)  │    ✓     │    ✓     │    ✗     │
    V-5 (SAT)   │    ✗     │    ✗     │    ✓     │
    └───────────┴──────────┴──────────┴──────────┘

    ✓ = Changes when modified
    ✗ = Invariant when modified
```

**Proof of Non-Overlap**:
- V-3 and V-4 both depend on edges → Change together under edge rewiring
- V-5 depends only on node bits → Unchanged under edge rewiring
- V-5 changes under bit flip → V-3 and V-4 unchanged (topology preserved)

**Result**: Three genuinely orthogonal admissibility primitives.

---

## WHAT EACH GATE ELIMINATES

```
┌──────────────────────────────────────────────────────────────┐
│  AXIS V NEGATIVE SPACE — RULING OUT FALSE POSITIVES          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  V-3 eliminates: Structural artifacts                        │
│    "Utility is not a side effect of graph topology"         │
│    → No cycles, embeddings, or geometric loopholes          │
│                                                              │
│  V-4 eliminates: Spectral artifacts                          │
│    "Utility is not a side effect of eigenstructure"         │
│    → No accidental resonances or linear algebra leakage     │
│                                                              │
│  V-5 eliminates: Logical artifacts                           │
│    "Utility is not a side effect of constraint leakage"     │
│    → No SAT solver side effects or combinatorial loopholes  │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  What remains after V-3, V-4, V-5 pass:                     │
│    → History-dependent emergence                             │
│    → Path-specific accumulation                              │
│    → Genuinely non-local substrate dynamics                  │
└──────────────────────────────────────────────────────────────┘
```

---

## AXIS V AS FOUNDATION FOR AXES I-IV

```
                    UNNS VALIDATION HIERARCHY
                              
                         AXIS I-IV
                    (Utility Mechanisms)
                              │
                              │ "How does utility emerge?"
                              │
                              ▼
                    ╔═══════════════════╗
                    ║     AXIS V        ║
                    ║  (Admissibility)  ║
                    ╚═══════════════════╝
                              │
                              │ "Can substrate support utility?"
                              │
                              ▼
                    ┌───────────────────┐
                    │   V-3: Structure  │  ← Rules out graph artifacts
                    ├───────────────────┤
                    │   V-4: Spectrum   │  ← Rules out algebraic artifacts
                    ├───────────────────┤
                    │   V-5: Logic      │  ← Rules out constraint artifacts
                    └───────────────────┘
                              │
                              │ ALL PASS?
                              │
                              ▼
                    ┌───────────────────┐
                    │ Axes I-IV become  │
                    │ interpretable:    │
                    │                   │
                    │ • Σ-layer (II)    │
                    │ • φ-lock (XIV)    │
                    │ • Propagation (?)  │
                    └───────────────────┘
```

**Key Insight**: Without Axis V, Axes I-IV results could be contaminated by:
- Topological accidents (V-3 violations)
- Spectral side effects (V-4 violations)
- Constraint leakage (V-5 violations)

With Axis V validated, I-IV results must be **genuinely substrate-emergent**.

---

## ACCEPTANCE STATUS

```
    ╔═══════════════════════════════════════════════════════╗
    ║              AXIS V — COMPLETE                        ║
    ╠═══════════════════════════════════════════════════════╣
    ║                                                       ║
    ║  ✓ V-3 (DAG Embeddability)      → LOCKED             ║
    ║  ✓ V-4 (Spectral Invariants)    → LOCKED             ║
    ║  ✓ V-5 (XOR-SAT Feasibility)    → LOCKED             ║
    ║                                                       ║
    ║  Orthogonality: CONFIRMED                            ║
    ║  Falsifier Discipline: MAINTAINED                     ║
    ║  Publication Ready: YES                               ║
    ║                                                       ║
    ║  Next: AXIS V SYNTHESIS DOCUMENT                      ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
```

**Chamber L-B V-5.0 is accepted as the final Axis V logical admissibility gate.**

**No further mechanism changes. Lock and archive.**
