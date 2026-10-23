# CONTEXT — FIELD-I v012 (read this first when continuing)

## Where the project is
FIELD-I studies the fixed-nest rule: occurrence r=(M,N), d=N+1, v=M d²/N. The collective map C(x)=x+L²/G (L=lcm D(x), G=gcd{d−1}) is a **chosen** interaction (nonselection theorem, v002), not derived.
G_n is non-increasing in divisibility (v005). G_∞=1 ⇒ regime I, x_{n+3}=4x_n. G_∞=g>1 ⇒ persistent orbit, x=γL²/g (v008 T44). Every orbit is eventually exactly scaling, x_{n+P}=ρ²x_n (T51), with ρ=p^s for ONE prime p (T60/T61).
v011: the survivor is decided statically from one reset state (T64–T67): survivor = the saturated prime r with no smaller available competitor; carry word = gaps of Abs_r; ρ=r^s. Necessary for saturated survivors with prime g.

## What v012 established (THEOREMS.md T69–T73)
1. **T69 (sharp reset descent).** From a segment start with γ₀ the first reset needs at most κ(γ₀) carries, κ = iterations of f(a)=⌊a/4⌋+1 to 1 (≈ log₄; closed form: least k with 4ᵏ>(3a−4)/2). Attained (κ=1…11 found by the exact machine). The proposal's ⌈log₂γ₀⌉ is valid but loose.
2. **T70 (class counting).** After the first reset the reset-state class cycle is entered at index ≤ H(g)−1, H(g)=∏_{p²<g}(2o_p−1); segment ends (reducing event) before carry H after the reset; for prime g the entry state is statically certified for the active prime.
3. **T71 (polynomial bound).** Via epochs of the scheduler (L1 reduction to pure saturated powers or unsaturated support; L2 frozen competitor; potential Φ): entry index ≤ K_poly(g) = (Φ+1)(Σ+(Σ+1)(ω+1)+1), cubic in the orders. Valid for prime g (or whenever T67 applies).
4. **T72 (dynamic G).** Chain g₀⊋g₁⊋…, ≤Ω(g₀) segments with G>1; γ_{i+1} ≤ g_{i+1}(γ_i+4g_i+1)/g_i; segment carries ≤ κ(γ_i)+H(g_i)−1; G=1 tail ≤ 4κ₃(t); total R(g₀,γ₀) explicit.
5. **T73** registered corrections: v011 T68(a) is only proved for prime g (composite/even: S5 fails at every reset state of the six exact composite cycles tested); the proposal's T69 loses a factor 2 per carry.
All bounds are worst-case with enormous slack (observed entry index ≲ 200 vs H ≈ 10¹⁵, K_poly ≈ 2·10⁸).

## Tools (field12.py; helpers copied from v011/v010/v009)
`kappa`, `kappa_closed`, `kappa3`, `Pg`, `Hb`, `Kpoly`; `iterate_classes(g,E)` (carry-level iteration with class detection, T51+T67); `analyse_epochs`, `Bep`, `cU`, `sat_set`, `phi` (T71 lemmas);
`gstep(g,γ,E)` (exact general step incl. reducing events, independent of the residue machine, cross-checked with `direct_orbit`); `trace(g,γ,E)` (hybrid exact orbit: machine inside segments, gstep at reducing events; returns segments + G=1 tail);
`Rbound`, `Tailbound` (T72 totals); `gen_dyn_seed` (composite/even g₀ with two primes ≡1 mod g₀), `to_reset`, `adv_reset_seed` (competing saturated primes, run exactly to their first reset); `descent` (machine to the first reset with T54 check).
Note: `Gexact` in field12.py is a lazy early-exit version (same value as v011, returns None if the divisor count exceeds 3·10⁶); the v011 version enumerated all divisors and exhausted memory (exit 137) on adversarial seeds.
`FIELD12_QUICK=1` gives a ~1-minute run.

## Open items for v013 (suggested, in priority order)
- **O12.1** Exact transient time / a bound within a small factor of the observed entry index (observed ≲ 200 for g ≲ 200; bounds ≥ 10⁸). Natural route: bound the *number of epochs actually used* by the structure of the Abs tables (the potential Φ is attained only if every unsaturated prime fires), or prove an a-priori bound on the number of non-survivor firings from the minimax table (m_p ordering).
- **O12.2** (= O11.2) Static certification for composite/even g: S5 must be replaced by a condition on the plateau steps with gcd(g,w)>1; E5 shows all six exact composite cycles (g=15,39,51,57,68,87) fail S5 while being persistent.
- **O12.3** T71 for composite g where T67 does not apply (plateau steps with gcd(g,w)>1 change h and b′).
- **O12.4/O12.5** (= O11.3, O11.4) closed form m_p and survivor for the q-carry families; infinitely many carry sizes. q=11 (g=6689) class-closure certificate still not completed (needs ~50 000 machine steps).
- Possible extension: sample the *initial* fibres more broadly than `gen_dyn_seed` (arbitrary x₀ = a/b, not only seeds built from primes ≡1 mod g₀); the T72 bound is a theorem for every x₀, the test sample is not exhaustive.

## Hazards (environment)
Never `pkill -f`/grep-kill a pattern that appears in the shell command itself (kills the shell, exit 144): kill by explicit PID. Pure-Python factoring (no sympy). Foreground runs time out at ~600 s: run detached (`setsid nohup … &`) and poll with a bounded loop.
Memory: exact G checks on seeds with several primes of large exponent must not enumerate all divisors (see Gexact note above).
