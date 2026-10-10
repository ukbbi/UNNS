import SCR_IV_Solver
import SCR_IV_Prune
/-! # IV-4A: proof-tree certificate format and its independent checker, with a soundness theorem.

A certificate for "every completion has energy ≥ U" is a pre-order encoding of a binary proof tree over the FIXED branching order
(spin d is assigned at depth d). Each node carries a 2-bit token, stored in one natural number `cert` (token k at bit positions 2k, 2k+1):
  0 = PRUNE-BOUND : the exact bound  B(p) = acc − Σ|F_j| − T  satisfies  U ≤ B(p)             (any depth; at depth n, B(p) = H(p))
  1 = SPLIT       : both children (s_d = −1 first, then s_d = +1) are certified              (depth < n only)
  2 = PRUNE-LEAF  : depth n and `leafOK bits = true` (used for the non-grammar objective: the leaf is in the grammar)
Nothing about the search that PRODUCED the certificate is trusted: the checker recomputes every bound exactly (integers) from the path.
The state threaded by the checker is (acc, F, T, bits):  acc = A(p),  F = [f_d … f_{n−1}] with f_j = Σ_{i<d} K_ij p_i,  T = Σ_{d≤j<h<n}|K_jh|,
bits = the id of the prefix.  A child updates them in O(n) from one coupling row `R d = [K_{d,d+1}, …, K_{d,n−1}]`. -/
namespace SCR_IV

def sabs : List Int → Int
  | [] => 0
  | x :: xs => absZ x + sabs xs

/-- F' = F + v·row, elementwise (the field update when spin `d` is set to `v`). -/
def addScaled (v : Int) : List Int → List Int → List Int
  | f :: fs, k :: ks => (f + v * k) :: addScaled v fs ks
  | _, _ => []

def tokAt (cert pos : Nat) : Nat := (cert >>> pos) % 4

/-- The checker. `m` = remaining depth, `d` = current depth, `pos` = bit position of the current token.
Returns the position after the subtree, or `none` if any node fails. -/
def chk (R : Nat → List Int) (U : Int) (leafOK : Nat → Bool) (cert : Nat) :
    Nat → Nat → Nat → Int → List Int → Int → Nat → Option Nat
  | 0, _, pos, acc, F, T, bits =>
      if tokAt cert pos = 0 then (if U ≤ acc - sabs F - T then some (pos + 2) else none)
      else if tokAt cert pos = 2 then (if leafOK bits then some (pos + 2) else none)
      else none
  | m + 1, d, pos, acc, F, T, bits =>
      if tokAt cert pos = 0 then (if U ≤ acc - sabs F - T then some (pos + 2) else none)
      else if tokAt cert pos = 1 then
        match F with
        | [] => none
        | f :: fs =>
          match chk R U leafOK cert m (d + 1) (pos + 2) (acc + (-1) * f) (addScaled (-1) fs (R d)) (T - sabs (R d)) bits with
          | none => none
          | some pos1 =>
            chk R U leafOK cert m (d + 1) pos1 (acc + 1 * f) (addScaled 1 fs (R d)) (T - sabs (R d)) (bits ||| 2 ^ d)
      else none

/-- Σ_{j<n} Σ_{h>j} |K_jh| computed from the rows. -/
def rootT (R : Nat → List Int) (n : Nat) : Int := sumTo (fun j => sabs (R j)) n

/-- Full check: the whole tree is valid and the certificate is consumed exactly (sentinel bit `1` just after the last token). -/
def checkAll (R : Nat → List Int) (n : Nat) (U : Int) (leafOK : Nat → Bool) (cert : Nat) : Bool :=
  match chk R U leafOK cert n 0 0 0 (List.replicate n 0) (rootT R n) 0 with
  | none => false
  | some pos => decide (cert >>> pos = 1)

/-! ## Soundness -/

theorem sabs_map (g : Nat → Int) (m : Nat) : ∀ a, sabs ((List.range' a m).map g) = sumFrom (fun j => absZ (g j)) a m := by
  induction m with
  | zero => intro a; simp [sabs, sumFrom_zero]
  | succ m ih => intro a; rw [List.range'_succ, List.map_cons, sabs, ih, sumFrom_succ_left]

theorem addScaled_map (v : Int) (g h : Nat → Int) (L : List Nat) :
    addScaled v (L.map g) (L.map h) = L.map (fun j => g j + v * h j) := by
  induction L with
  | nil => simp [addScaled]
  | cons x xs ih => simp [addScaled, ih]

/-- The invariant relating the checker state to the abstract prefix `p` at depth `d`. -/
def Inv (n : Nat) (K : Nat → Nat → Int) (p : Nat → Int) (d : Nat) (acc : Int) (F : List Int) (T : Int) (bits : Nat) : Prop :=
  acc = Apair d K p ∧ F = (List.range' d (n - d)).map (fld K p d) ∧ T = Tail n d K ∧ bits < 2 ^ d ∧ ∀ i, i < d → p i = sigmaAt bits i

theorem bound_of_Inv {n : Nat} {K : Nat → Nat → Int} {p : Nat → Int} {d : Nat} {acc : Int} {F : List Int} {T : Int} {bits : Nat}
    (h : Inv n K p d acc F T bits) : acc - sabs F - T = Bnd n d K p := by
  obtain ⟨h1, h2, h3, _, _⟩ := h
  rw [h2, sabs_map, h1, h3]; unfold Bnd Fsum; rfl

theorem Tail_succ (R : Nat → List Int) (n : Nat) (K : Nat → Nat → Int) (hR : ∀ d, R d = (List.range' (d + 1) (n - (d + 1))).map (K d))
    {d : Nat} (hd : d < n) : Tail n d K = sabs (R d) + Tail n (d + 1) K := by
  unfold Tail
  have e : n - d = (n - (d + 1)) + 1 := by omega
  rw [e, sumFrom_succ_left, hR d, sabs_map]

theorem fld_assign (K : Nat → Nat → Int) (p : Nat → Int) (d j : Nat) (v : Int) :
    fld K (assign p d v) (d + 1) j = fld K p d j + v * K d j := by
  unfold fld
  rw [sumTo_succ]
  have : sumTo (fun i => K i j * assign p d v i) d = sumTo (fun i => K i j * p i) d := by
    apply sumTo_congr; intro i hi
    have hne : i ≠ d := by omega
    simp [assign, hne]
  rw [this]; simp [assign]; exact Int.mul_comm _ _

theorem Inv_child {n : Nat} {K : Nat → Nat → Int} (R : Nat → List Int) (hR : ∀ d, R d = (List.range' (d + 1) (n - (d + 1))).map (K d))
    {p : Nat → Int} {d m : Nat} (hdm : d + (m + 1) = n) {acc : Int} {f : Int} {fs : List Int} {T : Int} {bits : Nat}
    (h : Inv n K p d acc (f :: fs) T bits) {v : Int} {bits' : Nat}
    (hb : bits' < 2 ^ (d + 1)) (hbit : ∀ i, i < d + 1 → assign p d v i = sigmaAt bits' i) :
    Inv n K (assign p d v) (d + 1) (acc + v * f) (addScaled v fs (R d)) (T - sabs (R d)) bits' := by
  obtain ⟨h1, h2, h3, h4, h5⟩ := h
  have e1 : n - d = m + 1 := by omega
  have e2 : n - (d + 1) = m := by omega
  rw [e1, List.range'_succ, List.map_cons] at h2
  obtain ⟨hf, hfs⟩ := List.cons.inj h2
  refine ⟨?_, ?_, ?_, hb, hbit⟩
  · rw [Apair_succ, h1, hf]
    have hA : Apair d K (assign p d v) = Apair d K p := (Apair_congr K (p := assign p d v) (s := p) (d := d)
      (fun i hi => by have hne : i ≠ d := by omega
                      simp [assign, hne])).symm
    have hB : fld K (assign p d v) d d = fld K p d d := (fld_congr K (p := assign p d v) (s := p) (d := d)
      (fun i hi => by have hne : i ≠ d := by omega
                      simp [assign, hne]) d).symm
    have : Apair d K (assign p d v) = Apair d K p := hA
    rw [this, hB]; simp [assign]
  · rw [e2, hR d, hfs, e2, addScaled_map]
    apply List.map_congr_left; intro j _
    rw [fld_assign]
  · rw [h3, Tail_succ R n K hR (by omega)]; omega

theorem chk_sound {n : Nat} {K : Nat → Nat → Int} (R : Nat → List Int) (hR : ∀ d, R d = (List.range' (d + 1) (n - (d + 1))).map (K d))
    {U : Int} {leafOK : Nat → Bool} {cert : Nat} {Pp : (Nat → Int) → Prop}
    (hleaf : ∀ b, leafOK b = true → ∀ s : Nat → Int, (∀ i, i < n → s i = sigmaAt b i) → ¬ Pp s) :
    ∀ m d, d + m = n → ∀ pos pos' acc F T bits (p : Nat → Int), Inv n K p d acc F T bits →
      chk R U leafOK cert m d pos acc F T bits = some pos' →
      ∀ s : Nat → Int, Extends p d s → Pm1 s d n → Pp s → U ≤ Hs n K s := by
  intro m
  induction m with
  | zero =>
    intro d hdm pos pos' acc F T bits p hI hc s hext hpm hP
    have hd : d ≤ n := by omega
    unfold chk at hc
    by_cases t0 : tokAt cert pos = 0
    · simp only [t0, ↓reduceIte] at hc
      by_cases hu : U ≤ acc - sabs F - T
      · rw [bound_of_Inv hI] at hu
        have := lower_bound K hd hext hpm; omega
      · simp only [hu, ↓reduceIte] at hc; cases hc
    · simp only [t0, ↓reduceIte] at hc
      by_cases t2 : tokAt cert pos = 2
      · simp only [t2, ↓reduceIte] at hc
        by_cases hl : leafOK bits = true
        · exfalso
          apply hleaf bits hl s _ hP
          intro i hi
          rw [hext i (by omega)]; exact hI.2.2.2.2 i (by omega)
        · simp only [hl, ↓reduceIte] at hc; cases hc
      · simp only [t2, ↓reduceIte] at hc; cases hc
  | succ m ih =>
    intro d hdm pos pos' acc F T bits p hI hc s hext hpm hP
    have hd : d ≤ n := by omega
    unfold chk at hc
    by_cases t0 : tokAt cert pos = 0
    · simp only [t0, ↓reduceIte] at hc
      by_cases hu : U ≤ acc - sabs F - T
      · rw [bound_of_Inv hI] at hu
        have := lower_bound K hd hext hpm; omega
      · simp only [hu, ↓reduceIte] at hc; cases hc
    · simp only [t0, ↓reduceIte] at hc
      by_cases t1 : tokAt cert pos = 1
      · simp only [t1, ↓reduceIte] at hc
        obtain ⟨hI1, hI2, hI3, hI4, hI5⟩ := hI
        have e1 : n - d = m + 1 := by omega
        have hFne : ∃ f fs, F = f :: fs := by
          rw [hI2, e1, List.range'_succ]; exact ⟨_, _, rfl⟩
        obtain ⟨f, fs, hF⟩ := hFne
        subst hF
        have hI : Inv n K p d acc (f :: fs) T bits := ⟨hI1, hI2, hI3, hI4, hI5⟩
        simp only at hc
        have hpow : 2 ^ (d + 1) = 2 ^ d * 2 := Nat.pow_succ ..
        have hbd : bits.testBit d = false := Nat.testBit_lt_two_pow hI4
        -- the spin at d is ±1 and the completion lies in one child
        rcases partition_cover hext (hpm d (by omega) (by omega)) with hc1 | hc2
        · -- s d = +1 : second child
          cases hr1 : chk R U leafOK cert m (d + 1) (pos + 2) (acc + (-1) * f) (addScaled (-1) fs (R d)) (T - sabs (R d)) bits with
          | none => rw [hr1] at hc; cases hc
          | some pos1 =>
            rw [hr1] at hc
            have hbits : (bits ||| 2 ^ d) < 2 ^ (d + 1) :=
              Nat.or_lt_two_pow (by rw [hpow]; omega) (by rw [hpow]; omega)
            have hbit : ∀ i, i < d + 1 → assign p d 1 i = sigmaAt (bits ||| 2 ^ d) i := by
              intro i hi
              by_cases e : i = d
              · subst e; simp [assign, sigmaAt, Nat.testBit_or, hbd]
              · have hlt : i < d := by omega
                have : assign p d 1 i = p i := by simp [assign, e]
                rw [this, hI5 i hlt]
                have hne : d ≠ i := fun h => e h.symm
                simp [sigmaAt, Nat.testBit_or, Nat.testBit_two_pow, hne]
            have hIc := Inv_child R hR (m := m) hdm (v := 1) (bits' := bits ||| 2 ^ d) ⟨hI1, hI2, hI3, hI4, hI5⟩ hbits hbit
            exact ih (d + 1) (by omega) pos1 pos' _ _ _ _ _ hIc hc s hc1
              (fun i h1 h2 => hpm i (by omega) h2) hP
        · -- s d = -1 : first child
          cases hr1 : chk R U leafOK cert m (d + 1) (pos + 2) (acc + (-1) * f) (addScaled (-1) fs (R d)) (T - sabs (R d)) bits with
          | none => rw [hr1] at hc; cases hc
          | some pos1 =>
            have hbits : bits < 2 ^ (d + 1) := by omega
            have hbit : ∀ i, i < d + 1 → assign p d (-1) i = sigmaAt bits i := by
              intro i hi
              by_cases e : i = d
              · subst e; simp [assign, sigmaAt, hbd]
              · have hlt : i < d := by omega
                have : assign p d (-1) i = p i := by simp [assign, e]
                rw [this]; exact hI5 i hlt
            have hIc := Inv_child R hR (m := m) hdm (v := -1) (bits' := bits) ⟨hI1, hI2, hI3, hI4, hI5⟩ hbits hbit
            exact ih (d + 1) (by omega) (pos + 2) pos1 _ _ _ _ _ hIc hr1 s hc2
              (fun i h1 h2 => hpm i (by omega) h2) hP
      · simp only [t1, ↓reduceIte] at hc; cases hc

theorem map_const_range' (g : Nat → Int) (hg : ∀ j, g j = 0) (m : Nat) : ∀ a, (List.range' a m).map g = List.replicate m 0 := by
  induction m with
  | zero => intro a; simp
  | succ m ih => intro a; rw [List.range'_succ, List.map_cons, ih, hg]; rfl

theorem rootT_eq {n : Nat} {K : Nat → Nat → Int} (R : Nat → List Int)
    (hR : ∀ d, R d = (List.range' (d + 1) (n - (d + 1))).map (K d)) : rootT R n = Tail n 0 K := by
  unfold rootT Tail
  rw [Nat.sub_zero, sumFrom_zero_left]
  apply sumTo_congr; intro j _
  rw [hR j, sabs_map]

/-- THEOREM (checker soundness): if `checkAll` accepts a certificate, then every ±1 spin function `s` on `n` spins with property `Pp`
has energy ≥ U. `leafOK` is only consulted at depth n and must imply that no `Pp`-state agrees with the leaf's bit pattern. -/
theorem checkAll_sound {n : Nat} {K : Nat → Nat → Int} (R : Nat → List Int)
    (hR : ∀ d, R d = (List.range' (d + 1) (n - (d + 1))).map (K d))
    {U : Int} {leafOK : Nat → Bool} {cert : Nat} {Pp : (Nat → Int) → Prop}
    (hleaf : ∀ b, leafOK b = true → ∀ s : Nat → Int, (∀ i, i < n → s i = sigmaAt b i) → ¬ Pp s)
    (h : checkAll R n U leafOK cert = true) :
    ∀ s : Nat → Int, Pm1 s 0 n → Pp s → U ≤ Hs n K s := by
  intro s hpm hP
  unfold checkAll at h
  cases hc : chk R U leafOK cert n 0 0 0 (List.replicate n 0) (rootT R n) 0 with
  | none => rw [hc] at h; cases h
  | some pos =>
    have hI : Inv n K s 0 0 (List.replicate n 0) (rootT R n) 0 := by
      refine ⟨?_, ?_, ?_, ?_, ?_⟩
      · unfold Apair; rfl
      · rw [Nat.sub_zero, map_const_range' _ (fun j => by unfold fld; rfl)]
      · exact rootT_eq R hR
      · simp
      · intro i hi; omega
    exact chk_sound R hR hleaf n 0 (by omega) 0 pos 0 _ _ 0 s hI hc s (fun i hi => by omega) hpm hP

end SCR_IV
