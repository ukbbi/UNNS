ROUTE-LADDER-EXTRACT v0.1.1
===========================

PURPOSE
-------
Create the frozen primary downstream chamber ladders from:

    outputs\exports\struc_route_i\jhtdb_pilot_a\
        jhtdb_pilot_a_20260904_235409.zip

The extractor reads the run's NODES.parquet and EDGES.parquet and creates:

    D_STITCH.csv   n = 4,957
    P_TIME.csv     n = 10,507
    P_SCALE.csv    n = 6,009

PLACEMENT
---------
Put this folder at:

    UNNS_TURB_JHTDB_v0_1\
        tools\
            derive\
                ROUTE_LADDER_EXTRACT_v0_1_0\

The frozen run ZIP must remain at:

    outputs\exports\struc_route_i\jhtdb_pilot_a\
        jhtdb_pilot_a_20260904_235409.zip

RUN
---
Double-click:

    RUN_EXTRACT.bat

The tool reuses the already working STRUC-ROUTE-I Python environment:

    %LOCALAPPDATA%\UNNS\ROUTE_I_v010

No new environment is created.

OUTPUTS
-------
Canonical source descendants:

    ladders\route_i\jhtdb_pilot_a\primary\
        D_STITCH.csv
        P_TIME.csv
        P_SCALE.csv
        MANIFEST.json
        README.txt
        SHA256SUMS.txt

Byte-identical STRUC-I-facing copies:

    ladders\struc_i\jhtdb_pilot_a\
        D_STITCH.csv
        P_TIME.csv
        P_SCALE.csv
        MANIFEST.json

Byte-identical STRUC-PERC-I-facing copies:

    ladders\struc_perc_i\jhtdb_pilot_a\
        D_STITCH.csv
        P_TIME.csv
        P_SCALE.csv
        MANIFEST.json

Records:

    outputs\records\ROUTE_LADDER_EXTRACT_REPORT.json
    outputs\records\ROUTE_LADDERS_PRIMARY.zip

EXTRACTION DEFINITIONS
----------------------
D_STITCH
    All finite NODES.stitch_defect values.
    This is the full source-object population, NOT the 36 cell averages in
    ROUTE-I's generic LADDERS.zip.

P_TIME
    NODES.time_persistence only for node IDs that are actual sources of
    eligible EDGES with axis=time.

P_SCALE
    NODES.scale_persistence only for node IDs that are actual sources of
    eligible EDGES with axis=scale.

NON-NEGOTIABLE RULES
--------------------
- duplicates preserved;
- no deduplication;
- no jitter;
- no smoothing;
- no normalization;
- no rescaling;
- full binary64 precision written with 17 significant digits;
- ascending stable sort only;
- chamber-facing copies must be byte-identical to the canonical derived files.

CHAMBER COMPATIBILITY
---------------------
Each CSV has exactly one column:

    value

This matches STRUC-I v1.0.4 generic single-column CSV ingestion.

It also matches STRUC-PERC-I v2.5.0 CSV ingestion: the nonnumeric header is
ignored and every numeric token is ingested.

RUN ORDER
---------
1. D_STITCH -> STRUC-I v1.0.4
2. D_STITCH -> STRUC-PERC-I v2.5.0
3. P_TIME   -> STRUC-I
4. P_TIME   -> STRUC-PERC-I
5. P_SCALE  -> STRUC-I
6. P_SCALE  -> STRUC-PERC-I

STRUC-I and STRUC-PERC-I are independent interrogations of the same frozen
route-derived ladders. STRUC-I output is not passed into STRUC-PERC-I.

FROZEN SOURCE SHA-256
--------------------
cc2c2caadca37d8f9cea7415bad37929da4e3a11d069a1414d18fba42126b788


V0.1.1 NUMERICAL-BOUNDARY PATCH
-------------------------------
The v0.1.0 extractor used an exact [0,1] comparison for D_STITCH.

D_STITCH is normalized Jensen-Shannon divergence and is mathematically in
[0,1], but floating-point evaluation can yield a machine-roundoff endpoint
such as 1.0000000000000002.

v0.1.1 validates D_STITCH, P_TIME and P_SCALE against [0,1] with a strict
1e-12 tolerance.

IMPORTANT:
- no value is clipped;
- no value is rounded;
- no value is altered;
- the observed extrema and numerical excursions are written to the extraction
  report.
