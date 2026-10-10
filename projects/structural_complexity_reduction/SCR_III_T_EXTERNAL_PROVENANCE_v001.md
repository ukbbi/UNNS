# SCR_III_T_EXTERNAL — Data Provenance Record and Eligibility Assessment v001 (DRAFT, UNFROZEN)

**Date:** 2026-10-10 · **Scope:** provenance and measurability only. No vertex value, count or correlation of the file was read or computed. No scientific measurement has been made. Nothing here is preregistered.

## 1. The file
| Item | Finding |
|---|---|
| Path | `scr_iii_b/data/raw/mean_200nm_300K_50x50_verteximage.npz` |
| SHA-256 / size | `06b9d169e9fcf5dde4e9b3d4b1fe6fd80ff2baad474403d08b5e3e0ab3416892` / 906,809 bytes |
| Container | one member `images.npy`, a **pickled 0-d object array** holding a dict. Loading it normally executes pickle code from a downloaded file, so it was not loaded with `allow_pickle`. Metadata was read with a restricted unpickler allowing only numpy array reconstruction (opcode inspection showed only numpy `ndarray`, `dtype`, `_reconstruct`). |
| Content (structure only) | 90 arrays, each 50×50 `int32`; keys `run{k}_{f}` with k = 0..29 (30 runs) and f ∈ {0.75, 0.5, 0.25} (30 each) |
| Not read | the cell values, their frequencies or any statistic |

## 2. Source (corrects an assumption in the scoping note)
- The Dryad deposit 10.5061/dryad.cz8w9gjk0 (Hurben, Chioar, Nisoli, Schiffer; SPMMC and MMC code and data) **does not list this file**, as far as the Dryad page summary shows.
- The file matches the **Zenodo record 10.5281/zenodo.15548088** (Menniti, Leo, Villalba-González, Pancaldi, Vavassori; "Relaxation pathways and emergence of domains in square artificial spin ice"; kinetic Monte Carlo; CC BY 4.0), which the acquisition manifest also lists.
- Per that record (as summarised by the fetch tool; not independently read by me): the `mean` model is the mean-field barrier model; the image values 1–4 are vertex types T1–T4; snapshots are taken at the times when net magnetisation of each run has decayed to 75%, 50% and 25% of its initial value; 200 nm is the lattice periodicity and 300 K the simulation temperature. The record page reports runs 0–20 for its global data files, while this image file holds 30 runs. That discrepancy is unresolved.
- Images exist in the same record for 200, 240, 280, 300, 340 and 380 nm and for both a mean-field and a "split" barrier model.

## 3. Prior exposure
- In the project tree the file is referenced only by `scripts/run_preflight.py` and `ACQUISITION_MANIFEST_v001.json`, which record its hash. No analysis script, plot or grammar/window choice refers to it.
- A search of the UNNS Substrate Project docs and of past chats found no reference to it.
- This cannot certify non-exposure. Only Igor can confirm that the image was never viewed or used when the grammar, windows or observables were chosen.

## 4. Domain match with the frozen model
| | Frozen SCR-III-B physics | This image |
|---|---|---|
| Model | Dryad SPMMC dumbbell model | kMC with mean-field barriers |
| Ensemble | static, Boltzmann energy window at 792 K | non-equilibrium relaxation from saturation |
| Conditioning | none | snapshots conditioned on magnetisation reaching 75/50/25% |
| Lattice / temperature | template a = 260 nm; T_ref = 792 K | a = 200 nm; 300 K |

A grammar defines a set of configurations, not a probability or a relaxation path. Predicting these snapshots would need a frozen sampler that reproduces a magnetisation-conditioned, time-dependent ensemble, which nothing in the frozen model provides. Under the strategy's own criteria this points to **T INCONCLUSIVE (domain mismatch)** if the file were used as the confirmatory target.

## 5. Eligibility
**Classification: development/pilot data, not an eligible confirmatory target for the frozen model.** Reasons: undocumented-in-project source (now identified), strong domain mismatch, unresolved run-count discrepancy, and exposure not excluded. It remains usable only to check that an observable can be extracted (vertex-type map, neighbour pairs, boundary handling), and any look at its values consumes it. If used that way, record the look before any confirmatory design is frozen.

## 6. Alternative T targets to decide between
1. **Same-model equilibrium observables.** The Dryad SPMMC/MMC "Main Data File" holds vertex-type fractions versus temperature from the very model the frozen physics comes from. Domain-matched and not an energy-window target, but it tests the grammar against a simulation of the same model, not against experiment. (Data not on disk; the Dryad archives are 0.12 GB and 2.9 GB.)
2. **Other kMC images** (other periodicities, split model): same non-equilibrium mismatch, so no gain over this file.
3. **Experimental images** from a source not yet identified: highest value, highest cost.
4. **Discrimination check first (any option):** before collecting a target, show that a grammar-restricted ensemble and the unrestricted Boltzmann ensemble predict observables that differ by more than the measurement uncertainty. If they do not, the data cannot test the grammar. This can be done on synthetic data from the frozen model, with no held-out data touched.

## 7. Extraction plan (target-independent, to be frozen before any look)
Vertex-type map from the 50×50 matrix with a stated boundary rule; observables: type frequencies, ice-rule-violation fraction (T3+T4, diagnostic only), nearest-neighbour vertex-type correlations (principal), defect clustering (secondary); uncertainty from run-to-run spread; baselines: unrestricted model and ice-rule-uniform model. Tolerances come from the measurement uncertainty and are fixed before the look. Verdicts: T PASS / T FAIL / T INCONCLUSIVE as defined in the strategy note.

## 8. Decisions needed from Igor
1. Was this image ever viewed or used before today's checks?
2. Choose the confirmatory target tier: same-model equilibrium data (option 1), an experimental source (option 3), or defer until the discrimination check (option 4) is done.
3. Should the pilot look at this image be permitted for extraction testing, knowing it then cannot serve as confirmatory data?
4. Confirm the Zenodo run-count discrepancy against the paper or notebook.

## Addendum A (2026-10-10) — Zenodo primary documents added and checked
Files placed in `scr_iii_b/data/reference/zenodo_15548088/` by Igor (hashes SHA-256): `summary.txt` f975c65b…739b · `Figures_kMC.ipynb` 47e949df…e8f3 · `Figures_kMC.pdf` f2912bc1…7c3b. The notebook was read as JSON source text only; it was not executed, and no figure output or image value was opened.
Verified against these primary documents (upgrading the earlier second-hand fetch summary):
- Source: Menniti et al., kMC data and code, Zenodo 10.5281/zenodo.15548088. `mean` = mean-field model, `split` = chiral-split barrier model; periodicities 190–380 nm in the data description.
- Image files hold 50×50 matrices with values 1…4 for vertex types T1…T4, "shown for run0 at times where the net magnetisation reaches 75%, 50%, 25% of its initial value"; Fig. 2 uses a = 200, 240, 280 nm and Fig. 6 uses 300, 340, 380 nm.
- The notebook loads the file with `allow_pickle=True` and the `images` key, and sets `run_index = 0` before plotting `images[f'run{run_index}_{quantile}']`. Global time series loop over `len(data.columns)//5` runs; `summary.txt` says run numbers run 0 through 20. Our file holds 30 image runs (0–29); the notebook is a plotting script and does not explain that difference.
- Exposure note: the published figures, and therefore the notebook outputs and the PDF, display the run-0 snapshots of this file. Anyone who has looked at those figures has seen run 0 of this file. Runs 1–29 do not appear in the published figures.
Status: `SOURCE_CONFIRMED / FILE_USAGE_CONFIRMED / RUN_COUNT_ORIGIN_UNRESOLVED`. Classification stays **pilot/development data**; the run-count question is deprioritized unless trajectory count becomes necessary for uncertainty estimates. Open decision 4 above is downgraded; decisions 1–3 stand.
