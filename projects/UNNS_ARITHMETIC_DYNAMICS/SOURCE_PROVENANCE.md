# Source release inventory and provenance

Input archive: `UNNS-U0(2).zip` (SHA-256 `347600a709240f566a9c93bd64d8338d0b91aef41bb6df750273029d08184286`).

All 16 nested source ZIPs were expanded as separate research releases. The SHA-256 values below refer to each **original ZIP byte stream** in the supplied archive, not to a reconstructed ZIP.

| Release | Theme | Original ZIP SHA-256 | Native manifest |
|---|---|---|---|
| `UNNS_U1_BND_v001` | `01_metric_geometry` | `912a068e2d26fb721c13d524f9bb18280e59a99fbafd79928781903c1c9d8e35` | 26 matches |
| `UNNS_U2_001_v001` | `02_routes_selectors` | `561a9558f713faa2905be18f2a6afc2d3aac6de955c58e73cace7051e057ca21` | 19 matches |
| `UNNS_U2_FP_R3_v001` | `02_routes_selectors` | `3e0e27295c8a1189aff7c8d4f92678b2b34db75ae05e2d9ea5aa652764594923` | 37 matches |
| `UNNS_U2_FP_SYM_v001` | `02_routes_selectors` | `a614e196fa059bc58a7bea5bb3c616c8eaf0eead37945cb08bd56ecb982668c6` | 48 matches |
| `UNNS_U2_FP_v001` | `02_routes_selectors` | `c8469e88b76c66b248c827f00edf6da07cb9af0d4daf14ed2db935951e89ee91` | 34 matches |
| `UNNS_U2_KI_v001` | `02_routes_selectors` | `b2e921c964fb05d57686733fd9f8410c7521756ad39a24176a6fb12399458769` | 51 matches |
| `UNNS_U2_RN_v001` | `02_routes_selectors` | `38f5e0a4490920992e042df734d076f1d91cc2de36e499ddde131bba2ad295c0` | 21 matches |
| `UNNS_U2_SQ_v001` | `02_routes_selectors` | `c13a9be6c9a3d1d9299a009ab08844a9840a8ec24236dd5da171806e14691733` | 28 matches |
| `UNNS_U2_TI_DYN_v001` | `02_routes_selectors` | `f2536563f2ed2442e969b64685a228cd68eb437bc5722d43a251ec386fe5deef` | 8 matches |
| `UNNS_U2_TI_v001` | `02_routes_selectors` | `8eb9dc9a66bae45992fd7034f9d31677a01902094ce32b8789f5ae77e4b7bcca` | 54 matches |
| `UNNS_U3_COR_v001` | `03_graph_structure` | `038c9d1102719f3a4ee6d2afd1719ff79a9c00acb85b21b68bc98a54e454b686` | 11 matches |
| `UNNS_U3_v001` | `03_graph_structure` | `4f6a59b63ab58bc2842dce08289a678e63a54b22a613ea24cf0490c6ed6ee929` | 14 matches; 1 historical mismatch: SHA256SUMS |
| `UNNS_U4_GEN_v001` | `04_symbolic_dynamics` | `042eb5b09b4d231283c9c7d9d40e29a8789625f4b073e724000d49f6d49e18df` | 25 matches |
| `UNNS_U4_M2_ENT_v001` | `04_symbolic_dynamics` | `1b6f1b26840a04eef4b6b175c6f8b3c9339085b8c23ba27dea9d9e8dbbcf0b2f` | 11 matches |
| `UNNS_U4_SPEC_v001` | `04_symbolic_dynamics` | `6291949dce44fca3baaaf764ffa03667b5a547dce2c6575c2493a0235e633daa` | 17 matches |
| `UNNS_U4_STAGE2_v001` | `04_symbolic_dynamics` | `1b68eb08bcc8c99f708ab2c986d43c6d0f0fdad3cb9e453cd51d9022aeb2eada` | 26 matches |

The native manifest in `UNNS_U3_v001` contains a self-entry recording the SHA-256 of an **empty** file (`e3b0c442...`) for `SHA256SUMS`, which is not empty. All its other native manifest entries match; the historical anomaly is preserved rather than rewritten. The new `COLLECTION_SHA256SUMS.txt` independently hashes every file in this curated output.

This collection has not rerun the original long scientific verifiers. Archive-integrity, native-manifest (with the documented exception), and newly generated collection-hash tests are performed.
