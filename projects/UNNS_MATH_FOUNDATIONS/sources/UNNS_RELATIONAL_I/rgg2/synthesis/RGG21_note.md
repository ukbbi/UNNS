# RGG-2.1 — consolidation (2026-10-21)

RGG-1, RGG-2 files and the 43-page manuscript are unchanged (rgg2.py SHA-256 still 1923013335…085e7).
New: `rgg21.py` (14 checks pass, 2 data rows; SHA-256 9faab8cb445a70b80bb86a957d94cdb91ce569f31eb8d85380a1f95b7997225b), `rgg21_section.tex/.pdf` (4 pp, draft section, not merged).

## 1. Correction (accepted, independently confirmed)
RGG-2 note: "mixed operations stay in the fibre, so the fibre is a lattice" is **false** on d≥2.
(lcm k, gcd d) = (m/g², g) is inadmissible when g=gcd(d,d')=1: (18,2),(8,3) → (72,1); 501/2745 same-value pairs (m≤6000). (gcd k, lcm d) is always admissible and is the lub in the d-order. So F(m) is a **join-semilattice**; it is a lattice only after adjoining the formal route (m,1). RGG-2 check 9b verified the algebra but not admissibility; rgg21.py A1–A6 close that gap. Principal RGG-2 theorems unaffected.
Two bugs in my first rgg21 draft (a mis-chosen example, and Python `|` used for divisibility) were test bugs, fixed before the reported run.

## 2. Single-Probe Fibre Reconstruction [proved; checked on 7840 nonempty fibres, m≤20000]
h(m)=∏p^⌊e_p/2⌋, s_m=(m/h², h). Every d with d²|m divides h, so r∨s_m=(m/d², h) and v=m(h/d)². Hence d = h·√(m/v): one fixed probe per fibre reconstructs every route. Extension I added: any probe with h|d_s and k_s|m/h² works (probe may lie outside the fibre); sufficient only (13238/45672 probes in a 12×12 grid resolve, 1146 meet the condition). Note s_m depends on m; it is not one probe for all fibres.

## 3. Robustness [partly upgraded to proof]
Lemma: if v is strictly increasing in each coordinate and J(r,s) ≥ r,s coordinatewise, equal-value distinct routes are separated (fibres are antichains). Covers joins in (k,d), (k,N), (M,N); (M,N) join is anchor-closed since lcm N | lcm M. **Not** upgraded: the formulas T2/T4 are specific to (k,d); the single probe s_m under the other two joins resolves 693/693 fibres by check only.

## 4. Status after consolidation
Proved: order structure, join value, universal separation, weighted-L¹ metric/fibre geometry/diameter, joint covariance, distance = refinement cost, set-theoretic quotient criterion, single-probe theorem, robustness lemma.
Checked only: one-argument invariance failure counts, s_m under alternative coordinates, excess ε non-functionality (e.g. values (4,36): ε∈{1,4}).
Open: independent generative constraint selecting ∨ (this is the central open question — Lemma and robustness show the *phenomenon* is insensitive to the coordinate choice, which weakens any claim that J_join in particular is distinguished); bilinear/tropical representation; field occurrences; anything physical or entanglement-related.

## 5. Proposed next step (not started)
Merge the section into a manuscript v3 as "Nonlinear Relational Invariants…", add rgg2.py + rgg21.py to Appendix B with SHA-256s, and record the erratum. Awaiting your decision.
