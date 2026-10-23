# Formal audit: necessary assumptions are not derived

## A. Normalization without noncontextuality
Consider contexts C={e,a} and D={e,b}. Define probabilities mu_C(e)=1/4, mu_C(a)=3/4, mu_D(e)=3/4, mu_D(b)=1/4. Each context is a valid normalized probability distribution, but there is no single context-independent function mu(e) reproducing both. This is a counterexample to normalization -> noncontextuality. Interpret event e as common only when an *event-identity principle* has been supplied. Here it is deliberately postulated for the test.

## B. Two-dimensional frame obstruction
For a real two-dimensional unit vector with angle theta, one can define f(theta)=(1+epsilon*cos(2*theta))/2, with |epsilon|<=1. Then f(theta+pi/2)=1-f(theta), so the orthogonal pair sums to 1. This *particular* example is Born-representable in 2D when |epsilon|<=1, so it is not a non-Born counterexample. Instead choose f(theta)=(1+epsilon*cos(6*theta))/2, 0<epsilon<=1. Its orthogonal companion satisfies f(theta+pi/2)=1-f(theta), and it is nonnegative, but it cannot be represented as v^T rho v for a fixed real symmetric 2x2 density matrix: the latter has only constant and second-angle harmonics. Thus two-dimensional frame normalization does not imply a Born density representation.

## C. Finite 3D q-frame audit
For an orthonormal frame with first row components (1,0,0), the total raw power weight equals 1 for every q>0. A rotated frame with first row (1/sqrt(3),1/sqrt(3),1/sqrt(3)) has raw weight 3^(1-q/2); it equals 1 only for q=2. This proves uniqueness for this *particular power-law family under assumed frame weight invariance*. It neither derives invariance from proto-closure nor establishes a general representation theorem.

## D. Conditional known theorem
The standard Gleason representation theorem applies to dimension >=3 projection measures and relies on noncontextual additivity. It is not a statement that proto-closure supplies those assumptions, and does not directly cover all generalized measurements without additional results. No unique state is inferred from the toy recurrences.

## E. Open UNNS bridge tasks
- Define observable event identity and how it survives admissible rewriting / refinement.
- Define orthogonality/exclusivity on generative events without starting from a Hilbert inner product.
- Derive disjoint coarse-graining and context-independent weights from a mechanism-level conservation rule, or produce counterexamples and stop.
- Identify composition rule, distinguish local causality from measurement independence, and extend beyond real two-dimensional states.

**Final claim:** R0–R3 provide validated obstructions/conditional mathematics. R5 remains BLOCKED/NOT DERIVED.
