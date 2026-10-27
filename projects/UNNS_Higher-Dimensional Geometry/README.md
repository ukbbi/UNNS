# GEO-I — Higher-Dimensional Arithmetic Geometry of the UNNS Substrate

**Research archive | GEO-I v001–v012**  
**Location in the UNNS repository:** `projects/UNNS_Higher-Dimensional Geometry/`

This directory preserves the twelve successive releases of **GEO-I**, the mathematical investigation of geometric structure arising from **distinct nested occurrences** in the UNNS Substrate. The releases develop exact occurrence-coordinate descriptions, modular relation lattices, Graver-generated cell complexes, embedding obstructions, topology, and universal stabilization theorems.

The archive is a **versioned mathematical research record**, not twelve interchangeable copies of the same software. Read each theorem with its original definitions, assumptions, proof, and status. Later releases resolve some questions left open by earlier ones without rewriting the historical record.

## 1. Mathematical origin and scope

For a positive rational value $x=a/b$ in lowest terms, the foundational occurrence arithmetic gives the eligible occurrence indices

$$
D(x)=\left\{d\geq 2 : d^2\mid a,\quad d\equiv 1\pmod b\right\}.
$$

Different nested occurrences of the same numerical value remain distinct occurrences. Factoring the index $d$ into prime powers yields an exact exponent-coordinate representation of the arithmetic occurrence fibre:

$$
\begin{aligned}
F_x &= (\Lambda_b\cap[0,q])\setminus\{\mathbf 0\},\\
\Lambda_b &= \left\{\alpha\in\mathbb Z^k:
\prod_{i=1}^{k}p_i^{\alpha_i}\equiv1\pmod b\right\},\\
q_i &= \left\lfloor\frac{v_{p_i}(a)}{2}\right\rfloor.
\end{aligned}
$$

GEO-I then studies **explicitly defined geometric constructions** on these arithmetic coordinates: coordinate and Graver-move cells, an abstract complex $K_{\mathrm{abs}}$, its realized cell union $U$, and embedded subdivisions $K_{\mathrm{emb}}$ where defined. These objects must not be conflated: abstract and realized topology can differ. A Graver-cell construction is an additional precisely specified geometric model built from the occurrence arithmetic; not every cell attachment is uniquely forced by the occurrence formula.

For the principal planar results, the normalized relation lattice is

$$
\Gamma_{d,s}=\{(i,j)\in\mathbb Z^2:j\equiv si\pmod d\},
\qquad \gcd(s,d)=1,
$$

with nonzero lattice points $F_{d,s,Q}$ in the coordinate box $Q$, convex hull $H_{d,s,Q}$, and source-admissible realized Graver-cell union $U_{d,s,Q}$. The binary 0/1 obstruction model is a **separately defined specialization**, not an unrestricted theorem about all higher-dimensional occurrence geometries.

## 2. Release index

| Release | Principal development |
|---|---|
| [`GEO_I_v001/`](GEO_I_v001/) | Finite arithmetic fibres, modular boundaries, and first geometric/orbit analyses. |
| [`GEO_I_v002/`](GEO_I_v002/) | Exact modular-lattice moves, cubical and Graver cell complexes, dimension and topology experiments. |
| [`GEO_I_v003/`](GEO_I_v003/) | Distinction between abstract and embedded geometry; crossing criteria and explicit non-embedding families. |
| [`GEO_I_v004/`](GEO_I_v004/) | Finite obstruction-template/embedding criterion; correction of a false depth-only planar stabilization conjecture. |
| [`GEO_I_v005/`](GEO_I_v005/) | Uniform planar results for $s=\pm1$, exceptional-box topology in those classes, and counterexamples to planar-only obstruction witnesses. |
| [`GEO_I_v006/`](GEO_I_v006/) | Broader exact modular surveys, two-triangle evidence, and binary 0/1 collision/circuit theory. |
| [`GEO_I_v007/`](GEO_I_v007/) | Universal large-box planar stabilization (G7-T1); general exceptional-hole lower bound; further binary reductions. |
| [`GEO_I_v008/`](GEO_I_v008/) | First-enlargement filling of distinguished holes, squareless residue staircase, and minimal binary rank results. |
| [`GEO_I_v009/`](GEO_I_v009/) | General nullity-five minimal binary obstruction classification and zero parity-check-column exclusion. |
| [`GEO_I_v010/`](GEO_I_v010/) | Exact exceptional hollow-box complement for the remaining unit classes; unconditional old-hull coverage; nullity-six binary classification. |
| [`GEO_I_v011/`](GEO_I_v011/) | Proof of W2 circuit-partition universality and universal minimum non-embedding witness rank three in the binary 0/1 model. |
| [`GEO_I_v012/`](GEO_I_v012/) | Pareto-minimality arithmetic lemma, boundary-step Graver theorem, constructive cap covering, and universal nonexceptional planar convex stabilization (G12-T8). |

Consult each release's `README.md`, `REPORT.md`, and `MATHEMATICS.md` (or its release-specific equivalent) for exact theorem statements, proof dependencies, counterexamples, and verification status. **A statement marked OPEN or CHECKED in an earlier release may be proved in a later release; the original release is intentionally left unchanged.**

## 3. Main established results

### Exceptional planar geometry — GEO-I v005/v007/v010

For the exceptional square $Q=(d,d)$, the source-defined realized geometry can have bounded complementary holes. For the non-special unit classes $d\ge5$, $2\le s\le d-2$, GEO-I v010 proves the exact complement consists of the interiors of two specified triangles, with first Betti number $\beta_1=2$. The earlier $s=+1$ and $s=-1$ results are separate; the $s=-1$ family has $\beta_1=d$ (in its stated range). The exceptional square is **excluded** from the stabilization theorem below.

### Universal planar convex stabilization — GEO-I v012

For $d\ge2$, every unit $s$ modulo $d$, and every box $Q=(Q_1,Q_2)$ with

$$
Q_1,Q_2\ge d,\qquad Q\ne(d,d),
$$

G12-T8 establishes, within the source-defined planar Graver-cell model,

$$
\boxed{U_{d,s,Q}=\operatorname{conv}(F_{d,s,Q})}.
$$

Its proof uses the v012 arithmetic and Graver-boundary theorems and the **previously established** G5-C1, G7-T1 and G10-R1 results. The cap is covered by explicit admissible cells, including mixed enlargements. Exact finite checks support the construction but are **not** the logical basis for the universal quantifiers.

### Universal binary minimum obstruction rank — GEO-I v011

Within the **frozen binary 0/1 cell model**, v011 proves W2: every minimal non-embedded box has at least two distinct two-circuit partitions of its all-ones word. For reduced supports of size $p\ge9$, the stronger bound $n_2\ge p-1$ holds. Combined with the inherited rank and minimal-support theorems, this yields

$$
\boxed{r_{\min}=3}
$$

for every non-embedded binary 0/1 box. **Minimum witness rank** must not be confused with the rank of an arbitrary individual collision witness.

## 4. Reading and reproducibility

**Suggested reading order:** `GEO_I_v012/REPORT.md` → `GEO_I_v012/MATHEMATICS.md` → `GEO_I_v011/MATHEMATICS.md` → `GEO_I_v010/MATHEMATICS.md`, then earlier releases for the original definitions, counterexamples, and theorem dependencies.

Each release is intended to be inspected and verified **from its own directory**. Commands and dependencies vary by version; use the release-local README rather than assuming one command works for all twelve versions.

For the final planar release (Python 3.10+ and the dependencies stated in its README, including `gmpy2`):

```powershell
cd "D:\GitHub\UNNS\projects\UNNS_Higher-Dimensional Geometry\GEO_I_v012"
python verify.py --smoke
python verify.py
```

The default v012 full command verifies the new results and performs inherited **smoke-mode compatibility checks**; it does **not** rerun the expensive inherited v010/v011 full gate. That gate can be explicitly requested with `--rerun-inherited-full`. See `GEO_I_v012/VERIFICATION_STATUS.md` and `PROVENANCE.json` for the exact policy and what was actually executed. The Windows portability wrapper for older optional `sha256sum` regression checks is included in v012; historical release files remain preserved.

The final revised v012 release passed a clean-unzip Windows smoke run: **25/25 new checks**, **33/33 inherited v011 gate**, and **125/125 inherited v010 gate**. The inherited full gate is recorded `NOT_RERUN` against previously verified baselines, not misrepresented as a fresh pass.

**Verification is not the same thing as a formal proof-assistant certification.** General arguments appear in the mathematical documents; deterministic tests, certificates, checksums, and recorded computational searches provide separate evidence and reproducibility.

## 5. Preservation, provenance, and publication

- **Preserve releases independently.** Do not replace v001–v011 files with later revisions or delete historic counterexamples and negative findings.
- **Use precise result labels.** Distinguish `PROVED`, `PROVED+CHECKED`, `CHECKED`, `FALSE`, `CORRECTED`, `OPEN`, and `UNAVAILABLE`; consult the theorem registry of the release making the claim.
- **Check manifests.** Release-local `MANIFEST.sha256` files and provenance records establish file integrity; do not silently modify certified inputs or reports.
- **Keep the research boundary clear.** The planar theorem and binary theorem concern their explicitly specified models. Neither, by itself, proves the global geometric organization of UNNS, a physical spacetime interpretation, or generality beyond its hypotheses.
- **Preserve the Foundations archive.** SELECT-I, SELECT-II, FIELD-I, and the two-volume `UNNS_MATH_FOUNDATIONS` reference collection are separate mathematical sources and are not rewritten by GEO-I.
- **Avoid unsupported priority claims.** The archived prior-art reviews are limited. Full comparison with relevant geometry-of-numbers, Graver-basis, and combinatorial-topology literature remains part of manuscript preparation.

## 6. Research status and open direction

By v012, the **exceptional planar hollow-box classification**, **binary 0/1 universal minimum rank-three theorem**, and **nonexceptional planar convex-stabilization theorem** are reported as proved within their respective formal frameworks. The broader task of relating individual occurrence geometries across fibres into a coherent **global geometric organization of the UNNS Substrate remains OPEN**.

This directory is the archival source base for mathematical manuscript development. It does not require modifying historical results, conflating distinct geometric models, or diverting the programme into unrelated applications.

For citation, refer to the exact GEO-I release, theorem ID, and—after publication on GitHub—the immutable repository commit. Cite manuscript versions separately once available. Consult the repository and release files for applicable licensing and third-party attribution; no additional license is asserted by this README.
