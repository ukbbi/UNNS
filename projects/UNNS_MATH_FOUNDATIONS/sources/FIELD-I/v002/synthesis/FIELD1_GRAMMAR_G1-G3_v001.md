# FIELD-I — Interaction grammar G1–G3 (v001)

Standalone research memo. Builds on FIELD-I v002 (THEOREMS.md T6–T16, field2.py). Nothing in v001, v002, manuscript v3, SELECT-I/II is modified.
Numerical claims below are reproduced by `synthesis/g_checks.py` (output in `g_checks_output.txt`).

**Status labels.** *Proved*: follows from the stated definitions by an argument given here or in THEOREMS.md. *Proposed*: a grammar rule offered for adoption; neither true nor false. *Open*: undecided. *Data*: finite observation.
**No physical or entanglement claim is made.**

---
## 0. Position

The fixed-nest rule fixes every future coincidence of routes, as arithmetic progressions. It does not say which coincidence is an "interaction", nor whether an interaction may use the routes' labels. That is where the existing grammar ends. G1–G3 are three explicit decisions a developing grammar would have to take. They are proposals, not consequences.

## 1. Setting (all proved in v002)
Occurrence r=(M,N), d=N+1, value v(r)=Md²/N, successor F(r)=(M+1,N), reduced step s_N=d²/N. Fibre F(x)={r : v(r)=x}, x=a/b; F(x) ↔ D(x)={d≥2 : d²|a, d≡1 mod b}. For distinct r,s∈F(x): L=lcm(d,d'), g=gcd(N,N'), **Δ_rs=L²/g**, h_rs=x/Δ_rs∈ℤ_{>0}. Collective: Δ_coll=lcm(d_i²)/gcd(N_i)=lattice-lcm of the Δ_rs, **γ(x)=x/Δ_coll=gcd H(x)**.
- (P1) Common future of r,s = {x+jΔ_rs : j≥0}; of the whole fibre = {x+jΔ_coll : j≥0}.
- (P2) Π=∏_x Sym(F(x)) (fibrewise relabelling) is the automorphism group of the value-only structure and is transitive on unordered pairs of each fibre. Any Π-invariant function on pairs of distinct equal-value occurrences is a function of x alone (the fibre is determined by x).
- (P3) Keeping route membership makes the structure rigid; (v(r),v(Fr)) determines (M,N).

## 2. Axioms for a value-valued pair operation (exact)
Dom={(r,s) : r≠s, v(r)=v(s)}. For (r,s)∈Dom with x=v(r), Δ=Δ_rs, and i∈ℤ_{≥0}: τ_i(r,s)=(F^{iΔ/s_N}r, F^{iΔ/s_{N'}}s) (exponents are integers by P1); v(τ_i(r,s))=x+iΔ. A pair operation is ⋆:Dom→ℚ_{>0}.
- **A2 symmetry:** ⋆(r,s)=⋆(s,r).
- **A3 common future:** ⋆(r,s)∈x+Δ_rs·ℤ_{≥1}.
- **A4 stationarity:** ∀(r,s)∈Dom ∀i≥0: ⋆(τ_i(r,s)) − v(τ_i(r,s)) = ⋆(r,s) − x.  (the *gap* ⋆−x is unchanged by advancing both routes whole rendezvous periods)
- **A6 label-blindness:** ∀π∈Π ∀(r,s)∈Dom: ⋆(πr,πs)=⋆(r,s).
- **A6w partner-independence:** ∀x, ∀ pairwise distinct r,s,t∈F(x): ⋆(r,s)=⋆(r,t).  A6⇒A6w (take π=(s t)).
- **A7p pairwise minimality:** ⋆(r,s)=x+Δ_rs.  **A7c collective minimality:** ⋆(r,s)=x+Δ_coll(x).

**Scope of label-blindness (proved).** For value-valued ⋆ with A2, A3, A6: ⋆(r,s)=Y(x), and Y can be *any* function of the realised value x with Y(x)∈x+Δ_coll(x)ℤ_{≥1}, i.e. Y(x)=x+j(x)Δ_coll(x)=x(1+j(x)/γ(x)), j(x)≥1 arbitrary. Permutation invariance restricts the *admissible set* (it depends on x only through Δ_coll=x/γ); it does **not** force the *selection* j(x) to depend on γ alone: j(x) may use any invariant of the fibre (γ, R, H, the rendezvous graph, x itself) or none. Example: Y(x)=2x is label-blind and uses no gcd data (it is the choice j=γ). *(This sharpens the wording of RESULTS.md, "only γ matters", which should be read as "γ determines the admissible set".)*

## 3. Non-selection theorem (proved; checked F8.1, F8.2)
**Theorem N.**
1. A2+A3 are satisfied exactly by ⋆(r,s)=x+j(r,s)Δ_rs with j:Dom→ℤ_{≥1} symmetric; A4 holds iff j is constant on τ-orbits.
2. R-family ⋆_j (constant j≥1) satisfies A2, A3, A4; fails A6 (and A6w) as soon as some fibre has two unequal Δ_rs; satisfies A7p iff j=1.
3. C-family Y_j(x)=x+jΔ_coll(x), with **C=Y_1**, satisfies A2, A3, A6, and A7c iff j=1; **fails A4**.
4. ⋆_1 and C coincide on every two-route fibre (488 of 1,116 corpus fibres; data) and differ on 1,340 of 3,642 pairs of fibres with R≥3 (data).
5. Hence A2+A3(+A7) are satisfied by competing operations that differ on every pair or on most; the choice between A4 and A6 is not made by the rule; A7 is independent of A1–A4 (model j=2).

|  | A2 | A3 | A4 | A6 | A7p | A7c |
|---|---|---|---|---|---|---|
| ⋆₁ | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ (R≥3) |
| ⋆_j, j≥2 | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| C=Y₁ | ✓ | ✓ | ✗ | ✓ | ✗ (R≥3) | ✓ |
| Y_γ=2x | ✓ | ✓ | ✗ | ✓ | ✗ | ✗ |

Why the rule privileges neither: both alternatives are built from the same data (P1), pair lattices versus the fibre lattice. A4 and A6 are the two natural invariances of that data; the rule does not rank them (Theorem I below shows they cannot both hold).
Concrete: x=2025/2, D={3,5,9,15,45}, H={1,1,1,2,2,2,9,9,9,25}. Pair (15,45) has h=1: ⋆₁=2025. Pair (3,9) has h=25: ⋆₁=1053. A6 fails for ⋆₁. C=2025 (γ=1).

## 4. Incompatibility theorem (proved; checked F8.6, F8.7, G.1–G.3)
**Theorem I.** There is no ⋆:Dom→ℚ satisfying A3, A4 and A6w (hence none satisfying A3, A4, A6).
*Hypotheses actually used:* A4 for one pair (r,s) and all i≥0; A3 for the pairs (r_i,q) below; A6w in the fibres F(y_i), each of which contains ≥3 routes. A2 is not used.

*Proof.* Take any x=a/b, r≠s in F(x), moduli d,d', N=d−1, N'=d'−1, g=gcd(N,N'), L=lcm(d,d'), Δ=L²/g. By v001 T1′, b|N and b|N', so b|g. Put y_i=x+iΔ=(ag/b+iL²)/g; the denominator of y_i divides g, and r_i,s_i (the τ_i shifts) lie in F(y_i). Let p be a prime with p>max(g,L) and p≡1 (mod g) (infinitely many, Dirichlet). Since p∤L, choose i≥0 with ag/b+iL²≡0 (mod p²). Then:
1. p² divides the numerator u of y_i (p∤g), and M''=y_i(p−1)/p²=u(p−1)/(ep²) with e|g|p−1 is a positive integer. So q=(M'',p−1)∈F(y_i). As p>L≥d, q∉{r_i,s_i}.
2. A6w at y_i: ⋆(r_i,s_i)=⋆(r_i,q)=:Y_i.
3. A3 for (r_i,q): Y_i−y_i=j·Δ(r_i,q), Δ(r_i,q)=(dp)²/gcd(N,p−1) (p∤d), with gcd(N,p−1)≤N<p. So P:=Y_i−y_i has p² dividing its numerator in lowest terms.
4. A4 for (r,s): ⋆(r_i,s_i)=⋆(r,s)+iΔ, so P=⋆(r,s)−x, a fixed positive rational independent of p.
A fixed non-zero rational cannot have numerator divisible by p² for infinitely many primes. ∎

*Counterexamples (exact; script G.1–G.3).*
- x=36, pair (2,3) (Δ=36, g=1, L=6): p=7 → i=48, y=1764, new route (M'',N'')=(216,6); Δ(2,7)=196. p=11 → i=120, y=4356, route (360,10), Δ(2,11)=484. In general Δ(2,p)=4p², so the fixed gap would be divisible by 4p² for p=7,11,13,17,19,23,….
- x=81, pair (3,9) (Δ=81/2): p=11 → i=119, y=9801/2, route (405,10), Δ(3,11)=1089/2=(3·11)²/2.
- Stationarity failure of C (A4): x=36, pair (2,3), shift 3Δ reaches y=144; C(x)−x=36 but C(y)−y=144.
- Label-dependence of ⋆₁ (A6): x=2025/2 above.

*Scope (what Theorem I does and does not say).*
1. Full domain Dom only. Restricting Dom (e.g. integer-valued fibres only) or restricting which shifts A4 must cover is **not** covered; unverified.
2. Value-valued outputs. Fibre-valued outputs escape the obstruction (G3).
3. A6w is the weak form: invariance under replacing one partner by another occurrence of the same value. Invariance under a proper subgroup of Π is not excluded (open).
4. It does not say label-blind operations are forced to depend on γ (§2).
5. It is not a failure of the fixed-nest dynamics: it says two reasonable invariances of the interaction cannot both be postulated.

## 5. The grammar rules

### G1 — Interaction regime *(choice; not forced by the rule)*
- **G1-R route-aware pair interaction:** r ⋆_j s = x + jΔ(r,s), j≥1. A2, A3, A4.
 *Permits:* j varying with the pair class (N,N',x mod Δ). *Excludes:* A6/A6w: results may depend on labels; by P3 these are recoverable, so the interaction is label-level information. *Changes vs v002:* adds only the declaration of j. With j constant, ⋆_j **renames** the common-future lattice of P1: the orbit of a fixed pair under ⋆_1 is the progression x+kΔ. *Discriminating test:* a proposed j must be given as a function constant on τ-orbits; the position-parity law j=1+((M+M') mod 2) is excluded (A4 fails, checked F8.1).
- **G1-C collective interaction:** C(x)=x(1+1/γ(x)). A2, A3, A6, A7c.
 *Permits:* any j(x) (§2). *Excludes:* A4 (Theorem I). *Changes vs v002:* defines a deterministic map C on realised values, hence an iteration x_{k+1}=C(x_k). *Proved:* x<C(x)≤2x; D(x)⊆D(C(x)) so R is non-decreasing along orbits (G.6, 1,116/1,116); while D is unchanged each step is the constant Δ_coll, an arithmetic progression with γ_k=γ_0+k (G.11). *Data:* orbit of 36: R=3,3,3,5,5,5,7,7,7,9; of 81: R=2…2,5,8; after fibre growth γ returns to 1 in 171 of 210 events, not all (exceptions: 272→288, γ=2; 1053→2187/2, γ=3). *Falsifiable conjectures (open):* R is unbounded along every orbit; characterise the growth events. *Renaming flag:* the closed form x(1+1/γ) restates T8 (gcd/lcm arithmetic); the new content is only the iteration.
- Both may be *named* in one grammar as different operators; no single operator may be asserted to satisfy A4 and A6.

### G2 — Continuation selection *(added axiom)*
Choose j (R) or j(x) (C) in ℤ_{≥1}.
- **G2-min (j≡1; A7p / A7c):** first meeting. **This is an added axiom**: by Theorem N(5) it is independent of the stated constraints (model j=2). *Permits:* x_next=x(1+1/h), resp. x(1+1/γ) ≤ 2x. *Excludes:* all later coincidences as results. *Renaming flag:* "the minimal positive element of the lattice P1".
- **G2-dbl (j=γ):** Y=2x, label-blind, uses no gcd data in its statement, fails A4. *Discriminates:* factor exactly 2 versus ≤2.
- **G2-free:** j arbitrary; unconstrained by A1–A4 (A4 forces τ-invariance only).
*Changes vs v002:* none numerically; fixes which element of the progression is "the" interaction.

### G3 — Output realization *(three options)*
- **G3-V value:** result is the number y. Satisfies all of the above.
- **G3-F fibre:** result is F(y), the set of occurrences at y (y given by G2). Π-invariant, hence label-blind; contains the continuations of r and s and, for C, every shifted occurrence of F(x) (so R(y)≥R(x)). Escapes Theorem I (not value-valued). Cost: the output is a set; no further binary composition without a rule.
- **G3-O occurrence:** result is one occurrence. **Proved (T14):** no Π-equivariant occurrence-valued operation with output in the common future exists, since R(y)≥2 and Sym(F(y)) fixes no element. So any selection needs extra information: (O1) an order on labels (tie-break by N): label-level, G1-R only; (O2) the join, occurrence with modulus lcm(d,d'): present at y=x+Δ in 3,725/3,767 integer-valued and 340/363 rational pairs (G.9), so **not total**, and it is lcm arithmetic on labels (v002 T16 closure obstruction); (O3) an external marking, a datum not in the rule.
*Excludes:* label-blind, fully composable occurrence algebra. *Changes vs v002:* specifies what an iterated interaction would act on.

## 6. Scientific status
| Item | Status |
|---|---|
| P1–P3; Theorem N; Theorem I; T14; properties of C listed in G1-C; non-totality of the join | **Proved** (checked) |
| G1–G3 as an interaction grammar; the choice A4 vs A6; j=1 | **Proposed** (axioms) |
| Whether an independent generative principle selects R-vs-C, j, or the output type; subgroup/weakened versions of Theorem I; R unbounded along C-orbits; which γ occur | **Open** |
| Orbit statistics, γ-reset frequency, join frequency | **Data** |

The absence of intrinsic selection locates where the present grammar stops and where a new rule must start. Each G-rule above can be adopted, replaced or rejected by later work; none is claimed to be derived.

## 7. Reproduce
`python synthesis/g_checks.py` (exit 0, ALL PASS). Depends on nothing outside `synthesis/`.
