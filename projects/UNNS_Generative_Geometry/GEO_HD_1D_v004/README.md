# GEO_HD_1D_v004 — resource-sensitive completeness for different-content history relations

Run:  `python RUN_VERIFY.py --fast` (or `--full`, `--shard Y4`, `--list`); `pytest tests`.  Windows: RUN_WINDOWS.bat.
Read first: theory/THEOREMS.md, theory/GLOBAL_CONNECTIVITY.md, theory/OPEN_PROBLEMS.md.

Headline (same-author, not independent review; C3 not claimed; novelty not assessed):
* PROVED: equal endpoint <=> V_A(c-c')=0; kernel relations are realisable with explicit minimal sources; block rewrite threshold; saturation theorem (P(c)|m for all contents + Graver-complete moves => one rewrite class).
* Obstructions below the resource condition split into algebraic (insufficient generators: {3^2 8,1^3 2} needs the Graver move (3,1,-2,-1)), exposure (family 2^4 3^j <-> 1·8^2 3^j is connected iff 3|m or 16|m for j<=8; exposure obstruction proved for all j) and emptiness.
* A content-changing relation can turn a 4-point swap space into a circle (m=280, 840).
* OPEN: general-j sufficiency, {1,2,3} completeness proof, coherence cells, complete roots, HD-1C/HD-1E bridges.
v001, v002, v003 are frozen and untouched. src/build_v004.py regenerates results/*.json (~70 s).
