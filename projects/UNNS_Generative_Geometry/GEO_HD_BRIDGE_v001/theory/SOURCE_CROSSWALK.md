# Source crosswalk (what is inherited, what is new)

Frozen inputs used read-only: GEO_HD_1_PROJECT/DEFINITIONS.md (SELECT-II R(N), D(x), FIELD-I map C), GEO_HD_1D_v001–v004 (thresholds K(w), route complex of v003, rewrite graphs of v004), FIELD-I v001 `src/fibres.py::admissible_d` and v012 notation (cross-check only; FIELD-I source is not shipped here).
| object | defined in | used here as |
|---|---|---|
| R(N)=(N+1)^2/N, Delta_p | HD-1D v001/v004 | valuation displacements |
| route complex K_A (permutohedral, GF(2)) | HD-1D v003 route_topology.py (pinned copy) | feature carrier for dimension tests |
| D(m) (integer fibre), D(x) (rational fibre) | DEFINITIONS.md | occurrence incidence |
| C(x)=x+L^2/G | DEFINITIONS.md; FIELD-I v012 notation | collective map (re-implemented, not imported) |
Not attached: GEO-I exponent-coordinate fibre E_x, relation lattice, Graver-cell union, realized geometry. Only the occurrence fibre D is used (HD-C4 in the specification is therefore only partly addressed; see OPEN_PROBLEMS).
The two dynamics are never identified: SELECT-II (integer edges m -> m R(N)) and FIELD-I (C on realized rationals).
