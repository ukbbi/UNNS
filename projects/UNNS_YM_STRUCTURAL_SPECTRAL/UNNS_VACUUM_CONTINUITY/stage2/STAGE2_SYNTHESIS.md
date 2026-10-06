# STAGE2_SYNTHESIS.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2 — Refinement-Stable Structural Vacuum Accessibility  
**Status:** **FROZEN — COMPLETE**  
**Date:** 2026-10-05

# Stage-2 Synthesis — No Refinement-Stable Structural Exclusion Detected

## 1. Stage-2 question

Stage 2 was designed to test the Stage-1 hypothesis:

> The Yang–Mills vacuum need not lie beyond a universal refinement-stable structural exclusion boundary.

The project did **not** define success as the appearance of one negative diagnostic value.

The test required a combination of:

- common refinement;
- vacuum-directed physical profiles;
- asymptotic zero-floor versus positive-floor competition;
- uncertainty control;
- independent structural chambers;
- smoothing sensitivity;
- independent operator / representation change;
- geometry sensitivity;
- preservation of negative and indeterminate results without retuning.

The physical mass gap was kept logically separate throughout.

---

## 2. Frozen evidence chain

### 2.1 Baker 2022 — VREF-I/A calibration

Frozen result:

```text
CALIBRATION-SENSITIVE
```

The Baker three-resolution branch showed that the representation could change qualitative refinement ordering under linear versus PCHIP interpolation.

Therefore it was **not** promoted to a continuity or isolation verdict.

Its main Stage-2 contribution is methodological:

> a structural-vacuum conclusion cannot be based on an interpolation-sensitive common-refinement construction.

---

### 2.2 CEA 2017 — VREF-I/B structural vacuum accessibility

Frozen result:

```text
REFINEMENT-INDETERMINATE
```

The CEA branch supplied a much deeper vacuum-directed tail and an explicit zero-field vacuum reference.

The important split was:

```text
structural path:
vacuum-directed

positive structural floor:
not detected

absolute cross-refinement agreement:
failed the frozen refinement-consistency rule
```

The zero-floor model was favored qualitatively, and under the frozen drop-first sensitivity the preference crossed the decisive AICc threshold, but the full preregistered branch could not be promoted because the two physical refinements retained a systematic amplitude mismatch.

Therefore:

```text
REFINEMENT-INDETERMINATE
```

was preserved unchanged.

This is not evidence for isolation.

It is evidence that the primary CEA observable does not yet provide a refinement-stable absolute vacuum-distance calibration.

---

### 2.3 CEA structural bridge — STRUC-I / STRUC-PERC-I

Frozen synthesis:

```text
ARCHITECTURE-PRESERVED
```

Across:

```text
R1 native
R2 native
R1 common support
R2 common-linear
R2 common-PCHIP
```

the canonical STRUC-I chamber returned the same regime:

```text
Geometric Persistence / Stable Structure
```

and STRUC-PERC-I returned:

```text
FULL_PERCOLATION
```

for all five ladders.

Thus the CEA absolute-amplitude refinement mismatch did **not** propagate into a regime/topology change in the ordered amplitude-ladder architecture.

The correct interpretation is narrow:

> refinement changes absolute amplitude more strongly than it changes structural organization.

---

### 2.4 Battelli 2019 — unsmoothed connected-correlator control

Frozen result:

```text
UNSMOOTHED-ARCHITECTURE-CONSISTENT
```

The three positive-transverse-distance unsmoothed ladders all returned:

```text
STRUC-I:
Geometric Persistence / Stable Structure

STRUC-PERC-I:
FULL_PERCOLATION
```

The unsmoothed control therefore reproduces the same structural architecture seen in the smeared CEA branch.

This removes one important alternative explanation:

> the preserved CEA architecture is not dependent on the CEA smoothing construction alone.

Because the Battelli ladders are extremely short, this remains corroborative structural evidence rather than an independent primary vacuum-distance measurement.

---

### 2.5 Yanagihara 2019 — independent continuum EMT representation

Primary geometry:

```text
R = 0.69 fm
EMT-UNCERTAINTY-LIMITED
```

The four-component vacuum-subtracted EMT norm is:

```text
VACUUM-DIRECTED
```

and both preregistered model families favor the zero-floor model numerically, but not by the frozen decisive `|Delta AICc| >= 6` criterion.

No primary EMT component returns `NONZERO-FLOOR`.

The branch therefore remains correctly frozen as:

```text
EMT-UNCERTAINTY-LIMITED
```

rather than being promoted to `EMT-CONTINUITY-CONSISTENT`.

---

### 2.6 Yanagihara geometry sensitivity

Frozen result:

```text
GEOMETRY-ROBUST-NO-FLOOR
```

At:

```text
R = 0.46 fm
R = 0.92 fm
```

the four-component EMT norm is vacuum-directed in both cases.

Neither geometry returns a positive structural floor.

No individual component returns `NONZERO-FLOOR`.

Together with the locked `R=0.69 fm` primary result, the independent EMT representation therefore shows:

\[
\boxed{
\text{vacuum-directed structural motion without a detected positive floor}
}
\]

across all three tested source separations.

---

## 3. Stage-2 falsification audit

Stage 1 specified strong ways in which structural vacuum continuity could fail.

### F1 — every admissible refinement path terminates before vacuum approach

**Not observed.**

The CEA and Yanagihara representations both contain vacuum-directed structural paths over their measured domains.

### F2 — common refinement produces a positive lower bound

\[
D_{\rm struct}\ge\delta>0
\]

**Not observed.**

No primary branch produces a stable positive-floor verdict.

### F3 — apparent approach disappears under independent representations

**Not observed.**

The connected-field branches and the independent vacuum-subtracted EMT branch are qualitatively compatible with vacuum-directed structural approach.

### F4 — approach requires loss of admissibility

**Not observed in the structural chambers used.**

CEA and Battelli amplitude ladders remain in canonical STRUC-I Geometric Persistence / Stable Structure regimes.

This does not prove that every point on a physical continuum path is admissible under every possible UNNS representation.

### F5 — effect is produced only by digitization, interpolation, or window choice

**Not supported by the evidence.**

Baker exposed a real interpolation sensitivity and was therefore downgraded rather than used as positive evidence.

CEA retained its frozen refinement-indeterminate result.

Yanagihara required no interpolation at all: all four EMT components shared exact native common coordinate grids in all three tested source-separation panels.

### F6 — continuity-like behavior occurs only in synthetic controls

**Not observed.**

The Stage-2 evidence is built from measured lattice Yang–Mills representations and published continuum EMT profiles.

### F7 — an independent structural chamber reproduces universal non-crossability

**Not observed.**

Canonical STRUC-I and STRUC-PERC-I do not produce a refinement-dependent structural isolation transition in the CEA or Battelli bridges.

---

## 4. What Stage 2 has established

Stage 2 supports the following empirical statement:

\[
\boxed{
\textbf{No universal refinement-stable positive structural exclusion zone around the Yang–Mills vacuum was detected in the tested representations.}
}
\]

More specifically:

1. vacuum-directed behavior survives the move from connected chromoelectric-field profiles to a vacuum-subtracted continuum EMT representation;
2. the independent EMT result survives the source-separation change \(R=0.46\rightarrow0.69\rightarrow0.92\) fm without producing a positive structural floor;
3. ordered structural architecture is preserved across the CEA refinements even where absolute amplitude agreement fails;
4. the same structural architecture appears in the unsmoothed Battelli connected-correlator control;
5. none of the frozen primary or secondary branches returns a robust `ISOLATION-SUPPORTED`, `EMT-POSITIVE-FLOOR`, or equivalent positive-floor result.

This is substantive positive evidence for **structural vacuum accessibility**.

---

## 5. What Stage 2 has not established

Stage 2 does **not** prove the mathematical closure statement

\[
V\in\overline{\mathcal A_{\rm YM}}
\]

as a theorem.

In particular, Stage 2 has not established all of the following simultaneously with decisive precision:

\[
D_{\rm struct}(L_n,V)\to0,
\qquad
L_n\in\mathcal A_{\rm YM}
\]

for a single fully refinement-stable measured-data sequence under a representation-independent metric.

The strongest primary CEA branch is still:

```text
REFINEMENT-INDETERMINATE
```

and the primary independent EMT branch is still:

```text
EMT-UNCERTAINTY-LIMITED
```

Those negative/limited outcomes are part of the synthesis and must not be softened or rewritten.

Therefore the correct Stage-2 scientific position is:

> **the evidence supports structural accessibility and fails to detect universal structural isolation, but it does not yet constitute a mathematical proof of structural vacuum continuity.**

---

## 6. Consequence for the original non-crossability picture

The old picture required something structurally equivalent to:

\[
D_{\rm struct}(L,V)\ge\delta>0
\]

through refinement and representation change.

Stage 2 does not recover such a \(\delta\).

Instead, the observed pattern is:

\[
\text{vacuum-directed profile}
+
\text{preserved admissible architecture}
+
\text{no detected positive floor}
+
\text{representation persistence}
+
\text{geometry persistence},
\]

with remaining limits coming from calibration, refinement disagreement, and statistical uncertainty.

Thus the universal structural-vacuum non-crossability interpretation is **not supported by Stage 2**.

---

## 7. UNNS interpretation

The Stage-2 evidence is compatible with the Stage-1 ontological proposal:

\[
\boxed{
V\in\overline{\mathcal A_{\rm YM}}
}
\]

and with the broader structural picture:

\[
\boxed{
\text{Vacuum may be an internal closure object of the UNNS Yang--Mills structural domain.}
}
\]

This remains an interpretation supported by the empirical program, not a theorem of Yang–Mills quantum field theory.

The most defensible current formulation is:

> The tested Yang–Mills structural representations approach the vacuum locus without revealing a universal positive structural exclusion floor. This supports treating the vacuum as structurally accessible within the same domain rather than as an empirically established exterior region beyond a non-crossable boundary.

---

## 8. Separation from the physical mass gap

Nothing in Stage 2 implies:

\[
\Delta E=0.
\]

Stage 2 tested structural accessibility, not Hamiltonian spectral closure.

The project therefore preserves the central distinction:

\[
\boxed{
\text{spectral separation}
\not\Rightarrow
\text{structural separation}.
}
\]

At the end of Stage 2, the structural side of that distinction has substantial support.

The spectral side has not yet been coupled to it in the same frozen experiment.

That is the purpose of Stage 3.

---

## 9. Frozen Stage-2 synthesis status

The Stage-2 project-level synthesis is:

```text
STAGE2:
NO-UNIVERSAL-STRUCTURAL-EXCLUSION-DETECTED

Interpretation:
STRUCTURAL-VACUUM-ACCESSIBILITY-SUPPORTED

Strength:
MULTI-REPRESENTATION / MULTI-GEOMETRY SUPPORT

Limitation:
NOT A PROOF OF D_struct -> 0
NOT A MASS-GAP VERDICT
```

This is a synthesis status, not a replacement for any chamber verdict.

The underlying verdicts remain immutable:

```text
BAKER VREF-I/A
CALIBRATION-SENSITIVE

CEA VREF-I/B
REFINEMENT-INDETERMINATE

CEA STRUC BRIDGE
ARCHITECTURE-PRESERVED

BATTELLI UNSMOOTHED CONTROL
UNSMOOTHED-ARCHITECTURE-CONSISTENT

YANAGIHARA EMT R=0.69
EMT-UNCERTAINTY-LIMITED

YANAGIHARA EMT GEOMETRY
GEOMETRY-ROBUST-NO-FLOOR
```

---

## 10. Stage-2 closure

Stage 2 is now closed.

No further Stage-2 chamber, threshold, tail cut, interpolation rule, or source geometry should be introduced merely to strengthen the result.

The next permitted project action is:

```text
STAGE 3 — Structural Continuity vs Spectral Discreteness
```

Stage 3 must be preregistered before any new calculation.

Its task is not to repeat Stage 2.

Its task is to test whether the structurally accessible vacuum picture established here can coexist, in the same physical Yang–Mills setting, with an independently retained nonzero spectral scale.

The target proposition becomes:

\[
\boxed{
\textbf{structural accessibility need not imply spectral gap closure.}
}
\]
