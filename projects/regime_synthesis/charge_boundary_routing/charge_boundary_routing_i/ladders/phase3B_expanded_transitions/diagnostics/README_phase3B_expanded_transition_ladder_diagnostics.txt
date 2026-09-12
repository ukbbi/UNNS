Charge Boundary Routing I
Phase 3B — Expanded Allowed Transition Corpus
README_phase3B_expanded_transition_ladder_diagnostics.txt

Generated UTC: 2026-06-15T19:11:20.601493+00:00
Input rows: 38
Files written: 48

Purpose:
  Diagnose Phase 3B expanded transition ladder encodings before chamber upload.

Encoding stats:
- charge_balance_error: rows=38, unique=1, min=0.0, max=0.0
- initial_total_charge: rows=38, unique=4, min=-1.0, max=2.0
- final_total_charge: rows=38, unique=4, min=-1.0, max=2.0
- charged_multiplicity_delta: rows=38, unique=3, min=0.0, max=2.0
- neutral_multiplicity_delta: rows=38, unique=4, min=-1.0, max=2.0
- layer_transition_code: rows=38, unique=7, min=1.0, max=7.0
- route_transition_code: rows=38, unique=13, min=1.0, max=13.0
- closure_transition_code: rows=38, unique=13, min=1.0, max=13.0
- category_transition_code: rows=38, unique=10, min=1.0, max=10.0
- boundary_preservation_code: rows=38, unique=1, min=1.0, max=1.0
- externalization_delta: rows=38, unique=3, min=0.0, max=2.0
- composite_count_delta: rows=38, unique=4, min=-1.0, max=2.0
- transition_class_code: rows=38, unique=10, min=1.0, max=10.0
- transition_family_code: rows=38, unique=8, min=1.0, max=8.0
- initial_multiplicity: rows=38, unique=1, min=1.0, max=1.0
- final_multiplicity: rows=38, unique=2, min=2.0, max=3.0
- charged_initial_count: rows=38, unique=2, min=0.0, max=1.0
- charged_final_count: rows=38, unique=3, min=0.0, max=2.0
- neutral_initial_count: rows=38, unique=2, min=0.0, max=1.0
- neutral_final_count: rows=38, unique=3, min=0.0, max=2.0
- composite_initial_count: rows=38, unique=2, min=0.0, max=1.0
- composite_final_count: rows=38, unique=4, min=0.0, max=3.0
- external_initial_count: rows=38, unique=2, min=0.0, max=1.0
- external_final_count: rows=38, unique=4, min=0.0, max=3.0

Flagged constant / low-diversity encodings:
- charge_balance_error: constant_seed_or_invariant_encoding; unique=1; values=[0.0]
- boundary_preservation_code: constant_seed_or_invariant_encoding; unique=1; values=[1.0]
- initial_multiplicity: constant_seed_or_invariant_encoding; unique=1; values=[1.0]

Codebooks:

layer_transition_code:
  1: A->A;A
  2: A->A;A;A
  3: C->A;A
  4: C->C;A
  5: C->C;A;A
  6: C->C;C
  7: C->C;C;C

route_transition_code:
  1: COMPOSITE_INTEGER_ROUTE->COMPOSITE_INTEGER_ROUTE;COMPOSITE_INTEGER_ROUTE
  2: COMPOSITE_INTEGER_ROUTE->COMPOSITE_INTEGER_ROUTE;COMPOSITE_NEUTRAL_ROUTE
  3: COMPOSITE_INTEGER_ROUTE->COMPOSITE_NEUTRAL_ROUTE;COMPOSITE_INTEGER_ROUTE
  4: COMPOSITE_INTEGER_ROUTE->FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE
  5: COMPOSITE_NEUTRAL_ROUTE->COMPOSITE_INTEGER_ROUTE;COMPOSITE_INTEGER_ROUTE
  6: COMPOSITE_NEUTRAL_ROUTE->COMPOSITE_INTEGER_ROUTE;COMPOSITE_INTEGER_ROUTE;COMPOSITE_NEUTRAL_ROUTE
  7: COMPOSITE_NEUTRAL_ROUTE->COMPOSITE_INTEGER_ROUTE;FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE
  8: COMPOSITE_NEUTRAL_ROUTE->COMPOSITE_NEUTRAL_ROUTE;COMPOSITE_NEUTRAL_ROUTE
  9: COMPOSITE_NEUTRAL_ROUTE->COMPOSITE_NEUTRAL_ROUTE;FREE_NEUTRAL_ROUTE
  10: COMPOSITE_NEUTRAL_ROUTE->FREE_NEUTRAL_ROUTE;FREE_NEUTRAL_ROUTE
  11: FREE_INTEGER_ROUTE->FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE
  12: FREE_INTEGER_ROUTE->FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE;FREE_NEUTRAL_ROUTE
  13: FREE_NEUTRAL_ROUTE->FREE_INTEGER_ROUTE;FREE_INTEGER_ROUTE

closure_transition_code:
  1: COMPOSITE_INTEGER_CLOSURE->COMPOSITE_INTEGER_CLOSURE;COMPOSITE_INTEGER_CLOSURE
  2: COMPOSITE_INTEGER_CLOSURE->COMPOSITE_INTEGER_CLOSURE;COMPOSITE_NEUTRAL_CLOSURE
  3: COMPOSITE_INTEGER_CLOSURE->COMPOSITE_NEUTRAL_CLOSURE;COMPOSITE_INTEGER_CLOSURE
  4: COMPOSITE_INTEGER_CLOSURE->FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE
  5: COMPOSITE_NEUTRAL_CLOSURE->COMPOSITE_INTEGER_CLOSURE;COMPOSITE_INTEGER_CLOSURE
  6: COMPOSITE_NEUTRAL_CLOSURE->COMPOSITE_INTEGER_CLOSURE;COMPOSITE_INTEGER_CLOSURE;COMPOSITE_NEUTRAL_CLOSURE
  7: COMPOSITE_NEUTRAL_CLOSURE->COMPOSITE_INTEGER_CLOSURE;FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE
  8: COMPOSITE_NEUTRAL_CLOSURE->COMPOSITE_NEUTRAL_CLOSURE;COMPOSITE_NEUTRAL_CLOSURE
  9: COMPOSITE_NEUTRAL_CLOSURE->COMPOSITE_NEUTRAL_CLOSURE;FREE_NEUTRAL_CLOSURE
  10: COMPOSITE_NEUTRAL_CLOSURE->FREE_NEUTRAL_CLOSURE;FREE_NEUTRAL_CLOSURE
  11: FREE_INTEGER_CLOSURE->FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE
  12: FREE_INTEGER_CLOSURE->FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE;FREE_NEUTRAL_CLOSURE
  13: FREE_NEUTRAL_CLOSURE->FREE_INTEGER_CLOSURE;FREE_INTEGER_CLOSURE

category_transition_code:
  1: baryon->baryon;gauge_boson
  2: baryon->baryon;lepton;lepton
  3: baryon->baryon;meson
  4: gauge_boson->lepton;lepton
  5: lepton->lepton;lepton;lepton
  6: meson->gauge_boson;gauge_boson
  7: meson->lepton;lepton
  8: meson->meson;gauge_boson
  9: meson->meson;meson
  10: meson->meson;meson;meson

transition_class_code:
  1: COMPOSITE_TO_COMPOSITES
  2: COMPOSITE_TO_COMPOSITE_PLUS_EXTERNALS
  3: COMPOSITE_TO_COMPOSITE_PLUS_RADIATION
  4: COMPOSITE_TO_EXTERNALS
  5: EXTERNAL_TO_EXTERNALS
  6: LEPTONIC_EXTERNAL_DECAY
  7: NEUTRAL_COMPOSITE_TO_COMPOSITES
  8: NEUTRAL_COMPOSITE_TO_COMPOSITE_PLUS_RADIATION
  9: NEUTRAL_COMPOSITE_TO_RADIATION
  10: NEUTRAL_EXTERNAL_TO_EXTERNALS

transition_family_code:
  1: baryon_decay
  2: baryon_resonance_decay
  3: charged_meson_decay
  4: neutral_meson_decay
  5: neutral_or_charged_vector_meson_decay
  6: radiative_decay
  7: seed_continuity
  8: w_z_mediated_channel

Recommended first chamber inputs:
  Use non-constant one-column ladders from:
    ladders/phase3B_expanded_transitions/one_column/

Usually skip first if constant:
  charge_balance_error
  boundary_preservation_code

Primary Phase 3B robustness targets:
  route_transition_code
  closure_transition_code
  transition_class_code
  transition_family_code
  category_transition_code