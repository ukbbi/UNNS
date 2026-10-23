# GCT Joint Correlation Representation Theorem — v002

## Statement of the research question

Can a shared recursively generated structure, constrained by admissibility and the basic operational symmetries of a Bell experiment, **uniquely determine** its joint correlations? This is a mathematical step toward the core UNNS entanglement question, not a test of Chamber XVI.

### Scope and provenance

This theorem uses operational assumptions adopted for a **candidate UNNS-style generator**. The assumptions have *not* been derived from canonical UNNS recursion. This distinction is essential. The v001 lock and its `NO_GO_WITH_LOCAL_FACTORIZATION` verdict remain unchanged.

## Theorem 1 — Binary joint-event representation

Let A,B ∈ {−1,+1}. For every measurement context (a,b), assume:

1. P(A,B|a,b) is nonnegative and normalized;
2. P(A,B|a,b) = P(−A,−B|a,b) (global outcome-flip symmetry).

Then **there exists a unique correlation number** C(a,b) ∈ [−1,+1] with

\[
P(A,B\mid a,b)=\frac{1+AB\,C(a,b)}4.
\]

Consequently both local marginals are exactly 1/2, independent of remote settings (operational no-signalling).

### Proof

Outcome-flip symmetry implies P(++ )=P(−−)=u and P(+−)=P(−+)=v. Normalization gives 2u+2v=1. The correlation C=E[AB]=2u−2v=4u−1, hence u=(1+C)/4, v=(1−C)/4. Nonnegativity is equivalent to |C|≤1. Conversely any such C gives a valid symmetric distribution. Summing over either outcome gives marginal 1/2. QED.

**Interpretation:** This representation is not the Born rule and provides no unique formula for C. It classifies all globally flip-symmetric binary pair distributions.

## Theorem 2 — Recursive representation without measure selection

Let z=AB∈{−1,+1} be a joint-route parity and let a context kernel C(a,b)∈[−1,+1] be supplied. Fix 0<r≤1 and define

\[
T_{a,b}(s\mid z)=(1-r)\mathbf1_{s=z}+r\frac{1+sC(a,b)}2.
\]

Then the unique stationary parity distribution is

\[
\pi_{a,b}(s)=\frac{1+sC(a,b)}2.
\]

For any initial parity law μ₀,

\[
\mu_n-\pi_{a,b}=(1-r)^n(\mu_0-\pi_{a,b}).
\]

### Proof

Write the update as \(\mu_{n+1}=(1-r)\mu_n+r\pi\). Subtract the fixed point \(\pi\) and iterate. Since |1-r|<1 for r>0, the stationary distribution is unique and attracting. Let an independent fair sign g∈{±1} label the two manifestations A=g, B=gz. Then P(A,B)=(1/2)π(AB), which is exactly Theorem 1's distribution. QED.

**Critical independence audit:** Recurrence and stationary-state uniqueness do not determine the context kernel C. It was put into the transition law. Thus the recursion does **not derive the singlet correlation law**.

## Theorem 3 — Symmetry-preserving countermodel family

Impose on C the additional requirements

\[
C(a,b)=c(a-b),\quad c(-d)=c(d),\quad c(0)=-1,\quad c(d+\pi)=-c(d).
\]

Together with |c|≤1, these encode common-rotation covariance, swap symmetry, perfect aligned anticorrelation, and measurement-axis reversal.

Each of the following functions obeys these conditions:

**Bell-local angular overlap:**
\[
c_L(d)=-1+\frac{2|\operatorname{principal}(d)|}{\pi},
\qquad \operatorname{principal}(d)\in[-\pi,\pi].
\]
Its standard local common-cause representation uses a shared uniform angle λ with A=sgn(cos(a−λ)), B=−sgn(cos(b−λ)). Its CHSH maximum cannot exceed 2; it equals 2 at the frozen settings.

**Quarantined quantum reference (not derived):**
\[
c_Q(d)=-\cos d.
\]
At the frozen CHSH settings its absolute CHSH value is exactly \(2\sqrt2\).

**Smooth stronger-than-quantum joint-context countermodel:**
\[
c_H(d)=-\frac{\tanh(K\cos d)}{\tanh K},\qquad K=6.
\]
Its absolute CHSH value at the same settings is
\[
4\frac{\tanh(K/\sqrt2)}{\tanh K}\approx3.9983975924.
\]

All three give unbiased marginals, obey operational no-signalling, display perfect aligned anticorrelation, and have the **same four-outcome support** for generic 0<|d|<π. Yet they yield different probabilities and CHSH values.

### Conclusion of Theorem 3

The operational symmetries, outcome support/admissibility, and the recursive joint-route architecture do **not** uniquely determine the quantum distribution. This is a constructive underdetermination theorem, not an unsuccessful numerical fit. QED.

## Theorem 4 — Bell-local boundary

If measurement independence and Bell-local factorization hold, define conditional local means X(a,λ), X(a',λ), Y(b,λ), Y(b',λ)∈[−1,1]. The pointwise CHSH integrand is

\[
X(Y+Y')+X'(Y-Y').
\]

Its absolute value is bounded by |Y+Y'|+|Y−Y'|≤2. Averaging over setting-independent ρ(λ) preserves the bound |S|≤2. QED.

The **joint-context** transition in Theorem 2 depends on both a and b. For its Bell-violating choices it therefore does not admit the Bell-local representation above. This is an explicit departure from v001's factorization assumption. The marginals nevertheless remain no-signalling. We make no physical claim that such global-context dependence is realizable by an underlying UNNS process.

## Final verdict

`UNDERDETERMINED_NONLOCAL_GENERATIVE_RULE`

We have formally constructed a family of no-signalling joint generative laws and identified the nonlocal assumption needed to escape the Bell-local gate. We have **not** derived the special singlet kernel from UNNS. Additional independent structural principles would be required, and merely choosing the cosine kernel would import the answer.
