import SCR_IV_Sums
/-! # IV-3 (abstract branch-and-bound theory, exact integer arithmetic)
For arbitrary integer couplings `K i j` (only `i < j` matters) and spin functions `s : Nat → Int`:
  H_n(s) = Σ_{i<n} s_i Σ_{i<j<n} K_ij s_j.
A prefix `p` assigns spins `0..d-1`; a completion `s` agrees with `p` below `d` and is ±1 on `[d,n)`.
The solver bound is  B(p) = A(p) − Σ_{j∈[d,n)} |f_j(p)| − Σ_{d≤j<h<n} |K_jh|,  f_j(p) = Σ_{i<d} K_ij p_i.
Nothing here is evaluated on the 40-spin space, and nothing depends on the C++ solver. -/
namespace SCR_IV

/-- |x| as an integer. -/
def absZ (x : Int) : Int := (x.natAbs : Int)

/-- Energy of `s` on the first `n` spins. -/
def Hs (n : Nat) (K : Nat → Nat → Int) (s : Nat → Int) : Int :=
  sumTo (fun i => s i * sumFrom (fun j => K i j * s j) (i + 1) (n - (i + 1))) n

/-- A(p): interactions among the assigned spins `< d`. -/
def Apair (d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) : Int :=
  sumTo (fun i => s i * sumFrom (fun j => K i j * s j) (i + 1) (d - (i + 1))) d

/-- f_j(p) = Σ_{i<d} K_ij s_i : field on unassigned spin `j` from assigned spins. -/
def fld (K : Nat → Nat → Int) (s : Nat → Int) (d j : Nat) : Int :=
  sumTo (fun i => K i j * s i) d

/-- Interactions between assigned (`< d`) and unassigned (`d ≤ j < n`) spins, grouped by the unassigned spin. -/
def Cross (n d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) : Int :=
  sumFrom (fun j => s j * fld K s d j) d (n - d)

/-- Interactions among unassigned spins `d ≤ i < j < n`. -/
def UU (n d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) : Int :=
  sumFrom (fun i => s i * sumFrom (fun j => K i j * s j) (i + 1) (n - (i + 1))) d (n - d)

/-- Σ_{j∈[d,n)} |f_j(p)|. -/
def Fsum (n d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) : Int :=
  sumFrom (fun j => absZ (fld K s d j)) d (n - d)

/-- Σ_{d≤j<h<n} |K_jh|. -/
def Tail (n d : Nat) (K : Nat → Nat → Int) : Int :=
  sumFrom (fun j => sumFrom (fun h => absZ (K j h)) (j + 1) (n - (j + 1))) d (n - d)

/-- The lower bound B(p). -/
def Bnd (n d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) : Int :=
  Apair d K s - Fsum n d K s - Tail n d K

/-! ## 1. Energy decomposition -/

theorem decomposition (K : Nat → Nat → Int) (s : Nat → Int) {d n : Nat} (hd : d ≤ n) :
    Hs n K s = Apair d K s + Cross n d K s + UU n d K s := by
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_le hd
  have hsub : d + m - d = m := by omega
  -- pointwise split of the row sums for assigned rows
  have key : ∀ i, i < d →
      s i * sumFrom (fun j => K i j * s j) (i + 1) (d + m - (i + 1)) =
        s i * sumFrom (fun j => K i j * s j) (i + 1) (d - (i + 1)) +
        s i * sumFrom (fun j => K i j * s j) d m := by
    intro i hi
    have h := sumFrom_split (fun j => K i j * s j) (i + 1) (d - (i + 1)) m
    have e1 : i + 1 + (d - (i + 1)) = d := by omega
    have e2 : d - (i + 1) + m = d + m - (i + 1) := by omega
    rw [e1, e2] at h
    rw [h, Int.mul_add]
  have hX : sumTo (fun i => s i * sumFrom (fun j => K i j * s j) d m) d = Cross (d + m) d K s := by
    unfold Cross fld
    rw [hsub]
    unfold sumFrom
    have e : ∀ i, s i * sumTo (fun t => K i (d + t) * s (d + t)) m =
        sumTo (fun t => s i * (K i (d + t) * s (d + t))) m := fun i => (sumTo_mul_left _ _ _).symm
    simp only [e]
    rw [sumTo_swap (fun i t => s i * (K i (d + t) * s (d + t))) d m]
    apply sumTo_congr
    intro t _
    rw [← sumTo_mul_left]
    apply sumTo_congr
    intro i _
    grind
  have hA : sumTo (fun i => s i * sumFrom (fun j => K i j * s j) (i + 1) (d + m - (i + 1))) d =
      Apair d K s + sumTo (fun i => s i * sumFrom (fun j => K i j * s j) d m) d := by
    unfold Apair
    rw [← sumTo_add]
    exact sumTo_congr (fun i hi => key i hi)
  unfold Hs UU
  rw [sumTo_split, hsub, hA, hX]
  rfl

/-! ## 2. Lower-bound validity -/

/-- `s` takes only the values ±1 on `[a, b)`. -/
def Pm1 (s : Nat → Int) (a b : Nat) : Prop := ∀ i, a ≤ i → i < b → s i = 1 ∨ s i = -1

theorem mul_pm_ge (s x : Int) (h : s = 1 ∨ s = -1) : -absZ x ≤ s * x := by
  unfold absZ; rcases h with rfl | rfl <;> omega

theorem cross_ge (K : Nat → Nat → Int) (s : Nat → Int) {d n : Nat} (hp : Pm1 s d n) :
    -Fsum n d K s ≤ Cross n d K s := by
  unfold Fsum Cross
  rw [← sumFrom_neg]
  apply sumFrom_le
  intro t ht
  exact mul_pm_ge _ _ (hp (d + t) (by omega) (by omega))

theorem uu_ge (K : Nat → Nat → Int) (s : Nat → Int) {d n : Nat} (hp : Pm1 s d n) :
    -Tail n d K ≤ UU n d K s := by
  unfold Tail UU
  rw [← sumFrom_neg]
  apply sumFrom_le
  intro t ht
  -- row j = d + t
  have hj : Pm1 s (d + t + 1) n := fun i h1 h2 => hp i (by omega) h2
  have hlo : ∀ u, u < n - (d + t + 1) →
      -absZ (K (d + t) (d + t + 1 + u)) ≤ K (d + t) (d + t + 1 + u) * s (d + t + 1 + u) := by
    intro u hu
    have := hj (d + t + 1 + u) (by omega) (by omega)
    unfold absZ; rcases this with h | h <;> rw [h] <;> omega
  have hhi : ∀ u, u < n - (d + t + 1) →
      K (d + t) (d + t + 1 + u) * s (d + t + 1 + u) ≤ absZ (K (d + t) (d + t + 1 + u)) := by
    intro u hu
    have := hj (d + t + 1 + u) (by omega) (by omega)
    unfold absZ; rcases this with h | h <;> rw [h] <;> omega
  have lo : -sumFrom (fun h => absZ (K (d + t) h)) (d + t + 1) (n - (d + t + 1)) ≤
      sumFrom (fun j => K (d + t) j * s j) (d + t + 1) (n - (d + t + 1)) := by
    rw [← sumFrom_neg]; exact sumFrom_le (fun u hu => hlo u hu)
  have hi : sumFrom (fun j => K (d + t) j * s j) (d + t + 1) (n - (d + t + 1)) ≤
      sumFrom (fun h => absZ (K (d + t) h)) (d + t + 1) (n - (d + t + 1)) :=
    sumFrom_le (fun u hu => hhi u hu)
  rcases hp (d + t) (by omega) (by omega) with h | h <;> rw [h] <;> omega

/-- B(p) ≤ H(s) for every ±1 completion. -/
theorem lower_bound_self (K : Nat → Nat → Int) (s : Nat → Int) {d n : Nat} (hd : d ≤ n)
    (hp : Pm1 s d n) : Bnd n d K s ≤ Hs n K s := by
  have h := decomposition K s hd
  have h1 := cross_ge K s hp
  have h2 := uu_ge K s hp
  unfold Bnd; omega

/-- A completion agrees with the prefix below `d`. -/
def Extends (p : Nat → Int) (d : Nat) (s : Nat → Int) : Prop := ∀ i, i < d → s i = p i

theorem Apair_congr (K : Nat → Nat → Int) {p s : Nat → Int} {d : Nat} (h : Extends p d s) :
    Apair d K s = Apair d K p := by
  unfold Apair
  apply sumTo_congr
  intro i hi
  rw [h i hi]
  congr 1
  apply sumFrom_congr
  intro t ht
  show K i (i + 1 + t) * s (i + 1 + t) = K i (i + 1 + t) * p (i + 1 + t)
  rw [h (i + 1 + t) (by omega)]

theorem fld_congr (K : Nat → Nat → Int) {p s : Nat → Int} {d : Nat} (h : Extends p d s) (j : Nat) :
    fld K s d j = fld K p d j := by
  unfold fld
  apply sumTo_congr
  intro i hi
  rw [h i hi]

theorem Bnd_congr (K : Nat → Nat → Int) {p s : Nat → Int} {d n : Nat} (h : Extends p d s) :
    Bnd n d K s = Bnd n d K p := by
  unfold Bnd Fsum
  rw [Apair_congr K h]
  have : sumFrom (fun j => absZ (fld K s d j)) d (n - d) = sumFrom (fun j => absZ (fld K p d j)) d (n - d) := by
    apply sumFrom_congr; intro t _; rw [fld_congr K h]
  rw [this]

/-- THEOREM (lower-bound validity): for every prefix `p` and every completion `s`, B(p) ≤ H(s). -/
theorem lower_bound (K : Nat → Nat → Int) {p s : Nat → Int} {d n : Nat} (hd : d ≤ n)
    (hext : Extends p d s) (hp : Pm1 s d n) : Bnd n d K p ≤ Hs n K s := by
  rw [← Bnd_congr K hext]; exact lower_bound_self K s hd hp

/-- At a full assignment the bound is exact. -/
theorem bound_exact_at_leaf (K : Nat → Nat → Int) (s : Nat → Int) (n : Nat) :
    Bnd n n K s = Hs n K s := by
  have h := decomposition K s (Nat.le_refl n)
  have c : Cross n n K s = 0 := by unfold Cross; simp [sumFrom_zero]
  have u : UU n n K s = 0 := by unfold UU; simp [sumFrom_zero]
  have f : Fsum n n K s = 0 := by unfold Fsum; simp [sumFrom_zero]
  have t : Tail n n K = 0 := by unfold Tail; simp [sumFrom_zero]
  unfold Bnd; omega

/-! ## 3. Pruning soundness (equality handled explicitly) -/

/-- If B(p) ≥ U, no completion of `p` has energy strictly below U. -/
theorem prune_sound (K : Nat → Nat → Int) {p s : Nat → Int} {d n : Nat} {U : Int} (hd : d ≤ n)
    (hext : Extends p d s) (hp : Pm1 s d n) (hB : U ≤ Bnd n d K p) : U ≤ Hs n K s := by
  have := lower_bound K hd hext hp; omega

theorem prune_no_strict_improvement (K : Nat → Nat → Int) {p s : Nat → Int} {d n : Nat} {U : Int}
    (hd : d ≤ n) (hext : Extends p d s) (hp : Pm1 s d n) (hB : U ≤ Bnd n d K p) :
    ¬ Hs n K s < U := by
  have := prune_sound K hd hext hp hB; omega

/-- A strict prune (B(p) > U) discards no state with energy ≤ U, in particular no tie with the incumbent. -/
theorem prune_strict_keeps_ties (K : Nat → Nat → Int) {p s : Nat → Int} {d n : Nat} {U : Int}
    (hd : d ≤ n) (hext : Extends p d s) (hp : Pm1 s d n) (hB : U < Bnd n d K p) : U < Hs n K s := by
  have := lower_bound K hd hext hp; omega

/-- Counterexample showing that the non-strict prune `B(p) ≥ U` CAN discard a state that ties the incumbent:
n = 1, K = 0, empty prefix, U = 0. Hence the solver certifies the minimum VALUE, not the set of minimisers. -/
theorem prune_may_discard_tie :
    ∃ (K : Nat → Nat → Int) (p s : Nat → Int) (d n : Nat) (U : Int),
      d ≤ n ∧ Extends p d s ∧ Pm1 s d n ∧ U ≤ Bnd n d K p ∧ Hs n K s = U :=
  ⟨fun _ _ => 0, fun _ => 1, fun _ => 1, 0, 1, 0, by decide, fun i hi => by omega,
    fun i _ _ => Or.inl rfl, by decide, by decide⟩

/-- Interface for the numerical bridge (NOT proved here): if an approximate evaluation `Bapprox` of B(p) carries
an error of at most `e`, and the prune test subtracts a guard `g ≥ e`, then `Bapprox - g ≥ U` forces `B(p) ≥ U`.
The floating-point error bound itself (SCR-III audit) is not formalised in Lean. -/
theorem guarded_prune_interface {B Bapprox U e g : Int} (herr : Bapprox - e ≤ B) (hg : e ≤ g)
    (hprune : U ≤ Bapprox - g) : U ≤ B := by omega

/-! ## 4. Search-partition completeness -/

/-- Assign spin `d` to `v`. -/
def assign (p : Nat → Int) (d : Nat) (v : Int) : Nat → Int := fun i => if i = d then v else p i

/-- Every ±1 completion of an unfinished prefix is a completion of the `+1` child or of the `−1` child. -/
theorem partition_cover {p s : Nat → Int} {d : Nat} (hext : Extends p d s) (hd : s d = 1 ∨ s d = -1) :
    Extends (assign p d 1) (d + 1) s ∨ Extends (assign p d (-1)) (d + 1) s := by
  rcases hd with h | h
  · left; intro i hi
    unfold assign; by_cases e : i = d
    · subst e; simp [h]
    · simp [e]; exact hext i (by omega)
  · right; intro i hi
    unfold assign; by_cases e : i = d
    · subst e; simp [h]
    · simp [e]; exact hext i (by omega)

/-- ... and never of both (no duplication). -/
theorem partition_disjoint (p : Nat → Int) (d : Nat) (s : Nat → Int) :
    ¬ (Extends (assign p d 1) (d + 1) s ∧ Extends (assign p d (-1)) (d + 1) s) := by
  intro ⟨h1, h2⟩
  have a := h1 d (by omega); have b := h2 d (by omega)
  simp [assign] at a b; omega

/-- Children only contain completions of the parent. -/
theorem partition_sound {p s : Nat → Int} {d : Nat} {v : Int} (h : Extends (assign p d v) (d + 1) s) :
    Extends p d s ∧ s d = v := by
  constructor
  · intro i hi
    have := h i (by omega); have hne : i ≠ d := by omega
    simpa [assign, hne] using this
  · have := h d (by omega); simpa [assign] using this

end SCR_IV
