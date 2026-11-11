# Curation / exclusions log

- All **16** source ZIPs were expanded; no release was replaced by a manuscript and no frozen source was edited.
- All verification code, search code, partial run logs, historical experiments, source copies in `frozen_*` directories, proof documents and native hash manifests were retained within their original releases. These can be important for exact reproduction and status traceability, even when duplicative.
- **24 loose PDF/TEX files** at the input archive root were omitted only after byte-for-byte equality with the relevant file inside an expanded release was confirmed. The retained internal file path is recorded below.
- The sole other loose file, `UNNS_U2_TI_DYN_v001.pdf`, differs byte-for-byte from the packaged PDF, though both are four pages with identical extracted text. It was retained under `90_document_variants/`, not substituted for the native PDF. Its file origins are distinguished below.
- The native `UNNS_U3_v001/SHA256SUMS` has one historical self-entry that does not match; it is preserved unchanged and described in `SOURCE_PROVENANCE.md`.
- Additional version labels or theorem proof statuses have not been inferred or altered.

## Outer loose-file disposition

| Loose file | Disposition | Output file |
|---|---|---|
| `UNNS_U1_BND_v001.pdf` | Exact duplicate omitted | `01_metric_geometry/UNNS_U1_BND_v001/UNNS_U1_BND_v001.pdf` |
| `UNNS_U1_BND_v001.tex` | Exact duplicate omitted | `01_metric_geometry/UNNS_U1_BND_v001/manuscript/UNNS_U1_BND_v001.tex` |
| `UNNS_U2_001_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_001_v001/UNNS_U2_001_v001.pdf` |
| `UNNS_U2_001_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_001_v001/manuscript/UNNS_U2_001_v001.tex` |
| `UNNS_U2_FP_R3_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_FP_R3_v001/UNNS_U2_FP_R3_v001.pdf` |
| `UNNS_U2_FP_R3_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_FP_R3_v001/manuscript/UNNS_U2_FP_R3_v001.tex` |
| `UNNS_U2_FP_SYM_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_FP_SYM_v001/UNNS_U2_FP_SYM_v001.pdf` |
| `UNNS_U2_FP_SYM_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_FP_SYM_v001/manuscript/UNNS_U2_FP_SYM_v001.tex` |
| `UNNS_U2_FP_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_FP_v001/UNNS_U2_FP_v001.pdf` |
| `UNNS_U2_FP_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_FP_v001/manuscript/UNNS_U2_FP_v001.tex` |
| `UNNS_U2_KI_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_KI_v001/UNNS_U2_KI_v001.pdf` |
| `UNNS_U2_KI_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_KI_v001/manuscript/UNNS_U2_KI_v001.tex` |
| `UNNS_U2_RN_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_RN_v001/manuscript/UNNS_U2_RN_v001.pdf` |
| `UNNS_U2_RN_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_RN_v001/manuscript/UNNS_U2_RN_v001.tex` |
| `UNNS_U2_SQ_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_SQ_v001/UNNS_U2_SQ_v001.pdf` |
| `UNNS_U2_SQ_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_SQ_v001/manuscript/UNNS_U2_SQ_v001.tex` |
| `UNNS_U2_TI_DYN_v001.pdf` | Distinct binary retained in variant folder | `90_document_variants/UNNS_U2_TI_DYN_v001.pdf` |
| `UNNS_U2_TI_v001.pdf` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_TI_v001/manuscript/UNNS_U2_TI_v001.pdf` |
| `UNNS_U2_TI_v001.tex` | Exact duplicate omitted | `02_routes_selectors/UNNS_U2_TI_v001/manuscript/UNNS_U2_TI_v001.tex` |
| `UNNS_U3_COR_v001.pdf` | Exact duplicate omitted | `03_graph_structure/UNNS_U3_COR_v001/manuscript/UNNS_U3_COR_v001.pdf` |
| `UNNS_U3_COR_v001.tex` | Exact duplicate omitted | `03_graph_structure/UNNS_U3_COR_v001/manuscript/UNNS_U3_COR_v001.tex` |
| `UNNS_U3_v001.pdf` | Exact duplicate omitted | `03_graph_structure/UNNS_U3_v001/manuscript/UNNS_U3_v001.pdf` |
| `UNNS_U3_v001.tex` | Exact duplicate omitted | `03_graph_structure/UNNS_U3_v001/manuscript/UNNS_U3_v001.tex` |
| `UNNS_U4_SPEC_v001.pdf` | Exact duplicate omitted | `04_symbolic_dynamics/UNNS_U4_SPEC_v001/manuscript/UNNS_U4_SPEC_v001.pdf` |
| `UNNS_U4_SPEC_v001.tex` | Exact duplicate omitted | `04_symbolic_dynamics/UNNS_U4_SPEC_v001/manuscript/UNNS_U4_SPEC_v001.tex` |

## Source-context not present

The following records needed for full future alignment to the four manuscripts were **not in the supplied source archive**: the ADJ4 certificate/selector source release (`UNNS_GUP_ADJ4_v001`), `UNNS_U4_GEN_C_v001`, `UNNS_U4_GEN_C_ORDER_v001`, and related autonomous-a-periodicity audit packages. Their absence is listed, not silently filled. The completed four manuscript ZIP/PDF packages themselves are also intentionally excluded.
