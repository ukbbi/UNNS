# GEO_HD_1D_v003 -- global structure of generative histories (D-Q1 -> D-Q2 -> D-Q3, D-Q4 open)

Naming: the programme was specified as "v002", but GEO_HD_1D_v002 already exists (threshold theory) and is kept frozen, so this release is v003. v001 and v002 are untouched; the copied builder modules are pinned by hash (results/V001_PINS.json).

What is new (details and statuses in results/THEOREMS.md):
* Prefix-set form of the threshold law: a history is a maximal chain of feasible subsets; everything is governed by the family of infeasible subsets.
* **Feeding digraph** (A feeds B iff gcd(A+1,B)>1): Lemma NF, **block factorisation of swap classes over SCCs (F2)**, acyclic => connected (F1); the {2,3,N} converse is now **proved**; exact **3-label classification (T3)**.
* **Route topology** (permutohedral complexes, GF(2) Betti numbers): Alexander duality, contractibility for acyclic contents (T-LOWER), the complementary-pair theorem (T-SPHERE). Connected swap graphs with an unfilled loop ({2,3,8,9} at 72) and a 2-dimensional void ({2,3,8,9,14} at 1008); the cube-only complex misses the void.
* **Occurrence bridge** (72^r, r<=3): orthant form of the fibre, closed form of the local discrepancy, persistence-restricted swap graphs.
* D-Q4 is kept open (results/OPEN_PROBLEMS.md).

Scope and honesty: fixed source; distinct labels for route complexes; same-author verification (not human review); C3 NOT claimed; novelty NOT assessed. Prior-art neighbours (directed algebraic topology, higher-dimensional automata, Mazurkiewicz traces) were only seen by title and are not claimed to be compared.

Run (Python 3, no third-party packages):
    python RUN_VERIFY.py --fast           (about 10 s; shards X0..X7)
    python RUN_VERIFY.py --full           (larger boxes)
    python RUN_VERIFY.py --list           (shard descriptions)
    RUN_WINDOWS.bat [full]                (stage by stage, stops at the first failure)
    python src/build_v003.py              (regenerates results/*.json, about 30 s)
    python -m pytest tests                (if pytest is installed)

Layout: theory/ (THRESHOLDS, CONNECTIVITY, OBSTRUCTIONS, ROUTE_TOPOLOGY, OCCURRENCE_BRIDGE), src/ (thresholds.py, swap_classes.py, route_topology.py, topo_census.py, occurrence_bridge.py, build_v003.py, verify_v003.py, copied v001 modules), results/ (THEOREMS.md, COUNTEREXAMPLES.md, OPEN_PROBLEMS.md, *.json), tests/, STATUS.json, MANIFEST.json.
