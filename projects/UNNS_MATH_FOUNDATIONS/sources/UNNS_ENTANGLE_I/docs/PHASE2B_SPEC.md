# Phase 2B — Proto-Closure to Observable Measure (v001)

**Scope.** This is a limited logical audit, not an identification with canonical Operator XVI or a derivation of quantum probabilities. Phase 1/2 JSON baselines are locked byte-for-byte under `output/frozen/` and checked against SHA-256 values in `config/PHASE2B_LOCK.json`. No prior files are replaced.

## Source-grounded definitions

From *Mechanisms, Structural Closure, and Proto-Closure in the UNNS Substrate* (provided PDF): Definitions 3–9 define a mechanism `M=(Σ,R,C,O)`, structural states up to admissible equivalence, refinement sequences, nontrivial recurrent structural closure, and proto-closure prior to numerical evaluation. Appendix A Definition 12 formalizes eventual near-periodicity `d(S_n,S_{n+k})<ε` with more than one equivalence class. The paper does **not** define a probability measure on a vector space or an observable projection. Chamber XXIX verdicts are `PROTO-CLOSED` and `STRUCTURAL-COLLAPSE`; this audit does not reassign those verdicts to new physics.

## Target and independent obligations

Let `S` be the set of structural equivalence classes of a specified mechanism, `V` a finite-dimensional real inner-product measurement space, `Π:S→V` an observable map, and `W:V→[0,∞)` a structural outcome weight. Define a refinement `r:S→S` using the mechanism's symbolic rules, independent of W and of the Born rule.

- **B0 — Integrity:** phase 1/2 SHA-256 match frozen inputs.
- **B1 — Proto-closure:** demonstrate a nontrivial recurrent orbit under r with an explicit distance/equivalence and deterministic rule; fixed-point freezing does not qualify.
- **B2 — Observable bridge:** specify Π and demonstrate it is defined on equivalence classes, and state its operational meaning (not established by an arbitrary toy map).
- **B3 — Compatibility:** prove a *measure-independent* structural consequence of refinement that gives orthogonal additivity `W(u+v)=W(u)+W(v)` for `u⊥v`; do not insert that equation into the operator or call it closure.
- **B4 — Select q:** if B3 is established, show for `W_q(v)=||v||^q`, `q>0`, additivity forces q=2. This conditional lemma is known mathematics, not a new UNNS law.
- **B5 — Entanglement transfer:** only after B1–B4, define physical measurement settings, context probabilities, and complete Bell/no-signalling tests. Deferred here.

**Primary theorem status:** OPEN/BLOCKED (B2 and B3 unproved); passing code tests never upgrades this verdict.

## Proof attempt and adversarial counterexample

Take `Σ={A,B}` with deterministic rewrite `A→B`, `B→A`; let structural states be distinct singleton classes `{A}` and `{B}`; discrete metric `d(A,B)=1`. Its sequence alternates with period k=2 forever, hence d(S_n,S_{n+2})=0<ε for any 0<ε<1 and two distinct classes. This is proto-closure before numerical evaluation.

Let the *toy* observable map be `Π(A)=(1,0)`, `Π(B)=(0,1)` in `R²`. For every `q>0`, `W_q(v)=||v||^q` is invariant along the recurrent orbit (both vectors have norm 1). Yet with `u=(1,0),v=(0,1)`:

`D_q(u,v)=W_q(u+v)-W_q(u)-W_q(v)=2^(q/2)-2`.

The defect vanishes **only at q=2**, but proto-closure holds for every q. Thus proto-closure and constant weight along the orbit do **not** imply orthogonal additivity. Π is deliberately not a physically justified measurement map; this is a no-go counterexample to the bare implication.

If *orthogonal additivity* is separately assumed and `W_q(v)=||v||^q`, the above vectors give `2^(q/2)=2⇒q=2`. This is conditional and cannot be credited to UNNS without B3.

## Counterexample audit and safeguards

- A period-1 fixed point is not nontrivial closure.
- Recurrence of a symbolic orbit does not establish norm, measure, or branch-additivity conservation.
- Merely renaming orthogonal additivity to 'refinement compatibility' would be circular.
- π-dependent measurement rules, independence of settings, multipartite complexity, and complex amplitudes are outside this narrowly scoped stage.
- No modification of canonical Operator XVI, and no assumption that 'proto-closure' means Operator XVI Closure.

**Falsification condition:** Any proto-closed mechanism/observable bridge compatible with the proposed premises and with q≠2 refutes the assertion that those premises alone select the quadratic weight. The constructed alternating mechanism already refutes the unqualified assertion. The project may only advance if further independently justified assumptions exclude the countermodel.
