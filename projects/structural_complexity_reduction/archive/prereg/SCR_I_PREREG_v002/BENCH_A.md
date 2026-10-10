# Benchmark A — mechanism-space reduction with independent viability target

For each frozen primary seed:

1. generate 40,000 candidates with the pinned P4 adversarial generator;
2. evaluate the source-equivalent viability target on the full pool;
3. evaluate G1→G4 on the full pool with early termination;
4. evaluate the same viability target on SCR survivors only;
5. compare candidate IDs and target labels exactly;
6. derive cells for N=2,500, 10,000 and 40,000 from prefixes of the frozen pool;
7. run timing and null controls without changing scientific definitions.

Baseline and SCR use the same target evaluator implementation. Filter cost is included in the SCR arm.
