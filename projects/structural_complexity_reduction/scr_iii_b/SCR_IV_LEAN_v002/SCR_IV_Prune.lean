import SCR_IV_Solver
import SCR_IV_Grammar
import SCR_IV_Witness
/-! # IV-3 (configuration-id level pruning, partition, grammar filter)
Everything is universally quantified over configuration ids `q : Nat`; no id is enumerated. -/
namespace SCR_IV

/-- `q` is a completion of the depth-`d` prefix held in the low `d` bits of `p`. -/
def AgreesBelow (p q d : Nat) : Prop := ∀ i, i < d → q.testBit i = p.testBit i

theorem pm1_sigmaAt (q d n : Nat) : Pm1 (sigmaAt q) d n := fun i _ _ => sigmaAt_pm q i

theorem extends_of_agrees {p q d : Nat} (h : AgreesBelow p q d) : Extends (sigmaAt p) d (sigmaAt q) := by
  intro i hi; unfold sigmaAt; rw [h i hi]

/-- Energy of the decoded id, in the abstract form. -/
theorem hScaled_eq (q : Nat) : hScaled q = Hs 40 kAt (sigmaAt q) := hScaled_eq_Hs q

/-- THEOREM (id-level lower bound, B(p) ≤ H(q) for every prefix and every completion). -/
theorem lower_bound_ids {p q d : Nat} (hd : d ≤ 40) (h : AgreesBelow p q d) :
    Bnd 40 d kAt (sigmaAt p) ≤ hScaled q := by
  rw [hScaled_eq]; exact lower_bound kAt hd (extends_of_agrees h) (pm1_sigmaAt q d 40)

/-- THEOREM (id-level pruning soundness, ties handled): if B(p) ≥ U then no completion q has hScaled q < U. -/
theorem prune_sound_ids {p q d : Nat} {U : Int} (hd : d ≤ 40) (h : AgreesBelow p q d)
    (hB : U ≤ Bnd 40 d kAt (sigmaAt p)) : U ≤ hScaled q := by
  have := lower_bound_ids hd h; omega

/-- Strict prune keeps every state tying the incumbent. -/
theorem prune_strict_ids {p q d : Nat} {U : Int} (hd : d ≤ 40) (h : AgreesBelow p q d)
    (hB : U < Bnd 40 d kAt (sigmaAt p)) : U < hScaled q := by
  have := lower_bound_ids hd h; omega

/-- THEOREM (solver prune, id level): the C++ bound (loop-faithful, any guard g ≥ 0) at the C++ accumulator. -/
theorem solver_prune_sound_ids {p q d : Nat} {U g : Int} (hd : d ≤ 40) (h : AgreesBelow p q d) (hg : 0 ≤ g)
    (hB : U ≤ solverBound 40 d kAt (sigmaAt p) (pathAcc kAt (sigmaAt p) d) - g) : U ≤ hScaled q := by
  rw [hScaled_eq]
  have := guard_prune_sound kAt hd (extends_of_agrees h) (pm1_sigmaAt q d 40) hg hB
  omega

/-- At the leaf the C++ accumulator is exactly the frozen scaled energy. -/
theorem leaf_acc_eq_hScaled (p : Nat) : pathAcc kAt (sigmaAt p) 40 = hScaled p := by
  rw [pathAcc_eq_Apair, hScaled_eq]; unfold Apair Hs; rfl

/-! ## Partition completeness (id level) -/

/-- The two children of the depth-`d` prefix `p`: bit `d` set / cleared, lower bits kept. -/
def childPlus (p d : Nat) : Nat := (p % 2 ^ d) ||| 2 ^ d
def childMinus (p d : Nat) : Nat := p % 2 ^ d

theorem testBit_childPlus (p d i : Nat) :
    (childPlus p d).testBit i = ((decide (i < d) && p.testBit i) || decide (d = i)) := by
  unfold childPlus; simp [Nat.testBit_or, Nat.testBit_mod_two_pow, Nat.testBit_two_pow]

theorem testBit_childMinus (p d i : Nat) : (childMinus p d).testBit i = (decide (i < d) && p.testBit i) := by
  unfold childMinus; simp [Nat.testBit_mod_two_pow]

/-- Every completion of an unfinished prefix is a completion of exactly one child (cover). -/
theorem partition_ids_cover {p q d : Nat} (h : AgreesBelow p q d) :
    AgreesBelow (childPlus p d) q (d + 1) ∨ AgreesBelow (childMinus p d) q (d + 1) := by
  cases hq : q.testBit d
  · right; intro i hi
    rw [testBit_childMinus]
    by_cases e : i < d
    · simp [e, h i e]
    · have : i = d := by omega
      subst this; simp [hq]
  · left; intro i hi
    rw [testBit_childPlus]
    by_cases e : i < d
    · have hne : d ≠ i := by omega
      simp [e, h i e, hne]
    · have : i = d := by omega
      subst this; simp [hq]

/-- ... and of no more than one child (no duplication). -/
theorem partition_ids_disjoint (p q d : Nat) :
    ¬ (AgreesBelow (childPlus p d) q (d + 1) ∧ AgreesBelow (childMinus p d) q (d + 1)) := by
  intro ⟨h1, h2⟩
  have a := h1 d (by omega); have b := h2 d (by omega)
  rw [testBit_childPlus] at a; rw [testBit_childMinus] at b
  simp at a b; rw [a] at b; exact absurd b (by simp)

/-- Children contain only completions of the parent. -/
theorem partition_ids_sound_plus {p q d : Nat} (h : AgreesBelow (childPlus p d) q (d + 1)) : AgreesBelow p q d := by
  intro i hi
  have := h i (by omega); rw [testBit_childPlus] at this; simpa [hi, Nat.ne_of_gt hi] using this

theorem partition_ids_sound_minus {p q d : Nat} (h : AgreesBelow (childMinus p d) q (d + 1)) : AgreesBelow p q d := by
  intro i hi
  have := h i (by omega); rw [testBit_childMinus] at this; simpa [hi] using this

/-! ## Grammar filter: the exact loops of `possible_violation` and `violates` -/

/-- One iteration of the C++ loop over islands i: updates (count, left) for vertex (mask, plusIn) at depth d on prefix p. -/
def clStep (mask plusIn p d : Nat) (cl : Nat × Nat) (i : Nat) : Nat × Nat :=
  if mask.testBit i then
    (if i < d then (cl.1 + (if p.testBit i == plusIn.testBit i then 1 else 0), cl.2) else (cl.1, cl.2 + 1))
  else cl

/-- The C++ pair (count, left) for vertex (mask, plusIn) at depth d on prefix p: a single left fold over i = 0..39. -/
def cppCL (mask plusIn p d : Nat) : Nat × Nat := (List.range nSpins).foldl (clStep mask plusIn p d) (0, 0)

/-- `possible_violation(d)` when `want_violation` is true: true iff some vertex has count>2, count+left<2 or left>0. -/
def cppPossible (p d : Nat) : Bool :=
  vertices.any (fun v =>
    let cl := cppCL v.1 v.2 p d
    decide (cl.1 > 2) || decide (cl.1 + cl.2 < 2) || decide (cl.2 > 0))

/-- `violates()`: some vertex has count != 2 over all 40 islands. -/
def cppViolates (id : Nat) : Bool := vertices.any (fun v => inCount v.1 v.2 id != 2)

def predA (mask plusIn p d i : Nat) : Bool := mask.testBit i && decide (i < d) && (p.testBit i == plusIn.testBit i)
def predR (mask d i : Nat) : Bool := mask.testBit i && !decide (i < d)

theorem cppCL_fold (mask plusIn p d : Nat) (L : List Nat) : ∀ c l,
    L.foldl (clStep mask plusIn p d) (c, l) = (c + L.countP (predA mask plusIn p d), l + L.countP (predR mask d)) := by
  induction L with
  | nil => intro c l; simp
  | cons x xs ih =>
    intro c l
    have hs : clStep mask plusIn p d (c, l) x =
        (c + (if predA mask plusIn p d x = true then 1 else 0), l + (if predR mask d x = true then 1 else 0)) := by
      unfold clStep predA predR
      by_cases hm : mask.testBit x = true <;> by_cases hd : x < d <;> by_cases hb : (p.testBit x == plusIn.testBit x) = true <;>
        simp [hm, hd, hb]
    rw [List.foldl_cons, hs, ih, List.countP_cons, List.countP_cons]
    simp only [Prod.mk.injEq]; omega

theorem cppCL_eq (mask plusIn p d : Nat) :
    cppCL mask plusIn p d = ((List.range nSpins).countP (predA mask plusIn p d), (List.range nSpins).countP (predR mask d)) := by
  unfold cppCL; rw [cppCL_fold]; simp

theorem inCount_eq_countP (mask plusIn id : Nat) :
    inCount mask plusIn id = (List.range nSpins).countP (fun i => mask.testBit i && (id.testBit i == plusIn.testBit i)) := by
  unfold inCount
  have key : ∀ (L : List Nat) (c : Nat), L.foldl (fun a i => if mask.testBit i && (id.testBit i == plusIn.testBit i) then a + 1 else a) c
      = c + L.countP (fun i => mask.testBit i && (id.testBit i == plusIn.testBit i)) := by
    intro L; induction L with
    | nil => intro c; simp
    | cons x xs ih =>
      intro c
      rw [List.foldl_cons, List.countP_cons]
      by_cases h : (mask.testBit x && (id.testBit x == plusIn.testBit x)) = true
      · simp only [h, ↓reduceIte, ih]; omega
      · simp only [h, ih]; simp
  rw [key]; omega

theorem predA_congr {p q d : Nat} (h : AgreesBelow p q d) (mask plusIn i : Nat) : predA mask plusIn q d i = predA mask plusIn p d i := by
  unfold predA
  by_cases e : i < d
  · simp [e, h i e]
  · simp [e]

/-- count ≤ inCount q ≤ count + left, for every completion q of the prefix p. -/
theorem inCount_bounds {p q d : Nat} (h : AgreesBelow p q d) (mask plusIn : Nat) :
    (cppCL mask plusIn p d).1 ≤ inCount mask plusIn q ∧ inCount mask plusIn q ≤ (cppCL mask plusIn p d).1 + (cppCL mask plusIn p d).2 := by
  rw [cppCL_eq, inCount_eq_countP]
  simp only
  have hA : (List.range nSpins).countP (predA mask plusIn p d) = (List.range nSpins).countP (predA mask plusIn q d) := by
    apply List.countP_congr; intro i _; simp [predA_congr h]
  rw [hA]
  constructor
  · apply List.countP_mono_left; intro i _ hi
    unfold predA at hi; simp at hi ⊢; exact ⟨hi.1.1, hi.2⟩
  · have key : ∀ L : List Nat, L.countP (fun i => mask.testBit i && (q.testBit i == plusIn.testBit i))
        ≤ L.countP (predA mask plusIn q d) + L.countP (predR mask d) := by
      intro L; induction L with
      | nil => simp
      | cons x xs ih =>
        simp only [List.countP_cons, predA, predR]
        by_cases hm : mask.testBit x = true <;> by_cases hd : x < d <;> by_cases hb : (q.testBit x == plusIn.testBit x) = true <;>
          simp [hm, hd, hb] <;> omega
    exact key _

/-- A certainly-violated vertex (count > 2 or count + left < 2) is violated in EVERY completion. -/
theorem violated_persists {p q d : Nat} (h : AgreesBelow p q d) (v : Nat × Nat)
    (hv : (cppCL v.1 v.2 p d).1 > 2 ∨ (cppCL v.1 v.2 p d).1 + (cppCL v.1 v.2 p d).2 < 2) : vertexOK v q = false := by
  have := inCount_bounds h v.1 v.2
  unfold vertexOK; simp; omega

/-- In particular a COMPLETED violated vertex (left = 0, count ≠ 2) stays violated under any later spins. -/
theorem completed_violation_persists {p q d : Nat} (h : AgreesBelow p q d) (v : Nat × Nat)
    (hl : (cppCL v.1 v.2 p d).2 = 0) (hc : (cppCL v.1 v.2 p d).1 ≠ 2) : vertexOK v q = false := by
  apply violated_persists h; omega

theorem isGrammar_iff (q : Nat) : IsGrammar q ↔ ∀ v ∈ vertices, vertexOK v q = true := by
  unfold IsGrammar violations
  rw [List.countP_eq_zero]
  constructor
  · intro hh v hv; have := hh v hv; simpa using this
  · intro hh v hv; simp [hh v hv]

/-- Grammar-constrained pruning: a certainly-violated vertex makes every completion non-admissible. -/
theorem grammar_prune_sound {p q d : Nat} (h : AgreesBelow p q d) (v : Nat × Nat) (hmem : v ∈ vertices)
    (hv : (cppCL v.1 v.2 p d).1 > 2 ∨ (cppCL v.1 v.2 p d).1 + (cppCL v.1 v.2 p d).2 < 2) : ¬ IsGrammar q := by
  intro hg
  have := (isGrammar_iff q).1 hg v hmem
  have h2 := violated_persists h v hv
  rw [this] at h2; exact absurd h2 (by simp)

/-- THEOREM (soundness of the C++ non-grammar filter): if `possible_violation` returns false, EVERY completion is in the grammar. -/
theorem cppPossible_false_sound {p d : Nat} (hf : cppPossible p d = false) {q : Nat} (h : AgreesBelow p q d) : IsGrammar q := by
  rw [isGrammar_iff]
  intro v hv
  unfold cppPossible at hf
  have hv' := (List.any_eq_false.1 hf) v hv
  have b := inCount_bounds h v.1 v.2
  simp at hv'
  unfold vertexOK; simp; omega

theorem cppViolates_iff (id : Nat) : cppViolates id = true ↔ ¬ IsGrammar id := by
  unfold cppViolates
  rw [isGrammar_iff, List.any_eq_true]
  constructor
  · intro hex hall
    obtain ⟨v, hv, hne⟩ := hex
    have h1 := hall v hv
    unfold vertexOK at h1
    simp at h1 hne
    omega
  · intro hn
    apply Classical.byContradiction
    intro hc
    apply hn
    intro v hv
    unfold vertexOK
    apply Classical.byContradiction
    intro hne
    apply hc
    refine ⟨v, hv, ?_⟩
    simp at hne ⊢
    omega

/-! ## Objectives (kept distinct) and discard soundness -/

/-- U is the exact minimum of hScaled over the VALID ids satisfying P (attained). -/
def IsMinOn (P : Nat → Prop) (U : Int) : Prop :=
  (∃ id, ValidId id ∧ P id ∧ hScaled id = U) ∧ ∀ id, ValidId id → P id → U ≤ hScaled id

/-- Objective "ground": minimise over ALL configurations (no grammar condition). -/
def ObjAll (U : Int) : Prop := IsMinOn (fun _ => True) U
/-- Objective "grammar": minimise over configurations satisfying every 2-in/2-out vertex. -/
def ObjGrammar (U : Int) : Prop := IsMinOn IsGrammar U
/-- Objective "non-grammar": minimise over configurations with at least one violated vertex. -/
def ObjNonGrammar (U : Int) : Prop := IsMinOn (fun id => ¬ IsGrammar id) U

theorem objectives_distinct : (fun id => IsGrammar id) ≠ (fun id => ¬ IsGrammar id) := by
  intro h
  have a : IsGrammar groundId := ground_in_grammar
  have b : ¬ IsGrammar groundId := by
    have := congrFun h groundId; simp only [eq_iff_iff] at this; exact fun hg => (this.1 hg) hg
  exact b a

/-- The three optima are related by min(all) = min(grammar, non-grammar), but they are different quantities. -/
theorem objective_relation {Ua Ug Un : Int} (ha : ObjAll Ua) (hg : ObjGrammar Ug) (hn : ObjNonGrammar Un) :
    Ua ≤ Ug ∧ Ua ≤ Un ∧ (Ua = Ug ∨ Ua = Un) := by
  obtain ⟨⟨ia, hiv, _, hia⟩, hamin⟩ := ha
  obtain ⟨⟨ig, hgv, hgg, hgi⟩, hgmin⟩ := hg
  obtain ⟨⟨inn, hnv, hng, hni⟩, hnmin⟩ := hn
  have h1 : Ua ≤ Ug := by have := hamin ig hgv trivial; omega
  have h2 : Ua ≤ Un := by have := hamin inn hnv trivial; omega
  refine ⟨h1, h2, ?_⟩
  by_cases hG : IsGrammar ia
  · left; have := hgmin ia hiv hG; omega
  · right; have := hnmin ia hiv hG; omega

/-- THEOREM (discard soundness, generic objective): a subtree may be discarded for objective P with incumbent U
if it contains no P-state, or if B(p) ≥ U. Then every P-completion has energy ≥ U (so none is strictly better). -/
theorem discard_sound_generic {P : Nat → Prop} {p d : Nat} {U : Int} (hd : d ≤ 40)
    (hdisc : (∀ q, AgreesBelow p q d → ¬ P q) ∨ U ≤ Bnd 40 d kAt (sigmaAt p)) :
    ∀ q, AgreesBelow p q d → P q → U ≤ hScaled q := by
  intro q h hP
  rcases hdisc with h1 | h2
  · exact absurd hP (h1 q h)
  · exact prune_sound_ids hd h h2

/-- Ground objective, as run by the solver (`possible_violation` is constant true): the only discard is the bound test. -/
theorem discard_ground {p d : Nat} {U g : Int} (hd : d ≤ 40) (hg : 0 ≤ g)
    (hB : U ≤ solverBound 40 d kAt (sigmaAt p) (pathAcc kAt (sigmaAt p) d) - g) :
    ∀ q, AgreesBelow p q d → U ≤ hScaled q :=
  fun _ h => solver_prune_sound_ids hd h hg hB

/-- Non-grammar objective, as run by the solver: discard if `possible_violation` is false OR the (guarded) bound test fires. -/
theorem discard_nonGrammar {p d : Nat} {U g : Int} (hd : d ≤ 40) (hg : 0 ≤ g)
    (hdisc : cppPossible p d = false ∨ U ≤ solverBound 40 d kAt (sigmaAt p) (pathAcc kAt (sigmaAt p) d) - g) :
    ∀ q, AgreesBelow p q d → ¬ IsGrammar q → U ≤ hScaled q := by
  intro q h hn
  rcases hdisc with h1 | h2
  · exact absurd (cppPossible_false_sound h1 h) hn
  · exact solver_prune_sound_ids hd h hg h2

end SCR_IV
