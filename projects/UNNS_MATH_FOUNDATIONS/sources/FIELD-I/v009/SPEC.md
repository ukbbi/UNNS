# FIELD-I v009 — SPEC (what is computed, and what each tag means)

Package: Arithmetic Carry Cycles and Regime Classification. Preserves FIELD-I v002–v008, the G1–G3 memo and the relational manuscript byte-for-byte.

## Objects
- Fixed-nest rule, collective map C(x) = x + L²/G on rationals, D(x) = {d ≥ 2 : d² | a, d ≡ 1 (mod b)} for x = a/b (unchanged).
- Persistent state: G(x) = g constant; x = γL²/g, L = lcm D, gcd(L,g) = 1.
- **Residue machine** (field9.py, section "ABSTRACT MACHINE"): state = (g, γ, exponent dict of L). One step implements T49 on residue sets mod g
  (never on the integers), so it runs with astronomically large L. `minit` builds the state of x₀ = γ₀·L_seed²/g (and checks G(x₀) = g exactly by
  explicit divisor enumeration at the initial state only); `mstep` advances one step; `run_cycle` iterates until the **class** (T51) repeats;
  `reduce_cycle` extracts the minimal γ-period, the uniform scaling ratio ρ_p = L_{n+p}/L_n and the carry events (w, r²).
- **Direct iteration** (`direct_orbit`): the collective map itself on exact `Fraction`s with the factoring helpers inherited from v005. The machine is **never trusted
  without** this check: section A compares them on every witness used later and on hundreds of random seeds; A3 checks the one-step law on arbitrary (g, L, w), including composite g with h = gcd(g,w) > 1.

## Tags
- `PASS` / `FAIL`: a test with a decided outcome (FAIL would mean the claim in THEOREMS.md is wrong).
- `DATA`: exact but finite computation (tables, random-seed statistics, witnesses).
- `OPEN`: explicitly not proved.
No theorem is "proved by enumeration". Two kinds of evidence are kept apart: (1) hand proofs (T49–T57) whose hypotheses are finite checks; (2) **class-closure certificates**, which are
finite-state arguments justified by T51 (a repeated class ⇒ periodic forever), not bounded runs.

## Sections of field9.py
A. One-step law and machine vs direct iteration. N1. Eight-step theorem (G = 11). N3. Window theorem, carry completeness, carry criterion, odometers, prime-power carries.
N2. General q-carry theorem, table of (q, g), witnesses q = 3, 5, 7 with direct orbits and class-closure certificates. N4. Erratum checks (v008 M4a/M4b/T48). E. Extra data: even-g persistent orbit, nonstandard cycles.
Environment variable `FIELD9_QUICK=1` shrinks sample sizes (class-closure certificates and all PASS/FAIL logic are unchanged).
