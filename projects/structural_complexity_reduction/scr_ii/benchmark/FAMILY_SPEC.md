# ROUTE_CSP_I — Benchmark Family

## Candidate object

An instance contains a layered binary decision route of depth `d`. A candidate is a bit string

\[
x=(x_1,\ldots,x_d), \qquad x_i\in\{0,1\},
\]

so the nominal leaf space is

\[
|S_{nominal}|=2^d.
\]

Each branch choice carries:

- a route symbol in `{A,B,C,D}`;
- a boundary phase in `{0,1,2}`;
- an integer cost;
- an integer checksum weight.

The route symbol and boundary phase are structural metadata. Cost and checksum define the independent downstream solution predicate.

## Independent exact solution predicate

A complete route is an exact solution when all of the following hold:

1. its checksum equals the instance target modulo `p=31`;
2. its accumulated cost lies inside the frozen interval `[C_min, C_max]`;
3. its terminal route layer matches the instance terminal seal bit.

The downstream solver knows only these global solution constraints. It does not use G1–G4.

## Planting rule

Every instance contains one guaranteed exact backbone solution generated from the frozen structural grammar. Arithmetic targets are derived from that backbone after structural metadata is fixed.

The generator does not forbid accidental additional exact solutions. Therefore the exact solution set must be enumerated independently. SCR-II succeeds only if the structural filter preserves **all** exact solutions, planted or accidental.

## Why the benchmark is nontrivial

The structural filter is not the downstream solver:

- the filter never evaluates the modular checksum target;
- the filter never evaluates the global cost interval;
- the filter never evaluates the terminal seal as a solution criterion;
- the solver never uses the structural grammar.

This separation makes solution preservation an empirical test rather than a tautology.
