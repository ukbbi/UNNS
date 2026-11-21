# MUG-I v008 — Exact research theorems

**Research record, not a manuscript.** Model: the one-dimensional transverse Maxwell/Hill equation on the 2π-periodic coordinate,

\[
-E''(z)=\lambda\varepsilon(z)E(z),\qquad
\varepsilon(z)=1+2\delta\cos(qz),\quad q\in\mathbb N_{>0},\quad 0<|\delta|<1/2,\quad \lambda=\omega^2>0.
\]

This model is a scalar reduction of a Maxwell system for a particular polarization/propagation configuration, not general vector Maxwell theory. All *exact* field statements refer to actual solutions of the untruncated differential equation. Numerical evidence uses a truncated Fourier/Galerkin approximation and is separately flagged.

The UNNS law is unchanged: \(T_N(g)=g(N+1)^2/N\), \(N\mid g\), \(N\in\mathbb N_{>0}\). Its field-level *declared* pullback (not physical evolution) is \(D_NE(z)=E(r_N z)\), \(r_N=(N+1)^2/N>1\), when every occupied Fourier index maps to an integer. The zero Fourier harmonic, if present, is left at zero by the pullback; this is a coordinate-map convention, not a new positive-integer UNNS vertex.

## T1 [PROVED] — Exact Fourier-content lemma for a single Bloch sector

Let a nontrivial positive-frequency eigenfunction \(E\) lie in a Bloch sector \(\kappa\pmod q\). Write
\(E(z)=\sum_{j\in\mathbb Z}c_j\exp(i(\kappa+jq)z)\).
Then its occupied integer-frequency set has gcd exactly

\[
  \boxed{d(E)=\gcd(\kappa,q)}.
\]

**Proof.** Substitution into the Hill equation gives the exact recurrence

\[
 ((\kappa+jq)^2-\lambda)c_j=\lambda\delta(c_{j-1}+c_{j+1}). \tag{1}
\]

As \(\lambda\delta\ne0\), no nonzero solution can have finite Fourier support: at an uppermost occupied index \(J\), recurrence (1) at \(J+1\) would require \(\lambda\delta c_J=0\). Suppose no two consecutive coefficients are nonzero. Every occupied \(j\) then has \(c_{j-1}=c_{j+1}=0\), and (1) implies \((\kappa+jq)^2=\lambda\). At most two indices satisfy this, contrary to the infinite-support observation. Thus there are consecutive occupied \(j,j+1\). Their Fourier indices have gcd \(\gcd(\kappa+jq,\kappa+(j+1)q)=\gcd(\kappa,q)\). Every occupied index is congruent to \(\kappa\) mod \(q\), hence divisible by \(\gcd(\kappa,q)\), and the two occupied neighbors prevent any larger common divisor. QED.

This *proves*, in the specified scalar model, a full-content claim that was only perturbatively/numerically supported in v007. Do not extrapolate to multimode superpositions in unrelated Bloch sectors or to all vector Maxwell systems without checking their corresponding coupled recurrences.

## T2 [PROVED] — Exact whole-field admissibility and inherited history geometry

For a field Fourier support \(S\subset\mathbb Z\) with positive gcd \(d\), strict whole-field \(D_N\) is defined on the same 2π torus iff \(N\mid d\). If so, its new support content is

\[
  d(D_N E)=\frac{(N+1)^2}{N}d=T_N(d).
\]

**Proof.** \(N\mid d\) iff every occupied nonzero integer \(m\) is divisible by \(N\). Then \(m\mapsto m(N+1)^2/N\) is integral. The multiplier is injective, so no coefficients cancel; the gcd of the images equals \((N+1)^2\gcd\{m/N\}\). QED.

By induction, the legal histories on this whole-field Fourier-support representation are exactly the positive-integer \(T_N\) histories starting at \(d\). Whenever two legal words have the same total multiplier, they produce the identical transformed field \(E(Rz)\). This is **a field correspondence**, not a claim that intermediate fields stay stationary eigenstates of the same medium.

For a single Bloch eigenmode, T1 fixes the starting content to \(d=\gcd(\kappa,q)\). This imposes the initial step condition \(N\mid q\), but *not* a permanent \(N\mid q\) restriction on later steps: the transformed field is generally no longer a full eigenstate in one original Bloch class.

## T3 [PROVED] — Explicit identity for v007's rule E

Let \(Q_N\) be the Fourier projector retaining only occupied indices divisible by \(N\). The implemented v007 Bloch-class projector \(P_N^{(q)}\) retains coefficient \(m\) iff \(N\mid\gcd(m\bmod q,q)\). For arbitrary Fourier fields,

\[
\boxed{P_N^{(q)}=\begin{cases}Q_N,&N\mid q,\\0,&N\nmid q.\end{cases}}
\]

**Proof.** If \(N\nmid q\), no divisor of \(q\) can be divisible by \(N\). If \(N\mid q\), \(N\mid(m\bmod q)\) iff \(N\mid m\), and since \(N\mid q\), the same is equivalent to \(N\mid\gcd(m\bmod q,q)\). QED.

Consequently **v007 rule E** is \(D_NQ_N\) when \(N\mid q\) and zero otherwise. It is **not** the strict whole-field rule (which rejects a field outright if it contains any inadmissible occupied index), and its additional global \(N\mid q\) veto is not required by the Fourier index condition after previous dilations.

A simple field \(E(z)=e^{2iz}+e^{3iz}\) at \(q=6,N=2\) demonstrates that E's projector partially retains components even though the *whole field* has content 1 and hence no strict whole-field \(T_2\) step. Its spectral consequences require a separately specified physical filtering/coupling operation.

## T4 [PROVED] — Fixed-medium exact-eigenstate no-go theorem

Assume \(\lambda>0,\delta\ne0,q>0\). If a nonzero exact eigenmode \(E\) has a periodic pullback \(\widetilde E(z)=E(rz)\) for any real \(r>1\), then \(\widetilde E\) **cannot** be an exact eigenmode of the same fixed scalar Maxwell/Hill medium for any frequency \(\widetilde\lambda\).

**Proof.** By chain rule,
\(-\widetilde E''=r^2\lambda\varepsilon(rz)\widetilde E\).
If also \(-\widetilde E''=\widetilde\lambda\varepsilon(z)\widetilde E\), then
\([r^2\lambda\varepsilon(rz)-\widetilde\lambda\varepsilon(z)]\widetilde E(z)=0\).
The eigenfunction is analytic and nonzero on a dense open set, so the bracket vanishes identically. At \(z=0\), since \(\varepsilon(0)>0\) and \(\varepsilon(r\cdot0)=\varepsilon(0)\), we obtain \(\widetilde\lambda=r^2\lambda\). It follows that \(\cos(qrz)=\cos(qz)\) for all \(z\). Equality of their second derivatives at zero forces \(r^2=1\), contradicting \(r>1\). QED.

Since every UNNS multiplier is \(r_N>1\), **no nontrivial forward edge preserves exact stationary eigenstates in this one fixed nonuniform medium** under direct spatial pullback. This is a theorem about a chosen induction rule and this dielectric, not about impossibility of Maxwell mode conversion through external driving, boundary changes, scattering or other physical interactions.

## T5 [PROVED] — Vacuum and co-dilating medium controls

If \(\delta=0\), a plane wave \(e^{igz}\) remains a fixed-medium exact eigenmode after any integer-periodic dilation, with \(\widetilde\lambda=r^2g^2\). For \(\delta\ne0\), the field \(\widetilde E(z)=E(rz)\) is **exactly** an eigenmode of the *different* dielectric \(\varepsilon_r(z)=\varepsilon(rz)\) with \(\widetilde\lambda=r^2\lambda\), by the chain rule. The natural rescaled spatial torus has circumference \(2\pi/r\); if one insists on the original torus, both \(r q\in\mathbb Z\) and the transformed support's integer periodicity are needed.

This control reveals that the fixed-medium obstruction arises from the independently specified material profile. It is not a UNNS-specific obstruction: arbitrary nonunit dilations meet the same issue.

## T6 [PROVED] — Complete eigenbasis resolution introduces no necessary projection

On a fixed compact periodic domain with strictly positive dielectric, the generalized eigenproblem has a complete eigenbasis in the dielectric-weighted Hilbert space \(L^2(\varepsilon dz)\). Any admissible transformed field is representable as a (generally infinite) superposition of the fixed-medium eigenstates. **Keeping the full expansion is an exact change of representation**, not mode blocking. Replacing it by a subset, dephasing, measuring, or physically coupling selected modes requires an additional rule specifying that operation. A weighted kernel built from the squared expansion coefficients is a mathematical diagnostic unless such an operation is physically supplied.

## Decisive equal-endpoint witness

Start with a genuine eigenstate in the \(q=6,\kappa=0\) sector (T1 gives \(d=6\)). The two label histories have the same total multiplier \(288\):

- \(A=(3,8,3):\ 6\to32\to324\to1728\).
- \(B=(1,1,1,2):\ 6\to24\to96\to384\to1728\).

T2: both are legal, with exactly the same terminal Fourier field \(E(288z)\). T3: v007 rule E blocks A at N=8 because 8 does not divide the fixed medium harmonic q=6, while B survives. T4: neither *first step* produces another stationary eigenmode of the original fixed medium. T5: if the medium co-dilates at every step, both histories consist of exact eigenmode correspondences between **different** media, and the final medium and field agree.

## Scientific status

**PROVED:** T1–T6, each within the explicitly specified induction and dielectric assumptions. **VERIFIED EXACT FINITE:** computational oracle checks and rational support witness. **VERIFIED NUMERICAL:** one reconstructed q=6 eigenstate and fixed/co-dilating residuals. **OPEN:** a physically defined and independently validated Maxwell process implementing a nontrivial UNNS-selected mode transition or history-dependent selection. No novel physical predictive advantage is claimed.
