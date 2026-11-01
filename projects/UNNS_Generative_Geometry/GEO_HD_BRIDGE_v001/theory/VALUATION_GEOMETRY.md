# HD-C0 — valuation-space geometry

A state m has valuation vector u_P(m) in Z^P; a SELECT-II label N moves it by Delta_P(N) = (2 v_p(N+1) - v_p(N))_p and requires v_p(m) >= v_p(N) for every p.  A history is a lattice path.
Three different dimensions (all computed in results/DIMENSIONS.json):
* d_span = rank_Q{Delta_P(N)}: coordinate rank of the displacement span.
* d_constraint(m, content): primes whose admissibility inequalities change the set of admissible histories when relaxed.
* d_topological(m, content): size of a smallest prime set S such that keeping only the constraints at S preserves the Betti vector of the route complex.
Controls: {2,3,8,9}@72: d_span 3 (primes 2,3,5), d_constraint 2, d_topological 2.   {2,3,8,9,14}@1008: d_span 4, active primes 2,3,7, d_constraint {2,3} (prime 7 never binds at 1008), d_topological 2.  So a rank-4 valuation realization carries a void whose obstruction is 2-dimensional.
