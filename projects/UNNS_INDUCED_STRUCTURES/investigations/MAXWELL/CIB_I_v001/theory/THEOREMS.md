# CIB-I v001 — Exact comparative results

**Research register, not a manuscript.** The fixed original UNNS transition is

\[T_N(m)=\frac{m}{N}(N+1)^2,\qquad N\in\mathbb N_{>0},\quad N\mid m.\]

Scope: positive Fourier indices of a 2π-periodic scalar Maxwell reduction, with **one independently specified dielectric profile** per benchmark medium. There is no claim that this Maxwell dynamics implements the full-field map \(E(z)\mapsto E(r_Nz)\).

## The physical input (fixed before the edge comparison)

Let \(D=a/b\in(0,1)\), \(a,b\) coprime. Take a periodic binary dielectric profile

\[\varepsilon_D(z)=1+\eta u_D(z),\quad u_D(z)=\mathbf1_{[0,2\pi D)}(z)-D,\]

and \(|\eta|\) sufficiently small that \(\varepsilon_D>0\). A binary layered medium with fill fraction \(D\) is a standard photonic/periodic-wave construction; here it is a **synthetic analytic control**, not a measured independent sample. Consider the scalar transverse Maxwell eigenvalue problem

\[-E''(z)=\omega^2\varepsilon_D(z)E(z).\]

In the free Fourier basis \(E(z)=\sum_{m\in\mathbb Z}c_me^{imz}\), its generalized eigenproblem is

\[m'^2c_{m'}=\omega^2\big(c_{m'}+\eta\sum_m \widehat u_D(m'-m)c_m\big).\]

Thus the *normalized first-order dielectric Fourier coupling kernel* is \(K_D(m',m)=\widehat u_D(m'-m)\). This is a statement about the operator matrix and perturbative mixing. A zero entry is **not** an all-orders dynamical blockade.

## T1 — Exact UNNS harmonic gate [PROVED]

Every single UNNS edge can be written \(m=tN\), \(m'=t(N+1)^2\), for positive integers \(N,t\). Its Fourier shift is

\[\boxed{q=m'-m=t(N^2+N+1).}\]

For a *single-harmonic grating of order q*, the direct edge \(m\to m'\) coincides with a first-order Maxwell Fourier coupling iff \(N^2+N+1\mid q\), and then \(t=q/(N^2+N+1)\). Each admissible label \(N\) gives at most one edge for a specified positive q; the labels are finite since \(N^2+N+1\le q\).

For a finite, fixed set of spatial harmonics Q, all first-order matching UNNS edges are finite in number and satisfy \(m\le\max(Q)/3\). For fundamental single-harmonic \(q=1\) there are zero first-order UNNS edges. MUG-I v009 used q=6 and 28, exactly producing \((m,N,m')=(2,1,8)\) and \((8,2,36)\).

## T2 — Exact binary-medium selection gate [PROVED]

For any nonzero Fourier index q,

\[\widehat u_D(q)=\frac{1-e^{-2\pi iqD}}{2\pi iq}=e^{-i\pi qD}\frac{\sin(\pi qD)}{\pi q}.\]

Since \(D=a/b\) is reduced,

\[\boxed{\widehat u_D(q)=0\iff b\mid q.}\]

Consequently the first-order induced graph \(G_D^{(1)}=G_{\mathrm{UNNS}}\cap\{(m,m'): \widehat u_D(m'-m)\ne0\}\) retains an original edge labelled \(N\) and source multiple \(t\) iff

\[\boxed{b\nmid t(N^2+N+1).}\]

This is a *joint structural classification* produced by the unchanged arithmetic and a separately chosen physical-material Fourier kernel. It applies only to the linear material matrix / first-order mixing, not all orders of Maxwell evolution.

## T3 — Prime residue-class suppression theorem [PROVED]

For \(b=p\) prime, a label family \(N\) is suppressed for **every** positive source multiple \(t\) precisely when

\[N^2+N+1\equiv0\pmod p.\]

For \(p=3\), the single root class is \(N\equiv1\pmod3\). For other primes, roots are nontrivial cube roots of unity in \(\mathbb F_p^\times\); therefore there are two root classes when \(p\equiv1\pmod3\) and none when \(p\equiv2\pmod3\) (including p=2). Indeed \((N-1)(N^2+N+1)=N^3-1\), and for p≠3 any root is not 1. Since the multiplicative group has order p−1, it contains an element of exact order 3 iff 3|p−1.

Examples: p=3 blocks N≡1; p=7 blocks N≡2,4; p=13 blocks N≡3,9. For unblocked labels, *particular* edges can still be suppressed whenever p|t. For p=2 all \(S_N=N^2+N+1\) are odd, so a 50% duty profile retains exactly edges with odd source quotient \(t=m/N\).

The theorem is an exact infinite-family **first-order material-admissibility** classification; it does not imply whole-field UNNS dynamics in Maxwell.

## T4 — The equal-endpoint UNNS diamond responds to non-tuned dielectric profiles [PROVED]

Two valid histories starting at index 2 and ending at 36 are A: \(2\to8\to36\), with Fourier shifts (6,28), and B: \(2\to9\to36\), with shifts (7,27). Under the independent fixed binary-medium profile:

- D=1/2: A has zero first-order coupling on both edges; B has nonzero first-order coupling on both edges.
- D=1/3: both two-step routes have at least one zero first-order edge, but on different steps.
- D=1/5: both routes have nonzero first-order couplings on both edges.

This refers to *composable nonzero entries* of the material matrix. It is not a claim that one or the other entire history is dynamically realized or isolated under an unpulsed stationary material.

## T5 — An identifiability obstruction [PROVED]

Suppose a first-order operator has spatially translation-invariant normalized matrix elements \(K(m',m)=F(m'-m)\). Any two directed edge collections having exactly the same **multiset of differences** \(m'-m\) have identical aggregated Fourier coupling scores \(\sum |F(q)|^2\) and identical counts of zero/nonzero entries, for all profiles F.

We construct a deterministic source-scrambled control which preserves the difference multiset of every UNNS edge in 1≤m<m'≤512. It produces **exactly the same coupling scores in all eight media**, despite changing the intermediate graph topology. Therefore these aggregated first-order Fourier statistics **cannot distinguish the UNNS edge graph from a q-matched non-UNNS graph**. This limitation does not rule out more informative path-level, dynamical, or polarization observables.

## T6 — Cross-framework equivalence of the spatial Fourier kernel [PROVED]

The same material Fourier matrix \(\widehat u_D(m'-m)\) appears as a potential perturbation in a periodic 1D Schrödinger problem \(H=-\partial_z^2+\eta u_D(z)\), and as a mass/density matrix in a scalar 1D acoustic generalized eigenproblem \(-p''=\omega^2(1+\eta u_D)p\). The eigenvalue prefactors, normalization, units, and dynamical responses differ; **spatial selection by q alone does not identify Maxwell specifically**. The included FFT-based numerical oracle checks the equality of these normalized first-order kernels for six mode pairs and four independent media.

## T7 — Finite-window structural outcomes [VERIFIED EXACT FINITE]

On 1≤m<m'≤512, the UNNS first-order graph has 301 edges. With binary fill fractions D=1/2,1/3,1/5,1/7, it retains respectively 155, 97, 248, 189 nonzero first-order edges. A 1/3-duty profile suppresses the entire label N≡1 mod 3 family; the observed depletion is predictable from T3. The q-preserving control ties all eight profiles exactly in the aggregate first-order metrics.

The **post-protocol exploratory** topology counts also distinguish the graph structures: for D=1/5, the UNNS-restricted finite graph has 173 composable two-edge routes and 28 common-source/common-target two-route pairs, compared with 42 two-edge routes and zero such pairs in the source-scrambled control. These are graph-count differences, **not** measured Maxwell multipath amplitudes or a degree-matched statistical superiority test.

## Meaning and limits

This research yields an exact interaction between the unchanged UNNS grammar and independently specified periodic-material Fourier structure, with infinite label-class gates and induced path-topology changes. It shows **no unique Maxwell relationship and no independent UNNS physical predictive advantage** under the present first-order, q-only observables. A fair further test must use independent material measurements (not engineer q), full electromagnetic dynamics and degree/path-matched alternative grammars with prospectively locked metrics.
