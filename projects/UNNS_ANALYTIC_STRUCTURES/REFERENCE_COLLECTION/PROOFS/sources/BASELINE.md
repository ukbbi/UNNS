# Initial analytic baseline

Superseded in part by ANS-I v001 (`02_INVESTIGATIONS/ANS_I/v001/`): AS-004 is extended to the sharp boundary.

Status: elementary deductions with proofs below; not yet independently audited or checked for literature novelty.

## AS-001 — Immediate predecessor series
For the selected integer nesting grammar, T_N(Nk)=k(N+1)^2 for N,k >= 1. The labelled in-degree D(y) counts m >= 2 with m^2 dividing y.

$$\sum_{y\ge1}D(y)y^{-s}=\zeta(s)(\zeta(2s)-1),\qquad \Re s>1.$$

Proof: sum over y=km^2 and use absolute convergence in the stated half-plane.

## AS-002 — Root series
A(y)=1 if D(y)=0 and 0 otherwise. These are exactly the squarefree integers, including 1, hence A(y)=mu(y)^2.

$$\sum_{y\ge1}A(y)y^{-s}=\frac{\zeta(s)}{\zeta(2s)},\qquad \Re s>1.$$

Proof: the Euler factor for each prime p is 1+p^{-s}; use the classical Euler product. Possible cancellations must be checked before claiming poles at zeros of the denominator.

## AS-003 — History factorization and inversion
Let E_G(w) be the least endpoint of a legal word in an integral-image grammar G with finite ancestry and endpoint divisibility as in the monograph. Define a_G(n)=#{w:E_G(w)=n}, H_G(n)=#{w:E_G(w)|n}, including the empty word. Then

$$H_G(n)=\sum_{d\mid n}a_G(d),\qquad a_G(n)=\sum_{d\mid n}\mu(d)H_G(n/d).$$

Proof: group words by their minimal endpoints, then use Möbius inversion. Consequently, wherever both series converge absolutely,

$$\mathcal Z_{H,G}(s)=\zeta(s)\mathcal G_G(s),\quad \mathcal G_G(s)=\sum_w E_G(w)^{-s}.$$

The depth-weighted version follows by replacing each word's weight by t^{|w|}, subject to absolute convergence (or coefficientwise at fixed n).

## AS-004 — Sufficient convergence bound for the selected grammar
For r_N=(N+1)^2/N, E(w)=K(w) product r_N >= product r_N. Write B(sigma)=sum_{N>=1}r_N^{-sigma}. At sigma>1 this is finite. If |t| B(sigma)<1, then

$$\sum_w |t|^{|w|}E(w)^{-\sigma}\le \sum_{j\ge0} (|t|B(\sigma))^j = \frac{1}{1-|t|B(\sigma)}.$$

For t=1 and sigma=2, B(2)=zeta(2)-2 zeta(3)+zeta(4)<1 (also r_N>N+2, so B(2)<sum_{m>=3}m^{-2}<1). Thus the unweighted history factorization is justified at Re s>=2. This is a sufficient bound, not a determination of the true abscissa.

## Open directions
Determine sharp convergence, depth-dependent coefficients, grammar-specific singularities and multiplicative obstructions. Classical zeta identities are not claimed as new analytic number theory. Any novelty lies in the generative interpretation or additional grammar-dependent theorems and requires a literature review.
