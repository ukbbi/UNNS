# PREFLIGHT_v008 — fair solver implementations and outcome-blind implementation gate (SCR-III-B)

Additive package: extract into the project root; v005–v007 must be in place (read-only; hashes checked, test F1). Ubuntu/WSL, `g++`, Python 3.

```bash
python3 scr_iii_b/solvers/validate_v008.py     # ~1 min
python3 scr_iii_b/solvers/test_v008.py
```

* `solvers_v008.cpp` — B0 (Gray-code exhaustive), G1 (nominal scan + grammar check, direct energy on survivors), G2 (constructive generation with incremental pair-energy updates), B1 (exact branch-and-bound, admissible bound), boundtest mode, operation counters, built-in outcome-blind guard (3×3, W>0 refused without `--unblind-after-freeze`).
* `tie_policy_v008.py`, `diagnostics_v008.py` — candidate tie policy (proposed for testing, not frozen) and Δ_G / ρ_G = W/Δ_G diagnostics (tested on public 1×1/2×2 only; not run on 3×3 or nulls).
* The 3×3 patch is run only at the published W=0 anchor. The verdict is an implementation verdict and implies nothing about H-G/H-P/H-T/H-C.
* `scr_iii_b/drafts/` — wording-amended copies of the unfrozen SPEC and PREREG drafts plus `DRAFT_AMENDMENTS_v008.md`.
