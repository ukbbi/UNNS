# UNNS Arithmetic Dynamics

**Arithmetic Geometry, Generative Routes, Graph Structure, and Symbolic Dynamics in the UNNS Substrate**

Research source collection of the **UNNS Research Collective**.

## Overview

This collection contains mathematical investigations of integer generation, arithmetic graph geometry, intrinsic reachability, finite-control selection, prime and Fibonacci structures, symbolic dynamics, and entropy in the UNNS Substrate.

The central arithmetic transition is

$$
T_N(x)=x\frac{(N+1)^2}{N},\qquad N\mid x,\quad x,N\ge1.
$$

Its undirected arithmetic graph has vertices $\mathbb N_{>0}$ and edges

$$
\{kN,\;k(N+1)^2\},\qquad k,N\ge1.
$$

The research develops several distinct mathematical objects arising from these transitions: graph distances, admissible routes, autonomous selectors, finite-state mechanisms, arithmetic cycles, prime-valuation dynamics, and symbolic spaces of admissible histories.

## 1. Metric Geometry

**Folder:** [`01_metric_geometry/`](01_metric_geometry/)

### UNNS_U1_BND_v001 — Bounded Successor Distance

Establishes the sharp universal distance law

$$
\sup_{n\ge1}d_G(n,n+1)=6.
$$

The upper bound is constructed from nine exact polynomial path identities covering the required residue classes. Sharpness is witnessed by the certified distance $d_G(163,164)=6$.

The release contains the mathematical manuscript, path identities, exact neighbour-enumeration engines, distance tables, figures, and verification reports.

## 2. Arithmetic Routes and Generative Selectors

**Folder:** [`02_routes_selectors/`](02_routes_selectors/)

This group investigates how arithmetic paths are constructed, how their labels can be determined from the current integer, and how finite-control mechanisms generate specified sequences.

### UNNS_U2_001_v001 — Intrinsic Generative Selectors

Develops a finite-control arithmetic selector that traverses successive positive integers as waypoints, using the graph's bounded successor routes.

Principal results include a 43-state controller and the sharp doubling-distance theorem

$$
\sup_{n\ge1}d_G(n,2n)=5.
$$

Contains selector implementations, control automata, route verification, trajectory data, and mathematical proofs.

### UNNS_U2_SQ_v001 — Squares and Power Sequences

Establishes the sharp consecutive-square distance law

$$
\sup_{n\ge1}d_G(n^2,(n+1)^2)=5,
$$

using 24 symbolic route identities and an exact lower-bound certificate.

Develops multiplicative power lifting,

$$
d_G(x^k,y^k)\le k\,d_G(x,y),
$$

alongside finite-control selectors for squares and fixed powers.

Contains polynomial path certificates, exact square-distance tables, selector programs, and verification results.

### UNNS_U2_FP_v001 — Fibonacci Numbers and Prime Geometry

Investigates arithmetic graph distances involving prime numbers and successive Fibonacci numbers.

Results include the prime-neighbour formula

$$
\mathrm{Nbr}(p)=\{4p,(p+1)^2\}.
$$

certified prime-distance examples, exact finite-distance tables, and computationally validated Fibonacci path families.

The release also examines the information required by arithmetic selectors.

### UNNS_U2_FP_SYM_v001 — Symbolic Fibonacci Route Certificates

Extends the Fibonacci route investigation through exact symbolic certificates covering all twelve residue classes of Fibonacci indices.

Establishes the uniform bound

$$
d_G(F_k,F_{k+1})\le12,\qquad k\ge2.
$$

Includes algebraic path identities, class certificates, route data, symbolic verification, and finite-control selector analysis.

### UNNS_U2_FP_R3_v001 — Algebraic Parameter Recovery

Studies the recovery of Fibonacci route parameters from the current arithmetic state.

Contains algebraic monotonicity certificates, state-based Fibonacci recognition, controller simulations, and an audit of the arithmetic information needed to identify route labels.

Distinguishes graph-step counts from parameter-recovery computation.

### UNNS_U2_KI_v001 — Exact Knowledge Identities

Develops symbolic knowledge identities for arithmetic route selectors.

Investigates which labels can be recovered through constants, affine formulas, and square-root expressions, and computes algebraic degrees for more complicated cases.

Includes optimized controller implementations, symbolic identity certificates, degree calculations, and computational cost comparisons.

### UNNS_U2_TI_v001 — Target-Blind Arithmetic Selection

Investigates target-independent selection mechanisms using a defined graph-local observation language.

Contains registered selector experiments, information accounting, symbolic controllers, and verification reports.

### UNNS_U2_TI_DYN_v001 — Maximal-Neighbour Dynamics

Establishes the exact local-degree structure of the arithmetic graph:

$$
\deg_G(x)=\tau(x)+\left|\{q\ge2:q^2\mid x\}\right|.
$$

Proves that the largest neighbour of $x$ is $(x+1)^2$, that prime vertices have degree two, and that no vertex has degree three.

Contains the mathematical addendum, degree-structure visualization, exact verification script, and provenance record.

### UNNS_U2_RN_v001 — Ranked-Neighbour Dynamics

Investigates graph-local arithmetic selection based on ranked neighbours and observable vertex properties.

Contains selector definitions, registered experiments, computational graph engines, state-transition records, and verification reports.

## 3. Arithmetic Graph Structure

**Folder:** [`03_graph_structure/`](03_graph_structure/)

### UNNS_U3_v001 — Universal Sequence Embeddings and Structural Preservation

Develops the arithmetic graph as a setting for sequence representation, graph-local operations, structural constraints, and admissible symbolic constructions.

Contains graph engines, sequence-embedding experiments, registry data, computational certificates, and a mathematical manuscript.

Its results distinguish proved structural statements from bounded computational observations and proposed extensions.

### UNNS_U3_COR_v001 — Corrected Cycle and Girth Structure

Contains the corrected cycle-theoretic results for the arithmetic graph.

The graph is triangle-free, with

$$
\mathrm{girth}(G)=4,
\qquad
\mathrm{girth}_{\mathrm{odd}}(G)=5.
$$

Includes mathematical corrections, proofs, exact graph checks, and verification records associated with the original U3 release.

## 4. Symbolic Dynamics and Entropy

**Folder:** [`04_symbolic_dynamics/`](04_symbolic_dynamics/)

This group studies admissible arithmetic histories, their symbolic representations, intrinsic graph entropy, autonomous prime selection, and structural restrictions on generative dynamics.

### UNNS_U4_SPEC_v001 — Symbolic and Generative Dynamics Specification

Contains a mathematical specification and a structured registry of claims concerning generative dynamics, symbolic realizability, structural obstructions, and universality criteria.

Includes claim-status records, hypotheses, dependencies, mathematical sketches, compatibility information and verification utilities.

The specification distinguishes established results from conditional statements and open constructions.

### UNNS_U4_STAGE2_v001 — Memory-Two Admissible Histories

Studies symbolic systems constructed from finite arithmetic graph histories, including memory-dependent admissibility and graph-local selection.

Contains proofs, a theorem-status registry, independent graph engines, registered experiments, symbolic surveys, and verification reports.

The release develops the memory-two nonbacktracking history construction used in subsequent entropy research.

### UNNS_U4_M2_ENT_v001 — Intrinsic Nonbacktracking Entropy

Studies the symbolic entropy of admissible nonbacktracking histories in finite arithmetic graph subsystems.

Establishes a lower bound of the form

$$
h_{\mathrm{NB}}(F(x))
\ge\frac14\log\bigl(\tau(x)-1\bigr),
$$

and unbounded entropy capacity over the constructed finite subsystems.

Contains proof records, finite-state symbolic matrices, exact rational entropy certificates, numerical spectral data, and verification scripts.

### UNNS_U4_GEN_v001 — Autonomous Prime-Valuation Generation

Develops arithmetic generation through prime-valuation updates and autonomous state-based selection.

Results include finite reduction of prime-fire dynamics to primes $2$ and $3$, eventual periodicity for specified selectors, and the maximum-prime-power selector (MAXPP).

For MAXPP, the branch itinerary is Sturmian, with

$$
p(n)=n+1,\qquad h=0,
$$

and is non-eventually-periodic from every initial integer greater than one.

Contains mathematical proofs, registered experiments, prime-valuation engines, verification scripts, and structured theorem records.

## 5. Document Variants

**Folder:** [`90_document_variants/`](90_document_variants/)

Contains a separate PDF version of `UNNS_U2_TI_DYN_v001`. The primary mathematical release and its LaTeX source are located in `02_routes_selectors/UNNS_U2_TI_DYN_v001/`.

## Research Records and Indexes

The repository root also contains:

| File | Contents |
|---|---|
| [`SOURCE_INDEX.csv`](SOURCE_INDEX.csv) | Index of the 16 research releases, their locations and source identifiers |
| [`SOURCE_PROVENANCE.md`](SOURCE_PROVENANCE.md) | Release provenance and archive SHA-256 fingerprints |
| [`MANUSCRIPT_REFERENCE_MAP.md`](MANUSCRIPT_REFERENCE_MAP.md) | Relationships between research releases and the associated mathematical manuscript subjects |
| [`COLLECTION_SHA256SUMS.txt`](COLLECTION_SHA256SUMS.txt) | File-integrity hashes for the collection |
| [`CURATION_LOG.md`](CURATION_LOG.md) | Collection-level file records and document-variant information |

Each versioned research folder contains its own `README.md` describing the corresponding results and the files specific to that release. Depending on the release, these include LaTeX manuscripts, PDFs, figures, computational engines, numerical datasets, symbolic certificates, theorem registries, and machine-readable verification reports.

---

**UNNS Research Collective**

UNNS Substrate — [unns.tech](https://unns.tech)

Source repository — [github.com/ukbbi/UNNS](https://github.com/ukbbi/UNNS)
