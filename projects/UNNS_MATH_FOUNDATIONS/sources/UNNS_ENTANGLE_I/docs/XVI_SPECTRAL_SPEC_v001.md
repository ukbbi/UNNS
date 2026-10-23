# XVI_SPECTRAL_CONDITIONING_v001 — Source-Locked Protocol

**Scope:** numerical reliability of the original Chamber XVI spectrum diagnostic; not a repair to canonical code, new dynamics, a new invariant, or a quantum-measure theorem.

## Source and negative baseline

The original HTML `docs/sources/XVI_ENGINE_v084.html` is immutable. Its SHA-256 is verified. The supplied `XVI_INVARIANTS_AUDIT_v001.json` is frozen, byte-identical, at `docs/frozen/XVI_INVARIANTS_AUDIT_v001.json` and verified before execution. Its `INVARIANT_FIDELITY_NOT_CERTIFIED` verdict and `NOT_DERIVED` Born rule must stay in force. Four historical Chamber exports contain metrics only and cannot be reconstructed at the raw-field level.

## Original source formulas — reproduced, not improved

The original `TauFieldEngineN.captureSpectrum()` computes `kappa=computeLaplacian(0)` (FFT Laplacian), `FFT(kappa)`, individual Fourier powers, and radial bins `floor(sqrt(kx²+ky²))`, ignoring k=0 and bins k≥N/2. It averages each bin's power and fits **every** nonempty bin on log(k), log(Pk), reporting p=-slope and R². No power floor appears in the original fit. Canonical source validation targets +2.28 ±0.05 in strict mode; older actual exports report negative slopes. Never flip sign to force agreement.

## Reproducible source-executed raw fields

`tools/xvi_spectral_source_probe_v001.cjs` reads the class directly from the original HTML into a VM with its original functions, without patching that source. It creates **new** random-initialized N=64/128, seed=41 fields at step=0 and step=24, with sigma and anneal_sigma set to zero after construction, and stores full τ arrays and native JavaScript k/Pk/p/R² values at `output/XVI_SPECTRAL_SOURCE_RAW_v001.json`. These are **not** the historical export fields. The included witness is frozen with the original source SHA. Python uses exactly these same numeric arrays.

## Predeclared conditioned diagnostic (not canonical)

For the *separate* robust fit, restrict k to 2..floor(N/4), remove bins whose mean power is less than 10⁻¹² of the peak in that interval, require ≥8 supported bins, ≥1 octave, ≥80% supported bins within the fixed fit window, and largest supported-bin mass ≤90% of the total supported power. A recognizable power-law fit additionally requires R²≥0.95. No reweighting or retuning of source spectra is permitted. Candidate sensitivity windows: k=2..N/4, k=3..N/3, k=4..N/4, with floors 10⁻⁸/10⁻¹⁰/10⁻¹²/10⁻¹⁴. Those are *sensitivity diagnostics*, not an opportunity to choose the most favorable fit.

## Controls

A broad Fourier power-law field with **deliberately programmed** κ-spectrum p≈+2.28 tests the estimator's ability to recover a known signal; narrowband fields test rejection of unsupported fits; white-noise fields test the k⁴ effect of the source Laplacian (which naturally produces p≈−4 even without structural physics). A separate fixed-seed additive-noise stress study tests levels 0, 10⁻¹², 10⁻⁹ times initial field standard deviation.

## Frozen gates

- **P0:** input source and exact negative report locks pass.
- **P1:** original JS engine (not reconstructed Python evolution) produced new raw τ fields.
- **P2:** source-JS original all-bin fit matches Python on *same new field* to |Δp|, |ΔR²| < 10⁻⁸.
- **P3:** fixed-policy conditioned p matches JS/Python to relative 10⁻⁸ on shared fields.
- **P4:** numerical support/reliability audit passes/fails independent of source p target.
- **P4b:** source **+2.28 ±0.05** target, separately recorded: failed values cannot be reinterpreted as passes.
- **P5:** known-positive and negative controls executed and verdicts preserved.
- **P6:** historical export reproduction remains BLOCKED without its original raw arrays.
- **P7:** quantum probability is NOT DERIVED.

A numerical PASS for spectral parity or sufficient support is **not** a discovery of an invariant. The original failed Phase XVI invariant verdict cannot be revised by this audit. Quantitative original-engine results use one seed (41) at two grids and two steps; the synthetic controls use an independent deterministic seed (20261021). A later investigation would require more source seeds, physical conditions, and full field exports for historical runs.
