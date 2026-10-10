# Data and code from: Superparamagnetism in an interacting nanomagnet array: A tale of three temperatures

**Authors:** Anthony Hurben¹, Ioan-Augustin Chioar¹²³⁴, Cristiano Nisoli⁵, Peter Schiffer¹²

¹ Department of Applied Physics, Yale University, New Haven, CT, USA
² Department of Physics, Princeton University, Princeton, NJ, USA
³ Department of Physics and Astronomy, University of Maine, Orono, ME, USA
⁴ Frontiers Institute for Research in Sensor Technologies, University of Maine, Orono, ME, USA
⁵ Theoretical Division and Center for Nonlinear Studies, Los Alamos National Laboratory, Los Alamos, NM, USA

**Associated publication:** A. Hurben, I.-A. Chioar, C. Nisoli, and P. Schiffer, "A tale of three temperatures: superparamagnetism in an interacting nanomagnet array," *Physical Review Letters* (2026). [https://doi.org/10.1103/f92d-w6fn](https://doi.org/10.1103/f92d-w6fn)

## Summary

This dataset contains the C++ source code and the raw simulation output that support the figures of the publication above. We model artificial square spin ice as an array of interacting, ellipsoidal, single-domain permalloy macrospins (Ising-like "dipoles") whose magnetization depends on temperature as M(T) = M₀(1 − T/T_C)^β. We use two Monte Carlo methods:

1. **Equilibrium Metropolis Monte Carlo (MMC: MMC_Code.zip and MMC_Data.zip ).** This method gives the equilibrium thermodynamics. From it, we extract the ordering temperature T_O, defined as the maximum of the first derivative of the order parameter.
2. **Superparamagnetic Metropolis Monte Carlo (SPMMC: SPMMC_Code.zip and SPMMC_Data.zip ).** This is a fixed-timestep kinetic Monte Carlo method. The Metropolis acceptance probability is replaced by the ratio Δτ/τᵢ between the simulation time step and each macrospin's Néel–Brown reversal time. The method simulates real-time cooling on laboratory timescales, so it captures the blocking/freezing of the array.

All simulations use a 24 × 24 vertex square-ice array (1200 macrospins, 576 vertices) with free boundary conditions. Material parameters are those of permalloy: M₀ = 7.9 × 10⁵ A/m and T_C = 820 K. The acquisition time is τ_aq = 1 s and the inverse attempt frequency is τ₀ = 10⁻⁹ s. The lattice parameter a and island length l are fixed at 260 nm and 160 nm unless noted otherwise. Section II of the Supplemental Material gives the full model and algorithm.

---

## Description of the data and file structure

### Top-level layout

```
3T Data Repository/
├── ReadMe.md                              
├── no copyrighted materials used.txt      
├── SPMMC Code/
│   └── SPMMC-SSI-Unix-v1.00.cpp           (superparamagnetic Metropolis Monte Carlo source code)
├── MMC Code/
│   └── MMC-SSI-Unix-v1.00.cpp             (equilibrium Metropolis Monte Carlo source code)
├── SPMMC Data/
│   └── spmmc_runs.zip                     (SPMMC runs, geometry sweep, β = 0.5)
└── MMC Data/
    ├── MMC_beta05.zip                     (MMC runs, geometry sweep, β = 0.5)
    └── MMC_vary_beta.zip                  (MMC runs, β sweep 0.05–0.95, 5 geometries)
```

### Mapping of data to manuscript figures

| Figure                                                                                                                 | Data used                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Main text Fig. 2(a): T\_B and T\_O vs β                                                                                | `MMC_vary_beta.zip`: T\_O is extracted from the Main Data Files (mean of 3 runs). T\_B is tabulated in `Fig2BlockingTemperatureData.txt`. |
| Main text Fig. 2(b): T\_O/T\_B contour vs w/l and h/l                                                                  | `MMC_beta05.zip` (T\_O, w = 40–74 nm, h = 10–25 nm). T\_B is computed analytically from Eq. (28)/(29) of the Supplemental Material. |
| Main text Fig. 3 and Supplemental Fig. 6: order parameter and vertex fractions vs T (w = 40, 50, 60, 70 nm; h = 16 nm) | Solid lines: `MMC_beta05.zip` (mean of 10 runs). Squares: `spmmc_runs.zip` (mean of 20 runs). |
| Main text Fig. 4: final Type 1 vertex fraction and order parameter vs w and h                                          | `spmmc_runs.zip`, last temperature row of each Main Data File (mean of 20 runs), w = 40–74 nm, h = 10–25 nm. |
| Supplemental Table I                                                                                                   | Derived from the same data as Fig. 3. |

Only the **Main Data Files** (and `Fig2BlockingTemperatureData.txt`) were used to make the figures. The other outputs (snapshots, time averages, system info, neighbourhood statistics) are included for completeness and reproducibility.

**Geometries not used in the paper:** both `spmmc_runs.zip` and `MMC_beta05.zip` contain folders for island widths w = 76, 78 and 80 nm. These were **not used** in the publication. In `spmmc_runs.zip` they are also incomplete. Only `Run1` contains data (`Run2`–`Run20` are empty folders), and these `Run1` simulations were stopped before reaching their final temperature: they contain between 0 and 78 temperature rows. Three of them (`w78_h22`, `w80_h22`, `w80_h25`) have a header-only Main Data File. In most of them, the Snapshots and Time Averages folders hold one more file than the Main Data File has rows, because the last temperature step was not completed.

### Naming conventions

| Pattern                                                      | Meaning                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `a{A}_l{L}_w{W}_h{H}`                                        | System geometry folder. A = lattice parameter (centre-to-centre distance between neighbouring vertices), L = island length, W = island width, H = island height (thickness), all in nm. Example: `a260_l160_w60_h16` → a = 260 nm, l = 160 nm, w = 60 nm, h = 16 nm. |
| `beta_{X.XX}`                                                | Value of the magnetization critical exponent β used in that run (only in `MMC_vary_beta.zip`). |
| `Run{N}`                                                     | Independent repetition N of the same simulation, with a different random seed. Results in the paper are averages over runs. |
| `Runs_7_3_2025`, `MMC_8_21_2025`, `MMC_vary_beta_10_27_2025` | Root folder of each archive. The suffix is a date label (month\_day\_year) identifying the simulation batch. |
| `Temperature Index (N)`                                      | Zero-based index of the temperature step. It matches the `Index` column of the Main Data File in the same `Output` folder, so it can be converted to a temperature in K using that file. |
| `SPMMC-SSI-Unix-v1.01.cpp`, `MMC-SSI-Unix-v1.01.cpp`         | The exact source file compiled for that folder (v1.01). See [Code versions](#code-versions). |
| `run.out`                                                    | The Linux executable compiled from the `.cpp` file in the same folder (`g++ -O3`, linked against GSL). It is included only as a record and is not needed to use the data. |

### Archive structures

#### `SPMMC Data/spmmc_runs.zip`

```
Runs_7_3_2025/
└── a260_l160_w{W}_h{H}/                 126 geometry folders: W = 40, 42, …, 80; H = 10, 13, 16, 19, 22, 25
    ├── SPMMC-SSI-Unix-v1.01.cpp         source with W and H set for this folder
    ├── run.out                          compiled executable
    └── Run1/ … Run20/                   20 independent runs
        └── Output/
            ├── Main Data File.txt
            ├── Simulation Info/
            │   ├── Log File.txt
            │   ├── Dipole System Info File.txt
            │   └── Vertex System Info File.txt
            ├── Snapshots/                Run1–Run5 only (empty folder for Run6–Run20; w76–80: Run1 only)
            │   └── Snapshots - Temperature Index (N).txt
            └── Time Averages/            Run1–Run5 only (empty folder for Run6–Run20; w76–80: Run1 only)
                └── Time-Averaged Moments - Temperature Index (N).txt
```

All SPMMC runs use β = 0.5. The temperature window (initial/final temperature) is chosen automatically for each geometry (see the SPMMC code description), so the temperature range and number of rows differ between geometry folders. For example, w40_h10 covers 752 → 702 K and w60_h16 covers 790 → 752 K.

#### `MMC Data/MMC_beta05.zip`

```
MMC_8_21_2025/
└── a260_l160_w{W}_h{H}/                 126 geometry folders: W = 40, 42, …, 80; H = 10, 13, 16, 19, 22, 25
    ├── MMC-SSI-Unix-v1.01.cpp           source with W and H set for this folder
    ├── run.out
    └── Run1/ … Run10/                   10 independent runs
        └── Output/
            ├── Main Data File.txt
            ├── Spin Vertex Neighborhood Statistics File.txt
            ├── Simulation Info/
            │   ├── Log File.txt
            │   ├── Dipole System Info File.txt
            │   └── Vertex System Info File.txt
            └── Snapshots/
                └── Snapshots - Temperature Index (N).txt
```

All runs use β = 0.5. Each run starts at 819 K and cools in 1 K steps until the halting criterion is reached (decorrelation steps ≥ 1000; see the MMC code description). The number of temperature rows therefore varies between geometries.

#### `MMC Data/MMC_vary_beta.zip`

```
MMC_vary_beta_10_27_2025/
├── Fig2BlockingTemperatureData.txt      T_B vs β for the 5 geometries (see below)
├── Legend.txt                           column legend for Fig2BlockingTemperatureData.txt
└── a{A}_l{L}_w{W}_h{H}/                 5 geometry folders (below)
    ├── MMC-SSI-Unix-v1.01.cpp           generic template (default parameters; geometry and β are inserted by the script)
    ├── bash_create_folders_and_insert_compiled_cpp_varied_beta.sh
    └── beta_0.05/ … beta_0.95/          19 β values in steps of 0.05
        ├── MMC-SSI-Unix-v1.01.cpp       source with this folder's geometry and β set
        ├── run.out
        ├── Run1/ … Run3/                3 independent runs
        │   └── Output/                  same structure as MMC_beta05 above
        └── Run4/, Run5/                 empty folders (created by the script, never run)
```

The five geometry folders are `a260_l160_w60_h16`, `a260_l160_w80_h16`, `a260_l180_w60_h16`, `a260_l160_w60_h20` and `a300_l160_w60_h16`. Main text Fig. 2(a) shows the w = 60 nm and w = 80 nm series (a = 260, l = 160, h = 16 nm), averaged over the 3 runs. The maximum number of decorrelation steps (the halting criterion) is 5000 for `a260_l160_w60_h16` and 1000 for the other four geometries; each run's value is recorded in its `Log File.txt`.

Runs at low β freeze very close to T_C, so they contain only a few temperature rows. In 24 runs, all with β ≤ 0.15, the halting criterion was already met at the first temperature (819 K), so their Main Data File contains only the header and their Snapshots folder is empty.

The bash script `bash_create_folders_and_insert_compiled_cpp_varied_beta.sh` generates the `beta_*` folders. The geometry is hard-coded at the top of each folder's copy of the script. For each β, the script:

1. creates `beta_X.XX/Run1…Run5`;
2. copies the template `.cpp` into the folder;
3. uses `sed` to overwrite the lattice parameter, island length, width and height (source lines 62, 64, 66 and 68) and β (line 100);
4. compiles the result to `run.out`.

---

## Files and variables

All data files are plain-text, tab-delimited ASCII. Unless stated otherwise, each file has a single header row of column names. Blank lines may appear between data rows and should be skipped. Within each run, "Mean" and "Stdev" are the mean and standard deviation over the samples taken *at that temperature*: the acquisitions for SPMMC and the sampled snapshots for MMC. Averages over independent runs (`Run1`, `Run2`, …) are **not** pre-computed and must be calculated by the user. A Main Data File that contains only the header row means the run completed no temperature steps (see the notes on the w = 76–80 nm SPMMC runs and the low-β MMC runs above).

### File: `Main Data File.txt` (SPMMC)

One row per temperature, 24 columns. Rows are in cooling order. At each temperature, the system evolves for 60 consecutive acquisitions of τ_aq = 1 s each (a dwell time of 1 min).

| Column | Name in header                                                                 | Description                                                                                                                                                                                                                                                                                                                                 | Units          |
| ------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| 1      | `Index`                                                                        | Temperature index (0 = first/highest temperature)                                                                                                                                                                                                                                                                                           | –              |
| 2      | `Temperature`                                                                  | Simulation temperature                                                                                                                                                                                                                                                                                                                      | K              |
| 3–4    | `Time_Step(Mean)`, `Time_Step(Stdev)`                                          | Simulation time step Δτ per lattice sweep (Eq. 30 of the SM), averaged within each acquisition, then mean/stdev over the 60 acquisitions. Δτ = τ\_aq = 1 s means the system is effectively frozen. | s              |
| 5–6    | `Number_of_Sweeps(Mean)`, `Number_of_Sweeps(Mean)`                             | Number of lattice sweeps needed to cover one acquisition time. **Header typo:** the second column (6) is the **standard deviation**, not a second mean. | –              |
| 7–8    | `Reversal_Times(Mean)`, `Reversal_Times(Stdev)`                                | Mean and standard deviation, over all 1200 macrospins, of the Néel–Brown reversal time τᵢ (Eq. 3 of the main text) at the end of the temperature step                                                                                                                                                                                       | s              |
| 9–10   | `Number_of_Single_Flips_per_Dipole(Mean)`, `Number_of_Flips_per_Dipole(Stdev)` | Average number of moment reversals per macrospin during one acquisition (mean/stdev over acquisitions)                                                                                                                                                                                                                                      | –              |
| 11–12  | `Snapshot_Autocorrelator(Mean)`, `(Stdev)`                                     | Spin autocorrelator between the configurations at the start and end of an acquisition, (1/N)Σᵢ σᵢ(start)·σᵢ(end). 1 = no change (frozen), ≈0 = fully decorrelated. | –              |
| 13–14  | `Average_Dipole_Moment(Mean)`, `(Stdev)`                                       | Time-averaged absolute moment per macrospin during an acquisition, (1/N)Σᵢ \|⟨σᵢ⟩\_t\|. 1 = static (blocked) moments, ≈0 = rapidly fluctuating (superparamagnetic) moments. | – (normalised) |
| 15–22  | `Vertex_Type_I…IV_Percentage(Mean)`, `(Stdev)`                                 | Fraction of the 576 vertices in Type 1, 2, 3 and 4 configurations at the end of each acquisition. **Despite the header name, values are fractions (0–1), not percentages.** Type 1 is the ground-state vertex (see main text Fig. 1). | fraction       |
| 23–24  | `Order_Parameter(Mean)`, `(Stdev)`                                             | Absolute value of the staggered antiferromagnetic (F-model) order parameter, computed from the Type 1 vertices: \|Σ\_v c\_v s\_v\|/N\_vertices. Here c\_v = ±1 alternates in a checkerboard pattern over the vertex lattice, and s\_v = +1 or −1 for the two Type 1 configurations (0 for all other types). 1 = perfect ground-state order. | –              |

For Fig. 4 of the paper, the "final" Type 1 fraction and order parameter are taken from the last row of each run and averaged over the 20 runs.

### File: `Main Data File.txt` (MMC)

One row per temperature, 21 columns. Rows are in cooling order, starting at 819 K in 1 K steps. At each temperature, the code performs 10,000 thermalisation "modified MC steps", then samples 10,000 configurations, each separated by `Decorrelation_Steps` lattice sweeps.

| Column | Name in header                                               | Description                                                                                                                                                                                              | Units    |
| ------ | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| 1      | `Index`                                                      | Temperature index                                                                                                                                                                                        | –        |
| 2      | `Temperature`                                                | Simulation temperature                                                                                                                                                                                   | K        |
| 3–4    | `Spin_Flip_Acceptance_Ratio_Thermalization(Mean)`, `(Stdev)` | Fraction of macrospins flipped per lattice sweep during the thermalisation phase. | –        |
| 5–6    | `Spin_Autocorrelator_Decorrelation_MCsteps(Mean)`, `(Stdev)` | Number of lattice sweeps needed for the spin autocorrelator to drop below the threshold of 0.05 during thermalisation. A cap of 100 is applied when this value is used to compute `Decorrelation_Steps`. | sweeps   |
| 7      | `Decorrelation_Steps`                                        | Number of lattice sweeps between successive sampled configurations: 2 × (autocorrelator steps + ⌈1/acceptance ratio⌉). The run stops when this reaches the maximum given in the Log File. | sweeps   |
| 8–9    | `Spin_Flip_Acceptance_Ratio_Sampling(Mean)`, `(Stdev)`       | Fraction of macrospins flipped per lattice sweep during sampling. | –        |
| 10–11  | `Snapshot_Autocorrelator(Mean)`, `(Stdev)`                   | Spin autocorrelator between successive sampled configurations. | –        |
| 12–19  | `Vertex_Type_I…IV_Percentage(Mean)`, `(Stdev)`               | Fractions (0–1, not percentages) of vertices of Type 1–4, averaged over the sampled configurations                                                                                                       | fraction |
| 20–21  | `Order_Parameter(Mean)`, `(Stdev)`                           | Absolute staggered order parameter, as defined for SPMMC                                                                                                                                                 | –        |

T_O (used in Figs. 2 and 3) is the temperature at which the run-averaged `Order_Parameter(Mean)` has the steepest slope, i.e., the maximum of its first derivative with respect to temperature.

### File: `Spin Vertex Neighborhood Statistics File.txt` (MMC only)

Columns: `Index`, `Temperature`, then `Spin_Vertex_Neighborhood_Configuration_Class(#k)(Mean)` and `(Stdev)` for k = 1…21 (44 columns in total). Each macrospin touches two vertices. Its "spin-vertex neighbourhood" is the configuration of the 7 macrospins on those two vertices, and the code groups the possible configurations into 21 symmetry classes. Each value is the fraction of macrospins whose neighbourhood falls in class k. **This file was not used in the publication.**

### File: `Simulation Info/Log File.txt`

A human-readable list of the input parameters used for the run, in the form `Parameter name: value`. It includes periodic boundary conditions (always NO), whether the vertex interaction model is enabled, the interaction cut-off radius (nm), the spontaneous magnetization at 0 K (10⁵ A/m), the critical exponent β, and the Curie temperature (K). It also includes the initial and final temperatures and the temperature step (K). SPMMC logs also list τ₀, the acquisition time, the number of acquisitions, the initial/final reversal frequencies, and the time-step fraction f_τ. MMC logs list the thermalisation/sampling steps and the decorrelation settings.

### File: `Simulation Info/Dipole System Info File.txt`

One row per macrospin (1200 rows; the array has 24 × 24 vertices with free edges).

| Column                                                                             | Description                                                                                                                            | Units |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| `Dipole_Index`                                                                     | Index of the macrospin (0–1199). This index is the column position in the Snapshots and Time Averages files. | –     |
| `Dipole_Coordinate_X(nm)`, `Dipole_Coordinate_Y(nm)`                               | Position of the island centre                                                                                                          | nm    |
| `Dipole_Unit_Vector_X`, `Dipole_Unit_Vector_Y`                                     | Reference direction of the island's moment. A state σ = +1 means the moment points along this vector; σ = −1 means it points opposite. | –     |
| `Dipole_Island_Length(nm)`, `Dipole_Island_Width(nm)`, `tDipole_Island_Height(nm)` | Island dimensions. The leading "t" in the last header is a typo. | nm    |
| `Dipole_To_Vertex(0)`, `Dipole_To_Vertex(1)`                                       | Indices of the two vertices at the ends of the island. −1 means the island is on the array edge and has no vertex on that side. | –     |

### File: `Simulation Info/Vertex System Info File.txt`

One row per vertex (576 rows).

| Column                                               | Description                                                    | Units |
| ---------------------------------------------------- | -------------------------------------------------------------- | ----- |
| `Vertex_Index`                                       | Index of the vertex (0–575). Vertex index = row × 24 + column. | –     |
| `Vertex_Coordinate_X(nm)`, `Vertex_Coordinate_Y(nm)` | Vertex position                                                | nm    |
| `Vertex_To_Dipole(0)` … `Vertex_To_Dipole(3)`        | Indices of the four macrospins meeting at this vertex          | –     |

### File: `Snapshots/Snapshots - Temperature Index (N).txt`

There is no header. Each line is a full microstate: 1200 tab-separated values of ±1 (σᵢ), where column i corresponds to `Dipole_Index` i.

* **SPMMC:** 61 lines per file. Line 1 is the configuration at the start of temperature step N; lines 2–61 are the configurations at the end of each of the 60 acquisitions.
* **MMC:** 1 line per file, the final sampled configuration at temperature step N.

### File: `Time Averages/Time-Averaged Moments - Temperature Index (N).txt` (SPMMC only)

There is no header. The file has 60 lines (one per acquisition) × 1200 tab-separated columns (one per macrospin). Each value is the time-averaged moment ⟨σᵢ⟩_t of macrospin i over that 1 s acquisition, in [−1, 1]. ±1 means the moment did not reverse; values near 0 mean it fluctuated rapidly.

### File: `Fig2BlockingTemperatureData.txt` (in `MMC_vary_beta.zip`)

There is no header. It has 19 rows (one per β) and 6 tab-separated columns.

| Column | Description                                                                                                                            | Units |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| 1      | Magnetization critical exponent β (0.05–0.95)                                                                                          | –     |
| 2–6    | Intrinsic (non-interacting) single-island blocking temperature T\_B for the geometries listed as "Column 1"–"Column 5" in `Legend.txt` | K     |

T_B is the temperature at which an isolated island's reversal time equals τ_aq = 1 s. It is the solution of Eq. (28) of the Supplemental Material, [ln(τ_aq/τ₀)/(t₀ΔN)]·t_B = (1 − t_B)^{2β}, with t_B = T_B/T_C. It depends on the island dimensions only, not on the lattice parameter. At small β, T_B saturates at T_C = 820 K.

### File: `Legend.txt` (in `MMC_vary_beta.zip`)

Maps data columns 2–6 of `Fig2BlockingTemperatureData.txt` to geometries, in the format `length × width × height – lattice parameter`:

| Legend entry | Data column | Geometry (l × w × h, a)      |
| ------------ | ----------- | ---------------------------- |
| Column 1     | 2           | 160 × 60 × 16 nm, a = 260 nm |
| Column 2     | 3           | 180 × 60 × 16 nm, a = 260 nm |
| Column 3     | 4           | 160 × 80 × 16 nm, a = 260 nm |
| Column 4     | 5           | 160 × 60 × 20 nm, a = 260 nm |
| Column 5     | 6           | 160 × 60 × 16 nm, a = 300 nm |

---

## Code/software

Both programs are single-file C++ codes written for Linux/Unix. They need the [GNU Scientific Library (GSL)](https://www.gnu.org/software/gsl/), which they use for the Mersenne-Twister random number generator and for the elliptic integrals in the Osborn demagnetization factors. They take no input files: every parameter is set in the `SIMULATION PARAMETERS` block at the top of the source, and the code must be recompiled after a change. Each run is seeded from`std::random_device`, so repeated runs are statistically independent and not bit-for-bit reproducible.

**Compile and run (both codes):**

```bash
g++ -Wall -O3 SPMMC-SSI-Unix-v1.00.cpp -o run.out -lgsl -lgslcblas -lm   # or MMC-SSI-Unix-v1.00.cpp
./run.out /path/to/RunN
```

The only command-line argument is the folder to write to. The program creates `Output/`, `Output/Simulation Info/`, `Output/Snapshots/` (and, for SPMMC, `Output/Time Averages/`) inside that folder. It writes the files described above, appending one row to the Main Data File after each temperature. To reproduce a dataset folder, compile the `*-v1.01.cpp` copy stored in that folder; it contains the exact parameters used.

Post-processing (averaging over runs, extracting T_O and plotting) was done separately and is not included.

### Code versions

Each code exists in two versions in this dataset:

| Version   | Location                                                                                                               | Purpose                                                                                                |
| --------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **v1.00** | `SPMMC Code/SPMMC-SSI-Unix-v1.00.cpp`, `MMC Code/MMC-SSI-Unix-v1.00.cpp`                                               | General-purpose template with default parameters. Start here to run new simulations. |
| **v1.01** | `SPMMC-SSI-Unix-v1.01.cpp` / `MMC-SSI-Unix-v1.01.cpp` inside every geometry (and `beta_*`) folder of the data archives | The exact code compiled to produce the data in that folder. Use it to reproduce the published results. |

The v1.01 copies differ from v1.00 as follows. There are no changes to the physics or the algorithm, apart from MMC item 3.

**SPMMC (v1.01 vs v1.00):** only the values of `island_width_mean` and `island_height` differ; they are set to the folder's w and h.

**MMC (v1.01 vs v1.00):**

1. The geometry is set to the folder's values: `lattice_parameter` (260 nm, or 300 nm for `a300_…`; the v1.00 default is 220 nm), `island_length_mean`, `island_width_mean` and `island_height`. In`MMC_vary_beta.zip`, β (`magnetization_critical_exponent`) is also set per folder, and for the `a260_l160_w60_h16` geometry only, `decorrelation_steps_maximum` is raised from 1000 to 5000.
2. `#include <random>` is added. It is required for`std::random_device`, which seeds the random number generator, and some compilers need it for v1.00 to compile.
3. In `compute_vertex_statistics()` the absolute value of the order parameter is taken (`order_parameter = abs(order_parameter);`), matching the SPMMC code. The published MMC order parameters are therefore the absolute values.
4. An unused `time(0)` call is commented out.

In `MMC_vary_beta.zip`, the v1.01 copy at the geometry level is a template that still has the default geometry (w = 60 nm, h = 15 nm) and β = 0.5. `bash_create_folders_and_insert_compiled_cpp_varied_beta.sh` copies it into each `beta_*` folder, sets the geometry and β`sed`, and compiles the result. The copies inside the `beta_*` folders are therefore the ones that produced the data.

### `SPMMC Code/SPMMC-SSI-Unix-v1.00.cpp` — Superparamagnetic Metropolis Monte Carlo

This file implements the SPMMC algorithm of the main text and Supplemental Material Sec. II.B (flowchart in SM Fig. 4). It simulates real-time thermal evolution of an interacting array of macrospins during a stepwise cooling protocol.

**Physics.** Each macrospin i has a reversal time from the modified Néel–Brown law, ln(τᵢ/τ₀) = t₀·[(1 − t)^{2β}/t]·(ΔN − σᵢHᵢ) (main text Eq. 3), with t = T/T_C.

* ΔN is the easy/hard-axis demagnetization-factor difference of an ellipsoid (Osborn formulae).
* Hᵢ is the normalised dumbbell ("centres of charge") interaction field from all other islands. In these runs the interaction is effectively unlimited in range (cut-off 10⁷ nm, `Vertex Interaction Model = NO`).
* t₀ = μ₀M₀²V/(2k_BT_C).

**Algorithm (main loop in** **`main()`):**

1. **Initialisation.** The code builds the square-ice lattice, assigns random initial spins, computes ΔN, the pairwise coupling factors and the interaction fields, and writes the Simulation Info files. When `enable_automatic_temperature_window_initialization = true` (used for all data), it sets T_init and T_final automatically from SM Eqs. (31)–(32). T_init is where the most stable spin reverses on average 10 times per acquisition (`initial_dipole_reversal_frequency = 10`). T_final is where the least stable spin reverses on average 10⁻⁴ times per acquisition (`final_dipole_reversal_frequency = 0.0001`).
2. **Temperature loop.** The code cools from T_init to T_final in steps of `T_step` = 1 K and recomputes all τᵢ at each temperature.
3. **Acquisition loop.** It runs `number_of_acquisitions` = 60 acquisitions of `acquisition_time` = 1 s each, giving a 1 min dwell per temperature.
4. **Time loop.** Within an acquisition, the code repeatedly picks a time step Δτ = f_τ·min(τᵢ)/N (f_τ = `time_step_fraction` = 0.5, capped at τ_aq) and performs a lattice sweep until the acquisition time is reached.
5. **Lattice sweep.** All N spins are visited once, in a freshly randomised order, and each is flipped with probability Δτ/τᵢ. After each flip, the code updates the reversal times of the flipped spin and of all spins it interacts with.
6. **Output.** At the end of each acquisition it computes the flips per dipole, the autocorrelator, the time-averaged moments, the vertex fractions and the order parameter. At the end of each temperature it writes the mean/stdev row to `Main Data File.txt`.

**Code sections** (marked by `#pragma region` comments): `SIMULATION PARAMETERS`; `GENERAL FUNCTIONS` (file I/O and statistics helpers); `INITIALIZATION` (lattice, demagnetization factors, interaction web, temperature window, output files); `THERMAL DYNAMICS` (reversal times, time step, lattice sweep); `DATA OUTPUT` (observables and Main Data File); `MAIN FUNCTION`.

**Key user parameters** (with the values used for the published data):

| Parameter                                                                  | Value     | Meaning                                                                                                   |
| -------------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------- |
| `lattice_linear_size`                                                      | 24        | Vertices per side                                                                                         |
| `lattice_parameter`                                                        | 260       | a (nm)                                                                                                    |
| `island_length_mean`, `island_width_mean`, `island_height`                 | 160, w, h | Island dimensions (nm); set per geometry folder                                                           |
| `island_length_stdev`, `island_width_stdev`                                | 0         | Optional size disorder (nm)                                                                               |
| `Curie_temperature`                                                        | 820       | T\_C (K)                                                                                                  |
| `spontaneous_magnetization0`                                               | 7.9       | M₀ (10⁵ A/m)                                                                                              |
| `magnetization_critical_exponent`                                          | 0.5       | β                                                                                                         |
| `periodic_boundary_conditions_enabled`                                     | false     | Free boundaries                                                                                           |
| `vertex_interaction_model_enabled`                                         | false     | false = all pairs within `interaction_range_cutoff_radius`; true = only the 6 neighbours sharing a vertex |
| `barrier_adjustment_ratio`, `interaction_adjustment_ratio`                 | 1.0       | Optional global scaling of barrier/interaction energies                                                   |
| `tau0`                                                                     | 10⁻⁹      | Inverse attempt frequency (s)                                                                             |
| `acquisition_time`, `number_of_acquisitions`                               | 1.0, 60   | τ\_aq (s) and acquisitions per temperature                                                                |
| `time_step_fraction`                                                       | 0.5       | f\_τ                                                                                                      |
| `T_step`                                                                   | 1.0       | Cooling step (K)                                                                                          |
| `enable_dipole_flip_sequences_storage`, `enable_dipole_flip_times_storage` | false     | Optional extra outputs (very large)                                                                       |

**Note on snapshots in the deposited SPMMC code.** To save disk space, the call to `store_acqusition_data(...)` in `compute_acquisition_run_output_data()` is commented out, and the `enable_snapshots_storage` / `enable_time_avg_storage` flags inside that function are `false`. As deposited, the code therefore writes only the Main Data File and the Simulation Info files. The Snapshots and Time Averages provided for Run1–Run5 were produced with this storage switched on. To regenerate them, uncomment that call and set both flags to `true`.

**Version used for the data:** `SPMMC-SSI-Unix-v1.01.cpp` in each geometry folder (see [Code versions](#code-versions)).

### `MMC Code/MMC-SSI-Unix-v1.00.cpp` — Equilibrium Metropolis Monte Carlo

This is a standard single-spin-flip Metropolis Monte Carlo code using the same macrospin energy model (ΔN, dumbbell interactions, M(T) with critical exponent β). It gives at-equilibrium properties as a function of temperature and is used to extract T_O. Free boundary conditions are used. In these runs `vertex_interaction_model_enabled = true`, so each macrospin interacts with the 6 macrospins that share its two vertices.

**Algorithm:**

1. Starting at `T_init` = 819 K, it cools in steps of `T_step` = 1 K.
2. At each temperature, it performs `number_of_thermalization_steps` = 10,000 × (current decorrelation steps) lattice sweeps to thermalise. During thermalisation it measures the spin-flip acceptance ratio and the number of sweeps for the spin autocorrelator to drop below 0.05 (capped at 100).
3. It sets decorrelation steps = `decorrelation_multiplier` (2) × (autocorrelator sweeps + ⌈1/acceptance ratio⌉).
4. If decorrelation steps < `decorrelation_steps_maximum`, it samples `number_of_sampling_steps` = 10,000 configurations, each separated by that many sweeps. It records vertex fractions, the order parameter, the autocorrelator and the neighbourhood statistics, then writes one row of the Main Data File, the neighbourhood statistics file and a snapshot. **Otherwise the simulation halts:** the system is too slow to equilibrate, which sets the low-temperature end of each run. `T_final` = 1 K is only a nominal lower bound.

`decorrelation_steps_maximum` was 1000 for all of `MMC_beta05.zip` and for four of the five `MMC_vary_beta.zip` geometries. It was 5000 for `MMC_vary_beta.zip/…/a260_l160_w60_h16`. Each run's value is recorded in its `Log File.txt`.

**Code sections:** the same layout as the SPMMC code (`SIMULATION PARAMETERS`, `GENERAL FUNCTIONS`, `INITIALIZATION`, `THERMAL DYNAMICS`, `DATA OUTPUT`, `MAIN FUNCTION`). Each lattice sweep makes N single-spin Metropolis attempts on spins chosen at random (with replacement), starting from a random initial configuration.

**Version used for the data:** `MMC-SSI-Unix-v1.01.cpp` in each geometry/β folder. To reproduce the published MMC data exactly, compile that copy rather than v1.00 (see [Code versions](#code-versions) for the four differences).

---

## Access information

Other publicly accessible locations of the data:

* None.

Data was derived from the following sources:

* None. All data were generated by the simulation codes included in this dataset.

