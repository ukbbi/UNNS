# GCT-III: Observable-Null Refinement Theorem Audit v003

## Exact question

Does the independently documented UNNS substrate imply

\[
\Pi(X)=0\quad\Longrightarrow\quad B(X,Y)=B(Y,X)=0\qquad \text{for every route }Y?
\]

The answer for the *documented source axioms reviewed* is **no**. Below is a countermodel. This is not a universal statement about all possible future UNNS definitions.

## Source-grounded axioms actually used

1. A UNNS substrate is a layer of states, operations, admissible domains, routes, and structural-status criteria (introductory definition).
2. A mechanism is \(M=(\Sigma,R,C,O)\). Structural state equivalence is specified by admissible renaming/canonicalization, not by equality of an arbitrary observable projection (Mechanisms, Definitions 3-4).
3. A refinement sequence may recur on multiple structurally distinct states (Definitions 5-7).
4. An exact UNNS morphism satisfies \(\Pi\circ T=T_{obs}\circ\Pi\) (Introduction, section Morphisms).

No quoted source requires a bilinear interaction to factor through \(\Pi\).

## Source-compatible extension/countermodel

Take the additive route space \(\mathcal R=\mathbb R^3\oplus\mathbb R^3\), with two distinguishable route channels (0,1). Define:

\[
\begin{aligned}
\Pi(u,v)&=u+v,\\
T(u,v)&=(v,u),\\
T_{obs}(w)&=w,\\
B((u,v),(x,y))&=-u\cdot x-v\cdot y.
\end{aligned}
\]

Let route labels be structurally distinct, and allow identity renaming/canonicalization only. The rewriting rules swap the two channels on each refinement step. Both channel states are admissible. This creates a genuine period-two orbit, hence nontrivial recurrence as defined in the structural-closure text.

The exact morphism relation holds:

\[
\Pi(T(u,v))=u+v=T_{obs}(\Pi(u,v)).
\]

Moreover \(B\) is bilinear, invariant under simultaneous \(T\), and covariant under rotations acting identically in both channels. The normalized elementary routes \(r_0(a)=(a,0)\), \(r_1(a)=(0,a)\) each obey aligned anticorrelation \(B(r_i(a),r_i(a))=-1\) when \(\|a\|=1\).

Now define \(X=r_0(e_x)-r_1(e_x)=(e_x,-e_x)\) and \(Y=r_0(e_x)\).

\[
\Pi(X)=0,\qquad B(X,Y)=-1\neq 0.
\]

The sought observable-null condition **fails** in this admissible mathematical extension. No experimental statement about entangled particles follows from this countermodel; it is a logical test of the proposed implication.

## Factorization criterion (exact mathematical equivalence)

For a surjective linear \(\Pi:\mathcal R\to V\) and bilinear \(B\), the following are equivalent:

- There exists a well-defined bilinear \(b:V\times V\to\mathbb R\) such that \(B(X,Y)=b(\Pi X,\Pi Y)\).
- \(\ker\Pi\) lies in the left and right radicals of \(B\); that is, \(B(N,Y)=B(Y,N)=0\) for all \(N\in\ker\Pi\) and all \(Y\).

**Proof:** If the factorization exists, \(b(0,\Pi Y)=b(\Pi Y,0)=0\) by bilinearity. Conversely, choose lifts \(X,Y\) of observable vectors \(u,v\). Set \(b(u,v)=B(X,Y)\). Any two lifts differ by elements of \(\ker\Pi\); the radical condition makes the definition lift-independent. Bilinearity descends from \(B\). QED.

This explains precisely why deriving the condition requires a new structural premise about **interaction equivalence**, not just an exact morphism of recursive action.

## Verdict

`NOT_ENTAILED_BY_DOCUMENTED_UNNS_AXIOMS`.

The candidate theorem remains conditional on an extra premise that all interactions descend through observable equivalence. In the source framework, route histories can remain structurally distinct despite equal projected observables. It is not established that this difference is irrelevant to interactions.
