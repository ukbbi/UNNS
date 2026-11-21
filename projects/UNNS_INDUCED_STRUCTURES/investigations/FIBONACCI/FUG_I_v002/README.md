# FUG-I v002 — Fibonacci Geometry Induced by the UNNS Substrate

**Phase 2: Complete Directed Ancestry and the Geometry of Fibonacci Layers**

**Status:** runnable / independently checked / locally staged. **No GitHub changes.** This release is separate from and preserves the verified `FUG_I_v001` baseline.

## What changed from v001

v001 verified all directed paths of length 1, 2, or 3 between the first 48 indexed Fibonacci numbers. Phase 2 removes the path-depth cutoff entirely and expands the exact finite endpoint window to **indices 1 through 84**. A finite exact predecessor descent determines all possible path lengths. The release also constructs **squarefree ancestral-root spectra** and proves scale-lifting monotonicity for complete backward histories.

### Primary findings

- **All-depth endpoint census:** exactly 4 reachable indexed Fibonacci endpoint pairs with 8 labelled routes, still the same pairs witnessed by v001. There are no new endpoint pairs through index 84 (and no hidden longer routes in that window).
- **Richer intermediate ancestry:** `F_12=144` has height 3, four squarefree terminal roots, 11 ancestral nodes including itself; `F_72=498454011879264` has height 5 and seven squarefree terminal roots, with 23 ancestral nodes including itself.
- **Theorem:** for any positive integer B, all depth-k ancestral paths of y inject into depth-k paths of By; `H_k(By)>=H_k(y)`, `h(By)>=h(y)`. In particular this holds from `F_m` to `F_n` when `m|n`.
- **Important obstruction:** root-set inclusion is not forced, even when Fibonacci indices divide and the route counts are monotone. The squarefree root sets of F12 and F24 are disjoint.
- **Controls:** complete all-depth Lucas and shifted-Fibonacci probes find 3 pairs and 3 routes each. No statistical significance is claimed.

## Install in the local research workspace

Extract the archive so it creates a NEW sibling directory to `FUG_I_v001`:

```text
UNNS_INDUCED_STRUCTURES\
  investigations\
    FIBONACCI\
      FUG_I_v001\  (unchanged)
      FUG_I_v002\  (this package)
```

Open the extracted `FUG_I_v002` directory in Windows Explorer; type `powershell` in its address bar and press Enter. Run:

```powershell
py -3 scripts\run_p2.py
py -3 scripts\verify_p2.py
```

If `py` is unavailable, replace `py -3` by `python`. **No BAT, PS1, admin privilege, or Windows security-setting change is needed.** All output is regenerated under `results\`, regardless of your working-directory drive or spaces in the path.

## Files

- `theory/SPEC.md`: exact mathematical scopes and definitions.
- `theory/THEOREMS.md`: proofs and status-labelled results / open problems.
- `scripts/arith.py`: stdlib exact arithmetic, certified 64-bit factoring and predecessor sets.
- `scripts/run_p2.py`: complete ancestry-route enumeration, Fibonacci endpoint census, controls and figure.
- `scripts/verify_p2.py`: independent route-count DP, naive square-divisor oracle for the F1..F60 ancestral closure, edge checks and scaling tests.
- `results/fib_routes_all_84.csv`: eight complete routes.
- `results/fib_pairs_all_84.csv`: four endpoint pairs.
- `results/fib_ancestry_84.csv`: ancestral geometry profiles of all 84 Fibonacci layers.
- `results/summary.json`: machine-readable findings and controls.
- `results/controls_84.json`: complete finite controls.
- `figures/ancestry_144.svg`: diagram derived from the true 144 predecessor graph.

## Interpretation discipline

The fixed original UNNS primitive is `M ⟂ N = M(N+1)^2/N` for positive integers M,N, including rational non-anchor outputs. The directed integer-only `T_N(x)` self-substitution rule is an explicit **SELECT-II continuation choice**. Conclusions about its directed path geometry are not automatically universal statements about the entire Substrate.

Finite comparisons are not claims that Fibonacci obeys UNNS evolution; the purpose is to analyze mathematical structures induced by superimposition. We do not assume a universality thesis or physical mechanism.

## Reproducibility status

- Exact 84-index reverse-factor census with 64-bit deterministic primality and factor recombination: PASS.
- Independent route-count dynamic program: PASS.
- Naive square-divisor predecessor oracle on all 150 unique reverse states reached by Fibonacci targets with indices <=60: PASS.
- All 210 reverse states reached by first 84 Fibonacci targets checked for factored prime product: PASS.
- Every depth-k ancestry injection across all index-divisible Fibonacci pairs in the window: PASS.

See `RELEASE_NOTES.md`, `SOURCE_PROVENANCE.md` and `MANIFEST.json` for boundaries and provenance.
