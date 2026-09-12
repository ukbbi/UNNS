# High-Re source verification bugfix v0.1.1

The v0.1.0 verifier redundantly compared `EXPORT_MANIFEST.json` per-file hashes to a separately transcribed list in the tool config *before* hashing the extracted HDF5 files. This duplicate transcription gate could reject an otherwise exact, already SHA-256-locked `HIGH_RE_EXPORT.tar`.

v0.1.1 changes only the integrity logic:

1. Verify the frozen archive SHA-256: `bbda6ab3fe3b22679a0bccdaad4287cca7f0f0f06e28caa1f9692d92298c105f`.
2. Read `EXPORT_MANIFEST.json` from the extracted copy of that archive.
3. Hash each of the seven HDF5 files and require equality with its manifest SHA-256.
4. Preserve the duplicated config hashes as audit notes only.

No scientific parameter, source selection, coordinate, snapshot role, scale grammar, adapter code, ROUTE-I code, null specification, or interpretation criterion is changed.
