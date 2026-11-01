# Source crosswalk — what is inherited, what is new

Governing question (GEO-HD-1): can the arithmetic of UNNS generation determine how occurrence geometries transform, branch, merge, preserve
information or become obstructed, and can this be stated as laws in 3, 4 and more dimensions?  This release works on the mathematics directly:

    Generation  ->  Relationships  ->  Geometry  ->  General laws        (no arrow is assumed; each is a theorem or an obstruction below)

## Frozen inputs (read-only, hash-pinned or cited)
| object | source | role here |
|---|---|---|
| `x=a/b`, `D(x)={d>=2: d^2|a, d=1 (mod b)}`, `L=lcm D`, `G=gcd{d-1}`, `C(x)=x+L^2/G` | `GEO_HD_1_PROJECT/DEFINITIONS.md`; `src/frozen/geo1lib.py` (`fibre_q`, `Cstep`) | the collective map is **applied**, never replaced by SELECT-II arithmetic |
| exponent fibre `F`, lattice `Lambda_b`, region-Graver moves, parallelotope cells, GF(p) homology | GEO-I v012 `frozen/geo2lib.py` (`analyse`) — pinned, sha-256 in `results/PINS.json` | the complete state record G(m) |
| SELECT-II edge `m --N--> m(N+1)^2/N`, `N | m`; square-root transport `S' = S(N+1)/c` | DEFINITIONS.md (A2) | histories |
| FIELD-I v005 T31/T32 (`D(x) ⊂ D(x')`; `G_inf=1 ⇒ x_{n+3}=4x_n` eventually), v009 T49–T58 (one-step law, T50 eight-step orbit for G=11, T51 eventual exact scaling), v012 T69–T73 (reset-descent κ, regime-I tail bound `4κ₃(t)`) | `UNNS_ENTANGLE_I/FIELD-I/FIELD-I_v00x/THEOREMS.md` (read-only; not re-proved here) | G>1 theory is **cited**, only spot-checked (T50) |
| route complex of HD-1D v003, contents of the four v001 multidimensional examples | `GEO_HD_BRIDGE_v001` (unchanged) | benchmark contents B4/B5 only |

## What is new in v002 (all with proofs or exact checks in this package)
`theory/GEOMETRIC_HISTORIES.md` (B2-T1,T2) · `RECOMBINATION_GEOMETRY.md` (B2-T3,T4,T5) · `FIELD_REGIMES.md`, `CARRY_TRANSITIONS.md` (B2-T6,T7,T8) ·
`EVENT_CORRESPONDENCE.md` (B2-T9…T13) · `HIGH_DIMENSIONAL_LAWS.md` (B2-T3 corollary, finite-exact tables) · `GLOBAL_SYNTHESIS.md` (B2-T14).

## Not attached / not re-derived (stated, not hidden)
* GEO-I geometry of **rational** states with `b>1` (non-trivial `Lambda_b`) is only sampled (`GEOMETRIC_HISTORIES.md` §5); no theorem.
* FIELD-I `G>1` regimes (carry cycles, class closure) are cited from v009–v012, not re-derived; only T50 is re-derived from the definition.
* HD-1B counterexamples and the HD-1D arithmetic-history theorems are not repeated (they are used as input contents only).
Same-author caveat: all sources and this release come from one research line; C3 is **not claimed** and novelty is **not assessed**.
