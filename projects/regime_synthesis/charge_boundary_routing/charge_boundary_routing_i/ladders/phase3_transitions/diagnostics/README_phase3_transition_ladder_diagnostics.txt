Charge Boundary Routing I
Phase 3 — Transition Ladder Diagnostics

Generated UTC: 2026-06-15T18:31:26.061331+00:00
Input rows: 7
Files written: 24

Encoding stats:
- charge_balance_error: rows=7, unique=1, min=0.0, max=0.0
- initial_total_charge: rows=7, unique=3, min=-1.0, max=1.0
- final_total_charge: rows=7, unique=3, min=-1.0, max=1.0
- charged_multiplicity_delta: rows=7, unique=2, min=0.0, max=2.0
- neutral_multiplicity_delta: rows=7, unique=3, min=0.0, max=2.0
- layer_transition_code: rows=7, unique=4, min=1.0, max=4.0
- route_transition_code: rows=7, unique=5, min=1.0, max=5.0
- closure_transition_code: rows=7, unique=5, min=1.0, max=5.0
- boundary_preservation_code: rows=7, unique=1, min=1.0, max=1.0
- externalization_delta: rows=7, unique=2, min=1.0, max=2.0
- composite_count_delta: rows=7, unique=2, min=-1.0, max=0.0
- transition_class_code: rows=7, unique=5, min=1.0, max=5.0

Codebooks:
layer_transition_code:
  1: A->A;A
  2: A->A;A;A
  3: C->A;A
  4: C->C;A;A
route_transition_code:
  1: COMPOSITE_INTEGER_ROUTE->FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE
  2: COMPOSITE_NEUTRAL_ROUTE->COMPOSITE_INTEGER_ROUTE;FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE
  3: COMPOSITE_NEUTRAL_ROUTE->FREE_NEUTRAL_ROUTE;FREE_NEUTRAL_ROUTE
  4: FREE_INTEGER_ROUTE->FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE
  5: FREE_INTEGER_ROUTE->FREE_INTEGER_ROUTE;FREE_NEUTRAL_ROUTE;FREE_NEUTRAL_ROUTE
closure_transition_code:
  1: COMPOSITE_INTEGER_CLOSURE->FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE
  2: COMPOSITE_NEUTRAL_CLOSURE->COMPOSITE_INTEGER_CLOSURE;FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE
  3: COMPOSITE_NEUTRAL_CLOSURE->FREE_NEUTRAL_CLOSURE;FREE_NEUTRAL_CLOSURE
  4: FREE_INTEGER_CLOSURE->FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE
  5: FREE_INTEGER_CLOSURE->FREE_INTEGER_CLOSURE;FREE_NEUTRAL_CLOSURE;FREE_NEUTRAL_CLOSURE
transition_class_code:
  1: COMPOSITE_TO_COMPOSITE_PLUS_EXTERNALS
  2: COMPOSITE_TO_EXTERNALS
  3: EXTERNAL_TO_EXTERNALS
  4: LEPTONIC_EXTERNAL_DECAY
  5: NEUTRAL_COMPOSITE_TO_RADIATION

Constant / low-diversity encodings flagged:
- charge_balance_error: constant_or_low_diversity_seed_encoding
- boundary_preservation_code: constant_or_low_diversity_seed_encoding
