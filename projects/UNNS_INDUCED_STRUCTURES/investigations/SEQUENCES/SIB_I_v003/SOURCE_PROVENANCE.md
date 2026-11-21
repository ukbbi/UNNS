# Provenance

The user proposed this investigation after independently validating SIB-I v002.
The fixed grammar, incoming-fibre identity, source-versus-observation distinction,
and all-depth finite-domain method are inherited from the existing project and
SIB-I v001/v002. Neither earlier release is modified.

This release contains new standard-library Python implementations of recursive
signature interning and source/content propagation. It compares them with complete
ordered-word forward propagation and a separately implemented backward recursion
that tests all square divisors. No external data or new web sources are required.

Exploratory searches first examined 1..4096, then 1..65536. The published census
is the latter complete domain. Selected counterexamples are discovery results,
not held-out confirmations. All comparison groups and selected examples can be
reconstructed from the exported membership tables and exact signature definitions.

The observed success of E3 and Efull on the census is explicitly finite evidence.
The exact recurrence proofs are independent of that success. Baseline ZIP hashes
are recorded in MANIFEST.json; local baseline contents were checked unchanged.
