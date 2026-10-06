# YANAGIHARA_EMT_EXTRACT.md

**Status:** FROZEN AND EXECUTED VALIDLY  
**Source SHA-256:** `fe549266b6a2483aa0c0104835ddf3215a9b2d8812110aacb86ea2368aa10423`

The deterministic extractor is hash-locked to the uploaded final vector PDF and recovers the `R=0.69 fm` panel by PDF drawing geometry.

Frozen axis mapping:

```text
panel = [550.7438, 10.7, 1052.9437, 382.148] pt
r=0.0 fm -> X=576.0344
r=0.1 fm -> X=648.2934
value=0 -> Y=367.3885
value=2 GeV/fm^3 -> Y=318.1901
```

Marker geometry:

```text
outline bbox = 15 x 15 pt
error cap    = 24 pt horizontal vector segment
```

Expected counts in the visible primary panel:

```text
185 markers/component
370 caps/component
```

The four component grids must be identical before extraction can return `EXTRACTION-VALID`.
