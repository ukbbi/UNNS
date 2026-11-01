# R3-B  The missing arithmetic information

## 1. Structure theorem (general)
`Gr(x) = Pos(D) ⊔ Edge(D) ⊔ Dormant(x)` with `Pos(D), Edge(D)` explicit functions of `F` (R3-T1a) and `Dormant(x)` = the conformally minimal elements of `Lambda_b ∩ [-q,q]` not witnessed by `F`. So the arithmetic descriptor needed beyond `D` is exactly the dormant relation set `J(x)`, and `Phi(D,J)` = `Pos(D) ∪ Edge(D) ∪ J` (not a recomputation of the lattice: `J` is a subset of `Cand(D)`, the vectors not excluded by `F`; closure under sums/differences inside the box constrains `J`, see §2).

## 2. Theorem R3-T2 (complete classification, two primes, box (1,1)) — PROVED
Let `p<r` be primes, `x = (pr)²/b`, `gcd(pr,b)=1`. Put  
A: `p ≡ 1`, B: `r ≡ 1`, C: `pr ≡ 1`, E: `p ≡ r` (all mod `b`).  
Then `Lambda_b ∩ {-1,0,1}²` contains `(1,0),(0,1),(1,1),(1,-1)` exactly when A,B,C,E hold.  
*Closure.* If two of the four vectors lie in the lattice, their sum/difference gives a third: A&B, A&C, A&E, B&C, B&E each force all four; C&E forces nothing in the box (`(2,0),(0,2)` are outside). So the type `T ⊆ {A,B,C,E}` is one of seven: `∅, A, B, C, E, CE, ABCE`.  
*Graver sets.* A or B present ⇒ `±(1,0)` / `±(0,1)` dominate `(1,±1)`; so  
`∅:∅`, `A:{±(1,0)}`, `B:{±(0,1)}`, `C:{±(1,1)}`, `E:{±(1,-1)}`, `CE:{±(1,1),±(1,-1)}`, `ABCE:{±(1,0),±(0,1)}`.  
*D.* `D = {p|A} ∪ {r|B} ∪ {pr|C}`.  
So `Gr = Phi(D,e)` where `e = [E]`: `D` determines the type except `D=∅ ⇐ {∅, E}` and `D={pr} ⇐ {C, CE}`; `D={p}`, `{r}`, `{p,r,pr}` fix the type. The bit `e` is **necessary** (both values occur for `D=∅` and `D={pr}`) and **sufficient**, hence a provably irredundant descriptor: `J(x) = [p ≡ r (mod b)]` for these two `D`.  
*Checks.* 12 788 states (builder, `p,r<40`, `b<260`) and 4 771 (independent verifier Z3): 0 deviations from the type table; both values of `e` occur for `D=∅` and `D={pr}`.

## 3. Higher dimensions
R3-T1 (family k) is the generalisation: for `q=1^k` the relation set is `{(T+,T-): p_{T+} ≡ p_{T-}}`; `D` witnesses exactly those with a completion `W` such that `T-∪W ∈ D`. In family k the whole `A_{k-1}` root system is dormant. What is *new with dimension* is the lattice-theoretic type (here: all `p_i` congruent), not the count of coordinates: for k=2 the same phenomenon is the single bit `e`.
**Adversarial test.** The scan includes all `p,r` below the bounds with every admissible `b`; the only random-looking cases (e.g. `a=900, b=13`: `D=∅` but Graver size 2) fall under type `E`.

## 4. Open
Complete classification for `q != 1^k`, for three or more primes, and the minimal descriptor when `q_p>1` (see `OPEN_PROBLEMS.md` O3-1, O3-2).
