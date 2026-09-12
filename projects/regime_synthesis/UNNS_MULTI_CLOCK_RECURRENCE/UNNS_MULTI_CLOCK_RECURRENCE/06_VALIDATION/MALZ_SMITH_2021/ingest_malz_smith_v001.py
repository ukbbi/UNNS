#!/usr/bin/env python3
"""
Neutral Malz-Smith experimental ingest for SPEC_v001.

Reads only the 12 source *_real.pkl experiment files with a restricted NumPy-only
unpickler. Uses source "corrected results" X/Y/Z, excludes t < source ramp_time,
and writes canonical time/source-cycle/tomography CSVs.

No smoothing, interpolation, normalization, FFT reconstruction, or simulation input.
"""
print("Use the locked MALZ_SMITH_ADAPTER_v001.json and the source archive.")
