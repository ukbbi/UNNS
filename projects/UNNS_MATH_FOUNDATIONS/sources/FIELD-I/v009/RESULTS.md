# RESULTS — FIELD-I v009: Arithmetic Carry Cycles and Regime Classification

Full run of `field9.py`: **0 FAIL, 541.6 s** (`output/field9_output.txt`). Proofs are in THEOREMS.md (T49–T58). v002–v008, the G1–G3 memo and the relational manuscript are unchanged.

## PROVED (hand proofs; tests are consistency checks, not the proof)
| # | Result | Checked by |
|---|---|---|
| T49 | One-step law: w=γ+1, h=gcd(g,w), σ'=L·∏p^⌊v_p(w/h)/2⌋, D(x')={d∣σ', d≥2, d≡1 mod g/h}; persistent iff all such d≡1 mod g | A1–A3 (machine = direct iteration; 1467 random (g,L,w)) |
| T50 | **Eight-step theorem (G=11)**: x_{8k+j}=(j+1)S_k²/11, S_k=2²3^{3+k}5⁴, x_{n+8}=9x_n, R=7+2k | N1.0–N1.7 (192-step direct orbit; residue equations for all k by period 5) |
| T51 | **Every persistent orbit is eventually exactly scaling** (x_{n+P}=ρ²x_n): finite class space ⇒ repeated class ⇒ periodic forever. Hence every orbit of C eventually scales exactly (with v005 T32 for G_∞=1) | Q2, Q3, E1, E2 (class-closure certificates) |
| T52 | Window: odd g ⇒ 2∣L and g∤γ+1; a complete carry M needs M²<g (odd g); even g: 4g∤γ+1 | W1, W2, Q4 |
| T53 | Absorption criterion: d available iff M(d)²∣w; r=lcm of available M(d); types none / partial / complete | K1 (414 states, 0 deviations) |
| T54 | Completeness: γ'≤γ_s/4+1 per carry; from γ=1 every later carry is complete (w=M², cycle length M²−1). **Partial absorption is a finite transient** | C1 (55 carries, 0 violations) |
| T55 | Recurring carries are prime powers p^j | P1 (65 eventual cycles, 0 exceptions) |
| T56 | Decoupled odometers: carry = min_p p^{j_p}, j_p from Abs_p⊂Z/ord_g(p) | O1, P2 (65 cycles, 0 mismatches; all single-prime) |
| T57 | **General q-carry theorem** under finite hypotheses (Q1)–(Q4): γ-cycle 1..q²−1, x_{n+q²−1}=q²x_n | Q1 direct orbits; Q2 closure certificates |
| T58 | Erratum: v008 M4a, M4b false; correct identity γ_{n+3}=4γ_n/ρ² | N4.1–N4.3 |

## Answer to "which carries are possible"
* Only **prime-power** carries recur (T55), and only **complete** ones after finitely many steps (T54).
* For odd g a carry M needs **M² < g** (T52); so there is no q-carry for odd g ≤ q².
* Not every size is excluded: exact witnesses exist for q = 3, 5, 7.

## DATA
* Exact q-carry witnesses (direct orbit of C, plus class-closure certificate):
  q=3: g=11 (γ-period 8); q=5: g=31 (24), and independently g=71; q=7: g=367 (48; transient 2832, class period 2928).
* Smallest odd prime g satisfying (Q1)–(Q4): q=3:11, 5:31, 7:367, 13:601, 17:1321, 23:1289. **q=11: none below 4000** (data only, not an impossibility claim).
* Persistent **even** g exists: g=68 (direct, 50 steps; γ-period 8, ρ=3). So no "persistent only for odd g" collapse theorem holds.
* Nonstandard finite-state cycles: g=31 mixed carries 2²,2²,2¹ (P=33, ρ=32) in both orders; g=31 P=24 with ρ=32; g=17 P=33, ρ=256; g=59 whose transient has both 3- and 4-carries but whose eventual cycle is single-prime. All explained by T56.
* Partial carries seen only in transients (g=131, γ ≈ 10¹⁷ → 10¹² over four partial carries).

## OPEN (not claimed)
* **O9.1 / Q0b** — is (Q1)–(Q4) solvable for every odd prime q? (A Chebotarev/Kummer argument looks plausible; not carried out. q=11 has no instance below g=4000.)
* **O9.2** — no persistent orbit with an eventual cycle having ≥2 active primes was found. T56's multi-prime clause is proved but not exercised by any test.
* Which g>1 admit persistent orbits at all (characterisation via T52/T56).
* Bound on the number of transient partial carries (T54 gives ≤ log₄γ₀+1).
* No claim is made that any regime outside the exhibited ones is impossible.

## Notes
* Mod-g residue-set machine validated against exact `Fraction` iteration of C (`direct_orbit`) throughout.
* Predecessor verifiers rerun separately (see MANIFEST / package notes); v002–v008 verified byte-identical to the v008 package.
