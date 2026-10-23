# SELECT-II — Intrinsic Generative Reachability (first results, 2026-10-21)

Graph G: vertices = positive integers m; edges m -> m(N+1)^2/N for N | m (direct nest self-iteration, integer successors only).
No joint operation is assumed. Manuscript v3, RGG-1/2/2.1 and SELECT-I are untouched.
Verifier `select2.py` (stdlib only, <1 s): 12 checks pass, 0 fail, 3 data rows; output `select2_output.txt`.
Labels: proved / checked (exact finite) / data / open.

## Your claims, verified
- In-degree of t equals R(t) [proved, checked t<=20000]: representations t=kd^2 (d>=2) give predecessors m=k(d-1), N=d-1. Distinct d give distinct m because t/m = d+1+1/(d-1) is strictly increasing in d.
- The four paths to 81 and 100 are valid; common successors of 1 and 2 up to 100 are exactly {81,100}; neither reaches the other (each step multiplies by (N+1)^2/N >= 4). So no least common successor exists [proved for this pair].

## Additional exact structure [proved; checked]
1. **An occurrence is an edge.** The generated occurrence (M,N), N|M, is the edge M -> M(+)N; the anchor route (k,d) in F(t) is the incoming edge from m=k(d-1) with N=d-1. The nest-fibre multiplicity is in-degree; route-level distinctness within a value fibre is distinctness of predecessors (checked t<=5000).
2. Out-degree of m is tau(m) (distinct N give distinct successors). Step factor is (N+1)^2/N = N+2+1/N >= 4, equal to 4 only for N=1: the graph is acyclic with no sinks, and predecessors satisfy 4p <= t, so ancestor chains have length <= log_4 t.
3. Sources (no incoming edge) are exactly the squarefree integers (checked t<=20000; follows from R(t)=0 iff squarefree).

## Join and meet both fail [proved for examples; counts checked]
- Joins: 1 and 2 have 21 minimal common successors <= 20000 (all globally minimal, since anything smaller is also <= 20000): 81, 100, 162, 200, 256, 512, ... Among pairs 1<=a<b<=40: 23 comparable, 702 with >= 2 minimal common successors (certified no join), 40 with exactly one minimal found (not certified as least), 15 with none <= 20000 (truncation unknown).
- Meets are decidable exactly (ancestor sets are finite). Pairs 2<=a<b<400: 374 comparable, 77916 with no common ancestor, 660 with a unique maximal one, 53 with >= 2 maximal (e.g. (32,300): maximal common ancestors exactly {2,6}). So the order is neither a join- nor a meet-semilattice.
- Relation to RGG-2: the manuscript's join value v(r v r') = t(L/g)^2 is not a successor-order object in general: for 112 tested fibre pairs (t<400) it is reachable from t in 72 cases and a common successor of both predecessors in 76. J_join is not recovered from intrinsic reachability. This is data, not a theorem about all fibres.

## What follows
- Under the intrinsic order, "least common continuation" is not available as a single-valued operation. The natural intrinsic object is set-valued: Min C(a,b), the antichain of minimal common successors (large: 21 elements for (1,2)). Theorem 11.9 of the manuscript is formulated for set-valued J, so the quotient machinery still applies; this is an open computation, not done here.
- Neither J_join nor J_ref is intrinsic to the nest graph. Whether any single-valued joint operation is justified by the graph is open; the evidence so far (non-join, non-meet) says it would need an additional selection principle, in line with SELECT-I.

## Open for SELECT-II
1. Characterise the reachability order m ⇝ t (necessary and sufficient conditions); only structure above is proved.
2. Compute Min C(a,b) systematically; does its image under value or route-history separate fibre routes, i.e. does the intrinsic set-valued joint continuation give a relational deficit?
3. Whether the predecessor structure of a fibre (common ancestry of p, p' for r, r' in F(t)) carries an intrinsic distance, and how it relates to D (tested only through D2, no relation found).
4. Nothing here bears on physics or entanglement.

SHA-256: select2.py 3c485a972ea63d4055023a95f6c1cce13e7676ce848103f591a6bb901148e9a0; select2_output.txt 7ae4a07cb6ddfe6b13c81b3c9e10ea3fbe42529b979d227d6285158545c098f4
