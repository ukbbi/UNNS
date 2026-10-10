# UPI Integration in SCR

## Status

**SCR-I role:** secondary diagnostic  
**Pruning status:** disabled

## Foundational scalar

The supplied UPI note defines:

```text
UPI = (D * R) / (M + S)
```

with recursive depth and self-reference acting as amplifying terms, and morphism divergence plus memory saturation acting as stabilizing terms.

The note treats UPI as a diagnostic of instability susceptibility rather than proof of paradox.

## SCR-I use

UPI is computed without access to the primary SCR rejection decision whenever the required variables are available.

After primary results are frozen, compare:

```text
UPI(rejected)
UPI(surviving)
P(reject | UPI band)
P(survive | UPI band)
```

## Why UPI does not prune in SCR-I

If SCR rejects candidates because UPI is high and then reports that rejected candidates have high UPI, the result is circular.

SCR-I therefore treats UPI as a blinded explanatory variable.

## Later promotion criterion

A future SCR version may test UPI as a pruning/allocation rule only if:

1. UPI predicts rejection or costly failure out-of-sample;
2. conditioned intervention preserves solutions;
3. a rate-matched random filter performs worse;
4. UPI computation cost is included;
5. thresholds are frozen before the confirmatory run.

## Possible future use

Rather than binary pruning, UPI may eventually support adaptive resource allocation:

```text
low UPI      → inexpensive/coarse evaluation
intermediate → additional refinement
high UPI     → intensified admissibility audit
```

This remains a future hypothesis, not part of SCR-I primary filtering.
