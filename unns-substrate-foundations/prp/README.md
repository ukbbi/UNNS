# Percolative Realizability Program (PRP)

This directory contains the principal public research artifacts of the **Percolative Realizability Program (PRP)** within the UNNS Substrate research program.

PRP develops and tests **realizability** as a structural coordinate complementary to **admissibility**. The program asks not only whether a structural ladder is internally admissible under the UNNS grammar, but also whether its admissible relations form a connected, traversable, or fragmented realizability structure.

The work in this directory is centered on **STRUC-PERC-I**, the percolative-realizability instrument, and on cross-domain comparison between STRUC-I admissibility diagnostics and realizability diagnostics.

---

## Research context

PRP forms part of the broader UNNS regime-synthesis program.

A public conceptual introduction to the dual-coordinate view is available at:

**The Two Coordinates of Reality**  
https://unns.tech/labs/the-two-coordinates-of-reality

The frozen cross-domain input corpus used by this research is archived separately on Zenodo:

**UNNS Percolative Realizability Corpus — Cross-Domain Structural Ladder Dataset v1.0**  
https://zenodo.org/records/22707994  
DOI: **10.5281/zenodo.22707994**

The Zenodo record is the archival reference for the frozen research inputs. This GitHub directory contains the theory, instrument, analyses, figures, manuscripts, public article, and result artifacts that operate on or interpret that corpus.

---

## Core idea

PRP treats structural realizability as a second coordinate of physical organization.

In simplified form:

- **admissibility** asks whether a ladder satisfies the relevant structural constraints;
- **realizability** asks whether admissible relations actually form a connected structural world;
- together they provide a two-coordinate description of structural existence.

STRUC-PERC-I analyzes the connectivity structure of admissible relations and distinguishes regimes such as:

- full connectivity;
- giant-component realizability;
- tail / fragmented realizability;
- hard disconnection.

This enables direct comparison between local admissibility and global realizability across heterogeneous physical domains.

---

## Contents

### `struc_perc_i_v2_4_0.html`

Frozen interactive / browser-readable build of **STRUC-PERC-I v2.4.0**.

This is the principal realizability instrument represented in this directory.

### `struc_perc_corpus_analysis.html`

Cross-domain STRUC-PERC-I corpus analysis.

It summarizes the behavior of the frozen PRP corpus under the percolative-realizability instrument and provides the domain-level realizability comparison.

### `cross_instrument_corpus_analysis.html`

Cross-instrument comparison of structural results.

This artifact compares admissibility-side and realizability-side observables and examines where the two structural coordinates agree, diverge, or provide complementary information.

### `unns_realizability_article.html`

Public-facing research article presenting the realizability framework, the STRUC-PERC-I instrument, the four realizability classes, and the relation between admissibility and connectivity.

### `Percolative_Realizability_Principle.pdf`

Research manuscript developing the **Percolative Realizability Principle** and its structural interpretation.

### `Structural_Realizability_Dual_Observability.pdf`

Research manuscript on the dual-observability framework linking structural admissibility and structural realizability.

### `percolation output/`

Frozen PRP / STRUC-PERC-I result material used by the analyses in this directory.

This is an **output/result directory**, not the canonical source of the cross-domain input corpus. The input corpus is archived on Zenodo.

### `perc_1.png`

Figure used in the PRP analysis / manuscript material.

### `perc_2.png`

Figure used in the PRP analysis / manuscript material.

---

## Data separation

Large input corpora are **not duplicated in this GitHub directory**.

The canonical frozen input dataset is archived on Zenodo:

https://zenodo.org/records/22707994

This separation is intentional:

- **Zenodo** provides the persistent archival record for frozen data inputs, provenance, manifests, checksums, and source-specific attribution;
- **GitHub** provides the research structure around those inputs: theory, instruments, analyses, manuscripts, figures, public exposition, and result artifacts.

When reproducing PRP results, use the Zenodo corpus corresponding to the cited dataset version rather than reconstructing inputs from unrelated external sources.

---

## Reproducibility

For reproducible use of this material:

1. obtain the frozen corpus from the Zenodo record;
2. preserve the package and file hashes recorded in its `CHECKSUMS.sha256` and `MANIFEST.csv`;
3. use the corresponding frozen STRUC-PERC-I instrument version represented in this directory;
4. keep source-derived attribution and provenance intact;
5. distinguish input data, instrument output, and interpretive analysis.

The archived corpus spans atomic, molecular, nuclear, cosmological, geodetic, atmospheric, condensed-matter, solar, adversarial, and methodological-control families.

---

## Provenance and rights

The PRP corpus is mixed-source.

UNNS contributes corpus selection, ladder construction and transformation, synthetic/control generation where applicable, normalization, packaging, provenance records, structural-analysis instruments, and interpretive framework.

Underlying third-party source rights remain with their respective rights holders. Package-specific attribution and provenance are documented in the Zenodo deposit.

See the Zenodo record for:

- `ATTRIBUTION.md`;
- `SOURCE_PROVENANCE.md`;
- `MANIFEST.csv`;
- `CHECKSUMS.sha256`.

---

## Citation

For the frozen input corpus, cite:

> UNNS Collective. (2026). *UNNS Percolative Realizability Corpus — Cross-Domain Structural Ladder Dataset v1.0* [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.22707994

For theory, instruments, manuscripts, analyses, and public explanatory material, cite the corresponding artifact or publication directly.

---

## Status

This directory represents the developed **PRP branch of the UNNS regime-synthesis program**.

It should remain focused on the scientific body of the PRP work itself. Large frozen input datasets belong in the linked Zenodo archive rather than being duplicated here.