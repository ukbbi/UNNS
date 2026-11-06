# Erratum to GIG-I v002, T12 — scope of "closure under intersection" (append-only; v002 itself is untouched)

**Issue (identified in the v002 Mathematical Assessment).** v002 DEFINITIONS.md defines a *realizable arrangement set* as **nonempty**, while the T12 statement
A_C(m) ∩ A_C(m′) = A_C(lcm-type combination) is used as "realizable sets are closed under intersection". The identity is correct; closure of the *nonempty-only*
collection is not: the intersection can be empty.

**Example.** C = (2,3): A_C(2) = {(2,3)} (from 2: apply 2 → 2·9/2 = 9, which 3 divides; applying 3 first is impossible since 3 ∤ 2), A_C(3) = {(3,2)} (from 3: apply 3 → 16, which 2 divides).
Then A_C(2) ∩ A_C(3) = ∅ = A_C(1). (Machine-checked: TESTS/test_v003.py::T12_Erratum.)

**Correction.** Define the *source-generated family* 𝒜(C) = { A_C(m) : m ∈ ℕ } **including ∅** (m = 1 gives ∅ whenever no arrangement is admissible from 1; in general ∅ occurs
as the intersection above). 𝒜(C) is closed under intersection and the fixed-point (closure) characterization of T12 holds for it with the convention **L(∅) = 1**
(the minimal source of the empty set is 1, cl_K(∅) = ∅-closure = A_C(1)). The subfamily of *nonempty* sets is a separate object (`realizable` in v002) and is not
intersection-closed. v003 uses 𝒜(C) when it speaks about regimes (D-V4, D-V9): a regime is a distinct nonempty member, and intersections are taken in 𝒜(C).

**Unaffected results.** T11 (cubical factorization), T13, T14, T15 and all census conclusions of v002 concern nonempty sets only and are unchanged.
v001 and v002 files are not modified; this note is the only record of the correction.
