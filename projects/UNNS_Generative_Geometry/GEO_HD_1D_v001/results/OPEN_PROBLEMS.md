# Open problems (HD-1D v001) - ranked

**D-Q1 (strongest next target). Classify swap classes.** Within a fixed (source, content), swap classes are the connected components of the monotone-path space of the cubical region P_u = {S : u + sum_{i in S} Delta_i >= 0} (D-W). D-T5 shows components can be separated by *resource contention* at a prime (capacity u_p, consumers N with p | N, producers N with p | N+1). Conjecture shape: the number of classes is determined by which consumers of each prime can claim the initial capacity before the first producer, subject to compatibility across primes. Data: 5 split endpoints in [4,6000]; 1 split group in 72^3; (14;2,3,14) is the minimal case. A theorem would give a Lock Lemma (order of two labels is invariant when no state in the class carries enough capacity for both) and a count of classes.

**D-Q2. Cube dimension and multiplicity of the 72^r family.** Maximum disjoint-swap cube dimension: 1, 2, 4, 5 for r = 1..4 (not r). H(72^r)^{1/r}: 4, 10, 15.3, 21.0, 26.9, 32.9 - growth rate unknown; no closed form for H(72^r). Is the maximum cube dimension linear in r, and with what slope?

**D-Q3. Common futures.** Prove or refute a necessary-and-sufficient arithmetic criterion for J(a,b) != empty in a restricted class (e.g. a,b prime powers). Only BOUNDED data (D_B5) is available here; bounded absence (15 pairs among 1..40 at bound 20000, all involving large primes against the bound) is a search artefact, not an obstruction.

**D-Q4. Image of the fibre-sequence map.** Which sequences of half-valuation vectors arise from admissible histories? (Faithful for fixed source, but the image is constrained by parity bookkeeping: parity flips by the odd-valuation kernel of each label.)

**D-Q5. Overlapping cells.** Complete description of the swap complex 2-skeleton: squares from disjoint swaps (always complete), hexagons from triples (iff product divides), and the role of repeated labels (non-reduced words).

**D-Q6 (interface). Valuation-strand geometry (HD-1E).** Relate the orthant walk of a history to FIELD-I strands through an explicit bridge definition; no identification of SELECT-II with FIELD-I is assumed.
