# SCR-IV — Lean Certificate Design v001

Status: DESIGN_ONLY / NO_LEAN_PROOF / NO_NEW_PHYSICAL_RUNS
Date: 2026-10-10
Parent: SCR-III-B GAP4 frozen evidence. Additive design; no source files changed.

## 1. Exact target

For 40 spins s_i ∈ {-1,+1}, define H_K(s)=Σ_{0≤i<j<40} K_ij s_i s_j. G(s) is true when every one of the 16 frozen four-arm vertices has exactly two inward-pointing spins according to its vertex mask and plus-in mask. Define E0=min_all H_K; Ebad=min_{¬G} H_K; Δ=Ebad−E0. The two optimization targets must be certified independently.

The certificate initially concerns the exact dyadic rational values of the 780 coefficients represented by the *binary64 values actually read by the frozen solver*, not an idealized infinite-precision geometry or external empirical physics. Each coefficient will be exported as (signed numerator, power-of-two denominator) from its binary64 bit pattern. Require an explicit parser/transcript check from source text to bit pattern. A separate optional bridge can enclose geometric K by rigorous intervals; do not silently equate these interpretations.

## 2. Frozen witnesses and observed targets (NOT YET FORMALLY CERTIFIED)

Ground witness ID: 711243241830; reported H=-0.16364841082886986 A.
Non-grammar witness ID: 161487427942; reported H=-0.1534031680911189 A.
Reported gap: 0.01024524273775096 A; delta4=0.9459172223430824 kBT.
Instance SHA256: 3d47ed1256da7620292a5fe4c64e0bc226b9836768ac87df0ff4fdbf91c5f7a2.
Reported search-node counts: 700405 / 1316073. No new run is required or authorized.

## 3. Formal lemmas

L1 (energy decomposition): For a prefix p assigning spins 0…d−1, write A(p)=Σ_{i<j<d}K_ij p_i p_j and f_j(p)=Σ_{i<d}K_ij p_i, for j≥d.
L2 (global relaxation): B(p)=A(p)−Σ_{j≥d}|f_j(p)|−Σ_{d≤j<h<n}|K_jh| ≤ H_K(s) for every completion s extending p. This is an exact rational inequality; no floating-point guard is needed in the Lean verifier.
L3 (vertex feasibility): If all vertices have four assigned arms and inward count exactly two, no completion is outside G. A stronger safe filter can be proved later but must remain equivalent to / stronger justified by the actual frozen predicate.
L4 (prefix coverage): Every 40-bit state extends exactly one leaf of a finite complete binary decision tree, even when a leaf stops before depth 40.
L5 (certified minima): If a complete tree has, at every leaf, either B(p)≥U for the relevant target, a formally justified absence of eligible states, or an exact 40-spin leaf with H_K(s)≥U; and a supplied eligible witness w satisfies H_K(w)=U, then U is the target's global minimum.
L6 (gap preservation): For W≥0, target states H(s)≤E0+W lie inside G iff W<Δ, for inclusive endpoints, assuming at least one non-G state. Operational tolerance τ replaces W by W+τ.

## 4. Certificate representation

Two separate certificates: `ground.cert` (all states) and `non_grammar.cert` (only ¬G states). Each is a complete prefix tree in canonical bit order (LSB spin 0, positive spin when bit=1), represented by terminal prefix records (prefix length d, lower d spin bits, reason) or an equivalent streamed pre-order proof tree.

Termination reasons:
- `BOUND`: verifier recomputes exact B(p), requires B(p)≥U (not just an exporter claim).
- `NO_ELIGIBLE`: allowed only in non-grammar certificate; verifier proves no completion of prefix can violate the grammar.
- `FULL`: d=40; verifier checks exact H_K(s)≥U for eligible leaves; for non-grammar, grammar membership must be checked as well or eligible/ineligible leaves distinguished explicitly.

A checker verifies prefix-free, exhaustive binary coverage and all terminal obligations. It must not trust bound numbers, vertex classifications, completeness flags, C++ node counts, or reported witness energy embedded in the certificate. It must compute them.

To avoid a huge Lean proof term, implement a reflected, terminating certificate checker with a soundness theorem: `check instance certificate = true → result`. Data parsing/decoding must be within the trusted verified path or supplied as a proof of fidelity to a canonical artifact. No `sorry`, `admit`, `unsafe`, or unchecked native shortcut in the proof-critical chain.

## 5. Existing solver connection

`solver_v010.cpp` has a correct mathematical bound form and a numerical outward guard, but the stored JSONL gives only two optimal values and witnesses; it is NOT a complete proof tree. Existing shadow audit reported 1,008,197 bound prunes with no unsafe events. For formal verification, an additive *certificate exporter* must replay the deterministic branch order with exact-rational pruning (a new mathematical proof-generation computation, not a physical Hamiltonian optimization rerun), or produce a faithful record of its existing decision tree. As the frozen run had no complete decision log, a certificate cannot be extracted from the two JSON lines alone.

A rational certificate generator may take frozen witness energies as incumbent bounds, recurse over prefixes, and emit safe termination records. Its output is untrusted until checked by Lean. It must have explicit resource/time limits, and neither its traversal node count nor elapsed time can be described as a new physical result. An alternative is an instrumented deterministic trace replay whose emitted pruning decisions are then independently checked with rationals.

## 6. Incremental implementation gates

IV-0: source fingerprint and dependency lock (Lean toolchain/mathlib revision), exact data representation and witness decoding, no optimizer call.
IV-1: formalize spins, grammar and exact H; machine-check two witnesses and vertex status.
IV-2: prove L1–L4 (generic finite-state theorems).
IV-3: implement and prove a small-tree checker on 1×1/2×2 frozen public instances, without repeating physical searches.
IV-4: produce/read the two 4×4 frontier certificates and check both exact minima. If resource limits prevent checking, report INCOMPLETE rather than inferred certification.
IV-5: prove finite exclusion gap, operational tolerance boundary and the frozen R2/δ4<1 comparisons using an explicitly certified conversion bound.

## 7. Acceptance/falsification

FORMAL_CERTIFIED iff exact input encoding is bound to frozen instance, both witnesses independently verify, all frontier leaves are justified, both trees cover their search universes, and Lean checks both minima and the gap. A mismatch in any of those yields CERTIFICATE_REJECTED or NOT_YET_CERTIFIED, not a correction to the frozen record by fiat. Geometry/physical transfer, thermodynamic limit, and competitive speedup remain explicitly out of scope.

## 8. Frozen provenance and placement

Recommended additive destination: `scr_iii_b/SCR_IV_v001/` with files `DESIGN_v001.md`, future `lean-toolchain`, `lakefile.toml`, `SCRIV/*.lean`, `cert/ground.cert`, `cert/non_grammar.cert`, `RESULT_v001.md`, `MANIFEST_v001.json`. The existing `GAP4_v010/`, `GAP4_AUDIT_v001/`, `GAP4_RESULT_FREEZE_v001.md` and historical primary files stay unmodified. No GitHub changes.
