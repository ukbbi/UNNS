# Affine Defect-Ray Result Report

## Verdict

**PROVED.**

For every positive affine monoid \(H\) with

\[
\operatorname{rank}H\ge2,
\qquad
\operatorname{ARD}(H)>0,
\]

the non-primal locus contains an infinite affine ray:

\[
\exists a\in\mathcal A(H),\ \exists\rho\in H\setminus\{0\}
\quad\forall n\ge0:\quad
 a+n\rho\notin P(H).
\]

Hence \(H\setminus P(H)\) is necessarily unbounded.

## Proof spine

1. `ARD>0` forces a non-prime atom.
2. Minimal atomic reduction produces an irredundant equality
   \(a+u=b+v\) with distinct atoms \(a,b\), where \(a\nmid v\) and \(b\nmid u\).
3. Because the cone is pointed, one orientation has \(a-b\notin C\).
4. A violated facet functional \(\lambda\) satisfies \(\lambda(a-b)<0\).
5. Rank at least two makes that facet positive-dimensional, so it contains a nonzero
   \(\rho\in H\) with \(\lambda(\rho)=0\).
6. Translating the witness along \(n\rho\) preserves the obstruction for every \(n\).

## Retained-control instantiation

The general construction was instantiated on all four retained affine failure controls:

- `NORMAL_PARITY`
- `NORMAL_CONE2`
- `NONNORMAL_2D`
- `NORMAL_SQUARE3`

The regression script checked 25 translated witnesses per system, 100 instances total.
These checks validate the concrete instantiations; the theorem itself is proved algebraically.

## Rank transition

Combined with the established rank-one theorem:

\[
\boxed{
\begin{array}{ccl}
\operatorname{rank}H=1,\ \operatorname{ARD}>0
&\Rightarrow& H\setminus P(H)\text{ finite},\\[1mm]
\operatorname{rank}H\ge2,\ \operatorname{ARD}>0
&\Rightarrow& H\setminus P(H)\text{ contains an infinite affine ray}.
\end{array}}
\]

Thus the finite-core versus persistent-channel distinction is a genuine dimension-sensitive
structural theorem.

## Conway / UNNS consequence

Higher-dimensional relation defects cannot in general be removed merely by moving to larger
structural scale.  A defect can be transported indefinitely along a face of the admissible cone.
The audited omnific architecture must therefore be read as a mechanism that establishes primality
at the structural base and preserves it under descent/transport, preventing such a persistent
route defect from surviving.

## Primary files

- `02_NONREF/systems/AFFINE_DEFECT_RAY_THEOREM.md`
- `04_PROOF_MAP/output/AFFINE_DEFECT_RAY_INSTANCES.csv`
- `scripts/BUILD_AFFINE_DEFECT_RAYS.py`
- `outputs/records/AFFINE_DEFECT_RAY_RESULT.json`
