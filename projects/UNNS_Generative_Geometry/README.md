# UNNS Generative Geometry — GEO-HD-1

**Higher-Dimensional Generative Geometry of the UNNS Substrate**  
**Research archive and manuscript source collection · 1 November 2026**

This directory preserves the **GEO-HD-1** mathematical research programme: the arithmetic geometry of distinct nested occurrences; transport between occurrence geometries; branching, interchange and recombination of generating histories; and changes of geometric and topological structure under actual UNNS transformations.

The archive is located locally at:

```text
D:\GitHub\UNNS\projects\UNNS_Generative_Geometry\
```

It is a **versioned research record**, not a single consolidated software release. The original preflight, subsequent releases, exact computational evidence, counterexamples and append-only corrections all remain part of that record. **No GEO-HD-1B, GEO-HD-1D or BRIDGE release is superseded merely by a later release.** Read the relevant theorem under its original hypotheses and status, together with any later correction.

**Current research baseline:** `GEO_HD_BRIDGE_v005` (1 November 2026). Active experimental expansion is paused while the results are consolidated for mathematical manuscript preparation. The existing GEO-I and Foundations archives remain separate, frozen references.

## 1. Scientific purpose

The governing question is whether the arithmetic structure of UNNS determines how occurrence geometries **transform, branch, merge, preserve information or become obstructed** under generation, and how these phenomena can be expressed as rigorous laws in three, four and arbitrary dimensions.

The programme distinguishes three related but nonidentical mathematical objects:

1. **State geometry:** occurrence indices and exponent-coordinate fibres, modular relation lattices, Graver relations, abstract or realized cell complexes and their topology.
2. **History geometry:** admissible ordered generating histories, legal swaps, different-content rewrites, recombination components, cubes and higher-dimensional homology.
3. **Evolving geometry:** structural changes along the explicitly defined FIELD-I collective map, including occurrence events, dormant-relation activation, primitive-move loss and topological transitions.

An identification between these objects requires an explicitly defined map and a proof. Similar numerical invariants or Betti numbers alone do not establish equivalence.

The SELECT-II successor rule and FIELD-I collective map are **specified mathematical grammars**; the original occurrence arithmetic does not uniquely force either interaction rule.

## 2. Release map

### HD-0 — Original baseline and preflight

| Location | Role |
|---|---|
| [`SPEC/`](SPEC/) | Original higher-dimensional research specification |
| [`BASELINE/`](BASELINE/) | Source locks, connecting-map analysis, overlap matrix and preflight verdict |
| [`DEFINITIONS.md`](DEFINITIONS.md), [`GEO_HD_1.pdf`](GEO_HD_1.pdf) | Initial definitions and original working proposal; read with later qualifications |
| [`STATUS.md`](STATUS.md), [`THEOREM_REGISTRY.md`](THEOREM_REGISTRY.md), [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) | **Historical 30 October preflight records**, not the current overall research status |
| [`src/`](src/), [`tests/`](tests/), [`Scripts/`](Scripts/), [`data/`](data/) | Original baseline scripts, exact examples and exploratory materials |

### GEO-HD-1B — Geometric transport and dimensional obstruction

| Release | Main subject |
|---|---|
| [`GEO_HD_E2_P1_v001/`](GEO_HD_E2_P1_v001/) | Geometric transport with changing relation lattices; initial exact failures of edge/cell preservation |
| [`GEO_HD_E2_P2_v001/`](GEO_HD_E2_P2_v001/) | Arithmetic criteria for transport between nontrivial relation lattices |
| [`GEO_HD_E2_P3_v001/`](GEO_HD_E2_P3_v001/) | Realized-cell transport, scoped planar preservation and higher-dimensional counterexamples |
| [`GEO_HD_E2_P4_v001/`](GEO_HD_E2_P4_v001/)–[`v005/`](GEO_HD_E2_P4_v005/) | Coupled-target obstruction theory, slab/cell criteria, exact planar-versus-3D boundary analysis |
| [`GEO_HD_E2_P4_v005_ERRATA_E1/`](GEO_HD_E2_P4_v005_ERRATA_E1/) | **Append-only correction** to the v005 closed-height-slab criterion |

A principal result is planar inclusion for the stated nested full-rank lattice and realized Graver-cell setting, while analogous 3D inclusion can fail even under vertex persistence. The geometry, lattice assumptions and exact correction to the slab condition matter; these are not universal claims about arbitrary geometric models.

### GEO-HD-1D — Global generative histories and recombination

| Release | Main subject |
|---|---|
| [`GEO_HD_1D_v001/`](GEO_HD_1D_v001/) | Exact admissibility thresholds for ordered histories; swap criteria, history counts and cubes |
| [`GEO_HD_1D_v002/`](GEO_HD_1D_v002/) | Source-dependent arithmetic filtration and swap-class threshold theory |
| [`GEO_HD_1D_v003/`](GEO_HD_1D_v003/) | Feeding digraphs, feasible subsets, disconnected swap classes and higher-dimensional history topology |
| [`GEO_HD_1D_v004/`](GEO_HD_1D_v004/) | Different-content endpoint equivalence through integer valuation kernels, admissible block rewrites and resource-sensitive completeness |

These releases show that equal numerical endpoints do not determine generating histories, and that admissible history spaces can have disconnected components, nontrivial loops and higher-dimensional structure. The history complex must not be conflated with the complex of an individual state.

### GEO-HD BRIDGE — Arithmetic, geometry and collective evolution

| Release | Main subject |
|---|---|
| [`GEO_HD_BRIDGE_v001/`](GEO_HD_BRIDGE_v001/) | Irreducible active-prime obstructions; connecting history arithmetic, occurrence events and selected FIELD-I dynamics |
| [`GEO_HD_BRIDGE_v002/`](GEO_HD_BRIDGE_v002/) | Integer-state geometric collapse; exact collective regimes and restricted event correspondence **subject to two errata** |
| [`GEO_HD_BRIDGE_v003/`](GEO_HD_BRIDGE_v003/) | Rational-state Graver structure beyond occurrence data; component invariants; persistent `G=5` and `G=11` families |
| [`GEO_HD_BRIDGE_v004/`](GEO_HD_BRIDGE_v004/) | Infinite arithmetic activation family, actual finite-exact collective activation and changing move-complex topology |
| [`GEO_HD_BRIDGE_v005/`](GEO_HD_BRIDGE_v005/) | Exact next-event sieve, divisor-interval move transitions, local/global homology-update identity and collective-tower results |

**Separate append-only BRIDGE v002 corrections:**

- [`GEO_HD_BRIDGE_v002_ERRATUM_B2-T9.md`](GEO_HD_BRIDGE_v002_ERRATUM_B2-T9.md): every SELECT-II edge strictly increases `σ` and changes `D`, but **does not generally preserve inclusion** `D(m) ⊆ D(m′)` or divisibility `σ(m) | σ(m′)`.
- [`GEO_HD_BRIDGE_v002_ERRATUM_B2-T7.md`](GEO_HD_BRIDGE_v002_ERRATUM_B2-T7.md): eventual `G=1` implies the stated three-step rigidity, but the converse fails; the persistent `G=5` family also has three-step multiplier 4.

Other correction and source-scope addenda are preserved in [`ERRATA/`](ERRATA/). Historical files remain unchanged.

## 3. Established mathematical results — selected overview

The following is an **orientation**, not a substitute for the theorem registers, proofs or release-specific restrictions.

**Arithmetic occurrence and geometric transport.** Exact exponent-coordinate occurrence models and relation-lattice cells support scoped planar transport theorems; genuinely higher-dimensional transport can fail. Later results identify arithmetic criteria for containment, loss and obstruction.

**Generative history geometry.** SELECT-II history admissibility has an exact valuation-based threshold. Labels can be reordered only when arithmetic resources permit the corresponding swaps. The feeding relation and feasible-subset structure explain disconnected classes; different-content histories with the same endpoint correspond to integer-kernel relations for a fixed finite label alphabet. Nontrivial homology occurs in specified history complexes.

**State geometry and dormant arithmetic information.** In the defined integer-state setting, the state geometric record is determined by `σ(m)`. The realized rational-state complexes considered in the BRIDGE releases depend on the occurrence inventory `D(x)`, but primitive arithmetic/region-Graver data can differ for states with identical `D`. Infinite families exhibit dormant relations and, after an arithmetic extension, their activation. **A difference in dormant Graver relations is not automatically a difference in realized topology.**

**Actual collective activation.** FIELD-I evolution can activate previously dormant relations; finite-exact trajectories exhibit both topological creation and destruction. Occurrence vertices are monotone along the stated collective orbits, but primitive-move edges and homology need not be monotone. The `G=5` and `G=11` collective scaling families are proved within their specified domains.

**Predictive geometric transitions (v005).** The next occurrence event is determined by exact arithmetic congruences in the established setting. The realized move complex is determined by `D`, and an old primitive edge is lost precisely when a newly appearing occurrence enters its divisor interval. A homology-update identity identifies both local cell changes and global attachment ranks. A rebuild-free exact update is proved at **graph level**, not generally in higher dimensions.

**Important finite-exact distinction.** The `G=5` and `G=11` tower Betti patterns were checked through `k ≤ 140`. The qualitative eventual quasi-polynomial result is scoped and proved, but no effective bound establishes that the observed concrete formulas hold for every larger `k`. Other finite scans and reached-target counts must not be presented as universal classification theorems.

## 4. What remains open

Major research questions left after v005 include:

- An effective onset bound and exact all-stage Betti formulas for the collective towers.
- Arithmetic prediction of higher-dimensional attachment ranks without rebuilding the target complex.
- Necessary-and-sufficient reachability criteria and infinite families of dynamically reached rational activation targets.
- Arithmetic criteria distinguishing topology creation, destruction and homology-preserving restructuring.
- A transition theory for **dormant primitive relations** beyond the realized-move laws.
- Broader classification of history-space topology and different-content rewrite coherence.
- Precise connecting maps, compatibility laws or obstructions among state geometry, history geometry and evolving geometry.

The root [`OPEN_PROBLEMS.md`](OPEN_PROBLEMS.md) describes the **initial preflight**. For current status consult each release's `theory/OPEN_PROBLEMS.md`, `theory/THEOREMS.md`, `STATUS.json` and applicable errata, beginning with [`GEO_HD_BRIDGE_v005/`](GEO_HD_BRIDGE_v005/).

## 5. Alignment with frozen UNNS mathematical sources

The manuscript and any future research must preserve alignment with these **immutable GitHub reference snapshots** at commit `9a021346b2b3d964523440d2737b9d0c4ddbb3e5`:

- [UNNS Mathematical Foundations](https://github.com/ukbbi/UNNS/tree/9a021346b2b3d964523440d2737b9d0c4ddbb3e5/projects/UNNS_MATH_FOUNDATIONS): SELECT-I; distinct SELECT-II base, v002 and v002b records; FIELD-I through v012; *The Mathematical Foundations of the UNNS Substrate*, Volumes I and II. This is a **stable reference collection, not a manuscript-writing workspace**.
- [UNNS Higher-Dimensional Geometry](https://github.com/ukbbi/UNNS/tree/9a021346b2b3d964523440d2737b9d0c4ddbb3e5/projects/UNNS_Higher-Dimensional%20Geometry): GEO-I v001–v012 and its existing Paper A (*Arithmetic Occurrence Geometry in the UNNS Substrate*) and Paper B (*Universal Rank-Three Obstructions in Binary Arithmetic Occurrence Geometry*).

Within those projects, earlier separately pinned reference commits are documented in their own citation and source records. Cite the **exact theorem ID, release, proof source, status and immutable commit**. Do not silently widen planar results, binary 0/1 obstruction results, integer-state statements, rational-state results or conditional FIELD-I theorems beyond their hypotheses.

Useful historical crosswalks in this directory include [`SOURCE_CROSSWALK.md`](SOURCE_CROSSWALK.md) and [`BASELINE/`](BASELINE/). They describe the initial source lock; release-local crosswalks contain the later theorem additions.

## 6. Reading order

For a first reading of the completed project:

1. [`SPEC/`](SPEC/) and [`BASELINE/HD0_VERDICT.md`](BASELINE/HD0_VERDICT.md) — original question, definitions and preflight boundaries.
2. [`GEO_HD_E2_P4_v005/`](GEO_HD_E2_P4_v005/) **with its E1 erratum** — mature geometric transport and obstruction results.
3. [`GEO_HD_1D_v004/`](GEO_HD_1D_v004/) — mature history and recombination results, then preceding HD-1D versions for dependencies.
4. [`GEO_HD_BRIDGE_v003/`](GEO_HD_BRIDGE_v003/) and [`GEO_HD_BRIDGE_v004/`](GEO_HD_BRIDGE_v004/) — rational-state structure and real activation.
5. [`GEO_HD_BRIDGE_v005/`](GEO_HD_BRIDGE_v005/) — current predictive transition theorems and open questions.
6. The frozen Foundations and GEO-I manuscripts linked above for underlying definitions and inherited results.

Use the release-local `README.md`, `STATUS.json`, theorem statements and verification records before citing any claim.

## 7. Verification and reproducibility

Each release provides its own scripts and commands. **There is no single whole-project verification command.** The root [`RUN_WINDOWS.bat`](RUN_WINDOWS.bat) and [`RUN_CHECKS.py`](RUN_CHECKS.py) run the **original HD-0 baseline tests only**; they do not verify the later seventeen research releases.

Example for the latest release, from a Windows terminal:

```bat
cd /d "D:\GitHub\UNNS\projects\UNNS_Generative_Geometry\GEO_HD_BRIDGE_v005"
python RUN_VERIFY.py --fast
```

Its recorded verification status is **38/38 fast checks and 10 pytest tests passing**; `--full` was **not run** for the delivered v005 report. Inherited releases were integrity-checked by hashes rather than freshly rerun. Other releases have different requirements and may use additional packages; consult their own instructions.

Deterministic checks and same-author independent implementations support reproducibility, but do not constitute external mathematical review or formal proof-assistant certification. General theorem claims depend on their written proofs, not on check counts alone.

## 8. Integrity and preservation policy

- **Preserve all releases and correction records unchanged.** Do not retroactively edit archived theorem text, scripts, results or manifests to make it agree with a later discovery. Use explicit append-only errata.
- **Preserve the original HD-0 records.** The top-level [`MANIFEST.json`](MANIFEST.json) was generated on **30 October 2026** for that original package, not for the entire expanded GEO-HD-1 archive. It includes a checksum for the *old* root `README.md`. Replacing this file will therefore invalidate that historical README checksum; preserve a copy of the original README and maintain any new project-wide manifest as a **separate updated record**. Do not misrepresent the old manifest as a newly verified whole-project manifest.
- **Use release-local integrity records.** Read manifests and verification logs in the release directory; a checksum match is not a rerun of a theorem verifier.
- **Keep Github read-only until local validation and explicit authorization.** The local extraction itself makes no remote repository changes.
- **Keep manuscript drafting separate from the frozen research archive.** The archived source records and their theorem IDs remain citable and unchanged.
- **Preserve status distinctions:** `PROVED`, `PROVED_SCOPED`, `FINITE_EXACT`, `COUNTEREXAMPLE`/`FALSE`, `OPEN`, `NOT_TESTED`, `NOT_RERUN`. Reconcile historical claims using later corrections rather than suppressing their provenance.
- **C3 is not claimed; novelty is not assessed.** These status flags must not be silently promoted by an overview document.

## 9. Manuscript consolidation

Following completion of BRIDGE v005, the priority is a comprehensive mathematical synthesis provisionally titled:

**The Geometry of Generation in the UNNS Substrate: Arithmetic Structure, Generative Histories, and Higher-Dimensional Evolution**.

This manuscript should focus on the GEO-HD-1 contributions **beyond** the two Foundations volumes and GEO-I Papers A/B. The source-to-manuscript crosswalk should record inherited and new theorems separately, incorporate all corrections, distinguish realized and abstract complexes, and explain which connections among arithmetic, histories and evolution are proved, conditional or open.

Any focused companion manuscripts should be derived from the consolidated theorem structure when justified by substantial distinct proof material, not created merely to reproduce each release chronologically.

**Archive boundary:** This directory records completed mathematics and its exact evidence; it does not by itself assert a universal common organizing law or equivalence among the different geometric constructions.
