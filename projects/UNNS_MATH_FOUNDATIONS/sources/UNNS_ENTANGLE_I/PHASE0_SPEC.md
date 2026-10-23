# UNNS Entanglement I — Phase 0 Preregistration and Theorem Specification

Version 0.1.0; frozen initial protocol, 2026-10-20. The tests do NOT establish an independent UNNS derivation.

## Research target
Determine whether a substrate-defined closure and projection principle uniquely select quadratic structural weight (`q=2`) **without postulating** an inner-product norm, Born weights, or a quantum singlet state. The q-family is a diagnostic stress test, not a UNNS prediction.

## Frozen mathematical family
Let `Delta=a-b`, and let the four standard antisymmetric two-rebit projection amplitudes have two magnitudes `|sin Delta|/sqrt(2)` and two `|cos Delta|/sqrt(2)`. For `q>0` set `w_xy=|A_xy|^q`, `Z_q=sum_xy w_xy`, and `P_q=w_xy/Z_q`.

`P(++ )=P(--)= |sin Delta|^q/[2(|sin Delta|^q+|cos Delta|^q)]`, `P(+-)=P(-+)= |cos Delta|^q/[2(|sin Delta|^q+|cos Delta|^q)]`.

`E_q(Delta)=(|sin Delta|^q-|cos Delta|^q)/(|sin Delta|^q+|cos Delta|^q)`. No-signalling: all local outcome marginals equal `1/2` for all q and all settings. This property does NOT select q=2.

Total unnormalized weight `Z_q(Delta)=2^(1-q/2)(|sin Delta|^q+|cos Delta|^q)`. `Z_q` is independent of `Delta` **iff** `q=2` (evaluate 0 and pi/4); this is a mathematical consequence of the chosen amplitudes, not a substrate derivation.

## Bell locality and independence assumptions
Bell-local causality: there exists an outcome-independent hidden-variable distribution `rho(lambda)` and local response factors satisfying `P(x,y|a,b)=int rho(lambda) P_A(x|a,lambda) P_B(y|b,lambda) d(lambda)`. Measurement independence: `rho(lambda|a,b)=rho(lambda)`. Operational no-signalling: `P_A(x|a,b)=P_A(x|a,b')`, similarly at B. A violation of CHSH under the usual assumptions excludes their conjunction, not necessarily relativistic causality.

**Precise status:** the conditional shared-state model violates Bell factorizability if measurement independence is retained. This describes its probability representation, not an established underlying mechanism. No superluminal influence is postulated, but an ontological explanation is unresolved. The model must not evade Bell by implicit setting-dependent sampling, detection postselection, or superdeterministic assignment without declaration.

## Settings and tests
Fixed CHSH: `(a,a',b,b')=(0, pi/4, pi/8, -pi/8)`; `S=|E(a,b)+E(a,b')+E(a',b)-E(a',b')|`.
Fixed-angle formula `S_q=4(1-t^q)/(1+t^q)`, `t=tan(pi/8)=sqrt(2)-1`, with threshold `q*=ln(3)/ln(1+sqrt(2))` for S=2. This fixed-angle threshold is NOT claimed to be the global one.

Numerically optimize `S` over `a',b,b' in [0,pi)`, fixing `a=0` by global rotational invariance. Differential evolution seed 20261020, maxiter=500, population multiplier 18, tol=1e-11, atol=1e-12, polishing on. These searches only give numerical **lower bounds** on the global maximum; they do not prove Tsirelson compliance for any q.

### Four gates and how each maps to proposed operators
1. **NS (no-signalling):** exact all-setting marginal independence. Candidate: XVI global closure / XXI tau-MSC stable joint assignment. In this q-family NS holds for every q, so it cannot select q.
2. **BV (Bell violation):** find valid independent settings and `S>2`. Candidate: XIII Interlace proposes structural nonseparability; it must supply a joint law not reducible to measurement-independent Bell-local factorization. Failure to do so falsifies that account.
3. **TC (Tsirelson compliance):** prove `max_{a,a',b,b'} S <= 2sqrt(2)` for the complete modeled physical setting domain. Candidate: XVI Closure and XXVIII Consistency Engine must establish an admissible bound, not simply reject outcomes based on known QM.
4. **SN (setting-independent unnormalized weight):** derive `Z_q` constant from the generator's measure-preserving recursion, before choosing q. Candidate: XVI Closure, XIV Phi-Scale, XXI tau-MSC. For this fixed amplitude family, SN forces q=2 immediately. Independence of SN from q=2 must be justified, otherwise the argument is circular.

These are proposed operator responsibilities, **not** established features or theorems of those operators. Global invariance of *normalized* probability (`sum P=1`) is automatic for all q and must not be confused with SN.

## Acceptance / falsification gates
- **P0-A implementation PASS:** unit tests pass, numerical fixed-angle values match closed form within `1e-9`, q=2 exactly reaches 2sqrt(2) to `1e-9`, and numerical marginals deviate by at most `1e-12`.
- **P0-B mathematical q-window PASS:** give an analytical proof of NS and SN uniqueness, and independently certified **global** CHSH bounds/thresholds on declared setting domain. Numerical optimizers alone cannot pass the global certification gate.
- **P0-C UNNS derivation PASS:** present a separately frozen explicit UNNS recursive generator, a theorem showing why it yields the antisymmetric state and setting-preserved total weight, and an independent proof of q=2 **without importing** squared-amplitude or Hilbert norm axioms. If those principles are assumptions, report `RECONSTRUCTION`, not `DERIVED`.
- **P0-D physical consistency PASS:** define source independence and its operational meaning, extend the formalism to phase-sensitive complex or equivalent structures and independent-source network tests, and compare predictions against experimental data. A two-rebit CHSH fit is insufficient.
- **Falsification:** observed `S>2sqrt(2)` in model predictions fails TC; context-dependent marginals fail NS; nonconstant `Z_q` fails SN; any derivation silently inserting q=2/Born weights fails P0-C. A model that is Bell-local plus measurement-independent cannot pass BV.

No fitting on benchmark data before freezing the generator. Keep frozen outputs immutable when advancing versions.

## Real versus complex structural models
Renou et al. (Nature 2021, DOI:10.1038/s41586-021-04160-4) derived a network test distinguishing conventional real Hilbert-space theory under independent-source assumptions from complex QT. 2022 photonic network experiments (PRL 128 040402; PRL 129 140401) reported violations of real-theory constraints. A March 2026 preprint by Hoffreumon and Woods (arXiv:2603.19208) argues the distinction relies on product-state independence rather than operational independence, and claims equivalence under the latter. Treat this dispute and the source-independence definition as open review requirements; do not make unconditional claims that real-number descriptions are excluded.

## References
- https://doi.org/10.1038/s41586-021-04160-4
- https://doi.org/10.1103/PhysRevLett.128.040402
- https://doi.org/10.1103/PhysRevLett.129.140401
- https://arxiv.org/abs/2603.19208
