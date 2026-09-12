# UNNS Turbulence — Zenodo Source Recovery Guide

## Purpose

This guide explains how to reconstruct the raw JHTDB-derived source layer required by
`UNNS_TURB_JHTDB_v0_1` from the published Zenodo dataset:

**UNNS Turbulence — JHTDB Analysis Cutouts and High-Re Export v0.1**

- Zenodo record: `https://zenodo.org/records/22650769`
- Exact version DOI: `10.5281/zenodo.22650769`
- Concept DOI (all versions): `10.5281/zenodo.22650768`

For exact reproduction of the frozen project state, use the **version DOI**
`10.5281/zenodo.22650769`, not a future replacement version.

The Zenodo record is the canonical public archival/distribution copy of the heavy source
artifacts. The project itself continues to use immutable local working copies under:

`data\raw\jhtdb\`

This guide assumes that the lightweight `UNNS_TURB_JHTDB_v0_1` project tree, including
its tools, frozen protocols, chambers, and compact provenance files, is already present.

---

## 1. What the Zenodo record contains

The published record contains nine files.

### Heavy source artifacts

1. `isotropic1024-coarse-velocity.h5`
   - role: Pilot A source
   - JHTDB dataset: `isotropic1024coarse`
   - field: velocity
   - selection: `x/y/z = 1:256` (1-based inclusive)
   - stored frames: `1:10`
   - stored `dt = 0.002`
   - physical time: `0.000–0.018`

2. `isotropic1024-coarse-pilot-b-velocity.h5`
   - role: Pilot B source
   - JHTDB dataset: `isotropic1024coarse`
   - field: velocity
   - selection: `x/y/z = 513:768` (1-based inclusive)
   - stored frames: `501:510`
   - stored `dt = 0.002`
   - physical time: `1.000–1.018`
   - spatial overlap with Pilot A: zero grid points
   - stored-frame overlap with Pilot A: zero

3. `HIGH_RE_EXPORT.tar`
   - role: frozen High-Re source export
   - contains:
     - `isotropic8192`, snapshots `0–5`
     - `isotropic32768`, snapshot `0`
   - each stored sample is a `256^3` velocity cutout
   - extraction source: JHTDB/SciServer Ceph/Zarr
   - this archive must be hash-verified before extraction

4. `HIGH_RE_EXPORT.tar.sha256`
   - native checksum companion for the High-Re archive

### Provenance and integrity companions

5. `ATTRIBUTION.md`
6. `MANIFEST.json`
7. `META_SHA256SUMS.txt`
8. `README.md`
9. `SHA256SUMS.txt`

The Zenodo deposit is a **source-data/provenance record**. It does not contain the complete
derived-result tree or all frozen chamber outputs. Those belong to the lightweight project
and its separate result/provenance records.

Total size of the three large source artifacts recorded in the manifest:
`5,440,019,888` bytes (about 5.44 GB decimal).

Plan for at least 6 GB of free space for the deposited files themselves, plus additional
space for the extracted High-Re content and derived pipeline outputs.

---

## 2. Recommended reproduction strategy

For exact reproduction, **do not reacquire these cutouts from JHTDB** unless the purpose
is specifically to reproduce the original acquisition step.

Instead:

1. obtain the lightweight `UNNS_TURB_JHTDB_v0_1` project;
2. download the frozen source artifacts from Zenodo version `0.1`;
3. verify their SHA-256 hashes;
4. place them at the exact canonical paths below;
5. keep the source files immutable;
6. begin the frozen adapter/pipeline stages.

This avoids dependence on JHTDB authentication, changing server interfaces, or repeating
large remote extraction operations. The deposited files are the byte-identified sources used
by the frozen project.

---

## 3. Download the record

### Option A — browser

Open:

`https://zenodo.org/records/22650769`

Download all nine files into a temporary directory, for example:

`Downloads\ZENODO_SOURCE_v01\`

For a full reproduction, download all nine files.

For a branch-specific reproduction:

- Pilot A requires `isotropic1024-coarse-velocity.h5`.
- Pilot B requires `isotropic1024-coarse-pilot-b-velocity.h5`.
- High-Re requires `HIGH_RE_EXPORT.tar` and `HIGH_RE_EXPORT.tar.sha256`.

The five small metadata/provenance files should also be retained with the project even when
only one scientific branch is being reproduced.

### Option B — Windows PowerShell / curl

Windows 10/11 normally provides `curl.exe`. The following commands download the exact
published files.

```powershell
$Base = "https://zenodo.org/records/22650769/files"
$Dest = "$env:USERPROFILE\Downloads\ZENODO_SOURCE_v01"

New-Item -ItemType Directory -Force -Path $Dest | Out-Null

$Files = @(
    "ATTRIBUTION.md",
    "MANIFEST.json",
    "META_SHA256SUMS.txt",
    "README.md",
    "SHA256SUMS.txt",
    "isotropic1024-coarse-velocity.h5",
    "isotropic1024-coarse-pilot-b-velocity.h5",
    "HIGH_RE_EXPORT.tar",
    "HIGH_RE_EXPORT.tar.sha256"
)

foreach ($File in $Files) {
    Write-Host "Downloading $File"
    curl.exe -L --fail --retry 5 --retry-delay 10 `
        -o "$Dest\$File" `
        "$Base/$File?download=1"

    if ($LASTEXITCODE -ne 0) {
        throw "Download failed: $File"
    }
}
```

Do not continue into the analysis pipeline if any download fails.

---

## 4. Verify the scientific source files

The frozen SHA-256 values are:

```text
Pilot A
e32c9225af656a2f0fa0a704be7dcd78fa12efc1a01b880af23eb45e02108a46
isotropic1024-coarse-velocity.h5

Pilot B
977e6ab3c437252395dc7f7185af1829619fe1eec754f59f5f3ceae2ca0b969f
isotropic1024-coarse-pilot-b-velocity.h5

High-Re
bbda6ab3fe3b22679a0bccdaad4287cca7f0f0f06e28caa1f9692d92298c105f
HIGH_RE_EXPORT.tar
```

The same values are stored in the deposited `SHA256SUMS.txt`.

### PowerShell verification

From the temporary download directory:

```powershell
Get-FileHash .\isotropic1024-coarse-velocity.h5 -Algorithm SHA256
Get-FileHash .\isotropic1024-coarse-pilot-b-velocity.h5 -Algorithm SHA256
Get-FileHash .\HIGH_RE_EXPORT.tar -Algorithm SHA256
```

Each returned hash must match the frozen value exactly.

For an automatic PASS/FAIL check:

```powershell
$Expected = @{
    "isotropic1024-coarse-velocity.h5" =
        "E32C9225AF656A2F0FA0A704BE7DCD78FA12EFC1A01B880AF23EB45E02108A46"
    "isotropic1024-coarse-pilot-b-velocity.h5" =
        "977E6AB3C437252395DC7F7185AF1829619FE1EEC754F59F5F3CEAE2CA0B969F"
    "HIGH_RE_EXPORT.tar" =
        "BBDA6AB3FE3B22679A0BCCDAAD4287CCA7F0F0F06E28CAA1F9692D92298C105F"
}

foreach ($File in $Expected.Keys) {
    $Actual = (Get-FileHash ".\$File" -Algorithm SHA256).Hash
    if ($Actual -eq $Expected[$File]) {
        Write-Host "[PASS] $File"
    } else {
        Write-Host "[FAIL] $File"
        Write-Host " expected:" $Expected[$File]
        Write-Host " actual:  " $Actual
    }
}
```

A hash failure is a hard stop. Delete the bad local copy and download it again. Do not
modify a file to make it fit the project.

---

## 5. Restore the canonical project paths

From the root of `UNNS_TURB_JHTDB_v0_1`, the heavy source files belong at exactly these
locations:

```text
data\
└─ raw\
   └─ jhtdb\
      ├─ isotropic1024coarse\
      │  └─ cutouts\
      │     └─ isotropic1024-coarse-velocity.h5
      │
      ├─ pilot_b\
      │  └─ isotropic1024-coarse-pilot-b-velocity.h5
      │
      └─ high_re\
         ├─ HIGH_RE_EXPORT.tar
         ├─ HIGH_RE_EXPORT.tar.sha256
         └─ HIGH_RE_EXPORT\        <- created after extraction when High-Re is needed
```

The five small Zenodo companion files belong under:

```text
data\source\zenodo\v01\
```

That directory should contain:

```text
ATTRIBUTION.md
MANIFEST.json
META_SHA256SUMS.txt
README.md
SHA256SUMS.txt
```

The large HDF5/TAR payload must **not** be placed under `data\source\zenodo\v01\`.
That directory is for compact archive metadata; the active immutable source copies belong
under `data\raw\jhtdb\`.

---

## 6. Example Windows restore commands

Assume:

```text
Project:
C:\...\UNNS_TURB_JHTDB_v0_1

Downloads:
%USERPROFILE%\Downloads\ZENODO_SOURCE_v01
```

Open PowerShell in the project root and run:

```powershell
$Src = "$env:USERPROFILE\Downloads\ZENODO_SOURCE_v01"

New-Item -ItemType Directory -Force `
    ".\data\raw\jhtdb\isotropic1024coarse\cutouts" | Out-Null
New-Item -ItemType Directory -Force `
    ".\data\raw\jhtdb\pilot_b" | Out-Null
New-Item -ItemType Directory -Force `
    ".\data\raw\jhtdb\high_re" | Out-Null
New-Item -ItemType Directory -Force `
    ".\data\source\zenodo\v01" | Out-Null

Copy-Item "$Src\isotropic1024-coarse-velocity.h5" `
    ".\data\raw\jhtdb\isotropic1024coarse\cutouts\"

Copy-Item "$Src\isotropic1024-coarse-pilot-b-velocity.h5" `
    ".\data\raw\jhtdb\pilot_b\"

Copy-Item "$Src\HIGH_RE_EXPORT.tar" `
    ".\data\raw\jhtdb\high_re\"

Copy-Item "$Src\HIGH_RE_EXPORT.tar.sha256" `
    ".\data\raw\jhtdb\high_re\"

Copy-Item "$Src\ATTRIBUTION.md" ".\data\source\zenodo\v01\"
Copy-Item "$Src\MANIFEST.json" ".\data\source\zenodo\v01\"
Copy-Item "$Src\META_SHA256SUMS.txt" ".\data\source\zenodo\v01\"
Copy-Item "$Src\README.md" ".\data\source\zenodo\v01\"
Copy-Item "$Src\SHA256SUMS.txt" ".\data\source\zenodo\v01\"
```

If the compact companion files are already present in the lightweight project, do not
silently overwrite differing copies. Compare their hashes against `META_SHA256SUMS.txt`
first.

---

## 7. High-Re extraction

The High-Re branch uses the contents of `HIGH_RE_EXPORT.tar`.

First verify the TAR SHA-256. Only then extract it.

From the project root:

```powershell
tar -xf ".\data\raw\jhtdb\high_re\HIGH_RE_EXPORT.tar" `
    -C ".\data\raw\jhtdb\high_re"
```

The project expects the extracted working view beneath:

```text
data\raw\jhtdb\high_re\HIGH_RE_EXPORT\
```

Keep the original `HIGH_RE_EXPORT.tar` unchanged after extraction. The TAR is the frozen
source artifact; the extracted directory is its working view.

The deposited manifest records:

```text
isotropic8192
  snapshots 0–4  -> PRIMARY_HIGH_RE
  snapshot 5     -> PRESPECIFIED_LOW_RE_CONTRAST
  x/y/z          -> 3969:4224 (1-based inclusive)
  cutout shape   -> 256^3

isotropic32768
  snapshot 0     -> PRIMARY_EXTREME_RE
  x/y/z          -> 16257:16512 (1-based inclusive)
  cutout shape   -> 256^3
```

---

## 8. Preserve the raw layer

The raw-data rule for this project is simple:

**Raw source files are immutable.**

Do not:

- edit an HDF5 dataset in place;
- rename a frozen source file;
- normalize, rescale, crop, or rewrite the source HDF5 before adapter execution;
- replace the TAR with a repacked TAR;
- treat the extracted 256^3 cubes as periodic domains;
- silently substitute a newer Zenodo version.

The original JHTDB simulation is periodic, but the extracted 256^3 cutouts are not treated
as periodic computational domains in this project. The frozen adapter therefore uses
boundary-safe finite differences, no FFT derivatives, no opposite-face wrapping, and rejects
boundary-truncated structures.

---

## 9. Source-ready checks before computation

### Pilot A

Confirm this exact file exists:

```text
data\raw\jhtdb\isotropic1024coarse\cutouts\
isotropic1024-coarse-velocity.h5
```

The frozen Pilot-A adapter configuration contains the same expected SHA-256 and has
`validate_sha256 = true`.

Adapter:

```text
tools\derive\JHTDB_ROUTE_ADAPTER_v0_1_0\
```

Optional code self-tests:

```text
TEST_ADAPTER_WINDOWS.bat
```

Full Pilot-A adapter entry point:

```text
RUN_ADAPTER_WINDOWS.bat
```

The adapter reads the HDF5 locally. Do not feed the HDF5 directly to STRUC-ROUTE-I.

### Pilot B

Confirm this exact file exists:

```text
data\raw\jhtdb\pilot_b\
isotropic1024-coarse-pilot-b-velocity.h5
```

Use the frozen Pilot-B runner present in the project:

```text
tools\derive\PILOT_B_RUN_v0_1_2\
```

Run preflight first:

```text
CHECK_PILOT_B.bat
```

Expected successful final line:

```text
[PREFLIGHT PASS] No Pilot-B derived data were generated.
```

Only after preflight passes, run:

```text
RUN_PILOT_B_ADAPTER.bat
```

Do **not** run the original Pilot-A `RUN_ADAPTER_WINDOWS.bat` against the Pilot-B source,
because its launcher/output identity is Pilot-A-specific.

### High-Re

After verifying and extracting `HIGH_RE_EXPORT.tar`, use the frozen High-Re scale adapter:

```text
tools\derive\JHTDB_HIGH_RE_SCALE_v0_1_2\
```

First verify the restored source:

```text
VERIFY_SOURCE_WINDOWS.bat
```

The High-Re branch is a separate generalization branch. Do not merge its scientific
interpretation into Pilot-B replication criteria.

---

## 10. Pipeline entry after raw-data recovery

Zenodo reconstructs the **source layer**. It does not replace the frozen pipeline.

The high-level Pilot-A/Pilot-B path is:

```text
Zenodo source HDF5
        |
        v
JHTDB_ROUTE_ADAPTER
        |
        v
objects + scale/time relations
        |
        v
STRUC-ROUTE-I
        |
        v
D_STITCH / P_TIME / P_SCALE ladders
        |
        +--> STRUC-I
        |
        +--> STRUC-PERC-I
        |
        +--> STITCH-MECH
        |
        v
frozen replication/synthesis records
```

For Pilot B, follow the already frozen project workflow:

```text
analysis\replication\jhtdb_pilot_b\WORKFLOW.md
analysis\replication\jhtdb_pilot_b\PROTOCOL.md
analysis\replication\jhtdb_pilot_b\CRITERIA.md
```

Do not reinterpret the project by rerunning until a desired outcome appears. The stopping
rule and criterion definitions are part of the reproducible experiment.

---

## 11. Expected source identity

### Pilot A

```text
File:
isotropic1024-coarse-velocity.h5

Canonical path:
data\raw\jhtdb\isotropic1024coarse\cutouts\
isotropic1024-coarse-velocity.h5

SHA-256:
e32c9225af656a2f0fa0a704be7dcd78fa12efc1a01b880af23eb45e02108a46
```

### Pilot B

```text
File:
isotropic1024-coarse-pilot-b-velocity.h5

Canonical path:
data\raw\jhtdb\pilot_b\
isotropic1024-coarse-pilot-b-velocity.h5

Bytes:
2,015,302,728

SHA-256:
977e6ab3c437252395dc7f7185af1829619fe1eec754f59f5f3ceae2ca0b969f

Expected HDF5 datasets:
Velocity_0501 ... Velocity_0510

Per-dataset shape:
256 x 256 x 256 x 3

Axis order:
z y x component
```

### High-Re

```text
File:
HIGH_RE_EXPORT.tar

Canonical path:
data\raw\jhtdb\high_re\HIGH_RE_EXPORT.tar

Bytes:
1,409,423,360

SHA-256:
bbda6ab3fe3b22679a0bccdaad4287cca7f0f0f06e28caa1f9692d92298c105f
```

The SHA-256 is the primary byte-identity check.

---

## 12. Troubleshooting Zenodo access

The record is Open and public. No Zenodo account or share-access link is required to
download the published files.

If Zenodo temporarily returns `504 Gateway Time-out`:

1. do not create a replacement source or new project version;
2. retry the exact version record later;
3. retain any already downloaded file only if its SHA-256 verifies;
4. the DOI can independently be checked through DataCite:

`https://api.datacite.org/dois/10.5281/zenodo.22650769`

A successful DOI lookup does not substitute for file verification; the downloaded scientific
source must still match the frozen SHA-256.

---

## 13. Upstream attribution

The deposited velocity fields are derived from the Johns Hopkins Turbulence Database
(JHTDB). UNNS did not generate the underlying DNS simulations.

Upstream source:

**Johns Hopkins Turbulence Database (JHTDB)**

Forced Isotropic Turbulence Dataset (Extended), 1024^3:

**DOI: `10.7281/T1KK98XB`**

JHTDB data are used under the Open Data Commons Attribution License (ODC-By) 1.0.

The UNNS contribution in the Zenodo source record is the frozen extraction selection,
provenance, packaging, checksums, and subsequent structural-analysis framework.

Retain `ATTRIBUTION.md` with any redistributed copy of this source package.

---

## 14. Citation

For exact reproduction of this source release, cite:

> UNNS Collective. (2026). *UNNS Turbulence — JHTDB Analysis Cutouts and High-Re
> Export v0.1* (Version 0.1) [Dataset]. Zenodo.
> DOI: `10.5281/zenodo.22650769`

Use the version DOI above when reporting results reproduced from this exact dataset.

---

## 15. Minimal reproduction checklist

Before beginning scientific analysis, all applicable items below should be true:

- [ ] lightweight `UNNS_TURB_JHTDB_v0_1` project is present;
- [ ] exact Zenodo version `0.1` was used;
- [ ] required heavy source file(s) were downloaded;
- [ ] SHA-256 verification passed;
- [ ] files were restored to the canonical `data\raw\jhtdb\...` paths;
- [ ] compact Zenodo provenance files are present under `data\source\zenodo\v01\`;
- [ ] High-Re TAR was verified before extraction, if the High-Re branch is being reproduced;
- [ ] raw HDF5/TAR source files remain unchanged;
- [ ] Pilot-B preflight passes before its adapter is run;
- [ ] frozen project protocol and stopping rules are used without retuning.

Only after these checks should the derived pipeline be executed.
