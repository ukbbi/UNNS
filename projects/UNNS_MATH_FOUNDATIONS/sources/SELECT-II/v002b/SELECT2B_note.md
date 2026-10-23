# SELECT-II v002 — exact reachability, complete histories, history-sensitive tests (2026-10-21)

SELECT-I, SELECT-II v001 (select2.py), manuscript v3 and RGG files are unchanged.
Verifier `select2b.py` (stdlib only): 15 checks pass, 0 fail, 8 data rows (`select2b_output.txt`); SHA-256 at the end.
Labels: proved / checked (exact finite) / data / open.

## Track A — exact reachability
- Backward recurrence m ~> t iff m=t or some p in P(t) has m ~> p [proved: your argument]. Terminates because p <= t/4, so every path m ~> t has at most floor(log_4(t/m)) edges. Checked against forward search on all 1,125,750 pairs 1<=m<=t<=1500, plus 60 random pairs with t up to 10^5.
- **No shortcuts (new, proved).** If p -> t is an edge, t is not reachable from p by any path of two or more edges. Proof: write phi(d)=d^2/(d-1) (lowest terms), so an edge multiplies by phi(d). A path of j>=2 edges to the same t needs phi(d)=prod phi(d_i). Since gcd(d^2,d-1)=1, d | prod d_i and (d-1) | prod(d_i-1); put prod d_i = d a, prod(d_i-1) = (d-1)b, then b=a^2. Then prod d_i - prod(d_i-1) = a(d-(d-1)a). For a>=2 the right side is <=0, but the left side is >0; for a=1 the left side is 1, but for j>=2 it is >=3. Contradiction. Checked: p<3000, t<=10^6; phi-product equations have no solutions for d_i<400 (two factors), <60 (three).
  Consequences: every edge is a cover relation (the graph is the Hasse diagram of the reachability order); the predecessors of any t form an antichain; every confluence is minimal.
- Not graded: 6 ~> 784 has paths of length 2 and 3. So path length is not a rank function.

## Track B — complete histories
- H(t) recurrence confirmed against explicit path enumeration (t<=3000); H(72)=4 (1-4-18-72, 1-4-16-72, 3-16-72, 10-72) versus R(72)=3.
- H(t) >= max(1,R(t)), and for non-sources H(t)=R(t) iff every predecessor has exactly one history. Data (t<=20000): 7840 non-sources, H>R for 1309 of them, smallest t=64 (not 72), maximum H=275 at t=16200.
- Histories of one endpoint can have different lengths (t=16: 3-16 and 1-4-16); this occurs for 2306 of the endpoints up to 20000.
- Route does not determine history: route (8,3) in F(72) comes from predecessor 16, which has two histories. 346 routes with t<=3000 have a predecessor with >=2 histories. So the tower value -> route -> history is strict at each level (data up to 5000: 5000 values, 3124 routes, 8283 histories).

## Track C — history-sensitive relational tests
1. **Markov no-go (proved; implementation checked).** Continuations of a history depend only on its endpoint; verified on every endpoint t<400 with >=2 histories (44 endpoints, depth 3). Hence every joint operation defined by extension, with the merge endpoint as observation, depends on endpoints only: the Theorem 11.9 criterion holds trivially and the set deficit is 0. A route or history can therefore never be told apart by continuation in this graph. History enters only retrospectively.
2. **J_pred leaks.** J_pred(r,s)=Min(Desc(p(r)) ∩ Desc(p(s))): for a probe r, J_pred(r,r)={p} equals J_pred(s,r) iff s's predecessor reaches p. By the antichain property this never happens, so J_pred separates every fibre pair (1277/1277, t<=3000) automatically. That is leakage (the inputs differ), not continuation information; it is not evidence for relational structure.
3. **Intrinsic confluence test (data).** For routes r,r' in F(t) with predecessors p,p': t is always a minimal common successor of p,p' (proved, 1277/1277). A second incomparable minimal merge below t exists for 9/1277 pairs, e.g. t=784 (routes (16,7),(1,28)) with minimal merges {432,784}; t=1089 ((9,11),(1,33)): {648,1089}; t=1568 ((32,7),(2,28)): {864,1568}. So the intrinsic order sees almost no route distinction; whether the 9 exceptional pairs have a pattern (in the three shown, d'=4d or 3d with d=7 or 11; a pattern from three examples only) is open and untested.

## Verdict
The only intrinsic route/history information in the nest graph is retrospective (ancestry, merge structure), and forward continuation never exposes it. A history-sensitive relational operation therefore needs a backward-reading definition, and then the separation of routes is driven by predecessors differing, which the test above shows is automatic. No relational deficit arises from the intrinsic dynamics.

## Open
1. Closed-form (number-theoretic) criterion for m ~> t; only a recursive one exists.
2. The pattern of the 9 double-confluence pairs, and larger-range counts.
3. Whether any natural retrospective invariant (merge geometry, common-ancestor structure) is non-trivially related to D from the manuscript; v001 found no relation via the join value.
4. Nothing here bears on physics or entanglement.
25a23f7144bb3c1b03a83cfb65972d07b2de66daacddfe9a669ce5ec3ae9fd71  select2b.py
f804fe3e60c28c05601706d53c1b2642860202aa61a0c2a144ec9e42c36191cc  select2b_output.txt
