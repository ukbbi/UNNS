# ATL-08: The mechanism at one third

## Mathematical object

The singularity of $G_k$ at $s=1/3$, produced by primes shared between an earlier letter through $N+1$ and a later letter through $N$.

## Established structure: depth three

- An exact decomposition expresses $G_3$ through a shifted series $V$, a remainder $R$ and $G_2$ (T46d). Models of one linked letter have only a simple pole at $1/3$ (T46c, T46f).
- Square-divisor identities (T46g) lead to the continuation of the remainder (T46h, T46i), whose first component has a natural boundary at $\operatorname{Re}s=0$ (T46h-i). A theorem on shifted series (T46j) then gives the continuation and residue of $V$ (T46e); positivity of its constants was proved in advance (T46e-i).
- $G_3$ has a pole of order **exactly two** at $1/3$, with an explicit leading coefficient near $-0.75916$ (T46k); the continuation reaches $\operatorname{Re}s>1/3-1/200$ (T46k-i), and smoothed counts have a second term of size $X^{1/3}\log X$ (T46l).

## Established structure: arbitrary depth

- For every $k\ge2$, on $\operatorname{Re}s>1/2$, $G_k$ decomposes by its end letters into a weighted middle-word sum $M_k$, a remainder and $G_{k-1}$ (T46m). Overlaps in the weight obey an exact identity (T46r).
- At one prime at most $\lfloor k^2/4\rfloor$ links can be active (T46n). A model with $r$ supplying and $t$ receiving letters has a pole of order exactly $rt$ (T46o).
- For a role pattern $R$ the local expectation is $1+L(R)/p+O(p^{-4/3})$, where $L(R)$ counts links; the resulting formula reproduces the proved leading coefficients at $k=2,3$ and in the model (T46s).
- Stated conditions on $M_k$, the remainder and $G_{k-1}$ would imply the pole order at depth $k$ (T46p). They are not established for any $k\ge4$.

## What it reveals

Under the role-pattern measure, each eligible supplier-to-receiver link contributes to the first-order coefficient $L(R)/p$ of the local expectation. The maximal link count is attained by a balanced complete bipartite pattern, with all suppliers preceding all receivers. This mechanism reproduces the proved singularities at depths two and three and in the comparison model. Its extension to the full history series at arbitrary depth remains conjectural.

## Further structure

Three statements of different strength are kept apart:

| Identifier | Content | Proved |
|----------------|----------------------------------------------------|--------------|
| T46b | $G_k$ has a pole at $1/3$ of order $\lfloor k^2/4\rfloor$ | $k=2,3$ |
| T46q | $M_k$ has a pole of order exactly $\lfloor k^2/4\rfloor-1$ | $k=2,3$ |
| T46t | Continuation near $1/3$, pole order $\lfloor k^2/4\rfloor$ and the leading coefficient | $k=2,3$ |

In the second row, order zero at $k=2$ denotes regularity, not a pole: $M_2=1$ is regular and nonzero at $\frac13$.

## Open boundary

Depth four and beyond at and past $\operatorname{Re}s=1/3$, and depth three further left (ANS-T46); singularities and natural boundaries at higher depth (ANS-T46a). ANS-I v014 records that no viable route to the continuation of $G_4$ past $\frac13$ has been established.

## Reading across (interpretation)

The quadratic growth of the conjectured order with depth is a candidate point of contact with generative geometry. Models are not the functions $G_k$.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T46k | Depth three: pole of order exactly two at 1/3 | PROVED | V |
| ANS-T46m | Every depth: decomposition by end letters | PROVED | V |
| ANS-T46s | Role patterns: local expectation and agreement with proved coefficients | PROVED | V |
| ANS-T46b | Pole of order floor(k^2/4) at 1/3 | PROVED for k <= 3; CONJECTURE for k >= 4 | V |
| ANS-T46q | Weighted middle-word sum: pole order floor(k^2/4)-1 | CONJECTURE (k = 2, 3 proved) | N |
| ANS-T46t | General continuation, pole order floor(k^2/4) and leading coefficient at 1/3 | CONJECTURE (k = 2, 3 proved) | N |

## Recorded open questions

- **ANS-T46:** Depth k >= 4 at and beyond Re s = 1/3; depth three further to the left.
- **ANS-T46a:** Singularities and natural boundaries at higher depth.

## Connected entries (cited dependencies)

- **Uses ATL-01** (Exact admissible composition): ANS-T03, ANS-T47.
- **Uses ATL-06** (Fixed-depth singularity architecture): ANS-T12, ANS-T34.
- **Uses ATL-07** (Depth two: an arithmetic singularity hierarchy): ANS-T45, ANS-T45a.

## Review boundary

Without a review verdict: ANS-T46q (N), ANS-T46t (N).

Qualified verdicts:

- ANS-T46h-i: A normal-convergence clarification was requested and added in ANS-I v013.
- ANS-T46j: Two scope clarifications were requested and made in ANS-I v013.

## All results and proof sources

- **ANS-I v010:** ANS-T46c.
- **ANS-I v011:** ANS-T46f, ANS-T46d, ANS-T46e-i.
- **ANS-I v012:** ANS-T46g, ANS-T46h, ANS-T46h-i, ANS-T46i, ANS-T46j, ANS-T46e, ANS-T46k, ANS-T46l.
- **ANS-I v013:** ANS-T46k-i, ANS-T46m, ANS-T46n, ANS-T46o, ANS-T46p, ANS-T46q.
- **ANS-I v014:** ANS-T46r, ANS-T46s.
- **ANS-I v009:** ANS-T46b.
- **ANS-I v015:** ANS-T46t.
