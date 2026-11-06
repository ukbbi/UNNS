# GIG-INFO v001 — Information recovery across arithmetic topological transitions (findings, mathematics first)

## Anchor A1: content (2, 3, 4, 5, 8, 9), m0=288

Survival law on the 60 sources t=1..60: Y=1 iff gcd(t,30)=1 (True); survivors 16/60; 8 distinct systems among the 60.

| level | classes | H(O) bits | H(Y) | H(Y given O) | I(Y;O) |
|---|---|---|---|---|---|
| O0 | 8 | 2.6402239 | 0.8366407 | 0.0000000 | 0.8366407 |
| O1 | 8 | 2.6402239 | 0.8366407 | 0.0000000 | 0.8366407 |
| O2 | 8 | 2.6402239 | 0.8366407 | 0.0000000 | 0.8366407 |
| O2c | 8 | 2.6402239 | 0.8366407 | 0.0000000 | 0.8366407 |
| O3 | 8 | 2.6402239 | 0.8366407 | 0.0000000 | 0.8366407 |

Pair search over ALL 56 system classes (every source m, grouped by capped valuations): binary-Y separating pairs per level {'O0': 0, 'O1': 0, 'O2': 0, 'O2c': 0, 'O3': 0}; three-valued (NA = anchor class not contained) {'O0': 2, 'O1': 1, 'O2': 1, 'O2c': 1, 'O3': 0}.

- equal N: m=432 (Y=NA) vs m=576 (Y=0), first separating level O1
- equal N: m=2160 (Y=NA) vs m=2880 (Y=0), first separating level O3

History count over prime indicators on the comparable window: N0=372, ΔN={'2': 36, '3': 72, '5': 240}, additive: True.

Divisibility arrows m→mp (comparable classes): Y transitions by prime {'2': [[0, 0], [1, 0]], '3': [[0, 0], [1, 0]], '5': [[0, 0], [1, 0]]}. Information change from the surviving source:
- ×2: N 372 → 408, ΔH_hist = log2(408/372) = 0.133267 bits, Y 1→0
- ×3: N 372 → 444, ΔH_hist = log2(444/372) = 0.255257 bits, Y 1→0
- ×5: N 372 → 612, ΔH_hist = log2(612/372) = 0.718229 bits, Y 1→0

Certificates (all comparable classes): 8, all independently verified: True.

## Anchor A2: content (2, 3, 6, 7, 8, 9), m0=432

Survival law on the 60 sources t=1..60: Y=1 iff gcd(t,42)=1 (True); survivors 17/60; 8 distinct systems among the 60.

| level | classes | H(O) bits | H(Y) | H(Y given O) | I(Y;O) |
|---|---|---|---|---|---|
| O0 | 8 | 2.4811879 | 0.8599530 | 0.0000000 | 0.8599530 |
| O1 | 8 | 2.4811879 | 0.8599530 | 0.0000000 | 0.8599530 |
| O2 | 8 | 2.4811879 | 0.8599530 | 0.0000000 | 0.8599530 |
| O2c | 8 | 2.4811879 | 0.8599530 | 0.0000000 | 0.8599530 |
| O3 | 8 | 2.4811879 | 0.8599530 | 0.0000000 | 0.8599530 |

Pair search over ALL 60 system classes (every source m, grouped by capped valuations): binary-Y separating pairs per level {'O0': 1, 'O1': 0, 'O2': 0, 'O2c': 0, 'O3': 0}; three-valued (NA = anchor class not contained) {'O0': 2, 'O1': 0, 'O2': 0, 'O2c': 0, 'O3': 0}.

- equal N: m=648 (Y=0) vs m=432 (Y=1), first separating level O1
- equal N: m=648 (Y=NA) vs m=432 (Y=1), first separating level O1
- equal N: m=4536 (Y=NA) vs m=3024 (Y=0), first separating level O1

History count over prime indicators on the comparable window: N0=276, ΔN={'2': 36, '3': 48, '7': 336}, additive: False.

Divisibility arrows m→mp (comparable classes): Y transitions by prime {'2': [[0, 0], [1, 0]], '3': [[0, 0], [1, 0]], '7': [[0, 0], [1, 0]]}. Information change from the surviving source:
- ×2: N 276 → 312, ΔH_hist = log2(312/276) = 0.176878 bits, Y 1→0
- ×3: N 276 → 324, ΔH_hist = log2(324/276) = 0.231326 bits, Y 1→0
- ×7: N 276 → 612, ΔH_hist = log2(612/276) = 1.148863 bits, Y 1→0

Certificates (all comparable classes): 8, all independently verified: True.

## Relabelling
{"A1": {"pairs_equal_O2c_different_labelled_set": [{"m_a": 2160, "m_b": 2880, "N": 648, "state_a": "NA", "state_b": "0", "relabelling_sigma": [2, 0, 1, 3, 5, 4]}]}, "A2": {"pairs_equal_O2c_different_labelled_set": []}}
