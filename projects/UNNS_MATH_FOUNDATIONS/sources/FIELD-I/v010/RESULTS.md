# RESULTS — FIELD-I v010: Multi-Prime Carry Coexistence

Full run of `field10.py`: **0 FAIL, 502 s** (`output/field10_output.txt`). Proofs are in THEOREMS.md (T59–T63). v002–v009, the G1–G3 memo and the relational manuscript are unchanged.

## Answer to the primary question (PROVED, not a search result)
> Does there exist x₀ and primes p ≠ q such that p and q both carry infinitely often?

**No.** In the eventual regime of every persistent orbit exactly one prime carries (T60). The mechanism is a scheduler with *frozen* pending carries: the prime whose **worst-case** pending carry m = max p^gap(Abs_p) is largest can never fire from that worst-case state, because every competitor's pending carry is ≤ its own m < that value. It therefore stops, and by induction only the prime with the smallest m survives (T60, Corollary 1).
This is true already for **abstract** odometer systems, before any arithmetic: the abstract question (verdict ABSTRACT_COEXISTENCE) has the answer "never".

| Verdict | Result |
|---|---|
| ABSTRACT_COEXISTENCE | none; proved impossible (T60). Exhaustive check: 6 prime pairs × all subsets of Z/s, Z/t for s,t ≤ 6 × all start states = 86 400 odometer pairs, 2 313 846 walks, 0 cycles with both primes firing; plus 6 000 random 2–3-prime systems (moduli ≤ 30), 72 000 walks, 0 |
| ARITHMETIC_REALIZABLE | none: 36 694 contested prime pairs built from the arithmetic of g (Abs from the definition, prime g < 400, random frozen backgrounds, window c² < g), 256 858 walks, 0 with both firing |
| COLLECTIVE_CERTIFIED | none: 475 exact eventual cycles of the collective map (T51 class closure), active-prime histogram {1 prime: 475} |
| EXCLUDED | every candidate pair, by the proof of T60 |
| UNRESOLVED | none for the coexistence question |

## PROVED
| # | Result | Checked by |
|---|---|---|
| T59 | Carry scheduler: at γ = 1 the prime with the smallest pending carry c_p = p^{j_p} fires; c_p depends on e_p mod o_p only (active p) and is frozen (inert p) | S1: 11 242 reset states in 357 eventual cycles, 0 mismatches with the residue machine; R4: 2 460 inert-prime pending carries all constant |
| T60 | **Single-prime dominance**; survivor = smallest worst-case carry m; threshold-overlap lemma is vacuous (m_q > m_p and m_p > m_q) | X1, X1b, X2 (survivor = smaller-m prime in 100 % of walks), R1, R3 (2 460 competitor pairs, 0 violations) |
| T61 | **ρ = p^s**: the eventual scaling factor is a prime power; P_γ = Σ(p^{2j_i}−1) over the gaps of Abs_p | R2: 475/475 cycles; controls C1 |
| T62 | Two saturated clocks have coprime periods o_p/gcd(o_p,o_q), o_q/gcd(o_p,o_q) (prime g) | X3: 36 694 pairs, 0 exceptions |
| T63 | Registered corrections to the v010 problem statement (threshold-overlap lemma, "alternating thresholds") | — |

Consequence for the whole project: every orbit of C eventually satisfies **x_{n+P} = p^{2s} x_n for a single prime p** (regime I is p = 2, s = 1, P = 3).

## Controls (all classified correctly by the new invariants)
| Example | active prime | Abs_p | s | γ-period | ρ |
|---|---|---|---|---|---|
| G = 11 three-carry | 3 | Z/5 | 1 | 8 | 3 |
| G = 31 five-carry | 5 | Z/3 | 1 | 24 | 5 |
| G = 31 mixed 2², 2², 2¹ | 2 | {0,2,4} ⊂ Z/5, gaps (2,2,1) | 5 | 33 | 32 |
| G = 17 | 2 | Z/8 \ {4}, gaps (1,1,1,2,1,1,1) | 8 | 33 | 256 |
| G = 59 (4-carries only in the transient) | 3 | Z/29 | 1 | 8 | 3 |
| even G = 68 | 3 | Z/16 | 1 | 8 | 3 |

## DATA
* Pool statistics: 2 287 random seeds tried → 357 exact cycles; 193 adversarial seeds (two small primes start saturated and compete, frozen auxiliary primes with random residues) → 118 exact cycles. In all 475, every other small prime has a pending carry ≤ 2√g (a competitor), and in all 2 460 competitor/cycle pairs the survivor's m is smaller than the competitor's frozen pending carry.
* The sample is limited by two caps: seeds whose transient needs γ > 2⁶⁴ (factoring γ+1) and seeds exceeding 6 s are skipped, so the exact counts depend slightly on the machine speed; the verdict does not.
* "0 empty Abs": Abs_p ∋ 0 always (d = p^{o_p} ≡ 1), so every prime always has a finite pending carry p^{gap}; the window c² < g (T52) decides whether the orbit survives (6 839 of 256 858 arithmetic walks leave persistence).
* Extended q-carry instances (T57 hypotheses (Q1)–(Q4), exact): q = 11: g = 6689; q = 19: g = 27631; q = 29: g = 7489; q = 31: g = 21673; q = 37: g = 4271 (v009: q = 3, 5, 7, 13, 17, 23: g = 11, 31, 367, 601, 1321, 1289). Residue-machine check of two full carries for q = 11 (γ-cycle 1..120), q = 29 (1..840), q = 37 (1..1368). q = 41: none with g < 30000 and ord ≤ 1500 (data only).
* The class-closure certificate (T51) for q = 11, g = 6689 is NOT part of this run and is NOT completed in this package: `q11_certificate.py` needs about 50 000 machine steps (≈ 207 transient carries × 120 steps plus the class period 120 × 209 = 25 080; the printed '≈ 25 080' in N4 understates this). `output/q11_certificate.txt` records the first attempt, which stopped at the 30 000-step cap after 919 s without a closure (not a failure of the orbit). The q = 11 claim therefore rests on T57 (hand proof, hypotheses verified exactly) and the two-carry machine check N2, not on a closure certificate.

## OPEN (not claimed)
* **O10.1** A closed rule giving the surviving prime from the seed without iterating the scheduler (T60 gives the necessary rule: the survivor's worst-case carry is below every frozen competitor's pending carry).
* **O10.2 (= O9.1)** Is (Q1)–(Q4) solvable for every odd prime q (an infinite family of distinct eventual carry sizes)? Eleven values q ≤ 37 are exact instances.
* **O10.3** Which triples (g, p, Abs_p) occur — the classification of eventual types; T52 (window c² < g) and T62 are restrictions, not a characterisation.
* **O10.4** The proofs of T59–T60 do not use primality of g, but almost all numerical samples are prime g (plus the even g = 68 control).
