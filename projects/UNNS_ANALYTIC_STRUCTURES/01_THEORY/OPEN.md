# Open questions

State after ANS-I v001.

| ID | Question | State |
|---|---|---|
| O01 | Sharp abscissa of the unweighted history generating function | Resolved: sigma_c, root of B = 1 (ANS-T09) |
| O02 | Closed forms or effective bounds at fixed depth | Partly: abscissa 1/2 at every depth (T12), depth two (T05, T13); depth >= 3 open (ANS-C1) |
| O03 | Multiplicativity and Euler products | Resolved at t = 1: no ordinary Euler product (T06) |
| O04 | History statistics distinguishing grammar families | Open; saturation criterion and a failing example (T11) |
| O05 | Continuation and singularities beyond absolute convergence | Open beyond depth two |
| O06 | RH-sensitive quantities and cancellation | Open |
| O07 | Behaviour on the surface |t| B(Re s) = 1; type of the singularity of G(s,1) at sigma_c | Open |
| O08 | Is A(X) asymptotic to c X^sigma_c, or with a slowly varying factor? | Open |
| O09 | Region of F(s,u,t) for Re(s+u) < 0 | Open (divergence side settled) |
| O10 | Proof of the second term c of A_2(X) and continuation of G_2 past Re s = 1/3 | Open |
| O11 | H(mn) > H(m)H(n) for coprime non-squarefree m, n (ANS-C2) | Open |

## Update from ANS-I v002 (26 November 2026, proofs pending review)
- O07: convergence on |t|B(a) = 1 settled for a > 1; the point sigma_c is a C-infinity singularity. Continuation elsewhere on the line is open.
- O08: A(X) is not asymptotic to c X^sigma_c; the deficit is exp(-(log X)^(1/sigma_c + o(1))). Exact order open.

## Update from ANS-I v003 (26 November 2026)
- Exact suppression order: depth bounds are now k^beta / log k to k^beta; conjectured order k^beta / log k (T28). The obstacle is repeated demands for introduced primes.
- Boundary derivatives: (j!)^(sigma_c + o(1)) (T27).
- Continuation along the line (T29), alphabet transition (T30), other grammars (T25): open.

## Update from ANS-II v001 (26 November 2026)
- Exact abscissa when some prime drift is negative, and the zero-drift case.
- Whether the depth ratios between torsion classes converge.
- A transfer operator between classes retaining source divisibility.
- Multipliers with no rational power.

## Update from ANS-II v002 (26 November 2026, new proofs pending review)
- Resolved from the v001 list: abscissa under any drift signs (T16); zero drift, abscissa and depth (T09, T09a); a transfer operator retaining source divisibility (T13, T14).
- Open: exact suppression order (O3); behaviour at the abscissa under negative drift (O5); spectrum and continuation of the operators (O6); existence of an exact zero drift (O7); counting under zero or negative drift (O8).
- Still open: ratios of depth terms between torsion classes; multipliers with no rational power.

## Update from ANS-II-ND v001 (26 November 2026, new proofs pending review)
- Resolved: counting exponents under any drift signs, including every fixed source (ANS2-O8 at exponent level); infinite support of the optimal weights under negative drift.
- Open: attainment of the entropy supremum (ANS2N-O1); behaviour at the abscissa (ANS2N-O2, formerly ANS2-O5); lower-order counting factors (O3); pattern of the optimal weights (O4).

## Update from ANS-II-ND v002 (26 November 2026, new proofs pending review)
- Attainment (ANS2N-O1): holds when the optimal weights are below 1/2 at the depleting primes (T10). Whether a weight can reach 1/2 is open (O5).
- Decay of the weights (ANS2N-O4): impossible together with "all weights below 1/2" under negative drift (T11). Otherwise open.
- Not addressed: behaviour at the abscissa (O2) and lower-order counting factors (O3).

## Update from ANS-II-ND v003 (26 November 2026, new proofs pending review)
- Attainment (O1): equivalent to convergence of the mean of v_p(N+1) at every prime (T14).
- Decay (O4): only the case with maximum weight exactly 1/2 remains. Half-weight threshold (O5) open.
- Average weight at most 1 - 1/a (T15); whether it is 0 is open (O6).
- Not addressed: O2 and O3.

## Update from ANS-I v005 (27 November 2026, new proofs pending review)
- Critical line (ANS-T29): the continuation exists across every point except sigma_c (T31). Open: behaviour at and to the left of sigma_c (T33).
- Higher depth: the real limit and the counting asymptotic hold for every k (T32, C1). Open: continuation of G_k left of 1/2 for k >= 3 (T34), other points of that line, lower-order terms, growth of kappa_k.
- Not addressed: continuation to a fixed half-plane, complex zeros, character-weighted functions.

## Update from ANS-I v006 (27 November 2026, new proofs pending review)
- v005 reviewed: T31, T32, C1 valid (one correction to T32 applied).
- Character-weighted continuation (T35) and sector singular parts (T36) proved, conditional on nothing beyond earlier ANS-I results.
- Open: pointwise sector distribution (T37), complex zeros (T38), the twists q^(i tau0) (T39), T33, T34.

## Update from ANS-I v007 (27 November 2026)
- v006 reviewed: T32a, T35, T36, T37a valid; T27 valid as infimal Gevrey order.
- Resolved: counting equidistribution over finite quotients (T37, supersedes the open item from v006); regular variation (T40), so A is X^sigma_c times a slowly varying factor (partial answer to O08).
- Open: rates in T37 and T40; the form of the slowly varying factor (T28); T33, T34, T38, T39.

## Update from ANS-I v008 (27 November 2026, new proofs pending review)
- v007 reviewed: T37, T37b, T40, T41, T42 valid; T24a valid.
- Resolved: continuation of G_k left of 1/2 (T34), other points of that line, and the lower-order terms of A_k (T34a).
- O10: continuation of G_2 past 1/3 resolved (T45); the second term is proved for smoothed counts only, the sharp form is open.
- Open: G_k, k >= 3, at and beyond 1/3 (T46); sharper error exponents; uniformity in k; T33, T38, T39.

## Update from ANS-I v009 (27 November 2026, new proofs pending review)
- v008 reviewed: T34, T34a, T45, T42a, T43, T44 valid.
- Resolved: the maximal meromorphic domain of G_2 (T45a); infinitely many non-real poles of G_2 (T38a).
- Open: depth k >= 3 at 1/3 (T46, conjectured pole order floor(k^2/4), T46b) and natural boundaries there (T46a); zeros of G_2; sharp second term of A_2; T33; T38 for the complete functions; T39.

## Update from ANS-I v010 (27 November 2026, new proofs pending review)
- v009 reviewed: T34b, T45a, T45b, T38a valid.
- Resolved: the location and order of the poles of G_2 on Re s > 0 in terms of the exponents e_n and zeta zeros (T45d); the sign densities of e_n (T45e).
- Model only: one letter linked on both sides gives a simple pole at 1/3 (T46c). T46b remains a conjecture.
- Open: G_3 at 1/3 (T46, T46b); natural boundaries at higher depth (T46a); zeros of G_2; sharp second term of A_2; T33; T38 for the complete functions; T39.

## Update from ANS-I v011 (27 November 2026, new proofs pending review)
- v010 reviewed: T45c, T45d, T45e, T38b, T38c, T38d, T46c valid.
- Depth three: exact decomposition proved for Re s > 1/2 (T46d). Continuation past 1/3 NOT proved; it is the conjecture T46e, which would give T46b at k = 3. Missing step: uniform control of square conditions on one side of the shifted series.
- Open: T46e; depth four and higher (T46, T46a); zeros of G_2; sharp second term of A_2; T33; T38 for the complete functions; T39.

## Update from ANS-I v012 (27 November 2026, new proofs pending review)
- v011 reviewed: T45f, T38e, T46f, T46d, T46e-i valid.
- Proofs offered: R continues to Re s > 2/7 (T46i); V continues past 1/3 (T46j); hence T46e, and G_3 has a pole of order exactly two at 1/3 (T46k, T46b at k = 3). These need independent review.
- Open: G_3 further left; sharp second terms of A_2, A_3; depth four and higher (T46, T46a, T46b); zeros of G_2; T33; T38 for the complete functions; T39.

## Update from ANS-I v013 (27 November 2026, new proofs pending review)
- v012 reviewed: T46g, T46h, T46h-i, T46i, T46j, T46e, T46k, T46l valid; T46b at k = 3 established.
- Offered: margin 1/200 (T46k-i); end-letter decomposition at every depth (T46m); link roles (T46n); model with pole order rt (T46o).
- Open: T46q and continuation of M_4, R_4 past 1/3 (hence T46b at k = 4); a general order principle for M_k; T33; G_3 further left; sharp counting terms; zeros; T38 for the complete functions; T39.

## Update from ANS-I v014 (27 November 2026, new proofs pending review)
- Proved: composition law and block factorization (T47); middle-word overlap identity (T46r); local expansion of role patterns and agreement with proved leading coefficients (T46s); order of G_k(1)^(1/k) (T48).
- Open: T46t (coefficient formula, k >= 4); continuation of G_4, M_4, R_4 past 1/3 (no viable route established); a divisor-weighted form of T46j as next target; constant in T48; T33; G_3 further left; zeros; T38 for the complete functions; T39.

## Update from ANS-I v015 (27 November 2026, T49 and T50 pending review)
- Proved: upper constant e^gamma and exponential-function growth (T48a, T48b); lower constant 1.1079... (T49); two-sided bounds in the window s = 1 + tau/log k (T50).
- Open: existence and value of lim G_k(1)^(1/k)/log k (heuristic: below e^gamma); optimised layered lower bound; s below the window; T33 (not advanced); T46t and depth four; zeros; T38 for the complete functions; T39.
