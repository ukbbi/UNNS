# Specification
Arithmetic domain, features and signatures as in GIG-INFO v003 (read from its RESULTS). Forbidden-flag complex Y_A and the duality: ENGINE/forbidden.py and THEORY/THEOREMS.md (T-AD).
Ensembles (ENGINE/ent2.py): natural = uniform over the listed systems; balanced = mass 1/2 on beta2>0, 1/2 on beta2=0, uniform inside each class. Entropies exact (Fractions), 30-digit log2.
Out-of-sample protocol (B11): fit on one sample, evaluate on the other; recovered information = 1 - balanced cross-entropy (probabilities clipped to [1e-6, 1-1e-6]); histogram gradient boosting (depth 4, 200 iterations, class_weight=balanced, random_state=0) and exact-signature lookup with back-off (N,h1,Q,S2) -> (N,h1,Q) -> (N,h1) -> N -> 0.5.
Symbolic grammar (ENGINE/sym.py): events with categories; rule set G subset Sigma x Sigma; history admissible iff every consecutive category transition lies in G; complex = full subcomplex of P_6; no divisibility.
Classes for the scope tests (A12): VS arbitrary vertex sets; PF prefix families; TF threshold families (sampled; no positive found).
