# TC_PHYS_v001 — Reproduction Guide

This file explains how to reproduce the **physics-validation stage** of the UNNS Time Crystal project on Windows using the supplied Frey–Rachel experimental data.

The purpose of this stage is strictly:

**raw experimental data → published-physics reconstruction → physics validation**

No UNNS temporal-closure metric is calculated here.

---

## 1. Required project layout

Your `Time_crystal` folder should contain:

```text
Time_crystal\
│
├── TC_INGEST_v001\
├── TC_PHYS_v001\
├── Data.zip
├── DTC_qiskit.ipynb.zip
└── Realization of a discrete time crystal on 57 qubits of a quantum computer.pdf
```

For reproducing `TC_PHYS_v001`, the essential input is:

```text
Data.zip
```

The Qiskit notebook and paper are retained as source/provenance material.

---

## 2. Preserve the supplied reference outputs

Open:

```text
Time_crystal\TC_PHYS_v001\
```

Before rerunning the analysis, rename:

```text
outputs
```

to:

```text
outputs_reference
```

This preserves the outputs supplied with the package.

After renaming, the folder should contain approximately:

```text
TC_PHYS_v001\
│
├── outputs_reference\
├── src\
├── MANIFEST.json
├── METHOD.md
├── README.md
├── requirements.txt
├── RESULT_SUMMARY.md
├── run_phys.py
├── RUN_WINDOWS.bat
└── SOURCE_HASHES.json
```

---

## 3. Copy the original data archive into TC_PHYS_v001

Copy:

```text
Time_crystal\Data.zip
```

into:

```text
Time_crystal\TC_PHYS_v001\
```

Do **not** extract, rename, or modify `Data.zip`.

The resulting folder should contain:

```text
TC_PHYS_v001\
│
├── Data.zip
├── outputs_reference\
├── src\
├── run_phys.py
├── RUN_WINDOWS.bat
└── ...
```

---

## 4. Check Python

Open `TC_PHYS_v001` in Windows Explorer.

Click the Explorer address bar, type:

```text
cmd
```

and press **Enter**.

A Command Prompt should open directly in the `TC_PHYS_v001` folder.

Check Python:

```bat
python --version
```

A normal response is:

```text
Python 3.x.x
```

If Windows reports that `python` is not recognized, install Python 3 and make sure the installer option **Add Python to PATH** is enabled.

---

## 5. Install the required Python packages

From the same Command Prompt run:

```bat
python -m pip install -r requirements.txt
```

The package requires:

```text
numpy
matplotlib
```

This installation normally needs to be done only once for the Python environment being used.

---

## 6. Run the reproduction

### Recommended first run

From Command Prompt:

```bat
python run_phys.py Data.zip outputs
```

Alternatively, double-click:

```text
RUN_WINDOWS.bat
```

or run:

```bat
RUN_WINDOWS.bat
```

The analysis reads `Data.zip` directly and creates a new:

```text
outputs\
```

folder.

---

## 7. Expected console result

A successful baseline reproduction should report approximately:

```text
STATUS: PASS_PHYSICS_RECONSTRUCTION
DAT files: 84
variance raw peak epsilon: 0.090000
variance smoothed peak epsilon: 0.075500
decay segmented break epsilon: 0.080000
consensus epsilon: 0.077750
published reference epsilon_c: 0.075000
|consensus - 0.075|: 0.002750
DTC/thermal half-frequency ratio: 31.532
DTC late aligned mean: 0.623396
thermal late abs aligned mean: 0.000868
```

Very small floating-point differences in the final decimal places can occur between Python/NumPy versions.

The important result is recovery of:

```text
PASS_PHYSICS_RECONSTRUCTION
```

with values close to:

```text
raw variance maximum      ≈ 0.090
smoothed variance peak    ≈ 0.0755
decay transition          ≈ 0.080
consensus transition      ≈ 0.07775
```

The published reference transition is approximately:

```text
epsilon_c ≈ 0.075
```

---

## 8. Expected output files

After a successful run:

```text
TC_PHYS_v001\
│
├── outputs_reference\
└── outputs\
    ├── epsilon_scan.csv
    ├── fig2_reproduction.png
    ├── file_metrics.csv
    ├── mitigation_sensitivity.csv
    ├── physics_validation.json
    ├── qubit_filter.csv
    ├── representative_traces.csv
    ├── RUN_LOG.txt
    ├── transition_decay.png
    └── transition_variance.png
```

Start by opening:

```text
outputs\RUN_LOG.txt
```

Then inspect:

```text
outputs\physics_validation.json
```

The final status should be:

```text
PASS_PHYSICS_RECONSTRUCTION
```

---

## 9. Visual checks

Open:

```text
outputs\fig2_reproduction.png
```

This should show the qualitative separation between the persistent `epsilon = 0.05` DTC-like oscillations and the rapidly depolarizing `epsilon = 0.50` thermal regime.

Open:

```text
outputs\transition_variance.png
```

The reconstructed smoothed critical-fluctuation maximum should lie near:

```text
epsilon ≈ 0.0755
```

Open:

```text
outputs\transition_decay.png
```

The reconstructed depolarization transition should lie near:

```text
epsilon ≈ 0.08
```

---

## 10. Compare your run with the supplied reference

You now have:

```text
outputs_reference\
```

and:

```text
outputs\
```

Compare the compact run logs:

```bat
fc outputs_reference\RUN_LOG.txt outputs\RUN_LOG.txt
```

If they are byte-identical, Windows reports:

```text
FC: no differences encountered
```

You can also compare:

```text
outputs_reference\physics_validation.json
outputs\physics_validation.json
```

and:

```text
outputs_reference\epsilon_scan.csv
outputs\epsilon_scan.csv
```

Minor numerical-formatting differences between software versions are acceptable. The transition values and PASS/FAIL result should remain numerically equivalent.

---

## 11. Optional source-integrity check

`SOURCE_HASHES.json` contains SHA-256 hashes of the source files used to build the package.

To calculate the hash of your local `Data.zip` in PowerShell:

```powershell
Get-FileHash .\Data.zip -Algorithm SHA256
```

Compare the result with the `Data.zip` entry in:

```text
SOURCE_HASHES.json
```

A matching hash confirms that the experimental archive is byte-identical to the source used for the reference run.

---

## 12. If the run fails

### Python is not found

Run:

```bat
python --version
```

If Python is unavailable, install Python 3 and enable **Add Python to PATH**.

### Missing NumPy or Matplotlib

Run:

```bat
python -m pip install -r requirements.txt
```

### `Data.zip was not found`

Confirm that `Data.zip` is physically inside:

```text
TC_PHYS_v001\
```

beside:

```text
RUN_WINDOWS.bat
run_phys.py
```

### The number of `.dat` files is not 84

Stop the reproduction and verify that the original `Data.zip` has not been modified.

### Numerical results differ substantially

Do not proceed to the UNNS closure stage. First compare:

```text
outputs\RUN_LOG.txt
outputs\physics_validation.json
outputs\mitigation_sensitivity.csv
```

against the corresponding files in:

```text
outputs_reference\
```

---

## 13. Reproduction gate

The physics-validation layer is considered reproduced when all of the following hold:

```text
DAT files = 84
DTC-like epsilon=0.05 response persists
epsilon=0.50 response thermalizes rapidly
critical-fluctuation transition is recovered near the published region
depolarization transition is independently recovered in the same region
STATUS = PASS_PHYSICS_RECONSTRUCTION
```

Only after this gate passes should the project proceed to the independent UNNS temporal-closure stage.

The next stage is:

```text
TC_CLOSURE_v001
```

where the physics-validated trajectories are converted into temporal recurrence ladders and the UNNS closure spectrum is tested without tuning it to reproduce the known DTC transition.
