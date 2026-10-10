/-! # IV-1 (spins): 40 binary spins and deterministic spin-ID decoding.
Convention (frozen, as in physical_energy_v005.decode and solver_v010): bit i of the ID is 1 iff s_i = +1. -/
namespace SCR_IV

abbrev nSpins : Nat := 40

/-- Spin i of configuration `id`: +1 if bit i is set, else -1. -/
def sigmaAt (id i : Nat) : Int := if id.testBit i then 1 else -1

/-- The full list of 40 spins. -/
def sigma (id : Nat) : List Int := (List.range nSpins).map (sigmaAt id)

/-- A configuration ID is valid iff it fits in 40 bits. -/
def ValidId (id : Nat) : Prop := id < 2 ^ nSpins

instance (id : Nat) : Decidable (ValidId id) := inferInstanceAs (Decidable (id < 2 ^ nSpins))

theorem sigma_length (id : Nat) : (sigma id).length = 40 := by simp [sigma]

theorem sigmaAt_pm (id i : Nat) : sigmaAt id i = 1 ∨ sigmaAt id i = -1 := by
  unfold sigmaAt; split <;> simp

/-- Decoding is injective on valid IDs: two valid configurations with equal spins are equal. -/
theorem id_eq_of_spins {a b : Nat} (ha : ValidId a) (hb : ValidId b)
    (h : ∀ i, i < 40 → sigmaAt a i = sigmaAt b i) : a = b := by
  apply Nat.eq_of_testBit_eq
  intro i
  by_cases hi : i < 40
  · have := h i hi
    unfold sigmaAt at this
    cases ha' : a.testBit i <;> cases hb' : b.testBit i <;> simp [ha', hb'] at this ⊢
  · have hle : 2 ^ 40 ≤ 2 ^ i := Nat.pow_le_pow_right (by decide) (by omega)
    have h1 : a.testBit i = false := Nat.testBit_lt_two_pow (Nat.lt_of_lt_of_le ha hle)
    have h2 : b.testBit i = false := Nat.testBit_lt_two_pow (Nat.lt_of_lt_of_le hb hle)
    rw [h1, h2]

end SCR_IV
