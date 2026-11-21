# SIB-I v001 — Sequence Induction Benchmark

Date: 2026-11-21. Status: exact bounded-depth computational investigation.
Intended project location: investigations/SEQUENCES/SIB_I_v001/.

Run with Python 3.10 or later; standard library only:

    python scripts/run_sib.py
    python scripts/verify_sib.py

Windows users can double-click RUN_SIB.bat. Read reports/RESULTS.md afterwards.

## Frozen scope

The unchanged continuation is T_N(s)=s(N+1)^2/N, N divides s, s,N positive integers.
Observed terms retain their original index and duplicates. Ambient ancestry may leave
the external support. This is distinct from the graph restricted to support values.

| Family | Index range / cutoff | Convention |
|---|---|---|
| Lucas | 0..83 (84 terms) | L0=2, L1=1, L(n+2)=L(n+1)+L(n) |
| Primes | 1..84 | Increasing positive primes |
| Totient | 1..84 | phi(n) counts 1<=k<=n with gcd(k,n)=1 |
| Powers of two | k>=0, at most 84 terms, 2^k<=10^18 | 60 terms |
| Catalan | n=0..29, C(n)<=10^18 | binomial(2n,n)/(n+1); 30 terms |
| Sylvester | n>=0, at most 8 terms, s(n)<=10^18 | s0=2, s(n+1)=s(n)^2-s(n)+1; 7 terms |

All original values lie below 10^18. Controls lie below 2^60 plus small offsets;
all factorizations are in the deterministic unsigned-64-bit primality domain.
Cutoffs and control seed were fixed before executing the benchmark.

## Metrics and exactness

Incoming edges enumerate d>=2 with d^2 dividing x; predecessor s=x(d-1)/d^2,
label N=d-1. Recursion enumerates ALL positive-length histories of lengths 1,2,3.
Each route is a source integer and an ordered forward label word. Every route
ends at the reported target; distinct endpoints therefore mean distinct sources.
Common-source pairs with identical label multisets are permutation mergers;
different multisets are different-content mergers. Mixed route lengths are included.
Counts of common-source pairs, source groups and target occurrences remain separate.

The minimal ambient positive route length is 1 whenever any route exists.
Longer-length activation is reported separately. Depth 3 is a scope boundary,
not a claim to enumerate unrestricted ancestry. Since T_N(s)>=4s, depth is
globally finite for a fixed target, bounded by floor(log_4(x)).

Repeated external observations do not create additional arithmetic histories.
Both occurrence-weighted and unique-support summaries are supplied.
Transport records compare consecutive external indices only; divisibility-based
homogeneous transport is justified in REGISTER.md.

## Controls

Eight reproducible replicates: nearby integer offsets, per-term bit-length-matched
uniform draws with replacement, sorted versions of those draws, and value-preserving
order scrambles. One cyclic shift checks the effect of the chosen start index.
These controls preserve different properties and are not interchangeable null models.
Order scrambles leave marginal profiles unchanged by construction; only chronology
and adjacency diagnostics may change. Cyclic shift preserves all cyclic adjacencies,
but the linear sequence omits a different boundary edge.
Alternative grammars y=2s and y=3s provide explicit one-step divisibility baselines;
they are not complete depth-3 alternative-grammar comparisons.

No fitted thresholds, significance tests or broad family rankings are asserted.
Full-depth mergers, arbitrary source-locked delayed activation, unbounded merger multiplicities,
and further sequence classes are follow-up investigations.

## Outputs

Data CSVs retain external indices. Per-family reports contain all target metrics.
summary.json contains activation indices and both weighting conventions.
witnesses.csv contains one common-source merger witness per active target occurrence.
controls.csv retains every replicate; transport.csv retains adjacency diagnostics.
input_factors.csv records input factorizations. Verification uses an independent
forward enumeration on small integers and replays exported merger witnesses.

This release is separate from FUG-I, MUG-I and QTI-I. Existing project files and
frozen source packages are unchanged. Root register integration is pending installation.

An explicit infinite powers-of-two merger family is proved in REGISTER.md SIB-07.
