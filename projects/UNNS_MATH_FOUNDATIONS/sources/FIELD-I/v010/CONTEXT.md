# CONTEXT — FIELD-I v010 (read this first when continuing)

## Where the project is
FIELD-I studies the fixed-nest rule: occurrence r=(M,N), d=N+1, v=M d²/N. The collective map C(x)=x+L²/G (L=lcm D(x), G=gcd{d−1}) is a **chosen** interaction (nonselection theorem, v002), not derived.
G_n is non-increasing in divisibility (v005). G_∞=1 ⇒ regime I, x_{n+3}=4x_n. G_∞=g>1 ⇒ persistent orbit, x=γL²/g (v008 T44).
v009: every persistent orbit is eventually class-periodic (T51), x_{n+P}=ρ²x_n; carries are complete (T54) and prime powers (T55); each active prime is an odometer on Z/ord_g(p) with admissibility set Abs_p (T56); window M²<g (T52); q-carry theorem T57.

## What v010 established (THEOREMS.md T59–T63)
1. **T59 scheduler.** At γ=1 the prime with the smallest *pending carry* c_p=p^{j_p} fires; for an active prime c_p depends only on e_p mod o_p; for an inert prime it is frozen.
2. **T60 single-prime dominance (resolves O9.2 negatively).** At most one prime carries infinitely often, for every g and seed. Proof: let p have the largest worst-case pending carry m_p=max p^gap; when p sits in its worst-case state its pending carry m_p exceeds every competitor's pending carry (≤ their m), so p never fires again. The survivor is the prime with the smallest m (among saturated primes). Holds for abstract odometer systems too.
3. **T61** ρ=p^s (s = minimal period of Abs_p in Z/o_p), P_γ=Σ(p^{2j_i}−1): the eventual scaling factor is a prime power. Every orbit of C eventually obeys x_{n+P}=p^{2s}x_n for ONE prime p.
4. **T62** two saturated clocks have coprime periods o_p/gcd(o_p,o_q), o_q/gcd(o_p,o_q) (prime g).
5. **T63** corrections to the v010 problem statement (the "threshold-overlap" lemma is true but vacuous; "alternating thresholds" cannot exist, even abstractly).
6. Data: T57 instances for q = 11 (g=6689), 19 (27631), 29 (7489), 31 (21673), 37 (4271) in addition to q = 3,5,7,13,17,23 (v009).

## Tools (field10.py)
`pend_j(g,E,p)`, `pendings(g,E)`, `sched_next(g,E)` — the exact scheduler; `abs_set`, `min_period`, `gap_list`; `eventual_cycle(g,Es,g0)` (T51 class-closure cycle with time/γ caps; returns states of one class period + closing state, carry events);
`build_pool(gen, seconds, seed)`; generators `gen_random_seed`, `gen_competing_seed`; abstract `sched_walk(primes,tabs,mods,start)`; `q_hyp_fast`, `q_seed_exact` (T57 hypotheses). The machine (`minit`, `mstep`, `run_cycle`, `reduce_cycle`, `machine_orbit`, `direct_orbit`) is copied from v009.
`q11_certificate.py` is a separate long run (class closure for q=11, g=6689; needs ~50 000 machine steps, now maxn=60000; the first attempt with maxn=30000 ended 'long' — see output/q11_certificate.txt). Hazards: direct exact iteration is infeasible for q=11 (u^208 with 1000-digit factorisations); γ>2^64 seeds are skipped by the pool builder (factoring γ+1).

## Open items for v011 (suggested, in priority order)
- **O10.1** Closed decision rule for the surviving prime from the seed (T60 gives the necessary rule only). Natural target: compute m_p for each saturated prime from (g, background F) in closed form via the discrete-log description of Abs_p (T62: Abs_p is a union of residue classes mod o_p/gcd(o_p,o_q)).
- **O10.3** Classify the realizable eventual types (g,p,Abs_p): which subsets of Z/o_p occur as Abs_p given the window c²<g? Combine T52, T62 and the structure Abs_p={k: p^{-k}∈⟨others⟩F}.
- **O10.2 (=O9.1)** A proof that (Q1)–(Q4) is solvable for every odd prime q (Chebotarev/Kummer on a cyclic quotient), giving infinitely many distinct carry sizes. Eleven q now realised.
- Composite/even g: T59–T60 hold (no primality used) but samples are almost all prime g; build an exact sample for composite g (known persistent: 15, 39, 51, 57, 87, 68).
- Connect to physics/clock reading: with one active prime, the asymptotic law is x_{n+P}=p^{2s}x_n; the "multi-clock" companion documents in the project are now seen as one-clock eventually.

## Hazards (environment)
Never `pkill -f`/grep-kill a pattern that appears in the shell command itself (kills the shell, exit 144): kill by explicit PID. Pure-Python factoring (no sympy). Foreground runs time out at ~600 s: run detached (`setsid nohup … &`) and poll with a bounded loop.
