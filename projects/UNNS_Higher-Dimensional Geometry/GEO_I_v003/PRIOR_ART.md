# GEO-I v003 — Prior art and what is (not) claimed

Each reference is marked **verified** (the bibliographic record or text was retrieved and read during this work) or **unverified** (cited from general knowledge; check before relying on it). No reference below is invented; where a source could not be confirmed it is labelled.

## Used (standard mathematics)

| Topic | Source | Status | Where used |
|---|---|---|---|
| Graver basis: the set of conformally minimal elements of an integer lattice / kernel; a finite set that generates every element conformally | J. E. Graver, “On the foundations of linear and linear integer programming I,” *Mathematical Programming* 9 (1975) 207–226 | **verified** | definition of the move set; Lemma 0–4 |
| Graver bases in the toric / Gröbner setting (Graver basis of a lattice ideal; finiteness; relation to Markov bases) | B. Sturmfels, *Gröbner Bases and Convex Polytopes*, AMS University Lecture Series 8 (1996) | **verified** (record) | context for the move set |
| Nerve theorem for covers by convex sets (nonempty intersections contractible ⇒ nerve ≃ union) | K. Borsuk, “On the imbedding of systems of compacta in simplicial complexes,” *Fund. Math.* 35 (1948) 217–234; see also the statement and discussion in M. Tancer, arXiv:1102.0417 (2011), §5.1 | Tancer **verified**; Borsuk **unverified** (cited from memory) | Corollary 1; independent homology route |
| Homology of a polyhedral/cellular complex; a compact planar polyhedron has no 2-homology; a continuous bijection from a compact space to a Hausdorff space is a homeomorphism | any algebraic-topology text, e.g. A. Hatcher, *Algebraic Topology* (2002), Ch. 2–3 and Cor. 4G.3 | Hatcher: the book is standard; the exact corollary numbering is **unverified** | Theorem 1; Proposition P2 (the proof given in `MATHEMATICS.md` is self-contained) |
| Embedded polyhedral complex: cells intersect in common faces | standard definition (e.g. G. M. Ziegler, *Lectures on Polytopes*, 1995, Ch. 5) | **unverified** (cited from memory) | definition of “embedded” |

## Not found / not claimed

* No source was found for a criterion deciding when *the straight-line realization of the Graver move graph of a one-dimensional modular fibre* has crossing edges, nor for the index formula `ι(g,h)=|det|/|H|` as stated here. The proof of Theorem T1 is elementary (a coset count in a rank-2 lattice) and might well exist, in other language, in the literature on lattice point enumeration, toric geometry or Markov-basis complexes. **The literature check is incomplete.** Nothing in this release should be read as a priority claim; the contribution is stated as *proved here, from first principles, with exact computation*.
* Likewise the Klein-four obstruction (Theorem T2(c)) and the diagonal obstruction (Proposition D) are elementary observations whose novelty has not been assessed.
* The relation between the UNNS fibre complex and any physical interpretation is outside this release.

## Frozen sources
v001, v002 and the published Foundations materials are read, never modified. The two arithmetic libraries (`frozen/geo1lib.py`, `frozen/geo2lib.py`) are byte-identical to the v002 release; their SHA-256 values are checked by `verify.py` (gate G6).
