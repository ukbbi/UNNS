# CIB-I v001 — Comparative Induction Benchmark, first research release

**Research, not manuscript.** Purpose: make the comparative question central to `UNNS_INDUCED_STRUCTURES` by testing whether the fixed UNNS graph provides distinguishable structure when a periodic Maxwell dielectric is defined **without selecting its grating harmonics from UNNS routes**. Keep FUG-I and MUG-I baselines unchanged. No GitHub changes.

## Main result

- An exact joint Fourier-activation law for a rational-duty binary medium: for source m=tN, its UNNS step has q=t(N²+N+1), and first-order dielectric coupling is nonzero iff b does **not** divide q, where D=a/b is the reduced fill fraction.
- Infinite prime residue-class families of entirely first-order-blocked UNNS labels: p=3 gives one class; primes p≡1 mod3 give two; primes p≡2 mod3 give none.
- Across 1≤m<m'≤512, 301 original UNNS edges are compared with three fixed arithmetic-grammar controls and a **q-preserving source shuffle**. The q-preserving control matches all first-order medium metrics **exactly**, proving a limit on the diagnostic power of Fourier-shift-only statistics.
- Structural differences occur in the *induced graph* beyond one edge (2-step histories and reconvergences), but the computed differences are not equivalent to measured electromagnetic path amplitudes.
- Schrödinger and acoustic analogue operators possess the same normalized spatial Fourier coupling kernel. This is not a Maxwell-specific signal.

## Physical model

Scalar Maxwell wave eigenproblem `-E'' = omega^2 * epsilon(z) * E` on a fixed 2pi periodic domain, `epsilon(z) = 1 + eta * (indicator(0<=z<2pi D)-D)`, with small contrast eta. The same material profile is used for every arithmetic grammar in each benchmark condition. These are **analytic model profiles**, not a real laboratory sample or blind prospective test. See `theory/THEOREMS.md` and `theory/RESEARCH_LIMITS.md`.

## Reproduce on your Ubuntu terminal

Extract alongside the existing `investigations` folder or into `UNNS_INDUCED_STRUCTURES/cross_system_synthesis/COMPARATIVE_BENCHMARK/CIB_I_v001/`.

```bash
python3 scripts/run.py
python3 scripts/verify.py
python3 scripts/verify_spectral.py
python3 scripts/verify_cross_system.py
python3 scripts/prime_gate.py
python3 scripts/explore_topology.py
```

The first two and final two programs need only Python's standard library. The spectral and cross-system verification programs use NumPy (already available in the user's Ubuntu setup). Outputs are plain CSV/JSON under `results/`; scripts do not modify previous research releases.

## Scope and statuses

**PROVED**: q=t(N²+N+1) gate; binary Fourier coefficient and exact zero condition; residue-class theorem for primes; first-order q-spectrum non-identifiability; cross-equation Fourier-kernel identity.

**VERIFIED EXACT FINITE**: all 301 UNNS edges and three comparator grammars in the 512-state window, primary eight media, independent enumeration, exact controls.

**VERIFIED COMPUTATIONAL**: Fourier FFT oracle and normalized Maxwell/Schrödinger/acoustic matrix comparison.

**EXPLORATORY**: 2-step topology comparisons, prime-residue extensions beyond the original protocol scores.

**OPEN**: discrimination in independent material measurements, full-vector Maxwell dynamics, physically observed UNNS-specific advantage.

## Comparison with previous MUG-I v009

The earlier q=6,28 pump was specifically engineered from the UNNS diamond; it serves here only as a disclosed positive reference and is excluded from the primary model comparison. Its original files and lock remain unchanged.

## External scholarly context (not input measurement data)

- Photonic crystal plane-wave expansion and periodic dielectric Fourier coupling: https://www.tfp.kit.edu/files/PhysRep-444-101-2007.pdf
- Experimental synthetic photonic frequency dimensions and controlled nearest/longer-range coupling: https://www.nature.com/articles/s41467-019-11117-9
- Bloch/Fourier representations across photonic, electronic and phononic crystals: https://www.sciencedirect.com/science/article/pii/S0165212513000036

These references ground the ordinary physical selection framework; none is claimed to independently detect UNNS.
