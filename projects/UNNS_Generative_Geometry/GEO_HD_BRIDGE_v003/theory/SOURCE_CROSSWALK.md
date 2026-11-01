# Source crosswalk (v003)

Programme question: what mathematical structure remains after the integer-state collapse (B2-T1), how is it organised over histories, and how does it behave under collective maps with G>1?  
The work is organised by the mathematics (state geometry -> histories -> collective dynamics -> comparison); programme labels are used only to cite earlier work. No arrow between these layers is assumed; each is a theorem, a finite-exact table or an obstruction below.

## Frozen inputs (read-only)
| object | source | used as |
|---|---|---|
| `x=a/b`, active primes `p` with `q_p=floor(v_p(a)/2)>=1`, box `B`, lattice `Lambda_b={alpha: prod p^alpha = 1 mod b}`, `F=(B ∩ Lambda_b)\{0}`, `D={prod p^alpha}` | GEO-I v012, `src/frozen/geo2lib.py` (pinned, sha-256 in `results/PINS.json`) | the state record G(x) |
| region-Graver set: conformally minimal nonzero vectors of `Lambda_b` inside `[-q,q]`; parallelotope cells with all vertices in `F`; GF(2) homology | same | `K_move`; `K_axis` uses the unit vectors |
| `D(x)={d>=2: d^2 | a, d = 1 mod b}`, `L=lcm D`, `G=gcd{d-1}`, `C(x)=x+L^2/G` | FIELD-I (`src/frozen/geo1lib.py`) | collective map, applied exactly |
| SELECT-II edge `m --N--> m(N+1)^2/N`, `N | m`; corrected B2-T9 (`sigma' > sigma`, `D' != D`, no inclusion) | v001/v002 + `GEO_HD_BRIDGE_v002_ERRATUM_B2-T9.md` | histories |
| contents of the 3/4-prime route complexes (source 4, labels 2,3,4,5,6[,7]) | HD-1D / v001 / v002 | test cases for R3-C/D |
| FIELD-I T31/T32/T50/T51/T69-T73 | FIELD-I v005-v012 | cited, **not re-proved** except T50 (re-proved for all k, R3-T5c) |

## Not attached / not re-derived
* FIELD-I G>1 transition theory T49-T58, T69-T73 (only T50's family is re-proved).
* GEO-HD-1B, HD-1D v001-v004 theorems (used only as contents).
* GitHub sources are read-only and were not consulted.

## Corrections carried in this release
* `GEO_HD_BRIDGE_v002_ERRATUM_B2-T9.md` (accepted).
* `GEO_HD_BRIDGE_v002_ERRATUM_B2-T7.md` (new, found here): rigid scaling `x_{n+3}=4x_n` does **not** characterise `G_inf=1`; see `COLLECTIVE_REGIMES.md` R3-T5c.

Inherited verification of v001/v002/HD-1D/E2_P4 is **NOT_RERUN** (sha-256 manifest integrity only). C3 not claimed; novelty not assessed; same-author caveat.
