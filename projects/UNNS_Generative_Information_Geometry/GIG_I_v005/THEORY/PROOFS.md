# GIG-I v005 (stage 1) — proofs and verification

**PS-5.** Faces of X_λ(m) are those F ⊂ P_6 with Pref(F) ⊆ A(m) (T16/T17). Fix K_z | m, so P_z ⊆ A(m). Whether [z]=0 depends only on S = A(m) ∩ EXTRA, because every 3-face of P_6 has Pref(F) ⊆ P_z ∪ EXTRA (checked for all 540). z bounds iff z ∈ im ∂_3 restricted to present 3-faces, a GF(2) linear-algebra test, monotone in S. E19 evaluates it for all 2^20 values of S (exact bitset elimination) and extracts the minimal bounding S: four of them. Nothing arithmetic enters; the statement holds for every content.

**PS-1 corollary.** Inspection: each B_i contains a full gate set (see THEOREMS), so a family missing one element from every gate contains no B_i.

**PS-3′ certificates.** For a certificate (labels, m): E20 recomputes D(I) exactly (Fractions), declares a face present iff m is divisible by lcm D(Pref(F)) — a rule independent of filling.py — checks z present, solves for φ′ over GF(2) on the present 2-faces with φ′(∂_3 F)=0 for every present 3-face F and φ′(z)=1, and re-checks both identities. This certifies [z] ≠ 0 with the gate open: the gate's prefix sets divide m (tested), 21 ∤ m.

**PS-6.** v_p of a product of ratios (ℓ+1)²/ℓ adds, and gcd(ℓ,ℓ+1)=1, giving the stated formula; D(I)|m iff v_p(D(I)) ≤ v_p(m) for all p. CRT lets residues of each ℓ_j modulo distinct prime powers be chosen freely. Extra prime factors of the ℓ_j only add constraints at primes where m is taken to be exactly lcm D(P_z ∪ gate), so they can only shrink A(m) — they keep the gate open and cannot create a filling (monotonicity).
