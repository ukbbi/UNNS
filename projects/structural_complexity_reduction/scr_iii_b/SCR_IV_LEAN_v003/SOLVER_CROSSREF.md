# Where the Lean bound comes from: line-by-line cross-reference to `solver_v010.cpp`

`data/provenance/solver_v010.cpp` is a byte-identical copy of the frozen solver (sha256 d56cf6d38a1622134359726c3ef56fd09066bc4ba27b2f167361c21574d5dd44, the hash recorded in the v001 manifest and the GAP4 audit). It is provenance only; nothing in the Lean build reads it.

| C++ (frozen) | Lean (`SCR_IV_Solver.lean` / `SCR_IV_Prune.lean`) |
|---|---|
| `double l=acc;` | `solverBound n d K s acc` starts its fold at `acc` |
| `for(int j=d;j<n;j++)` | `List.range' d (n - d).foldl …` (j outer, same order) |
| `field += k[i][j]*spin[i]` for `i<d` | `fieldLoop K s d j` = left fold over `List.range d` |
| `l -= fabs(field);` | `l - absZ (fieldLoop K s d j)` |
| `for(h=j+1;h<n;h++) l -= fabs(k[j][h]);` | inner `List.range' (j+1) (n-(j+1))` fold, `l' - absZ (K j h)` |
| `dfs(d+1, acc + s*field, …)`, `field = Σ_{i<d} k[i][d]*spin[i]` | `pathAcc K s (d+1) = pathAcc K s d + s d * fieldLoop K s d d` |
| `return l - 1e-11*max(1,scale)` | guard `g ≥ 0` subtracted: `guard_prune_sound`, `solver_prune_sound_ids` (any `g ≥ 0`) |
| `if(bound(d,acc)>=best) return;` | hypothesis `U ≤ solverBound … - g` of `discard_ground` / `discard_nonGrammar` |
| `d==n` leaf: `acc<best` | `solver_leaf_exact`, `leaf_acc_eq_hScaled`: bound = acc = `hScaled` at `d = 40` |
| `possible_violation(d)` (count, left loop; `count>2 \|\| count+left<2 \|\| left>0`) | `clStep`, `cppCL`, `cppPossible` |
| `violates()` (count over all 40 islands ≠ 2) | `cppViolates`, `cppViolates_iff : cppViolates id = true ↔ ¬IsGrammar id` |

Proved identity: `solverBound_eq_Bnd : solverBound n d K s (pathAcc K s d) = Bnd n d K s`, with
`Bnd = A(p) − Σ_{j≥d} |f_j(p)| − Σ_{d≤j<h<n} |K_jh|`, and `lower_bound : Bnd ≤ H(s)` for every ±1 completion.

## What is NOT formalised (read before relying on IV-3)
1. **Binary64 arithmetic.** Lean reasons over exact integers (the exact dyadic value of every double coupling, scaled by 2^70). The C++ evaluates the bound in `double`; its rounding error and the outward guard `1e-11·max(1,Σ|K|)` are the subject of the SCR-III numerical audit, not of this package. `guarded_prune_interface` states precisely what an error bound would have to supply (`Bapprox − e ≤ B`, `e ≤ g`).
2. **The DFS control flow.** IV-3 proves that each *discard rule* is sound and that the branch split is a partition. It does not prove that the recursive traversal visits every surviving node, that the incumbent update is correct, or that the returned `best` is the minimum; that is IV-4 (PENDING).
3. **Ties.** The solver prunes on `bound ≥ best` (non-strict) and accepts leaves only on `acc < best`. `prune_may_discard_tie` shows such a prune can discard a state tying the incumbent, so the solver certifies the minimum *value*, never the set of minimisers. `prune_strict_keeps_ties` is the strict variant.
4. **Grammar filter is weaker than it could be.** `possible_violation` returns `true` (keeps the node) whenever any vertex still has an unassigned island; it prunes only when every vertex is complete and satisfied (`cppPossible_false_sound`). Certainly-violated vertices (count>2 or count+left<2) persist in every completion (`violated_persists`, `completed_violation_persists`) — these are the facts a grammar-*constrained* search would prune on (`grammar_prune_sound`), but the v010 non-grammar search does not use them.
5. **Three objectives are kept distinct**: `ObjAll` (the solver's "ground" run), `ObjGrammar`, `ObjNonGrammar` (the solver's second run). `objective_relation` proves min(all) = min(grammar, non-grammar) at the level of definitions; no value of any of them is claimed here.
