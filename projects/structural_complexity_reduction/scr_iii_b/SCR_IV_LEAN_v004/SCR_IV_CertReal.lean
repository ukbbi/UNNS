import SCR_IV_Cert
import SCR_IV_Part
import SCR_IV_Witness
/-! # IV-4A: instantiation of the checker on the frozen instance. CONDITIONAL theorems only:
"if `checkAll … cert = true` for some natural number `cert`, then the stated global optimum holds". No certificate exists yet (IV-4B),
so no unconditional global-optimality statement is made here. -/
namespace SCR_IV

/-- Coupling row d of the frozen table: [K_{d,d+1}, …, K_{d,39}] (numerators over 2^70). -/
def Rreal (d : Nat) : List Int := kRows.getD d []

theorem rowsL_getD (K : Nat → Nat → Int) (n : Nat) : ∀ m a k, k < m →
    (rowsL K n a m).getD k [] = lst (K (a + k)) (a + k + 1) (n - (a + k + 1)) := by
  intro m
  induction m with
  | zero => intro a k hk; omega
  | succ m ih =>
    intro a k hk
    cases k with
    | zero => simp [rowsL]
    | succ k =>
      simp only [rowsL, List.getD_cons_succ]
      rw [ih (a + 1) k (by omega)]
      have e : a + 1 + k = a + (k + 1) := by omega
      rw [e]

theorem rowsL_length (K : Nat → Nat → Int) (n : Nat) : ∀ m a, (rowsL K n a m).length = m := by
  intro m; induction m with
  | zero => intro a; simp [rowsL]
  | succ m ih => intro a; simp [rowsL, ih]

theorem lst_eq_range' (f : Nat → Int) (m : Nat) (a : Nat) : lst f a m = (List.range' a m).map f := by
  rw [← map_range_eq_lst, List.range'_eq_map_range, List.map_map]; rfl

theorem hR_real : ∀ d, Rreal d = (List.range' (d + 1) (40 - (d + 1))).map (kAt d) := by
  intro d
  unfold Rreal
  by_cases hd : d < 40
  · rw [kRows_eq, rowsL_getD kAt 40 40 0 d hd, Nat.zero_add, lst_eq_range']
  · have : (rowsL kAt 40 0 40).length = 40 := rowsL_length kAt 40 40 0
    rw [kRows_eq, List.getD_eq_getElem?_getD, List.getElem?_eq_none (by omega)]
    have : 40 - (d + 1) = 0 := by omega
    rw [this]; rfl

/-- Leaf test for the non-grammar objective: every vertex of the leaf `b` is 2-in/2-out (so the leaf is in the grammar). -/
def leafGrammar (b : Nat) : Bool := vertices.all (fun v => vertexOK v b)

theorem inCount_congr {a b : Nat} (h : ∀ i, i < 40 → a.testBit i = b.testBit i) (mask plusIn : Nat) :
    inCount mask plusIn a = inCount mask plusIn b := by
  rw [inCount_eq_countP, inCount_eq_countP]
  apply List.countP_congr; intro i hi
  have : i < 40 := by simpa using hi
  simp [h i this]

theorem sigmaAt_inj {a b i : Nat} (h : sigmaAt a i = sigmaAt b i) : a.testBit i = b.testBit i := by
  unfold sigmaAt at h
  cases ha : a.testBit i <;> cases hb : b.testBit i <;> simp [ha, hb] at h ⊢

theorem isGrammar_congr {a b : Nat} (h : ∀ i, i < 40 → a.testBit i = b.testBit i) : IsGrammar a ↔ IsGrammar b := by
  rw [isGrammar_iff, isGrammar_iff]
  constructor <;> intro hh v hv <;> have := hh v hv <;> unfold vertexOK at this ⊢ <;> simpa [inCount_congr h] using this

theorem leafGrammar_sound {b q : Nat} (h : leafGrammar b = true) (hag : ∀ i, i < 40 → sigmaAt q i = sigmaAt b i) : IsGrammar q := by
  have hb : IsGrammar b := by
    rw [isGrammar_iff]; unfold leafGrammar at h
    intro v hv; exact List.all_eq_true.1 h v hv
  exact (isGrammar_congr (fun i hi => sigmaAt_inj (hag i hi))).2 hb

/-- CONDITIONAL THEOREM (ground objective): a certificate accepted by the checker for U = claimedGroundNum proves that this value is the
exact minimum of the encoded Hamiltonian over all valid configurations (the witness `groundId` attains it: IV-2). -/
theorem ground_min_of_cert {cert : Nat} (h : checkAll Rreal 40 claimedGroundNum (fun _ => false) cert = true) :
    ObjAll claimedGroundNum := by
  refine ⟨⟨groundId, ground_valid, trivial, ground_energy_exact⟩, ?_⟩
  intro id _ _
  have := checkAll_sound (K := kAt) (Pp := fun _ => True) Rreal hR_real
    (fun b hb => by simp at hb) h (sigmaAt id) (pm1_sigmaAt id 0 40) trivial
  rw [hScaled_eq]; exact this

/-- CONDITIONAL THEOREM (non-grammar objective): same for the minimum over configurations with at least one violated vertex. -/
theorem nonG_min_of_cert {cert : Nat} (h : checkAll Rreal 40 claimedNonGNum leafGrammar cert = true) :
    ObjNonGrammar claimedNonGNum := by
  refine ⟨⟨nonGId, nonG_valid, nonG_not_in_grammar, nonG_energy_exact⟩, ?_⟩
  intro id _ hng
  have := checkAll_sound (K := kAt)
    (Pp := fun s => (∀ i, i < 40 → s i = sigmaAt id i) ∧ ¬ IsGrammar id) Rreal hR_real
    (fun b hb s hs hP => hP.2 (leafGrammar_sound hb (fun i hi => (hP.1 i hi).symm.trans (hs i hi)))) h
    (sigmaAt id) (pm1_sigmaAt id 0 40) ⟨fun _ _ => rfl, hng⟩
  rw [hScaled_eq]; exact this

/-- CONDITIONAL THEOREM (partitioned form, ground objective): if all 2^D0 depth-D0 prefixes are certified, claimedGroundNum is the exact minimum. -/
theorem ground_min_of_frontier {D0 : Nat} (hD : D0 ≤ 40) {certOf : Nat → Nat}
    (h : ∀ b, b < 2 ^ D0 → subOK Rreal 40 claimedGroundNum (fun _ => false) D0 b (certOf b) = true) :
    ObjAll claimedGroundNum := by
  refine ⟨⟨groundId, ground_valid, trivial, ground_energy_exact⟩, ?_⟩
  intro id _ _
  have hall : ∀ b, b < 2 ^ D0 → Sub 40 kAt claimedGroundNum (fun _ => True) D0 b :=
    fun b hb => subOK_sound (Pp := fun _ => True) Rreal hR_real (fun b hb => by simp at hb) hD hb (h b hb)
  have := frontier_sound hD hall (sigmaAt id) (pm1_sigmaAt id 0 40) trivial
  rw [hScaled_eq]; exact this

/-- CONDITIONAL THEOREM (partitioned form, non-grammar objective). -/
theorem nonG_min_of_frontier {D0 : Nat} (hD : D0 ≤ 40) {certOf : Nat → Nat}
    (h : ∀ b, b < 2 ^ D0 → subOK Rreal 40 claimedNonGNum leafGrammar D0 b (certOf b) = true) :
    ObjNonGrammar claimedNonGNum := by
  refine ⟨⟨nonGId, nonG_valid, nonG_not_in_grammar, nonG_energy_exact⟩, ?_⟩
  intro id _ hng
  have hall : ∀ b, b < 2 ^ D0 → Sub 40 kAt claimedNonGNum (fun s => (∀ i, i < 40 → s i = sigmaAt id i) ∧ ¬ IsGrammar id) D0 b :=
    fun b hb => subOK_sound (Pp := fun s => (∀ i, i < 40 → s i = sigmaAt id i) ∧ ¬ IsGrammar id) Rreal hR_real
      (fun b hb s hs hP => hP.2 (leafGrammar_sound hb (fun i hi => (hP.1 i hi).symm.trans (hs i hi)))) hD hb (h b hb)
  have := frontier_sound hD hall (sigmaAt id) (pm1_sigmaAt id 0 40) ⟨fun _ _ => rfl, hng⟩
  rw [hScaled_eq]; exact this

end SCR_IV
