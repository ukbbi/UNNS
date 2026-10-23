# Research specification — EN-I v0.1.0

## Target experiment
Bipartite, two-outcome, four-setting CHSH experiment; x,y ∈ {-1,+1}; a,a′ assigned to Alice, b,b′ to Bob. Settings in radians, polarizer convention; E_Q(a,b) = −cos(2(a−b)). Quantum reference P_Q(x,y|a,b) = (1−xy cos(2(a−b)))/4 for a suitable entangled Bell state. Angles: a=0, a′=π/4, b=π/8, b′=−π/8. CHSH S = |E(a,b)+E(a,b′)+E(a′,b)−E(a′,b′)| = 2√2.

## Structural hypothesis (unproven)
Spatially separated outcome streams may be distinct observable branches of one generative substrate object. Define a joint probability rule from independent axioms for recursive generation, projection/measurement, admissibility and normalization. Ordinary common-cause hidden variables with measurement independence and Bell locality satisfy S≤2, irrespective of vocabulary.

## Required explicit derivation
1. State space and measurable events.
2. UNNS recursion operator(s) and fixed parameters, without quantum target terms in assumptions.
3. Measurement setting choice, conditional probabilities and instrument/projection rules.
4. Joint probability P_UNNS(x,y|a,b), nonnegative and normalized for **all** settings tested.
5. Distribution-level operational no-signalling for both wings.
6. Identify how Bell-local factorizability, measurement independence, or another assumption is handled; distinguish parameter dependence, outcome dependence and contextuality.
7. Establish robustness under untrained angle choices and independent seeds; disclose all tuning and exclusions.

## Prespecified gates
G0 Mathematical validity: every probability is finite and nonnegative within 1e-12; total 1 within 1e-12. Failure: stop.
G1 Bell benchmark: analytic or high-precision S_UNNS >2+1e-6 on the frozen CHSH angles without angle-specific fitting. Failure: no Bell violation. A finite-sample version must report CIs and cannot replace analytic evidence.
G2 Operational no-signalling: for all tested settings, marginals invariant to remote settings within 1e-10 analytic tolerance; finite samples treated separately with uncertainty. Failure: reject as standard entanglement account.
G3 Quantum reconstruction: maximum absolute correlation error <=1e-3 over a **held-out** fixed angle grid (32 pairs) plus all four CHSH pairs. Passing means reconstruction, not independent discovery. Grid definition must be frozen before model tuning.
G4 Novelty: identify one quantitative UNNS-specific observable prediction, preregistered measurement design, and a discrepancy from standard quantum theory distinguishable from experimental/systematic uncertainty. No novelty claim without this.

## Held-out grid
Let a_i=πi/32, i=0..7; b_j=πj/32, j=0..3 (32 angle pairs). This grid is public and therefore *cannot* be considered unseen after it is used for tuning; use a separately sealed validation collection if tuning occurs.

## Controls and exclusions
Classical Bell-local null; randomized outcome independence null; deterministic extremal strategy check; adversarial search for setting-dependence; normalization and no-signalling tests. No removal of trials by outcome, setting or purported admissibility unless a preregistered measurement-independent inclusion rule proves no detection loophole. Report original trial totals.

## Freeze and limitations
Reference configurations are fixed in `config/protocol.json`. Default RNG seed 1729, sample sizes 1000 and 10000 reserved for optional Monte Carlo extension. Current deterministic baseline does not sample. Report timestamps are omitted for bitwise reproducibility. No actual UNNS-derived joint law is included or claimed.
