# biological_admissibility_extension

Biological admissibility extension package for the UNNS Substrate Research Program.

This directory contains the biological-domain chamber array, corpus analysis pages, article/manuscript assets, and input files used to extend Universal Structural Law (USL) admissibility analysis from physical ladders into biological fitness landscapes.

---

## Directory purpose

This package assembles:

- the biological chamber pipeline interface
- the STRUC-BIO-I chamber
- biological and STRUC-I corpus analysis pages
- the biological extension article page
- the biological extension manuscript PDF
- the input data bundle used by the chambers

The central empirical claim documented here is that admissibility constraints were tested on a fully measured biological fitness landscape and found to remain satisfied across all evaluated configurations, extending prior physical-domain results into biology. 

---

## Contents

### `input_files/`
Input bundle for biological admissibility runs.

Expected role in this package:

- biological source data for chamber ingestion
- precompiled mutation / fitness inputs
- ladder CSVs and related chamber-ready datasets
- reproducibility support for STRUC-BIO-I and STRUC-I runs

### `Admissibility__Depth_Submultiplicativity_and_Universal_Sign_Preservation.pdf`
Primary manuscript for the biological extension.

Scope documented in the manuscript:

- cross-domain validation of admissibility constraints in a self-replicating RNA polymerase ribozyme system
- use of `STRUC-I v1.0.4` and `STRUC-BIO-I v0.1`
- zero recorded violations across the reported biological evaluations
- biological extension of previously established physical-corpus admissibility results 

### `chamber_pipeline_struc_bio_ii_i_struc_i.html`
Biological pipeline array / launcher page.

Function:

- presents the UNNS biological pipeline
- organizes the workflow around:
  - STRUC-BIO-II
  - STRUC-BIO-I
  - STRUC-I v1.0.4
- serves as the entry page for biological compilation, epistasis-graph evaluation, and ladder admissibility workflows 

### `struc_bio_corpus_analysis.html`
Biological corpus analysis page.

Function:

- summarizes biological-domain admissibility outputs
- positions biological results within the broader UNNS admissibility program
- supports comparison of biological ladders / graph configurations

### `struc_bio_ii_v0_1_0.html`
STRUC-BIO-II chamber.

Function:

- biological structure compiler
- upstream stage of the biological pipeline
- prepares structured biological inputs for downstream admissibility analysis

### `struc_i_v1_0_4_corpus_analysis.html`
STRUC-I v1.0.4 corpus analysis page.

Function:

- summarizes universal ladder admissibility results
- provides cross-domain context for the biological extension
- supports comparison between physical and biological structural-pressure regimes

### `struc-bio-i-chamber.html`
STRUC-BIO-I chamber.

Function:

- genotype-graph / epistasis compensation analysis chamber
- evaluates the biological-domain compensation condition and admissibility status
- complements STRUC-I ladder-based analysis with graph-based biological analysis

### `unns_biological_extension_article.html`
Article page for the biological admissibility extension.

Function:

- presentation layer for the biological extension write-up
- web publication counterpart to the manuscript and chamber outputs
- intended for unns.tech or related publication contexts

---

## Conceptual structure

This directory combines two analysis tracks over the same biological extension program:

### 1. Ladder-based admissibility track
Implemented through `STRUC-I v1.0.4`.

The manuscript describes six QT45 fitness ladders evaluated under the preregistered STRUC-I protocol, with zero clean violations reported across all 240 κ-step biological ladder evaluations. 

### 2. Genotype-graph compensation track
Implemented through `STRUC-BIO-I v0.1`.

The manuscript defines the biological compensation criterion `D(G) ≤ C(G)` and reports satisfaction of that condition across all three QT45 genotype-graph configurations. 

Together, these two tracks provide the biological extension of the admissibility program:
- ladder admissibility under perturbation
- graph compensation under epistatic interaction structure

---

## Biological system covered

Primary biological system:

- QT45 self-replicating RNA polymerase ribozyme

As described in the manuscript, the dataset includes exhaustive single-mutant measurements and a large directly measured double-mutant set, enabling both ladder construction and genotype-graph analysis without inferential gap-filling. 

---

## Core reported findings represented by this directory

From the manuscript:

- zero violations across 240 STRUC-I κ-step evaluations of six QT45 fitness ladders
- zero violations of the STRUC-BIO-I compensation criterion across three genotype-graph configurations
- clean QT45 genotype graph at low biological structural pressure
- identification of elevated-pressure biological regimes including a boundary-stabilized deletion ladder
- cross-instrument consistency between STRUC-I and STRUC-BIO-I on the same biological system 

---

## Role within the UNNS repository

This folder should be treated as the biological-domain extension pack of the broader admissibility / Universal Structural Law program.

Repository role:

- extends prior physical admissibility validation into biology
- links article, manuscript, chamber interface, and chamber implementations
- preserves input data and analysis pages in one deployable directory
- supports both local use and publication/export to UNNS web infrastructure

---

## Recommended placement logic

This directory is best interpreted as a complete biological-extension module containing:

- source manuscript
- web article
- chamber UI
- chamber implementations
- corpus analysis pages
- reproducibility inputs

It therefore fits naturally as a self-contained domain package within the wider UNNS admissibility / chamber ecosystem.

---

## Minimal usage map

```text
input_files/
   ├─ chamber-ready biological inputs
   └─ reproducibility assets

chamber_pipeline_struc_bio_ii_i_struc_i.html
   ├─ entry interface / workflow page
   ├─ links biological stages
   └─ frames the extension package

struc_bio_ii_v0_1_0.html
   └─ biological compilation stage

struc-bio-i-chamber.html
   └─ biological graph / compensation analysis

struc_i_v1_0_4_corpus_analysis.html
   └─ universal corpus comparison context

struc_bio_corpus_analysis.html
   └─ biological-domain result summary

unns_biological_extension_article.html
   └─ web article presentation

Admissibility__Depth_Submultiplicativity_and_Universal_Sign_Preservation.pdf
   └─ primary manuscript / formal reference