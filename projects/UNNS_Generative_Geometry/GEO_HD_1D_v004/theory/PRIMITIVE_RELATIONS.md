# D4-T2 (cont.) — which relations are primitive

Three relations on histories (all from a fixed source m):  ~swap  ⊆  ~rewrite  ⊆  ~endpoint.
* ~swap: adjacent swaps, preserve content.
* ~rewrite: swaps plus block replacement u <-> v for a chosen set of kernel vectors (u,v = arrangements of z-,z+).
* ~endpoint: equal endpoint (equivalently, D4-T1, V c = V c' and the same source).
The three are never assumed equal: equality of the last two is exactly the completeness question (GLOBAL_CONNECTIVITY.md).

Primitive = conformally minimal (Graver).  A kernel vector that is a non-conformal sum of others is NOT redundant operationally, because the pieces must each be realised through admissible intermediate states; v004 therefore keeps every Graver element as a candidate generator.
Result D-B4 (PROVED by the displayed example + verified Y5): in {1,2,3,8} the sub-set {z1=(1,-4,0,2), z2=(7,-2,-4,0)} does not connect the content fibre {3^2 8, 1^3 2} (contents (0,0,2,1) and (3,1,0,0)); only z3=(3,1,-2,-1) does.  This is an ALGEBRAIC obstruction: it holds at every source.  498 of 816 scanned fibres are deficient for {z1,z2}; with the Graver set every scanned fibre is connected.  No scanned fibre has irreducible contents of unequal length (so orientation by length is confluent there; the smallest "non-confluent-looking" case is the length-preserving move).
