# QTI-I v001 — Quantum Teleportation Induced Structures: audit, exact history theorems, QTI-I/A baseline

Research notes. No manuscript. New subfolder only; the existing QTEL v001 files (README, scripts, results, report, manifest) are untouched.
Inputs: the three *_gaps.csv files and results.json in QUANTUM_TELEPORTATION/results (read from your device). The raw .pt files are not in
the folder (data/raw holds only .gitkeep), so nothing below touches raw timestamps or channels.
Verification: verification/qti_v001.py, 15 checks, all pass (~20 s; numpy, scipy, sympy; seeded). Results file sha256 starts fb7372dd87cf.

## 1. Audit of QTEL v001 (from the CSVs, independent recomputation)
- All 18 647 analysed gaps: R, q recomputed with my own factorisation agree with the CSV columns; positive rate, mean R, max R and counts agree with results.json (A1).
- Raw gaps are all divisible by 4 and equal 312.5 × counter gap within ±4.5 units, consistent with the stated ±5 round-off of two rounded timestamps (A2).
- Not verifiable from this folder: the raw-file hashes and decoding (raw files absent), the .pt format, channel identity, and the STRUC-I / STRUC-PERC results mentioned in your summary (they are not in this folder, only QTEL v001 is). The Zenodo record page describes the three zips as raw detection files but gives no format, time-unit or channel description; the meaning of names such as iPsiM_156p45_tot is undocumented there.

## 2. Exact results
**T1 (clock lift; your statement verified).** For all positive integers d, h: every admissible history ending at d lifts to one ending at hd (same word, all states ×h), so W(d) ⊆ W(hd). Check: 5 400 pairs (d ≤ 90, h ≤ 60), inclusion holds on all. Strictness is not universal: 2 973 of the 5 400 pairs are strict, the rest equal (e.g. d=1, h=2: no incoming edge at 2 either). F(1)=1, F(4)=2 (T1b).
**T1c.** Every multiple of 4 has an incoming edge (m=2, N=1: y → 4y), so every raw gap (all ≡ 0 mod 4) has R ≥ 1. That is exactly the raw-unit "universality" found in v001, and it is the h = 4 case of T1.
**T2 (history counts, exact).** The incoming edges of d are the m ≥ 2 with m² | d, with predecessor d(m−1)/m². Hence the number of admissible histories ending at d is F(d) = 1 + Σ_{m²|d, m≥2} F(d(m−1)/m²) (empty history included), finite, and the longest history has length ≤ log₄ d because m²/(m−1) ≥ 4. Checked against brute-force forward enumeration of all histories for every d ≤ 3000 (T2, T2b).

## 3. QTI-I/A baseline: deeper history activation on the observed counter gaps
New statistics beyond one-step R: F(d) (all histories ending at d), depth, and mergers (history paths minus distinct ancestors, i.e. distinct words reaching the same earlier state).
- Observed (counter gaps): P(R>0) = 0.397 / 0.389 / 0.398 (iPsiM 156p45 / iPsiM 156p95 / iPsiP 156p45), P(depth ≥ 2) ≈ 0.18, max depth 8–10, max F up to 44 618 (heavy tail: use mean log F, not mean F).
- Control: integers drawn within ±10% of observed gap magnitudes (bootstrap, n matched). All 15 z-scores (5 statistics × 3 streams) have |z| < 2.5 (largest −2.46, P(merger) in iPsiM 156p45; no multiplicity correction) (B1).
- Clock-lift ladder on the observed gaps (h = 1,2,3,4,6,8,12,16; 1500 gaps per stream): P(R>0) and mean F are non-decreasing along every divisibility chain tested, as T1 requires; h = 4, 8, 12, 16 give P(R>0) = 1.0 (B2). Raw gaps give 1.0, raw/4 gives 0.43–0.46 (B3).
- Between-stream comparison of F distributions: KS D ≤ 0.009, p ≥ 0.97 (B4), descriptive; no channel timing used.
- Multiplicity statistics across controls (B5): the three streams sit at or slightly below nearly all controls in P(R ≥ 2) and P(merger). Pooled over streams: P(R ≥ 2) 0.1124 vs 0.1165 (z = −1.75), P(merger) 0.0741 vs 0.0776 (z = −1.79). Same direction in all three streams, but small, exploratory and uncorrected; it is a candidate to test again on new data, not a result.
**Reading.** With the clock grid corrected, deeper history statistics also look like ordinary integers. Nothing here involves the quantum protocol; it is again the geometry of gap integers. The only exact, robust structure found is the representation one (T1).

## 4. QTI-I/B: what must be defined before any state-resolved induction
The protocol objects are not integers: the teleported qubit state, the Bell-measurement outcome (4 branches, Z₂×Z₂), the Pauli correction, heralding and storage times. A UNNS-induced structure needs a declared correspondence φ with an explicit integer-valued content. Candidate definitions to be specified and compared (none chosen here):
1. Branch-count lift: φ(branch history) = number of recorded events per branch or per time bin (integer counts); T_N acts on counts.
2. Time-bin lift: φ(event) = integer clock count within a specified synchronised window (needs channel-resolved timestamps).
3. Process-matrix lift: φ(process tomography element) with integer-valued normalisation (only for the NIST teleported-CNOT dataset; not the same experiment).
4. Joint generative system (the PDF's fourth option): genuinely joint rule, which has to be defined first.
Requirements for each: the state-resolved data (not timestamps) must carry the information; entanglement or fidelity is not to be inferred from timing; controls must include a product-state/classical-correlation control and a relabelling-invariance test (analogue of T1 for the chosen content).
Not decided; I am not defining φ here, because the choice determines the whole structure.

