# Source provenance

Reviewed **actual** user-uploaded `MUG-I_v007.zip` as independently available in this conversation's container session (not a similarly named variant). No other user release was edited.

- ZIP SHA-256: `7d0de5b1065bf1f0e9bdf976fcb9a7058486c6a25a18644acd1a06344744a2b8`
- `MUG-I_v007/verification/verify_v007.py` SHA-256: `a33175d2e857377ae736f145457ff787214d45e79c8cc4f419785caff0e6b5d8`
- `MUG-I_v007/NOTES.md` SHA-256: `6af38b224f8dfdd5be3e2c8a3a5cc7830b47d50f7272a6ebeca2886736ed0d7f`
- `MUG-I_v007/results/verification_results_v007.json` SHA-256: `565be6c5eb07a1f393783c8863b41ee77ba02a3ca22762697aba4da72aa4b8bf`

The v007 script directly defines:

```python
keep = {m: c for m, c in x.items()
        if q % N == 0 and gcd(m % q, q) % N == 0}
```

The v008 mathematical identity for this rule is proved in `theory/THEOREMS.md` and independently verified in `scripts/verify_v008.py`. No web sources are needed: claims concern the supplied model and elementary algebraic/spectral reasoning.

The numerical Maxwell check reconstructs an eigenstate *independently* from the same `q=6, delta=0.1` generalized Fourier problem. It is not represented as the original v007 raw eigenvector (the archive does not store those coefficients).
