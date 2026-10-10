# PREFLIGHT_v007 — 3×3 exact-verification feasibility and solver-selection gate (SCR-III-B)

Additive package: extract into the project root. Requires frozen v005 and v006 in place (only read; verified against their local manifests, test F1). Needs `g++` and Python 3 (Ubuntu/WSL); the verifier is compiled into a temporary directory.

```bash
python3 scr_iii_b/exact3/validate_v007.py     # ~35 s, ~140 MB RAM
python3 scr_iii_b/exact3/test_v007.py
```

* `verify3_v007.cpp` — exact full-space verifier (direct + Gray-code energy, grammar scan, window counts, constructive generation). Takes K_ij from the frozen v005 evaluator and incidence masks from the v006 grammar; contains no physics constants.
* `validate_v007.py` — cross-validates it against the frozen python (every 1×1/2×2 level threshold, 2,002 seeded 3×3 states, grammar count by three routes), measures component costs, writes the solver-selection memo.

Design rule: the 3×3 space is scanned completely, but only the W=0 anchor is reported; the 3×3 spectrum and all W>0 window outcomes are deliberately withheld so that the window rule can still be frozen blind. This is a gate, not a primary run: no G_net, no transfer claim, nothing frozen.
