# Generative Information Geometry in the UNNS Substrate

**UNNS Research Collective**  
**Research archive:** `projects/UNNS_Generative_Information_Geometry`  
**Repository:** [ukbbi/UNNS](https://github.com/ukbbi/UNNS)  
**Research programme:** Generative Information Geometry (GIG)

## Overview

Generative Information Geometry (GIG) is a mathematical research programme within the **UNNS Substrate**. It investigates how the rules of generation determine the histories that are possible, how different histories can lead to the same observed result, how arithmetic and symbolic admissibility shape the topology of history spaces, and which structural observations are sufficient to recover information lost under a projection.

Its guiding question is:

> **How much mathematical information does a generative history contain beyond its final state, how is that information organized by admissibility and topology, and which parts can be recovered from observable projections?**

The programme develops two connected lines of work:

- **GIG-I:** mathematical foundations of ancestry, arithmetic realizability, permutohedral history geometry, homological obstructions, and higher-dimensional construction.
- **GIG-INFO:** information recovery, conditional entropy, accessibility signatures, forbidden-history duality, reduction to dead-set nerves, and symbolic-grammar transfer.

**SELECT-II** provides a precisely defined arithmetic grammar for many of the main theorems. It is **one UNNS grammar**, not a definition or limitation of the whole UNNS Substrate. Later GIG-INFO investigations also consider non-integer symbolic histories and their admissibility constraints.

This directory is intended as a **versioned, citable research-source collection**. Each release retains its own theory, results, experiments, checks, certificates, and provenance as supplied. The archive should not be confused with an active workspace for revising the manuscript or modifying frozen releases.

## Main mathematical results

### Generative ancestry and information

A single endpoint may have several distinct admissible generating histories. For a finite history fibre \(\mathcal F_t\), the uniform-history ambiguity is \(\log_2|\mathcal F_t|\); Shannon entropies require an explicitly specified probability distribution. GIG-I develops exact ancestry counts, source/content/recombination-class decompositions, and legal-swap accessibility profiles. For endpoint **72**, four complete histories give **2 bits** of uncertainty under the uniform convention.

### Arithmetic admissibility and history topology

For distinct-label SELECT-II contents, divisibility governs admissible orderings and the activation of cells in associated permutohedral complexes. The research establishes closure and threshold laws, source-divisibility filtrations, and exact arithmetic criteria for the survival or filling of specific homology classes. Finite certified examples exhibit nontrivial **\(H_2\), \(H_3\), and \(H_4\)**. General claims beyond the stated grammar, dimensions, and hypotheses are not implied.

### History counts do not determine topology

GIG-INFO v002–v003 certify systems with the **same number of admissible arrangements but different second homology**. In the main six-label arithmetic census, **346,859** source regimes over **8,008** contents include **158** regimes with \(\beta_2>0\). The later pooled six-label analysis covers **609,983** regimes with **290** positives. These are explicitly bounded computational domains, not universal frequencies.

Radius-2 accessibility and the two-step walk statistic reveal distinctions invisible to history counts or several first-order graph summaries. However, purportedly universal scalar recoverability signatures, including a general \((Q,S_2)\) separation principle, were **refuted outside the tested arithmetic class**. In-sample zero conditional entropy is also distinct from out-of-sample predictive performance.

### Forbidden-history reconstruction

For the specified six-label **prefix-defined** history systems, the work uses Alexander duality, an intersection lemma, and the nerve theorem to establish an exact relationship:

\[
\beta_2(K_A)=\dim_{\mathbb F_2}H_1(N[D_A];\mathbb F_2).
\]

Here \(K_A\) is the admissible-history complex and \(N[D_A]\) is the compatibility nerve built from **dead prefix sets**. Thus second homology of the admissible complex can be recovered from first homology of a forbidden-history construction. Strong collapses often reduce this nerve to a much smaller homotopy-equivalent core. This is a theorem-backed sufficient reconstruction, **not** a universal minimal-complexity algorithm.

### Symbolic generative grammars

For the defined six-event Hamiltonian-path construction, **pairwise directed-transition constraints** yield \(\beta_2=0\) (a computer-assisted theorem). In contrast, a certified example forbidding two consecutive triples has \(\beta_2=5\). Consequently, nontrivial history topology is not confined to integer-valued grammars; the organization and locality of constraints matter. No theorem about all alphabet sizes or all UNNS grammars is claimed.

## Research release index

The fifteen research folders below are the source records for this collection. Read each folder's `README.md`, `THEORY/`, and `RESULTS/report.md` for exact statements, hypotheses, evidence, and instructions.

### I. Generative geometry and homology — `GIG_I_*`

| Release | Research focus | Principal contribution |
|---|---|---|
| [`GIG_I_v001`](GIG_I_v001/) | Generative ancestry and information | Exact history fibres, information decomposition, accessibility profiles, homology distinctions and initial finite census. |
| [`GIG_I_v002`](GIG_I_v002/) | Arithmetic realizability | Threshold closure, commuting-swap cube factorization, graph/cell reconstruction and finite separation tests. |
| [`GIG_I_v003`](GIG_I_v003/) | Higher-dimensional boundary rigidity | Ordered-block factorization, exact face thresholds, divisibility filtrations, third-boundary-rank obstructions and \(H_2\) anchor laws. |
| [`GIG_I_v004`](GIG_I_v004/) | Arithmetic hole survival | Parametric \(H_2\) survival criteria, systematic six-label search and explicit seven-label \(H_3\) certificates; later gate claims refined. |
| [`GIG_I_v005`](GIG_I_v005/) | Exact filling families — Stage 1 | Finite-exact criterion for a common \(H_2\) cycle and counterexamples to overly strong gate-necessity assertions. |
| [`GIG_I_v005_S2`](GIG_I_v005_S2/) | Arithmetic \(H_2\) obstruction atlas | Certified cycles, minimal filling families, classification and held-out coverage tests; atlas not claimed exhaustive. |
| [`GIG_I_v005_S3`](GIG_I_v005_S3/) | \(H_2\to H_3\) lifting | Chain-level lifting identity, alternative fillings, certified higher cycles and arithmetic seven-label tests. |
| [`GIG_I_v006`](GIG_I_v006/) | Iterated obstruction lifting | Filling-dependence criteria and certified arithmetic \(H_4\) construction. |
| [`GIG_I_v007`](GIG_I_v007/) | Filling-dependence map | Induced map from a facet complex, its rank and kernel, with finite tests of injectivity and dependence. |

### II. Information and recovery — `GIG_INFO_*`

| Release | Research focus | Principal contribution |
|---|---|---|
| [`GIG_INFO_v001`](GIG_INFO_v001/) | Information recovery at arithmetic transitions | Two fixed-anchor survival ensembles; history count alone identifies survival within their comparable-source families. |
| [`GIG_INFO_v002`](GIG_INFO_v002/) | Entropy–topology separation | Equal-count/opposite-homology witnesses; entropy profiles over the 346,859-regime six-label census. |
| [`GIG_INFO_v003`](GIG_INFO_v003/) | Second-neighbourhood geometry | Proved two-swap ball identity, sharp witness, discriminating walk statistics and a failed preregistered held-out prediction. |
| [`GIG_INFO_v004`](GIG_INFO_v004/) | Recoverability and grammar transfer | Forbidden-history Alexander duality, scalar-signature counterexample, natural/balanced information ensembles, out-of-sample tests and symbolic grammars. |
| [`GIG_INFO_v005`](GIG_INFO_v005/) | Forbidden-history topology | Dead-set nerve theorem, certified nonbounding cycles, six-event pairwise-adjacency locality theorem and triple-restriction counterexample. |
| [`GIG_INFO_v006`](GIG_INFO_v006/) | Mathematical synthesis and minimal observation | Self-contained theorem records, standalone certificate verifier, exhaustive dead-set core analysis and the v005 provenance erratum. |

## How to navigate and reproduce the work

Individual packages typically contain some of the following (the precise layout and dependencies vary by release):

```text
THEORY/          definitions, theorem registers, proofs and scope conditions
RESULTS/         exact results, reports, tables and experimental findings
ENGINE/          mathematical implementations
EXPERIMENTS/     deterministic searches, calculations and runners
CERTIFICATES/    explicit cycles, cochains and other verification records
TESTS/           package-specific automated checks
PROVENANCE.md     inherited source references, scope and run status
MANIFEST.json     SHA-256 records for the package and/or parent releases
README.md        package-specific starting instructions
```

**Start with each package's own instructions:** there is no single universal command to reproduce all releases. Most mathematical engines use Python **3.10 or later**; some larger information experiments require additional packages (documented locally). Some full censuses are computationally expensive. Where a release marks prior tests or computations as `NOT_RERUN`, do not interpret its new tests as rerunning inherited work.

For a particularly compact independent check of the later central results, run from this directory:

```powershell
python .\GIG_INFO_v006\VERIFY\standalone_verify.py
```

This standalone verifier uses the Python standard library and rechecks the finite hypotheses of the six-event adjacency theorem, the triple-rule counterexample, and the supplied positive certificates according to its documented mode. Consult [`GIG_INFO_v006/README.md`](GIG_INFO_v006/README.md) for details and limitations.

### Reproducibility and provenance notes

- **Version immutability:** preserve each released folder as a source snapshot; publish corrections in separately identified releases or errata rather than silently rewriting the cited version.
- **Hash identification:** cite both the repository commit and the release's `MANIFEST.json` when precise reproducibility matters. Folder names alone do not identify a unique historical build.
- **v005 erratum:** [`GIG_INFO_v006/ERRATUM_v005.md`](GIG_INFO_v006/ERRATUM_v005.md) corrects a parent-path/hash attribution error in `GIG_INFO_v005`. Its reported impact concerns parent identification; the frozen v005 files are not rewritten.
- **Historical parent-build differences:** three GIG-I Stage-5 parent manifests (`v005`, `v005_S2`, `v005_S3`) have differed across previously circulated archive copies. Retain the exact hashes associated with the cited release and resolve build identity before claiming byte-for-byte equivalence.
- **Evidence categories:** distinguish general proofs, computer-assisted theorems, exact finite computations, representative examples, conjectures, and refuted hypotheses. Consult the release theorem registers rather than inferring status from a short index entry.

## Relationship to the comprehensive manuscript

These packages are the **research-source archive** supporting *Generative Information Geometry in the UNNS Substrate: Ancestry, Admissibility, Topology, and Information Recoverability*, attributed to the **UNNS Research Collective**.

The comprehensive manuscript is developed and reviewed **separately** from these frozen research references. A working manuscript directory such as `GIG_MANUSCRIPT_v002/`, if present locally, is **not** part of the fifteen-release source archive and should not be included in the initial research-only Git commit without a separate publication decision.

The manuscript should cite specific theorem/proof locations and package manifest hashes, with the **Git commit ID pinned** once this collection is uploaded. Research packages are not themselves a substitute for complete proofs and appropriately scoped claims in the manuscript.

## Citation and permanent reference

After the research folders have been committed and pushed, obtain the exact revision with:

```powershell
git rev-parse HEAD
```

A stable reference to this collection then has the form:

```text
https://github.com/ukbbi/UNNS/tree/<COMMIT_SHA>/projects/UNNS_Generative_Information_Geometry
```

A particular release can be cited at:

```text
https://github.com/ukbbi/UNNS/tree/<COMMIT_SHA>/projects/UNNS_Generative_Information_Geometry/GIG_INFO_v006
```

**Suggested research-source citation (complete the commit hash after publication):**

> UNNS Research Collective (2026). *Generative Information Geometry in the UNNS Substrate: GIG-I and GIG-INFO Research Releases*. `ukbbi/UNNS`, `projects/UNNS_Generative_Information_Geometry`, Git commit `<COMMIT_SHA>`; individual release manifests as identified in the cited packages.

For a theorem or numerical figure, additionally identify the **release**, **theorem or result label**, and **certificate or result file**. Do not fill in a placeholder commit hash until the push is verified.

## Attribution and scope

**Research authorship:** UNNS Research Collective.  
**Programme:** UNNS Substrate — Generative Information Geometry.  
**UNNS website:** [unns.tech](https://unns.tech/)  
**Repository:** [ukbbi/UNNS](https://github.com/ukbbi/UNNS)

The work uses classical Shannon information theory, combinatorial and algebraic topology, Alexander duality, nerve theory and related mathematics. These classical inputs are not presented as newly invented results. The project-specific contributions are the constructions, precise theorems, counterexamples and verified finite results identified by the individual releases.

This archive does **not** claim a replacement for Shannon entropy, a universal physical entropy law, or a proof of computational advantage in arbitrary applications. Information under genuine generative evolution, as distinct from static source-filtration comparisons, remains outside the completed scope of these releases.
