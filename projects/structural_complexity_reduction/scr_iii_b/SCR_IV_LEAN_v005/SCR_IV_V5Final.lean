import Fin_g
import Fin_n
import SCR_IV_V5
/-! # IV-5 FINAL: unconditional instantiation. Imports the ACCEPTED IV-4B result theorems (`ground_exact_min`, `nongT_exact_min`; the 1148 batch theorems are
imported as compiled modules, not re-run) and concludes the exact gap and both prospective predictions for the encoded model. -/
namespace SCR_IV
theorem iv5_final : ∀ U0 Un : Int, ObjAll U0 → ObjNonGrammar Un →
    U0 = claimedGroundNum ∧ Un = claimedNonGTrue ∧ Un - U0 = 12095447728404694790 ∧ 0 < Un - U0 ∧ PredLt1 U0 Un ∧ PredR2 U0 Un :=
  iv5_of_minima ground_exact_min nongT_exact_min
end SCR_IV
