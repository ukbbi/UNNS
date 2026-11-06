# GIG-I v006 — Iterated Obstruction Lifting and Generative Homology (theorem register)
Tags: [PROVED] proof in PROOFS.md · [FINITE-EXACT] exact computation on the stated objects, no generalisation claimed · [BOUNDED] exhaustive only within stated bounds · [OPEN].
All homology is over GF(2). Notation as in Stage 3: z a 2-cycle of P6, c_a, c_b 3-chains with boundary z, new rank 6, L_{a,b}=Λ(z)+first(c_a)+last(c_b); K(A) is the complex of faces whose prefix sets lie in A.

## Question answered
Does the topology of a generative history space depend only on which lower-dimensional cycles can be filled, or also on the relations between their alternative fillings?
**Answer [FINITE-EXACT, with a [PROVED] criterion]: it depends on the relations.** The class of a lift depends on the pair of fillings through the difference cycle d=c_a+c_a′, exactly via whether first(d) bounds in the complex (FI-2). For the anchor cycle this dependence is real and arithmetically realisable (FI-6).

## A. Filling-independence
- **FI-1 [PROVED]** L_{a′,b}+L_{a,b}=first(c_a+c_a′); L_{a,b′}+L_{a,b}=last(c_b+c_b′). (E33 re-verifies all 64 triples.)
- **FI-2 [PROVED]** For any A containing the supports of L_{a,b} and L_{a′,b}: [L_{a′,b}]=[L_{a,b}] in H₃(K(A)) ⇔ first(d)∈∂C₄(K(A)). Dependence-free criterion; it is the sharp statement, not a sufficient condition.
- **FI-3 [PROVED]** ∂Λ(d)=first(d)+last(d) for a 3-cycle d; hence [first(d)]=[last(d)] in every K(A) containing the cells of Λ(d).
- **FI-4 [PROVED]** L_{a,a′}=L_{a′,a′}+first(c_a+c_a′) and L_{a′,a′}=∂Λ(c_{a′}); so [L_{a,a′}]=[first(d)] in every K(A) containing the cells of Λ(c_{a′}).
- **FI-5 [FINITE-EXACT] (anchor cycle, 4 minimal fillings B0..B3).**
  (i) Inside one family: every filling in K(P_z∪B_i) differs from c_i by a 3-cycle d of K(P_z∪B_i) (dim Z₃ = 9, 9, 25, 31); first(d) bounds in its own complex for all 511+511 nonzero d (B0,B1, exhaustive) and for the 31+25 basis elements plus 2000 random sums each (B2,B3). So the class is independent of the filling chosen inside a family, in every complex containing both lifts.
  (ii) Between families: d_ij=c_i+c_j. For {i,j}∈{01,02,13,23} first(d) has the empty family (self-bounding): [L_{i,b}]=[L_{j,b}] in every complex containing both. For {03} and {12}, first(d) has exactly two single-prefix-set minimal families ({89},{102} resp. {85},{106}) plus two of size 62: independence holds iff A contains one of them.
  (iii) The minimal families of first(d) and last(d) coincide, and the P6 families of d embed as families of first(d) via s↦s∪{rank-6 marker} (σ-check in E33). The additional size-62 families have no P6 counterpart.
- **FI-6 [FINITE-EXACT / BOUNDED] Certified filling-dependence.** In K(P_L∪P_L′) the classes [L],[L′],[L+L′] are all nonzero for {a,a′}={0,3} (b=1,2) and {1,2} (b=0,3). Arithmetic realisations (identity role map, among the 202 E30 seed contents): (2,3,8,9,14,15,20) at m=33600 and (3,8,9,14,15,20,21) at m=793800, pair (a,a′;b)=(1,2;0) and (2,1;0). Verified against all admitted 4-faces (E35): L_{1,0}, L_{2,0} and their sum are non-bounding, i.e. two linearly independent H₃ classes from two minimal fillings of one H₂ cycle. **No universal independence theorem is true**; FI-2 is the exact criterion.
- **FI-7 [OPEN]** Independence criteria for the other 31 Stage-2 classes; integral (non-GF(2)) coefficients; whether dependence occurs for {0,3}/{1,2} arithmetically (not found among the 202 seeds).

## B. Non-degeneracy (priority 2)
- **ND-1 [FINITE-EXACT]** For all 12 off-diagonal anchor pairs the bridge chains Λ(c_a), Λ(c_b) are NOT contained in K(P_{L_{a,b}}) (E39). The reduction L_{a,b}≃last(c_a+c_b) in K(P_L) is therefore unavailable, and non-degeneracy is exactly the statement that the bridge cells are missing. [OPEN] general proof.

## C. X/Y structure of lifted families (priority 3)
- **XY-1 [FINITE-EXACT]** Records for all 12 pairs in S3 CERTIFICATES/lift_pairs.json; recurring pattern {B_a},{6·B_b} plus mixed unions for (0,1),(0,2) and reverses; exceptions (0,3),(1,3),(2,3) and reverses. First/last of a difference cycle have the same family lattice (FI-5 iii), which explains why the same extra sets recur. No closed formula. [OPEN].

## D. Iterated lift H₃→H₄ in P₈ (priority 4)
- **HL-1 [PROVED]** For a 3-cycle w of P₇ and 4-chains c,c′ with ∂c=∂c′=w, L²=Λ(w)+first(c)+last(c′) is a 4-cycle of P₈ (LT-0 is proved for arbitrary rank count; E37 re-checks the instances); the diagonal L²_{c,c}=∂Λ(c) always bounds.
- **HL-2 [FINITE-EXACT]** Base w=L_{0,1}: fill index pairs (0,1),(1,0),(0,2) give non-degenerate 4-cycles (weights 2146, 2146, 2418; prefix sets 187, 187, 215); (0,0) bounds in its own complex.
- **HL-3 [BOUNDED] One fully certified arithmetic H₄ example (and seven more).** Content (2,3,4,5,8,9,15,20), m=86400, pair (0,1), fillings (1,0): an explicit 2146-face 4-cycle and a cochain φ of 6 faces with φ(L²)=1 and φ∘∂=0 on all 3819 admitted 5-faces; checked by an independent verifier (E40, CERTIFICATES/h4_certificate_first_hit.json). Seven further contents (…,21,25,26,27,32,33,35) verified identically. All come from the first seed content (2,3,4,5,8,9,15) of the E30 list: the scan stopped at 5+ hits after 129 tests and is not a census.

## E. Role-map correction
- **RM-1 [FINITE-EXACT]** Stage 3 (E30) used the identity role map only. For both sub6 contents (2,9,15,20,26,27) and (8,9,15,20,26,27) the identity image has no H₂ regime, but 18 of 180 S₆-images of the anchor class do (E36). The Stage 3 statement “the lift does not require the lower-dimensional hole to survive” is supported for the identity role map only.
