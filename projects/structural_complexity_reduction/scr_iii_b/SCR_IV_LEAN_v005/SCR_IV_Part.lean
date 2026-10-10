import SCR_IV_Cert
/-! # IV-4A: PARTITIONED certificates. Calibration showed that the kernel's memory grows roughly linearly with the number of checked nodes
(≈0.5–0.7 MB/node), so a single `decide +kernel` over the full proof tree is infeasible. Instead, fix a frontier depth `D0` and certify each of the
2^D0 depth-D0 prefixes `b` INDEPENDENTLY with its own certificate `cert b` (a prefix already excluded by a shallower bound is a one-token certificate).
Coverage is then trivial: every ±1 configuration extends exactly one prefix `b < 2^D0`. Each `subOK … b (cert b) = true` is a separate kernel
theorem, so peak memory is per-batch, not per-tree. -/
namespace SCR_IV

/-- Checker state at depth `d` along the bit pattern `b`: recomputed by the same O(n) updates the checker uses. -/
def stateAt (R : Nat → List Int) (n b : Nat) : Nat → Int × List Int × Int
  | 0 => (0, List.replicate n 0, rootT R n)
  | d + 1 =>
    match stateAt R n b d with
    | (acc, f :: fs, T) => (acc + sigmaAt b d * f, addScaled (sigmaAt b d) fs (R d), T - sabs (R d))
    | (acc, [], T) => (acc, [], T)

/-- Check the subtree below the depth-`d` prefix `b` against certificate `cert` (consumed exactly, sentinel included). -/
def subOK (R : Nat → List Int) (n : Nat) (U : Int) (leafOK : Nat → Bool) (d b cert : Nat) : Bool :=
  match chk R U leafOK cert (n - d) d 0 (stateAt R n b d).1 (stateAt R n b d).2.1 (stateAt R n b d).2.2 b with
  | none => false
  | some pos => decide (cert >>> pos = 1)

/-- The claim certified for prefix `b` at depth `d`. -/
def Sub (n : Nat) (K : Nat → Nat → Int) (U : Int) (Pp : (Nat → Int) → Prop) (d b : Nat) : Prop :=
  ∀ s : Nat → Int, Pm1 s d n → (∀ i, i < d → s i = sigmaAt b i) → Pp s → U ≤ Hs n K s

/-- Prefix spin function of the bit pattern `b` at depth `d` (zero beyond `d`). -/
def pfx (b d : Nat) : Nat → Int := fun i => if i < d then sigmaAt b i else 0

theorem stateAt_Inv {n : Nat} {K : Nat → Nat → Int} (R : Nat → List Int)
    (hR : ∀ d, R d = (List.range' (d + 1) (n - (d + 1))).map (K d)) (b : Nat) :
    ∀ d, d ≤ n → Inv n K (pfx b d) d (stateAt R n b d).1 (stateAt R n b d).2.1 (stateAt R n b d).2.2 (b % 2 ^ d) := by
  intro d
  induction d with
  | zero =>
    intro _
    simp only [stateAt]
    refine ⟨?_, ?_, ?_, ?_, ?_⟩
    · unfold Apair; rfl
    · rw [Nat.sub_zero, map_const_range' _ (fun j => by unfold fld; rfl)]
    · exact rootT_eq R hR
    · simp [Nat.mod_one]
    · intro i hi; omega
  | succ d ih =>
    intro hd
    have hI := ih (by omega)
    generalize hst : stateAt R n b d = st at hI
    obtain ⟨acc, F, T⟩ := st
    simp only at hI
    have hF := hI.2.1
    have e1 : n - d = (n - (d + 1)) + 1 := by omega
    rw [e1, List.range'_succ, List.map_cons] at hF
    -- F is a cons
    generalize hFF : (List.range' (d + 1) (n - (d + 1))).map (fld K (pfx b d) d) = rest at hF
    subst hF
    have hI' : Inv n K (pfx b d) d acc (fld K (pfx b d) d d :: rest) T (b % 2 ^ d) := by
      rw [← e1] at *; exact hI
    have hdm : d + ((n - (d + 1)) + 1) = n := by omega
    have hb : b % 2 ^ (d + 1) < 2 ^ (d + 1) := Nat.mod_lt _ (Nat.two_pow_pos _)
    have hbit : ∀ i, i < d + 1 → assign (pfx b d) d (sigmaAt b d) i = sigmaAt (b % 2 ^ (d + 1)) i := by
      intro i hi
      by_cases e : i = d
      · subst e; simp [assign, sigmaAt, Nat.testBit_mod_two_pow]
      · have hlt : i < d := by omega
        have h2 : (b % 2 ^ (d + 1)).testBit i = b.testBit i := by
          rw [Nat.testBit_mod_two_pow]; simp; omega
        simp [assign, e, pfx, hlt, sigmaAt, h2]
    have hc := Inv_child R hR (m := n - (d + 1)) hdm hI' (v := sigmaAt b d) (bits' := b % 2 ^ (d + 1)) hb hbit
    have hp : assign (pfx b d) d (sigmaAt b d) = pfx b (d + 1) := by
      funext i
      by_cases e : i = d
      · subst e; simp [assign, pfx]
      · by_cases hlt : i < d
        · simp [assign, e, pfx, hlt, show i < d + 1 by omega]
        · simp [assign, e, pfx, hlt, show ¬ i < d + 1 by omega]
    rw [hp] at hc
    simp only [stateAt, hst]
    exact hc

theorem subOK_sound {n : Nat} {K : Nat → Nat → Int} (R : Nat → List Int)
    (hR : ∀ d, R d = (List.range' (d + 1) (n - (d + 1))).map (K d))
    {U : Int} {leafOK : Nat → Bool} {Pp : (Nat → Int) → Prop}
    (hleaf : ∀ b, leafOK b = true → ∀ s : Nat → Int, (∀ i, i < n → s i = sigmaAt b i) → ¬ Pp s)
    {d b cert : Nat} (hd : d ≤ n) (hb : b < 2 ^ d) (h : subOK R n U leafOK d b cert = true) : Sub n K U Pp d b := by
  intro s hpm hag hP
  unfold subOK at h
  cases hc : chk R U leafOK cert (n - d) d 0 (stateAt R n b d).1 (stateAt R n b d).2.1 (stateAt R n b d).2.2 b with
  | none => rw [hc] at h; cases h
  | some pos =>
    have hI := stateAt_Inv R hR b d hd
    rw [Nat.mod_eq_of_lt hb] at hI
    exact chk_sound R hR hleaf (n - d) d (by omega) 0 pos _ _ _ b (pfx b d) hI hc s
      (fun i hi => by rw [hag i hi]; simp [pfx, hi]) hpm hP

/-- Bit pattern of the first `k` spins of `s`. -/
def bitsOf (s : Nat → Int) : Nat → Nat
  | 0 => 0
  | k + 1 => bitsOf s k ||| (if s k = 1 then 2 ^ k else 0)

theorem bitsOf_spec (s : Nat → Int) : ∀ k, bitsOf s k < 2 ^ k ∧ ∀ i, i < k → (s i = 1 ∨ s i = -1) → sigmaAt (bitsOf s k) i = s i := by
  intro k
  induction k with
  | zero => exact ⟨by simp [bitsOf], fun i hi => by omega⟩
  | succ k ih =>
    obtain ⟨h1, h2⟩ := ih
    have hpow : 2 ^ (k + 1) = 2 ^ k * 2 := Nat.pow_succ ..
    have hlt : bitsOf s k ||| (if s k = 1 then 2 ^ k else 0) < 2 ^ (k + 1) :=
      Nat.or_lt_two_pow (by omega) (by split <;> omega)
    refine ⟨hlt, ?_⟩
    intro i hi hpm
    have hbk : (bitsOf s k).testBit k = false := Nat.testBit_lt_two_pow h1
    by_cases e : i = k
    · subst e
      by_cases hs : s i = 1
      · simp [bitsOf, sigmaAt, Nat.testBit_or, hs, hbk]
      · have : s i = -1 := by rcases hpm with h | h; exact absurd h hs; exact h
        simp [bitsOf, sigmaAt, Nat.testBit_or, hs, hbk, this]
    · have hlt' : i < k := by omega
      have := h2 i hlt' hpm
      have hne : k ≠ i := fun h => e h.symm
      by_cases hs : s k = 1
      · simp [bitsOf, sigmaAt, Nat.testBit_or, Nat.testBit_two_pow, hs, hne]; simpa [sigmaAt] using this
      · simp [bitsOf, sigmaAt, Nat.testBit_or, hs]; simpa [sigmaAt] using this

/-- THEOREM (frontier coverage): if every depth-`D0` prefix is certified, every ±1 configuration with property `Pp` has energy ≥ U. -/
theorem frontier_sound {n D0 : Nat} {K : Nat → Nat → Int} {U : Int} {Pp : (Nat → Int) → Prop}
    (hD : D0 ≤ n) (hall : ∀ b, b < 2 ^ D0 → Sub n K U Pp D0 b) :
    ∀ s : Nat → Int, Pm1 s 0 n → Pp s → U ≤ Hs n K s := by
  intro s hpm hP
  obtain ⟨h1, h2⟩ := bitsOf_spec s D0
  exact hall (bitsOf s D0) h1 s (fun i h1' h2' => hpm i (by omega) (by omega))
    (fun i hi => (h2 i hi (hpm i (by omega) (by omega))).symm) hP

/-- Batch of consecutive frontier prefixes `lo, lo+1, …` with their certificates. -/
def batchOK (R : Nat → List Int) (n : Nat) (U : Int) (leafOK : Nat → Bool) (d lo : Nat) (cs : List Nat) : Bool :=
  (List.range cs.length).all (fun i => subOK R n U leafOK d (lo + i) (cs.getD i 0))

theorem batchOK_sound {R : Nat → List Int} {n : Nat} {U : Int} {leafOK : Nat → Bool} {d lo : Nat} {cs : List Nat}
    (h : batchOK R n U leafOK d lo cs = true) {b : Nat} (hlo : lo ≤ b) (hhi : b < lo + cs.length) :
    subOK R n U leafOK d b (cs.getD (b - lo) 0) = true := by
  unfold batchOK at h
  have := List.all_eq_true.1 h (b - lo) (by simp; omega)
  have e : lo + (b - lo) = b := by omega
  rwa [e] at this

/-- A list of consecutive batches starting at frontier index `lo`. -/
def batchesOK (R : Nat → List Int) (n : Nat) (U : Int) (leafOK : Nat → Bool) (d : Nat) : Nat → List (List Nat) → Bool
  | _, [] => true
  | lo, cs :: rest => batchOK R n U leafOK d lo cs && batchesOK R n U leafOK d (lo + cs.length) rest

theorem batchesOK_sound {R : Nat → List Int} {n : Nat} {U : Int} {leafOK : Nat → Bool} {d : Nat} :
    ∀ (bs : List (List Nat)) (lo : Nat), batchesOK R n U leafOK d lo bs = true →
      ∀ b, lo ≤ b → b < lo + bs.flatten.length → subOK R n U leafOK d b (bs.flatten.getD (b - lo) 0) = true := by
  intro bs
  induction bs with
  | nil => intro lo _ b h1 h2; simp at h2; omega
  | cons cs rest ih =>
    intro lo h b hlo hhi
    unfold batchesOK at h
    obtain ⟨h1, h2⟩ := Bool.and_eq_true_iff.1 h
    simp only [List.flatten_cons, List.length_append] at hhi ⊢
    by_cases hc : b < lo + cs.length
    · have := batchOK_sound h1 hlo hc
      rwa [List.getD_eq_getElem?_getD, List.getElem?_append_left (by omega), ← List.getD_eq_getElem?_getD]
    · have := ih (lo + cs.length) h2 b (by omega) (by omega)
      rw [List.getD_eq_getElem?_getD, List.getElem?_append_right (by omega), ← List.getD_eq_getElem?_getD]
      have e : b - lo - cs.length = b - (lo + cs.length) := by omega
      rw [e]; exact this

/-- THEOREM (batch assembly): verified consecutive batches covering all 2^D0 frontier prefixes certify every prefix. -/
theorem batches_cover {R : Nat → List Int} {n : Nat} {U : Int} {leafOK : Nat → Bool} {D0 : Nat} {bs : List (List Nat)}
    (h : batchesOK R n U leafOK D0 0 bs = true) (hlen : bs.flatten.length = 2 ^ D0) :
    ∀ b, b < 2 ^ D0 → subOK R n U leafOK D0 b (bs.flatten.getD b 0) = true := by
  intro b hb
  have := batchesOK_sound bs 0 h b (by omega) (by omega)
  simpa using this

end SCR_IV
