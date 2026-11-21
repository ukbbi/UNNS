# Arithmetic controls — Phase 3

The exact same full-depth history and merger census is applied to 84 indexed observations for each input sequence:

- Fibonacci `F_n`, `F_1=1,F_2=1`;
- Lucas `L_n`, `L_0=2,L_1=1`;
- Shifted Fibonacci `F_n+1`.

Indices are distinct even when two successive observations have equal values (for example, the shifted sequence has the same value at indices 1 and 2).

The controls are **illustrative arithmetic controls**, not a matched null distribution, randomized significance test, or claim of a quantum/physical phenomenon. The values have different size ranges, prime-factor structures and divisibility patterns. `results/controls_phase3.json` records computed outcomes, and the independent verifier recomputes them.

The presence of content-kernel mergers in shifted Fibonacci rules out a uniqueness claim for the property itself. In this finite window the shifted Fibonacci sequence has MORE different-content merger pairs than Fibonacci. The Fibonacci-specific theorem concerns the F72 arithmetic witness and infinite index-multiple transport, not statistical exceptionality.

Next recommended controls: factorization-matched integer substitutions, randomized index-order versus value-preserving controls (for questions about index-incidence), and nulls preserving square-divisor signatures. Keep the value-level and indexed-pair counting protocols separate.
