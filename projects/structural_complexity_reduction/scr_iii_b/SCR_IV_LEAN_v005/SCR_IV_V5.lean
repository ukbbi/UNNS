import SCR_IV_V4
/-! # IV-5: exact finite gap and the two prospective predictions for δ₄.
Definition (frozen, `GAP4_v010/PREDICTION_FREEZE_v001.md`): δ₄ = (E_nonG,min − E_0) / (k_B · 792 K), both minima of the FULL 40-spin Hamiltonian,
E_nonG,min over configurations violating the grammar. In the encoded model E = hScaled / 2^kShift in units of A, and A = A(792 K) in joules.
Constants (traced to the frozen sources, NOT back-solved from the reported δ₄):
* k_B = 1.380649e-23 J/K = 1380649 / 10^29 (exact, SI 2019; `physical_energy_v005.py: KB`), T_ref = 792 K (protocol).
* A(792 K) = `aJoule` = the binary64 value 1.0095767595046513e-18 returned by the frozen `physical_energy_v005.A_joule(792.0)`, taken as the exact dyadic rational
  (SCR_IV_Data). Its derivation from the physical parameters is NOT re-done in Lean.
* Range endpoints are the frozen DECIMAL literals 0.790439676056526 and 1.0333534753990623 (PREDICTION_FREEZE), read as exact decimal rationals.
δ₄ = delta4Num U0 Un / delta4Den as an exact fraction; all comparisons below are cross-multiplied integer inequalities (no floating point). -/
namespace SCR_IV

/-- k_B = kBNum / 10^29 J/K, exact. -/
def kBNum : Nat := 1380649
def tRef : Nat := 792

/-- δ₄ = delta4Num U0 Un / delta4Den, with U0 = ground and Un = non-grammar minimum in units of 2^-kShift A. -/
def delta4Num (U0 Un : Int) : Int := (Un - U0) * aJoule.1 * 10 ^ 29
def delta4Den : Nat := 2 ^ kShift * 2 ^ aJoule.2 * kBNum * tRef

/-- Prediction 2 (directional): δ₄ < 1. -/
def PredLt1 (U0 Un : Int) : Prop := delta4Num U0 Un < (delta4Den : Int)
/-- Prediction 1 (R2 range, endpoints inclusive): 0.790439676056526 ≤ δ₄ ≤ 1.0333534753990623. -/
def PredR2 (U0 Un : Int) : Prop :=
  (790439676056526 : Int) * delta4Den ≤ delta4Num U0 Un * 10 ^ 15 ∧ delta4Num U0 Un * 10 ^ 16 ≤ (10333534753990623 : Int) * delta4Den

instance (U0 Un : Int) : Decidable (PredLt1 U0 Un) := by unfold PredLt1; infer_instance
instance (U0 Un : Int) : Decidable (PredR2 U0 Un) := by unfold PredR2; infer_instance

/-- Two minima of the same predicate over valid ids coincide. -/
theorem IsMinOn_unique {P : Nat → Prop} {U U' : Int} (h : IsMinOn P U) (h' : IsMinOn P U') : U = U' := by
  obtain ⟨⟨a, ha1, ha2, ha3⟩, hl⟩ := h
  obtain ⟨⟨b, hb1, hb2, hb3⟩, hl'⟩ := h'
  have h1 := hl b hb1 hb2
  have h2 := hl' a ha1 ha2
  rw [hb3] at h1; rw [ha3] at h2; omega

-- Exact arithmetic facts (no hypotheses).
theorem gap_exact : claimedNonGTrue - claimedGroundNum = 12095447728404694790 := by decide +kernel
theorem gap_pos : 0 < claimedNonGTrue - claimedGroundNum := by decide +kernel
theorem gap_frozen_exact : claimedNonGNum - claimedGroundNum = 12095447728404695718 := by decide +kernel
theorem pred_lt1_true : PredLt1 claimedGroundNum claimedNonGTrue := by unfold PredLt1; decide +kernel
theorem pred_r2_true : PredR2 claimedGroundNum claimedNonGTrue := by unfold PredR2; decide +kernel
/-- Margins: 1 − δ₄ > 0.054, and distance of δ₄ to the nearest range endpoint (the upper one) > 0.0874; to the lower endpoint > 0.155. -/
theorem margin_lt1 : 1000 * ((delta4Den : Int) - delta4Num claimedGroundNum claimedNonGTrue) > 54 * (delta4Den : Int) := by decide +kernel
theorem margin_upper : ((10333534753990623 : Int) * delta4Den - 10 ^ 16 * delta4Num claimedGroundNum claimedNonGTrue) * 10 ^ 4 > 874 * 10 ^ 16 * (delta4Den : Int) := by decide +kernel
theorem margin_lower : (delta4Num claimedGroundNum claimedNonGTrue * 10 ^ 15 - (790439676056526 : Int) * delta4Den) * 10 ^ 3 > 155 * 10 ^ 15 * (delta4Den : Int) := by decide +kernel
/-- Agreement with the REPORTED frozen numbers (evidence of consistency, tolerance stated): |Δ_exact − 0.01024524273775096| < 2e-17 A. -/
theorem gap_matches_reported_Delta :
    (((claimedNonGTrue - claimedGroundNum) * 10 ^ 17 - 1024524273775096 * 2 ^ kShift).natAbs : Int) < 2 * 2 ^ kShift := by decide +kernel
/-- |δ₄_exact − 0.9459172223430824| < 3e-16 (the reported δ₄ is a floating-point evaluation; the exact value differs from it in the 16th digit). -/
theorem delta4_matches_reported :
    ((delta4Num claimedGroundNum claimedNonGTrue * 10 ^ 16 - 9459172223430824 * (delta4Den : Int)).natAbs : Int) < 3 * (delta4Den : Int) := by decide +kernel
/-- The verdicts do NOT depend on the 928/2^70 correction: the frozen (non-minimal) value gives the same two verdicts. -/
theorem frozen_value_same_verdicts : PredLt1 claimedGroundNum claimedNonGNum ∧ PredR2 claimedGroundNum claimedNonGNum := by
  unfold PredLt1 PredR2; decide +kernel
/-- The correction changes δ₄ by less than 1e-15 (relative to the denominator). -/
theorem correction_effect_on_delta4 :
    ((delta4Num claimedGroundNum claimedNonGNum - delta4Num claimedGroundNum claimedNonGTrue) * 10 ^ 15).natAbs < delta4Den := by decide +kernel

/-- IV-5 CORE (conditional on the two certified minima): for ANY U0, Un that are the minimum over all configurations, resp. over non-grammar
configurations, the exact gap, its positivity and both prospective predictions hold. -/
theorem iv5_of_minima (hG : ObjAll claimedGroundNum) (hN : ObjNonGrammar claimedNonGTrue) :
    ∀ U0 Un : Int, ObjAll U0 → ObjNonGrammar Un →
      U0 = claimedGroundNum ∧ Un = claimedNonGTrue ∧ Un - U0 = 12095447728404694790 ∧ 0 < Un - U0 ∧ PredLt1 U0 Un ∧ PredR2 U0 Un := by
  intro U0 Un h0 hn
  have e0 : U0 = claimedGroundNum := IsMinOn_unique h0 hG
  have en : Un = claimedNonGTrue := IsMinOn_unique hn hN
  subst e0; subst en
  exact ⟨rfl, rfl, gap_exact, gap_pos, pred_lt1_true, pred_r2_true⟩
end SCR_IV
