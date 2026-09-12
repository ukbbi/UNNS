Charge Boundary Routing I
Phase 2C — Same-Charge Different-Route Control
README_phase2C_same_charge_route_control_diagnostics.txt

Generated UTC: 2026-06-15T20:26:34.871122+00:00
Rows: 5

Control question:
  Does same external charge Q = +1 imply same structural route?

Expected result:
  Same Q = +1 does not imply same structural route.

Objects:
  - positron
  - proton
  - pi_plus
  - k_plus
  - w_plus

Flagged constant encodings:
  - Q_over_e: constant_control_encoding; values=[1.0]
  - same_charge_constant: constant_control_encoding; values=[1.0]

Primary chamber inputs:
  phase2C_same_charge_ladder_structural_route_code.csv
  phase2C_same_charge_ladder_category_code.csv
  phase2C_same_charge_ladder_sub_category_code.csv
  phase2C_same_charge_ladder_layer_code.csv
  phase2C_same_charge_ladder_composite.csv
  phase2C_same_charge_ladder_external.csv
  phase2C_same_charge_ladder_boson.csv
  phase2C_same_charge_ladder_fermion.csv
  phase2C_same_charge_ladder_hadron.csv

Do not upload first:
  phase2C_same_charge_ladder_Q_over_e.csv
  phase2C_same_charge_ladder_same_charge_constant.csv

Codebooks:

layer_code:
  1: A
  2: C

route_class_code:
  1: COMPOSITE_INTEGER_ROUTE
  2: FREE_INTEGER_ROUTE

closure_class_code:
  1: COMPOSITE_INTEGER_CLOSURE
  2: FREE_INTEGER_CLOSURE

category_code:
  1: baryon
  2: gauge_boson
  3: lepton
  4: meson

sub_category_code:
  1: charged_baryon
  2: charged_lepton_antiparticle
  3: charged_light_meson
  4: charged_strange_meson
  5: charged_weak_gauge_boson

structural_route_code:
  1: composite_baryonic_integer_closure
  2: composite_mesonic_integer_closure
  3: composite_strange_mesonic_integer_closure
  4: external_gauge_integer_closure
  5: external_leptonic_integer_closure