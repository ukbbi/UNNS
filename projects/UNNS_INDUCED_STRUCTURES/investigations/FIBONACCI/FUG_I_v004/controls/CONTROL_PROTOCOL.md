# Activation controls (descriptive)

For each of Fibonacci, Lucas, and `F_n+1` over indices 1..84:

1. Independently build the *full* finite set of admissible positive-label histories for each indexed value using exact integer inverses.
2. On each of the 307 index pairs `(m,n)` where `m|n` and `m<n`, test whether every history present at the earlier value remains present at the later one.
3. For every distinct observed nonempty word, take its first observed index z and test whether the set of observed indices is exactly the positive multiples of z within 1..84.
4. Preserve index identities for duplicate observed values (`F1=F2=1`, and shifted Fibonacci gives two early 2s).

These are **not** null models matched on size, factorization, or square-divisor composition. Failure of Lucas or shifted-Fibonacci to show Fibonacci's index-periodic word appearances is compatible with classical differences in their divisibility structure. The controls neither prove nor disprove exceptional physical UNNS effects.

Primary results in `results/control_activation_84.json`.
