# HD-1D v001 definitions and conventions

* **Label, transition.** For integers N >= 1 and m >= 1 with N | m: T_N(m) = m (N+1)^2 / N. Label 1 is allowed (T_1(m) = 4m); it is used in the 72 benchmark. T_N(m) >= 4m.
* **Valuation walk.** u(m) = (v_p(m))_p. Displacement of a label: Delta(N) = (2 v_p(N+1) - v_p(N))_p. T_N(m) has u(T_N m) = u(m) + Delta(N).
* **History.** h = (m_0; N_1..N_l); admissible if every N_j divides m_{j-1}. States m_j = T_{N_j}(m_{j-1}). Endpoint eps(h) = m_l. The empty history is allowed.
* **Complete history of t.** Source m_0 squarefree; endpoint t. H(t) = number of complete histories of t. (A non-squarefree state has an incoming edge; a squarefree state has none; so the source of a complete history is a state without incoming edges.)
* **Content** c(h) = multiset of labels of h. **Parikh data** (source, content) determine the endpoint.
* **Elementary swap** at position i: exchange adjacent labels N_i != N_{i+1}, legal if the result is admissible (the endpoint is then automatically unchanged). Swapping two equal labels is not a swap (same history).
* **Swap class** = connected component of the swap graph on a given set of histories (here: all complete histories of a given endpoint, or all histories with given source and endpoint). h ~swap h' is strictly finer than eps(h) = eps(h').
* **Disjoint-swap cube.** d legal swaps at positions i_1 < ... < i_d with i_{k+1} >= i_k + 2 span 2^d histories (cube vertices); edges join histories differing by one of the swaps. Cube dimension of h = largest such d.
* **Occurrence fibre.** s(m) = prod p^floor(v_p(m)/2); D(m) = {d >= 2 : d | s(m)}; half-valuation e(m) = (floor(v_p(m)/2))_p. Birth/loss sets B_j = D(m_j) \ D(m_{j-1}), L_j = D(m_{j-1}) \ D(m_j). Signature rho_d(h) = (1[d in D(m_j)])_j. Fibre sequence F(h) = (D(m_0), .., D(m_l)).
* **Pair classification at state m** (A != B): DIAMOND (both orders), ONLY_AB / ONLY_BA, BOTH_LABELS_ADMISSIBLE_NEITHER_ORDER (A | m, B | m, no order completes), ONE_LABEL_ONLY, NEITHER_LABEL.
* **Bounded vs universal.** Any search with a numerical bound is labelled BOUNDED and is never used as a universal statement.
