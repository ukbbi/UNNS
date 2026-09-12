# 03 — Data Requirements

## Minimum event-level fields

| Field | Meaning |
|---|---|
| device | Tokamak / stellarator name |
| shot_id | Experimental discharge identifier |
| transition_time | L-H or H-L transition time |
| transition_type | LH, HL, dithering, ELM |
| mode_before | L, D, H, unknown |
| mode_after | L, D, H, unknown |
| P_heat | applied heating power |
| P_loss | power crossing plasma boundary if available |
| n_e | line/core/edge electron density |
| T_e_edge | electron temperature near edge/pedestal |
| I_p | plasma current |
| B_t | toroidal magnetic field |
| R | major radius |
| a | minor radius |
| kappa | elongation |
| q95 | edge safety factor if available |
| xpoint_height | divertor/X-point geometry if available |
| tau_E | energy confinement time if available |
| H98 | H98 confinement factor if available |
| ELM_flag | whether ELM occurs in the window |

## Preferred time-series fields

| Field | Why |
|---|---|
| time | alignment coordinate |
| D_alpha | transition/ELM marker |
| W_plasma | stored energy |
| density_time_series | confinement and threshold tracking |
| Te_profile | pedestal and edge-gradient reconstruction |
| ne_profile | pedestal and density-gradient reconstruction |
| Er_or_ExB | shear / edge reordering |
| turbulence_signal | route fragmentation proxy |
| magnetic_fluctuation | MHD / ELM / boundary instability |
| heat_flux | boundary release proxy |
| mode_label | supervised comparison label |

## UNNS computed fields

| Field | Description |
|---|---|
| m_edge | edge admissibility margin |
| kappa_edge | edge connectivity / route stability |
| route_persistence | persistence of transport-retention pathways |
| turbulence_fragmentation | local route fragmentation estimate |
| pedestal_load | gradient stress stored at boundary |
| boundary_overload_index | proximity to ELM-like release |
| transition_score | L-H transition likelihood |
| elm_risk_score | pre-ELM overload likelihood |
