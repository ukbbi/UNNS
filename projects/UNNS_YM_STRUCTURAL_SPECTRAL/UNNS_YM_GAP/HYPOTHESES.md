# Hypotheses

## H1 — Vacuum Boundary Non-Crossability

There exists a nonzero UNNS structural separation between the Yang–Mills vacuum and every non-vacuum admissible physical state represented within a valid gauge-invariant ladder family.

Symbolically,

\[
\inf_{X\in\mathcal A_{\rm YM},\,X\neq V} D_{\rm YM}(X,V)=\delta_{\rm YM}>0.
\]

The project does not assume in advance that `D_YM` is a universal scalar metric. During YM-1/YM-2 it may be instantiated by a frozen structural coordinate or a reproducible combination of canonical chamber outputs.

## H2 — Refinement Stability

The positive separation is not a discretization artifact:

\[
\liminf_{r\to\infty}\delta_{\rm YM}(r)>0,
\]

where `r` denotes the predefined refinement sequence.

A boundary that systematically collapses toward zero under refinement does not support H2.

## H3 — Gapless Non-Generability

A deliberately constructed sequence whose physical gap proxy approaches zero cannot remain inside the same admissible structural regime across refinement.

Expected signature:

\[
g_n\rightarrow0^+
\quad\Longrightarrow\quad
\text{stable structural boundary event before }g_n=0.
\]

The boundary event may appear as canonical rejection, collapse, non-generability, loss of persistence, or another preregistered canonical structural transition.

## H4 — Massive-Branch Persistence

Matched finite-gap branches remain admissible and structurally persistent over the same refinement program in which the gapless branch fails.

This hypothesis prevents the project from interpreting general numerical instability as evidence of a vacuum boundary.

## H5 — Gauge-Invariant Representation Robustness

The existence of the obstruction is reproduced in more than one independently motivated gauge-invariant observable representation.

Numerical metric equality is not required; structural agreement is.

## H6 — Null Specificity

Matched nulls that preserve simple smoothness, amplitude, or finite-size characteristics do not reproduce the same refinement-stable boundary at comparable frequency.

This tests whether the result is specific to the Yang–Mills structural organization rather than a generic property of decaying sequences.

## H7 — Physical Bridge

There exists a controlled monotone lower relation between structural separation and a physical spectral or correlation scale:

\[
M_{\rm phys}\ge F(D_{\rm YM})
\]

for an explicitly defined domain, with `F(d)>0` for `d>=δ_YM`.

Without H7, the result remains structural evidence rather than a mass-gap theorem.

## H8 — Continuum Relevance

The non-crossability structure persists under continuum-oriented refinement rather than being tied to a fixed lattice spacing or finite volume.

This is the hypothesis that must eventually connect computational evidence to the continuum Yang–Mills problem.

# Explicit competing hypotheses

## H0-A — Crossable Vacuum

Admissible branches can approach the vacuum with arbitrarily small positive gap proxy while remaining structurally admissible.

## H0-B — Artifact Boundary

An apparent structural boundary exists at coarse resolution but moves toward zero or disappears under refinement.

## H0-C — Representation Boundary

The obstruction is present only in one encoding/observable family and is absent in another physically equivalent gauge-invariant representation.

## H0-D — Generic-Sequence Boundary

Matched non-Yang–Mills nulls reproduce the same effect, indicating that the boundary is caused by generic sequence geometry rather than Yang–Mills organization.

# Decision discipline

A positive result must identify which hypotheses are supported separately.  
Failure of H7 does not erase a valid H1–H6 structural finding, but it prevents interpretation as a proof of the physical mass gap.
