# GIG-I v003 — Higher-Dimensional Information and Arithmetic Boundary Rigidity in UNNS Generative Histories

UNNS Generative Information Geometry · Phase III · independent package beside the frozen GIG_I_v001 and GIG_I_v002 (never modified; imported read-only).

**Read first:** `RESULTS/report.md` (mathematics before procedure; answers the eight questions of the specification in order).
Then `THEORY/THEOREMS.md` (status-tagged register), `THEORY/PROOFS.md`, `THEORY/OPEN_PROBLEMS.md`.

## What v003 does
| Layer | Content |
|---|---|
| Algebra | Lemma F (feasible-family law), **T16** ordered-block factorization, **T17** exact face thresholds K_F = lcm D(Pref(F)), **T18** divisibility filtration with the accounting law Δβ₂ = Δf₂ − Δρ₂ − Δρ₃ |
| Topology | **T19** third-boundary-rank obstruction; **T21a/b** what changes H₂ and the exact arithmetic obstruction theorem for the two β₂ = 1 anchors |
| Recognition | **T20a** completeness, **T20b** soundness in full P_k (k ≤ 7 all faces, k = 8 three-faces), **T20c** verified reconstruction domains, **T20d** open gap, **T20e** Z1 negative control |
| Information | J₃ = rank ∂₃, D₃ = f₃ − J₃, A₃([G];𝒟) = log₂|ℛ₃([G];𝒟)| (domain-relative) and H(J₃ | 2-skeleton data) |

## Layout
`THEORY/` definitions, theorems, proofs, open problems · `ENGINE/` block_factor, face_threshold, cell_boundary, source_filtration, cell_recognition, boundary_info (+ `_v2path` locator for the frozen packages) ·
`EXPERIMENTS/` E9 faces, E10 H₂ anchors, E11 source-transition events, E12 recovery, E13 information, E14 k=7 probe, `run_all.py`, `make_manifest.py` ·
`CERTIFICATES/` anchor H₂ certificates (cycle z, cochain φ, 3-cells and incidences) and complete event tables · `TESTS/test_v003.py` · `RESULTS/` · `CORRECTIONS/V002_T12_SCOPE.md` · `MANIFEST.json` (SHA-256 of every file and of the frozen parents' manifests).

## Run
`RUN_V003.bat test` (unit tests; add `set GIG_FROZEN_SRC=...\GEO_HD_1D_v004\src` for the read-only frozen cross-check) · `RUN_V003.bat quick` (minutes) · `RUN_V003.bat full` (about an hour on 2 CPUs).
Or: `python -m unittest discover -s TESTS -v`; `cd EXPERIMENTS && python run_all.py [--quick]`. Python ≥ 3.10, standard library only.
GIG_I_v001 and GIG_I_v002 must be siblings of this folder (or set `GIG_V001`, `GIG_V002`).

## Discipline
Exact integer/Fraction arithmetic for every divisibility, rank and homology certificate; floats only for entropies in the report. Bounded searches are reported as bounded searches
with their domains; domain-dependent and universal conclusions are separated in the report. No remote repository was modified.
