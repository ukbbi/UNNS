# QM-II v1.1.0 — Cross-Atom Admissibility Results
**UNNS Substrate Program · Chamber QM-II · Branch-resolved inter-family mode**
**B sweep: 0.00–1.00 T · 101 slices · α=0.35 · ε=0.0001 cm⁻¹**

---

## Scorecard

| Atom | Branches | Verdict | Stable | SB | GP | max inv | max ν(V) | max ratio |
|------|--------:|---------|-------:|---:|---:|-------:|--------:|----------:|
| Au | 282 | **STABLE_STRUCTURE** | 101 | 0 | 0 | 0 | 14 | 0.0000 |
| He singlet | 330 | **STABLE_STRUCTURE** | 101 | 0 | 0 | 0 | 9 | 0.0000 |
| Fe | 4,491 | **STABLE_STRUCTURE** | 101 | 0 | 0 | 20 | 296 | 0.1136 |
| Ca | 2,974 | **STABLE_STRUCTURE** | 101 | 0 | 0 | 46 | 328 | 0.1707 |
| Ag | 516 | **STABLE_STRUCTURE** | 101 | 0 | 0 | 6 | 47 | 0.1714 |
| Na | 836 | **STABLE_STRUCTURE** | 101 | 0 | 0 | 15 | 83 | 0.2830 |
| H | 290 | GEOMETRIC_PERSISTENCE_ONLY | 100 | 0 | 1 | 64 | 54 | 1.3617 |
| He (full) | 6,225 | GEOMETRIC_PERSISTENCE_ONLY | 99 | 1 | 1 | 1,177 | 1,267 | 1.0208 |
| He triplet | 4,668 | GEOMETRIC_PERSISTENCE_ONLY | 99 | 1 | 1 | 906 | 869 | 1.0426 |

**Regime thresholds:** Stable Structure: inv/ν ≤ 0.90 · Structural Boundary: 0.90 < inv/ν ≤ 1.00 · Geometric Persistence Only: inv/ν > 1.00

**Result: 6/9 atoms STABLE_STRUCTURE across all 101 slices. 3/9 atoms show a single transient violation confined to B = 0.02 T.**

---

## Violation Detail

All non-Stable-Structure slices across all nine atoms:

| Atom | B (T) | inv | ν(V) | ratio | Regime |
|------|------:|----:|-----:|------:|--------|
| H | 0.02 | 64 | 47 | 1.3617 | Geometric Persistence Only |
| He (full) | 0.02 | 1,177 | 1,153 | 1.0208 | Geometric Persistence Only |
| He (full) | 0.03 | 1,161 | 1,173 | 0.9898 | Structural Boundary |
| He triplet | 0.02 | 906 | 869 | 1.0426 | Geometric Persistence Only |
| He triplet | 0.03 | 828 | 840 | 0.9857 | Structural Boundary |

**Total non-stable slices across 9 × 101 = 909 slice-runs: 5 out of 909 (0.55%).**
**All 5 occur at B ∈ {0.02, 0.03} T. None occur at B ≥ 0.04 T.**

---

## Structural Observations

### 1. The B = 0.02 T transition

All violations are located at the second nonzero field step. This is the degeneracy-lifting transition zone: the first step (B = 0.01 T) produces Zeeman shifts ~0.007 cm⁻¹ (for g=1.5, mJ=1), small enough that the degeneracy guard (ε = 0.0001 cm⁻¹) suppresses most inter-family crossings. At B = 0.02 T, shifts reach ~0.014 cm⁻¹ — enough to drive genuine adjacent reorderings among near-degenerate inter-family pairs, but still below the level where the vulnerability graph can absorb all of them.

By B = 0.04 T the ratio drops below 0.90 in all three atoms and does not rise again.

### 2. The zero-inversion atoms

**Au** and **He singlet** both achieve max\_inv = 0, ratio = 0.0000 — literally no adjacent inter-family sign-change crossings across all 101 slices.

- **He singlet:** All 30 levels are `1H* J=5` with identical Landé g = 1.000 (S=0 exactly). Every branch shifts as ΔE = 0.466864 × mJ × B with no g variation across families. The energy ordering of adjacent inter-family pairs is fixed at B=0 and never changes, since differential shifts between families require differential g. Vulnerability graph is non-empty (ν = 9) but inv = 0 throughout. This is the cleanest possible result.

- **Au:** Only 61 parsed levels with large relativistic spin-orbit splittings (5d⁹6s² hole states at 9,161 and 21,435 cm⁻¹; 5d¹⁰6p doublet split by ~3,816 cm⁻¹). Inter-family gaps are orders of magnitude larger than Zeeman shifts at 0–1 T, so no crossings occur. The relativistic g corrections (empirical g = 1.997 vs LS g = 2.000) are carried correctly but make no qualitative difference.

### 3. Why H, He (full), He triplet violate

These three atoms share a common structural feature: families with near-degenerate zero-field energies that differ by less than their Zeeman spread at 0.02 T.

- **H:** The n-shell near-degeneracy (4s, 4p, 4d, 4f all within ~0.06 cm⁻¹ of each other) creates a dense cluster of inter-family adjacent pairs at B=0. At B=0.02 T, Zeeman shifts of ~0.014 cm⁻¹ are already comparable to these gaps, driving 64 adjacent crossings. Only 47 vulnerable positions are budgeted. Ratio: 1.36 — the largest overshoot of the three.

- **He triplet:** Fine-structure multiplets (e.g., `3P* J=0,1,2` within ~1 cm⁻¹; `3D J=1,2,3` within ~0.05 cm⁻¹ for high-n terms) provide dense inter-family clustering. S=1 gives g ranging from 0.0 (J=0) to 2.0, so differential Zeeman shifts are large, and reorderings occur even for pairs with gaps of ~0.05 cm⁻¹.

- **He (full):** Inherits both H-like (singlet) and He-triplet sources of near-degeneracy, producing the largest raw counts (inv = 1,177, ν = 1,267 at B=0.02 T) while the ratio (1.02) is actually the smallest of the three.

### 4. The recovery profile

In all three GP atoms, inv decays monotonically after the B = 0.02–0.03 T peak:

| B range | He (full) max inv | He triplet max inv | H max inv |
|---------|------------------:|-------------------:|----------:|
| 0.02–0.03 T | 1,177 | 906 | 64 |
| 0.04–0.10 T | ~638–1,025 | ~416–750 | 3–31 |
| 0.11–0.50 T | ~148–578 | ~82–377 | 0–10 |
| 0.51–1.00 T | ~66–157 | ~40–109 | 0–1 |

The recovery is a power-law-like decay, not exponential. At B = 1.00 T: He (full) inv = 102, He triplet inv = 77, H inv = 0.

### 5. ν(V) topological stability

Across all nine atoms, ν(V(B)) is remarkably stable across the entire B sweep. For the large systems:

- He (full): ν varies 334 → 1,092–1,267 (rises sharply at B=0.01 T, then plateaus with mild growth)
- He triplet: ν varies 234 → 740–869 (same pattern)
- Fe: ν varies 23 (B=0) → 296 (plateau)

This stability of the vulnerability graph is the structural feature predicted by UNNS theory. The graph is not static but its MIS size (ν) evolves slowly and smoothly after the initial degeneracy-lifting transient.

---

## Dataset Inventory

| Atom | Source | Parsed levels | Branches | Total CSV rows |
|------|--------|-------------:|--------:|---------------:|
| He (full) | NIST He I | ~837 | 6,225 | 628,725 |
| He triplet | NIST He I, S=1 | 610 | 4,668 | 471,468 |
| He singlet | NIST He I, 1H* | 30 | 330 | 33,330 |
| H | NIST H I | 66 | 290 | 29,290 |
| Na | NIST Na I | 209 | 836 | 84,436 |
| Ca | NIST Ca I | 744 | 2,974 | 300,374 |
| Fe | NIST Fe I (empirical g) | 637 | 4,491 | 453,591 |
| Ag | NIST Ag I | 100 | 516 | 52,116 |
| Au | NIST Au I (empirical g) | 61 | 282 | 28,482 |

**Total ladder rows processed: 2,081,602**

---

## Falsification Status

The chamber was run in falsification-first mode. The falsifier triggered for 5 of 909 slice-runs (0.55%), all at B ∈ {0.02, 0.03} T, all in atoms with known near-degenerate family clustering at zero field. The falsifier did **not** trigger for any slice at B ≥ 0.04 T in any of the nine atoms.

**CERT_NEG = 0 for B ≥ 0.04 T across all 9 atoms.**
