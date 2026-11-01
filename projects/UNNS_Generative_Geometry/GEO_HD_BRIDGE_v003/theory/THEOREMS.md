# Theorem register — GEO_HD_BRIDGE_v003 (R3-T1 … R3-T7)

Status classes: **PROVED**, **PROVED-RESTRICTED** (proof under stated hypotheses), **FINITE-EXACT**, **SAMPLED**, **FALSIFIED**, **OPEN**.  
New theorems are checked by verifier shards Z1–Z7 separately from integrity/regression checks (Z0). Proofs are in the linked documents.

| id | statement | status | doc |
|---|---|---|---|
| R3-T1a | For rational states the realised complexes `K_axis,K_move` (cells, components, homology) are functions of `D`; positive-primitive and edge-realised Graver moves are functions of `F` | **PROVED** (+ 631 / 159 state checks) | RATIONAL_GEOMETRY §2 |
| R3-T1 | Infinite families with equal `D` and different region-Graver sets: `|Gr|=2` vs `4` (k=2, Dirichlet); `2` vs `k(k−1)+2`, dormant set = root system `A_{k−1}` (all k≥2, Dirichlet). Realised geometry identical | **PROVED** | RATIONAL_GEOMETRY §3 |
| R3-T2 | Complete classification of two-prime, box (1,1) states: 7 relation types; `Gr`, `D` functions of type; the bit `[p≡r (mod b)]` is necessary and sufficient beyond `D` | **PROVED** (+12 788 / 4 771 states) | ARITHMETIC_CLASSIFICATION |
| R3-T2' | Classification for `q ≠ 1^k`, ≥3 primes in general | **OPEN** | O3-1 |
| R3-T3 | Component-separating invariant `I=[2 before 4]` = first occurrence event for source 4, contents `{2,4}∪A`, `A∩{1,2,4}=∅`; infinite disconnected family of unbounded dimension | **PROVED** (+121 contents) | HISTORY_INVARIANTS |
| R3-T3' | Completeness of pair-order bits; component count | **FINITE-EXACT** (counts 1/2/3 on 121 contents); formula **OPEN** | O3-3 |
| R3-T4 | Restricted: blocked junction ⇒ `π_0 ≥ 2` (arithmetic resource deficit ⇒ topology of the history complex). General law (components count, `H_1`, `H_2` families, filling obstructions) | **PROVED-RESTRICTED**; general **OPEN** | HIGHER_DIMENSIONAL |
| R3-T5a | Exact reduction for the class `G(x)=b`: `x=tL²/b`, `C(x)=(t+1)L²/b`, `D` monotone, `G` stays `b` while `gcd(t+1,b)=1` | **PROVED** | COLLECTIVE_REGIMES §1 |
| R3-T5b | First event of a fresh stage occurs at `t=u*²`; dichotomy (leave the class in finitely many steps, or infinitely many events) for prime `b` | **PROVED** | §2 |
| R3-T5b' | ℓ=11 tower `S_k=2²3^{3+k}5⁴`: `x_{8k+j}=(j+1)S_k²/11`, `x_{n+8}=9x_n`, `|D|=2k+7`, one 2-index event per period, for all k | **PROVED** | §3 |
| R3-T5c | ℓ=5 tower `S_k=126·2^k`: `x_{n+3}=4x_n` with `G=5` for all k. **Falsifies** "rigid ⇔ `G∞=1`" (erratum to B2-T7/G2-Q1) | **PROVED**; v002 wording **FALSIFIED** | §3 + ERRATUM |
| R3-T5d | Stage law `P=Σ(τ_i−1)`, `ρ²=Πτ_i` for periodic stage sequences; ℓ=29, S=1890: `(P,ρ²)=(35,900)`; census of 1 920 orbits shows only `(3,4),(8,9),(35,900)` among persistent ones | **FINITE-EXACT** (stage law proved given periodicity) | §4–5 |
| R3-T6 | Realised geometry is constant between events; silent arithmetic carries (box grows, `D` fixed); Betti vectors of the ℓ=11 tower | **PROVED** (constancy, silent carries); **FINITE-EXACT** (Betti table k≤11) | GEOMETRIC_TRANSITIONS |
| R3-T7 | Classification of all `R(N)`-ratio pairs of iterates on the ℓ=11 and ℓ=5 towers; L3 holds for N∈{1,2,5} (ℓ=11), N=1 (ℓ=5), fails for N=8, N=3; failure of event saturation for formal edges on rational states | **PROVED** (arithmetic + tower formulas) | CORRESPONDENCE |

Corrections to earlier releases: `GEO_HD_BRIDGE_v002_ERRATUM_B2-T9.md` (accepted), `GEO_HD_BRIDGE_v002_ERRATUM_B2-T7.md` (found here).  
Nothing here is a claim about C3 or novelty; same-author caveat.
