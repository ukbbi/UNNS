# SELECT-II — Context for continuation

- Parent project: `UNNS_ENTANGLE_I`.
- Prior independent completed result: `SELECT-I` (26 PASS, 4 DATA, frozen). Its mathematical conclusion is that factor preservation is an additional generative-order choice, not imposed by the nest plus T_q.
- Manuscript: Relational Invariants v3 revised, 58 pages, unchanged.
- RGG-1, RGG-2, RGG-2.1: unchanged.
- SELECT-II v001, 21 October 2026: exact self-nest *integer-value* directed graph for the deliberately chosen substitution `M := prior integer output m`, with arrows `m --N--> m*(N+1)^2/N` iff N divides m.
- Proved: all edges grow by at least 4; indegree(target) = R(target); outdegree(source) = tau(source); graph roots are precisely squarefree integers; the source and target identify the label N; 1 and 2 possess incomparable minimal common futures 81 and 100 so this order is not a join-semilattice.
- Tests: `python select2.py` -> 23 PASS + 3 DATA, deterministic, standard library only.
- Key caution: the self-substitution convention is a scoped investigation, **not** asserted to be the entirety of UNNS generative grammar. Nor is there a derivation of a unique two-input joint operation or any physical correlation.
- Next precise task: track edge-labelled histories and ask whether a defensible admissibility rule creates unique joins in selected subregimes; compare endpoint-only vs route-sensitive observation.
- All results stay local; no GitHub modification.
