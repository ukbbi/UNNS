import SCR_IV_Witness
import SCR_IV_Bound
import SCR_IV_Certificate
/-! Axiom audit: every theorem below must depend on no `sorryAx` and no `Lean.ofReduceBool` (native_decide). -/
open SCR_IV
#print axioms ground_valid
#print axioms nonG_valid
#print axioms ground_in_grammar
#print axioms ground_counts
#print axioms nonG_violations
#print axioms nonG_not_in_grammar
#print axioms nonG_violating_vertex
#print axioms nonG_counts
#print axioms ground_energy_exact
#print axioms nonG_energy_exact
#print axioms ground_energy_indexed
#print axioms nonG_energy_indexed
#print axioms ground_hRat
#print axioms nonG_hRat
#print axioms ground_matches_reported
#print axioms nonG_matches_reported
#print axioms witness_order
#print axioms witness_gap_interval
#print axioms table_wellFormed
#print axioms masks_distinct
#print axioms island_coverage
#print axioms kRows_count
#print axioms kRows_shape
#print axioms id_eq_of_spins
#print axioms sigma_length
