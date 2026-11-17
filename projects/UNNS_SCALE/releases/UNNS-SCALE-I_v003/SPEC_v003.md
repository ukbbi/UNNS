# UNNS-SCALE-I v003 — SPEC (Scaled-Successor Metric Geometry)

Release: local only. Frozen baselines: v001 (`UNNS-SCALE-I/`), v002 (`UNNS-SCALE-I_v002/`) — never modified; hashed read-only by `verify_all_v003.py`.

## Definitions
G: SELECT-II graph on ℕ>0, edges {kN, k(N+1)²}. d: distance in G (never truncated).
d_B(n) = d(Bn, B(n+1)); D_B = sup_n d_B(n).

## Claims, status and where they are checked
| id | claim | status | check |
|---|---|---|---|
| P1.1 | d_B(n) ≥ 2 | PROVED | edge ratio ≥ 4 > 2; verifier exhaustive N<2000 |
| P1.2 | A\|B ⇒ d_B(n) ≤ d_A(n) pointwise | PROVED | scale-copy map; 181,500 exact pairs, 0 violations |
| C1.3 | D_B ≤ D_A; D_lcm ≤ min; lower bounds propagate down; μ_B ≤ μ_A | PROVED | from P1.2 |
| L1.4 | shortening ⇒ shortest paths leave BN | PROVED | isomorphism G[BN] ≅ G |
| L1.5 | d_B(n) ≤ 1 + d(B(n+1)², B(n+1)) | PROVED | label N = n |
| D1 | exact d_B(n), n ≤ 6000, B ∈ {1,2,3,4,5,6,7,8,10,12} | CERTIFIED | explicit paths + sympy disjoint balls |
| D1 | D_7 = 6 (n=163) ; D_12 ≥ 5 (n=25199) | CERTIFIED | verifier |
| T3.1 | class covers d_B ≤ K (see THEORY table) | PROVED | sympy-free polynomial identities, t<t0 exact |
| D3 | certified D_B=6 for 21 scales ≤ 96 and divisors | CERTIFIED | survey + P1.2 |
| D4 | typical shortening, plateau ≈ 3.70 | EXPERIMENTAL | survey B ≤ 96, n ≤ 500 |
| O1–O4 | D_B ≤ 5 for any B≥2; D_B ≥ 5 for all B; plateau limit; exceptional-class closed form | OPEN | — |

## Engines
- `exact_lib.py` — untruncated exact distance (meet-in-the-middle radii (1,1),(2,2),(3,2),(3,3); complete neighbourhoods; Pollard ρ + Miller–Rabin).
- `indep_check.py` — independent neighbourhoods via sympy; ball-disjointness certificates.
- `sym_lib.py`, `cover2.py`, `cover_cls.py`, `resume_cover.py` — symbolic polynomial-state path search and adaptive residue-class refinement (primes 2,3,5,7).
- `finalize_cover.py` — verifies identities, exact finite checks, exact densities.
- `poly_check.py` — sympy-free re-verification of identities (exact polynomial division, Cauchy-bound positivity, numeric replay).
- `run_D1_exact.py`, `run_D1b_survey.py`, `run_D3_hierarchy.py`, `run_D4_smooth.py` — result generators.
- `verify_all_v003.py` — full verifier; `--quick` for a faster run.

## Reproduction (approximate wall-clock on 2 cores)
```
python run_D1_exact.py 6000 1 2 3 4 5 6 7 8 10 12     # ~15 min
python run_D1b_survey.py 96 500                       # ~6 min
python cover2.py B K 3000 400   (B=2,3,4,5,6,10 K=5 ; B=12 K=4 with maxM 1500, then cover_cls.py 12 4 1260 1259 20000 150)
python finalize_cover.py B K                          # reads results/raw/cover_B_K.json copy via /tmp path argument
python run_D4_smooth.py B 3000000 2,3,5,7 100         # B = 1 2 4 6 12 24 48
python run_D3_hierarchy.py ; python verify_all_v003.py
```
(`finalize_cover.py B K path/to/raw.json` accepts the stored raw files in `results/raw/`; without the path it reads `/tmp/cover_B_K.json`.)

## Evidence discipline
Finite maxima are certified lower bounds on D_B. Universal upper bounds are claimed only where a polynomial identity covers the class. The classes left undecided at each K are listed in the results files and are OPEN.
