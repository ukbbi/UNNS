# Conway Verification Source Record

Repository: `gaearon/conway-refinement`

Pinned commit:

`264445c93b78554c408e99e4e7f663693b4e91ab`

Observed during execution:
- repository `main` was identical to the pinned commit;
- GitHub Actions run `33806052174` completed successfully;
- `lake build` completed successfully with 3145 jobs;
- statement compatibility checked 51 declarations;
- axiom audit checked 13114 project declarations;
- allowed axioms were exactly `propext`, `Classical.choice`, `Quot.sound`;
- isolated-claim proof audit verified 32 claims.

External statement comparator:
L'Innocente–Mantova, *Advances in Mathematics* 442 (2024), Conjecture 1.1.1(2), states the same
four-factor refinement formula for `Oz`.

Local execution limitation:
the current container had no `lean` or `lake`, and shell Git access could not resolve `github.com`.
Therefore the independent fresh local rebuild was not executed here.
