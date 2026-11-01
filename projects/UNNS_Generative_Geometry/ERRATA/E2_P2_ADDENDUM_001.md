# E2-P2 — Addendum 001 (append-only; the delivered E2-P2 package is NOT edited)

Source of the two corrections: the E2-P2 research assessment (SPEC/E2_P2_ASSESSMENT_RECEIVED.md).  Both were re-derived and
re-checked here before being recorded.

## Correction 1 — P2-T1 (denominator divisibility)
E2-P2 `theory/THEOREMS.md` calls denominator divisibility "neither necessary nor sufficient" for lattice inclusion.  That is too broad.
Correct statement (proof: if b′ | b then every α with ∏ pᵢ^αᵢ ≡ 1 (mod b) satisfies the same congruence mod b′):

    b′ | b   ⇒   Λ_b ⊆ Λ_{b′}.

Divisibility is **sufficient, not necessary** for the inclusion, and it does **not** guarantee strict inclusion (Λ_b = Λ_{b′} is
possible).  The converse direction (b | b′ ⇒ Λ_{b′} ⊆ Λ_b) is the same statement with roles exchanged.  Lattice inclusion in
general is decided by the three procedures (K), (H), (B) of E2-P2, which are unchanged.

## Correction 2 — P2-TF1(v) (quasi-polynomial range)
The displayed quasi-polynomials for the source-edge count E_src(h) and the target-edge count E_tgt(h) of the family P2-F21
(21^{2h}/5 → 21^{2h}/4) are valid for **h ≥ 4** only.  Exact small-h source-edge counts (taken from the E2-P2 direct table, h = 1..4):

| h | actual E_src | stated polynomial |
|---|---|---|
| 1 | 0 | −2 |
| 2 | 1 | −1 |
| 3 | 2 | 0 |
| 4 | 11 | 11 |

The target-edge quasi-polynomial additionally has an h = 1 exception.  The principal surviving-edge formula
E_kept(h) = Σ_r c_r(h)² − 1 and the asymptotic survival ratio 1/6 hold for **all h ≥ 1**, as does the stated vertex/edge arithmetic in the
E2-P2 computational table.  These are corrections to the *stated scope* of theorem text, not to any verified number.
