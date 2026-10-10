# SCR-IV IV-4A — Certificate design and feasibility (no 4×4 certificate generated)

## 1. Goal
Certify, in the Lean kernel, `ObjAll claimedGroundNum` and `ObjNonGrammar claimedNonGNum`: each value is attained (IV-2 witness) and is a lower bound for every valid configuration. IV-4A defines the certificate and the checker, proves the checker sound, and measures cost. IV-4B (generation + verification) is NOT started.

## 2. Certificate format (proof tree over the fixed branching order; spin d is assigned at depth d)
Pre-order, 2 bits per node, packed in one natural number with a sentinel bit `1` after the last token (so truncation and trailing junk are both rejected):
| token | meaning | checker obligation |
|---|---|---|
| 0 PRUNE-BOUND | prune | exact integer bound `B = acc − Σ|F_j| − T` satisfies `U ≤ B` (at depth 40, `B = H`) |
| 1 SPLIT | branch | depth < 40; child s_d = −1 certified first, then s_d = +1 |
| 2 PRUNE-LEAF | non-grammar objective only | depth 40 and `leafGrammar bits` (all 16 vertices have 2 inward arms) |
Children states are recomputed from the parent in O(n) from one coupling row (`acc±f`, `F ± row`, `T − Σ|row|`). **Nothing produced by the search is trusted**: no incumbent trajectory, no floating point, no node counts. A fixed final `U` is used throughout; since every solver prune used an incumbent ≥ the final one, the certificate tree is never larger than the solver's tree.

## 3. Coverage invariant (proved: `chk_sound`, `Inv_child`, `partition_cover`)
Invariant `Inv`: `acc = A(p)`, `F = (f_j)_{j≥d}`, `T = Σ_{d≤j<h}|K_jh|`, `bits` = prefix id. Each accepted node proves "every ±1 completion of p with property P has H ≥ U": prune by `lower_bound`; split because every completion lies in exactly one child; leaf-grammar because a grammar leaf is not in P. Ties: pruning is non-strict, so the certified statement is a lower bound on the VALUE (the witness supplies attainment), never a claim about the set of minimisers.

## 4. Partitioned certificates (needed; found by calibration)
Single-theorem checking costs ≈0.5–0.7 MB of kernel memory per node (3,605 nodes → 2.5 GB; the 20,411-node subtree was OOM-killed on an 8 GB machine in one of two runs). So a frontier depth `D0` is fixed and each of the 2^D0 depth-D0 prefixes `b` gets an independent certificate `subOK … D0 b (cert b)`; shallow prunes become one-token certificates. Proved: `stateAt_Inv`, `subOK_sound`, `frontier_sound` (coverage of all 2^D0 prefixes), `batchesOK_sound`, `batches_cover` (assembly from separately checked batch theorems). Calibration shows memory is per theorem, not cumulative: 40 independent prefix theorems (6,780 nodes) peaked at 1.5 GB, the same as 8 theorems.

## 5. Exact conditional theorems already in the package
`ground_min_of_cert`, `nonG_min_of_cert` (single tree) and `ground_min_of_frontier`, `nonG_min_of_frontier` (partitioned): "if the checker accepts, the value is the exact minimum". Axioms: only propext / Classical.choice / Quot.sound.

## 6. Resource estimate for IV-4B (extrapolated; labelled uncertain)
Inputs (recorded SCR-III audit rerun, not recomputed here): ground run 700,405 nodes; non-grammar run 1,316,073 nodes. Certificate tree ≤ these.
| item | ground | non-grammar |
|---|---|---|
| tokens (upper bound) | ≤ 700,405 | ≤ 1,316,073 |
| certificate size (2 bits/node) | ≤ 175 KB | ≤ 329 KB (decimal literals ≈ 2.4×) |
| kernel time at 4.3–5.4 ms/node (calibrated) | ≤ ~50–65 min | ≤ ~95–120 min |
| peak memory per process | ≈ 1.5 GB if per-theorem nodes ≲ 2,500 | same |
| generation (untrusted Python, exact integers) | seconds–minutes (20k nodes in 0.2 s) | same |
| frontier theorems (D0 = 12) | 4,096 prefixes, packed into batches by node budget | same |
Calibration covered ≤ 0.5 % of the largest tree; true cost could differ by ~2×. The heaviest frontier prefix is unknown until generation; if it exceeds the node budget, raise `D0` (e.g. 16).

## 7. Proposed IV-4B gates (not authorised)
1. Generate certificates in Python (no Lean yet); report node counts per prefix and the maximum; confirm ≤ solver node counts.
2. Check a ≥1 % random sample of prefixes in Lean; record time/memory; stop if extrapolated cost > 3× this estimate.
3. Full verification in batches (≤ 2 parallel processes), logging hashes of certificate files; kernel only, no `native_decide`.
4. Acceptance: `ground_min_of_frontier` / `nonG_min_of_frontier` instantiated, axiom audit clean, negative controls (U+1, tampered token, truncated, trailing junk, wrong rows) rejected on the real instance.

## 8. Limits
Exact encoded model only (as IV-1); binary64 behaviour of the original solver is irrelevant to the certificate (the checker never uses it) but also is not certified by it; the 4×4 gap is not promoted until IV-4B and IV-5 complete.
