# Benchmark A — Basin-Preserving Mechanism-Space Reduction

The benchmark uses the same frozen mechanism domain as v002 and the LIII P4 source.

For each primary seed a 40,000-candidate adversarial pool is generated once. Prefixes of 2,500 and 10,000 provide the smaller preregistered sizes.

The baseline arm evaluates the independent viability oracle on all candidates and clusters target-positive mechanisms. The SCR arm evaluates G1→G4 first, then applies the *same* viability oracle only to survivors.

The computational question is therefore not whether candidate identities survive, but whether the **structure of the viable target space** survives after upstream pruning.
