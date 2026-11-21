# Curation audit — source-to-reference reduction

**Purpose:** prepare a browsable, compact, source-locked GitHub reference collection for a future monograph, not a new experimental release.

## Original archive

- Source upload: `UNNS_INDUCED_STRUCTURES(1).zip`
- SHA-256: `00b1e38030d77d777c1f24eb1f8d8957d65e4c6df21b9f791b957572e33f87e0`
- Original file entries: **515**; uncompressed bytes: **14,501,477**.
- Original local `MANIFEST.json` describes the **initial v001 phase only**, not all later FUG/SIB/MUG/QTI additions. Its exact bytes are preserved as `PROVENANCE/ORIGINAL_ROOT_MANIFEST_v001.json`.

## Curation decisions

- Original files retained byte-identically: **448**; original entries excluded: **67**.
- Additional unique files unpacked without modification from the nested `MUG-I_v001.zip`: **7** (scripts, tables, figures and results required for a browsable v001 source).
- Kept versioned FUG-I, SIB-I, MUG-I, CIB-I, QTI-I release **theorem statements, provenance, protocols, scripts, independent checks, significant finite witnesses/certificates and result tables**. Also kept FUG baseline copies required by verification, and QTI cached streams/parts needed for internal audit.
- Excluded nested duplicate release ZIPs, generated Python `__pycache__/*.pyc`, the superseded preliminary 17-page dossier and plots, preliminary four-observation pilot, obsolete root v001 register/synthesis, initial teleporter-probe report/intermediate gap CSVs, empty placeholders and old release wrapper.
- Large SIB-I v003 exact census/definition/control tables and SIB-I v004 comparison outputs **are retained**: they are evidence for scoped finite claims and used by existing verifiers, not dispensable visual decoration.

A **complete line-by-line inventory** (including SHA-256 of every original file, inclusion/exclusion reason and unpacked MUG-I additions) is at `PROVENANCE/SOURCE_FILE_LEDGER.csv`. This is the authoritative file-level accounting; aggregate counts do not replace it.

## Historical manifests: explicit qualification

Original per-release `MANIFEST.json` files are retained **as historical source records**, without modifying their claims or digest values. In the supplied archive, **15 pre-existing referenced-file hash/missing issues** were detected across selected FUG-I and Maxwell releases; these existed **before** curation. See `PROVENANCE/INHERITED_MANIFEST_ISSUES.csv`.

Additionally, excluding generated `.pyc` files leaves some historical manifest entries intentionally unresolved. These do not mean the present working source was edited: the curation acts on files, not on theorem assertions. The newly generated root `CHECKSUMS.sha256` is the authoritative integrity baseline for this **curated GitHub reference set**, and `python3 tools/verify_reference.py` verifies it.

The package does not assert that every historical script can be run from every folder with the original manifest unchanged, or that raw physical datasets are included. Avoid silently regenerating old manifests without retaining the mismatch record.

## Non-goals

- No modification to GitHub, local original ZIP or any frozen research collection.
- No claim of external peer review, independent rerun of all scientific experiments, universal physical law, or uniquely selected UNNS interaction.
- No monograph drafted here. This is the **reference source collection** on which monograph preparation can later rely.

## Placement

Unzip the delivered `UNNS_INDUCED_STRUCTURES_GITHUB_READY.zip` and place the single contained `UNNS_INDUCED_STRUCTURES/` directory under `projects/` in a **local GitHub clone**. Run the root integrity command, review the diff, and commit/push manually only after local approval. Record the resulting new Git commit SHA in the monograph's citations.
