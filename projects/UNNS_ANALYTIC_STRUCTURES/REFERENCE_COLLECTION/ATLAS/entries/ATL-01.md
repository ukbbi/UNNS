# ATL-01: Exact admissible composition

## Mathematical object

A word of letters acting on integers, subject to integrality. The data of a word are its minimal source $K(w)$ and least endpoint $E(w)$.

## Established structure

- **Sources and endpoints are exact progressions.** A word is admissible precisely from the multiples of $K(w)$, with endpoints the multiples of $E(w)$, and both obey a one-letter gcd recurrence (T03). This holds for every integral-image grammar under the stated hypotheses.
- **Prime coordinates.** Each letter shifts the exponent of $p$ by $2v_p(N+1)-v_p(N)$, and the minimal endpoint exponent is a maximum over suffixes (T04).
- **Composition.** With $d=\gcd(E(u),K(v))$ one has $K(uv)=K(u)K(v)/d$ and $E(uv)=E(u)E(v)/d$. Prime by prime this is multiplication in a bicyclic monoid, a classical object. It gives a block factorization of $G_{m+n}$ and the supermultiplicativity $G_{m+n}\ge G_mG_n$ (T47).
- **History series.** Counting histories by endpoint factorizes as $\mathcal Z_H(s,t)=\zeta(s)\,\mathcal G(s,t)$, with Möbius inversion depth by depth (T01, T02). A source weight gives a three-variable series with a closed form on its anti-diagonal (T14).
- **No ordinary Euler product** exists for the nesting grammar at $t=1$ (T06). Grammars with unit denominators, by contrast, have a closed rational form (T08).
- At one step, the in-degree and the root series reduce to classical Dirichlet series (AS-001, AS-002).

## What it reveals

Generation can be studied through two integers per word. The zeta factor records only the free choice of source; the structure specific to the grammar lies in $\mathcal G$. Although the evolution of a prescribed word separates into prime coordinates, the history population does not possess an ordinary Euler product. The ordered letter structure couples the arithmetic contributions when histories are counted.

## Further structure

The recurrence of T03 drives the fixed-depth convergence region (ATL-06) and the decompositions at one third (ATL-08).

## Open boundary

The supermultiplicativity conjecture ANS-C2 for the history counts has finite evidence only.

## Reading across (interpretation)

The prime-by-prime bicyclic structure is a point of contact with algebraic investigations of the Substrate. It is examined in the Cross-Structural Research Map (`CROSS_STRUCTURES/`), whose derived statements are unreviewed and are not part of this Atlas or the catalogue.

## Principal results

| ID | Result | Status | Review |
|---------------|--------------------------------------|---------------------|---------|
| ANS-T03 | Source and endpoint recurrences | PROVED | V |
| ANS-T04 | Prime-coordinate evolution | PROVED | V |
| ANS-T47 | Composition of words, block factorization, supermultiplicativity | PROVED | V |
| ANS-T01 | History Dirichlet factorization | PROVED | V |
| ANS-T06 | No ordinary Euler product | PROVED | V |

## Recorded open questions

- **ANS-C2:** Conjecture (v001): H(mn) > H(m)H(n) for coprime non-squarefree m, n. Finite evidence only.

## Connected entries (cited dependencies)

- **Uses ATL-03** (The characteristic exponent and its singular point): ANS-T07, ANS-T09.
- **Uses ATL-06** (Fixed-depth singularity architecture): ANS-T12.
- **Used by ATL-02** (Finite saturation and unbounded obstruction): ANS-T11.
- **Used by ATL-06** (Fixed-depth singularity architecture): ANS-T12.
- **Used by ATL-07** (Depth two: an arithmetic singularity hierarchy): ANS-T05, ANS-T13.
- **Used by ATL-08** (The mechanism at one third): ANS-T46m, ANS-T46r, ANS-T46s.

## Review boundary

Without a review verdict: AS-001 (B), AS-002 (B).

Qualified verdicts:

- ANS-T14: The stated convergence regions; not a complete classification for negative source weights.

## All results and proof sources

- **Initial analytic baseline:** AS-001, AS-002.
- **ANS-I v001:** ANS-T03, ANS-T04, ANS-T01, ANS-T02, ANS-T14, ANS-T06, ANS-T08.
- **ANS-I v014:** ANS-T47.
