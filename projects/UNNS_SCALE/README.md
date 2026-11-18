# UNNS-SCALE — Nested Scale Geometry and Arithmetic Wormhole Routing

**Research collection:** UNNS-SCALE-I, frozen local releases v001–v014  
**Research attribution:** UNNS Research Collective  
**Status:** curated, read-only research source archive; mathematical manuscripts and further generalization are separate undertakings.

UNNS-SCALE studies how the arithmetic SELECT-II transition graph behaves under integer scaling, numerical-window restrictions, and cross-scale routes. It supplies exact structural theorems, proofs, algorithms, and certified finite experiments, including results about *Arithmetic Wormhole Geometry*—short ambient routes that become longer or unavailable under numerical confinement.

## Main findings

| Result | Evidentiary scope | Reference |
|---|---|---|
| Multiplier-induced copies of the SELECT-II graph, with exact boundary arithmetic | Proved | [v001](releases/UNNS-SCALE-I/THEORY/UNNS_SCALE_I_THEORY_v001.md), [v002](releases/UNNS-SCALE-I_v002/THEORY/UNNS_SCALE_I_THEORY_v002.md) |
| Sharp ambient successor-distance maximum **4** for all 999,999 pairs \((10^6n,10^6(n+1))\), \(1\le n<10^6\) | Certified finite theorem; paths may leave the trillion window | [v005](releases/UNNS-SCALE-I_v005/THEORY/UNNS_SCALE_I_THEORY_v005.md) |
| **997,002** of those pairs have no route of ≤4 steps *inside* \([1,10^{12}]\) | Certified full finite-window scan | [v010](releases/UNNS-SCALE-I_v010/THEORY/UNNS_SCALE_I_THEORY_v010.md) |
| All 999,999 pairs remain connected below their larger endpoint if route length is unrestricted | Certified finite theorem | [v011](releases/UNNS-SCALE-I_v011/THEORY/UNNS_SCALE_I_THEORY_v011.md) |
| Prime-exponent parity forces arbitrarily large relative excursions along an infinite arithmetic family | Proved | [v011](releases/UNNS-SCALE-I_v011/THEORY/UNNS_SCALE_I_THEORY_v011.md), [v014](releases/UNNS-SCALE-I_v014/THEORY/UNNS_SCALE_I_THEORY_v014.md) |
| All 999,999 pairs have endpoint-confined routes of ≤18 steps; a certified pair requires 14 | Finite certified upper bound and exact lower witness; sharp maximum lies in [14,18] | [v013](releases/UNNS-SCALE-I_v013/THEORY/UNNS_SCALE_I_THEORY_v013.md), [v014](releases/UNNS-SCALE-I_v014/THEORY/UNNS_SCALE_I_THEORY_v014.md) |

**Open:** the universal infinite-scale quantity \(D_{10^6}=\sup_{n\ge1}d_G(10^6n,10^6(n+1))\) is known only to lie in \(\{4,5,6\}\). No computational speedup is established; Gate 4 remains untested. Numerical shortcut length is not computational runtime.

## Where to start

- [Release index](RELEASE_INDEX.md) — release-by-release map of the proof and code records.
- [Verification guide](VERIFICATION.md) — checksum checks and execution caveats.
- [Corrections and claim scope](CORRECTIONS.md) — errata and source-critical distinctions.
- [Source provenance](SOURCE_PROVENANCE.md) — read-only SELECT-II baseline and attribution.
- [GitHub preparation checklist](PUBLISH_CHECKLIST.md) — decisions still required before publication.

## Repository layout

```text
UNNS_SCALE/
  README.md                         publication-facing entry point
  RELEASE_INDEX.md                  v001–v014 research map
  VERIFICATION.md                   read-only integrity checks
  CORRECTIONS.md                    consolidated errata / caveats
  SOURCE_PROVENANCE.md              attribution and source baseline
  PUBLISH_CHECKLIST.md              publication decisions
  CURATION_AUDIT.md                 exact inclusion / exclusion record
  tools/check_manifests.py          stdlib-only, read-only checker
  releases/
    CHARTER.md, PROVENANCE.md, ...  original historical v001 root files
    UNNS-SCALE-I/                  v001
    UNNS-SCALE-I_v002/ ... _v014/ historical frozen chambers
```

Everything under `releases/` is preserved byte-for-byte from its tracked archive record; **those files should not be silently edited**, even when a later erratum corrects a statement. The historical `releases/README.md` and charter describe the local-development stage, not this GitHub-facing overview. The redundant preliminary `v005 seed` folder, local manuscript handoff note, and `.pyc` cache are intentionally excluded (see [audit](CURATION_AUDIT.md)).

## Verification

Run from this folder:

```bash
python tools/check_manifests.py
```

This verifies all fourteen supplied release manifests, including the original root v001 manifest. Full chamber computations need their individual dependencies and may take minutes; run them in a **writable scratch copy** rather than modifying a frozen archive. See [VERIFICATION.md](VERIFICATION.md).

## Scope 

This collection describes arithmetic graph mathematics, **not physical spacetime wormholes**. Independent literature originality and general computational advantage have not been established. 
