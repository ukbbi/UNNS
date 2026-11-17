# Pre-publication checklist

The ZIP is prepared for a manual upload into a GitHub project folder; **nothing has been uploaded or modified remotely**.

- [x] Preserve v001–v014 release files without edits.
- [x] Verify all fourteen historical SHA-256 manifests.
- [x] Remove untracked `.pyc` cache, superseded v005 preliminary seed and local machine-path context note.
- [x] Add a publication-facing README, release index, provenance, errata map and read-only integrity checker.
- [x] Retain exact proofs, scripts, result tables and large certification files rather than impair reproducibility for a smaller ZIP.
- [ ] Confirm the author/collective attribution and desired GitHub project path.
- [ ] Choose and add a `LICENSE` if public reuse permissions are intended; none was present in the source.
- [ ] Optionally create a manuscript citation or DOI once an actual publication exists; do not cite a speculative DOI.
- [ ] Run `python tools/check_manifests.py` after extraction and before manually committing.
- [ ] Decide whether to store the full research source history in the main Git repository or attach its large certificates to a formal release; the current ZIP keeps all data for integrity.

No files exceed common GitHub single-file size restrictions: the largest historical artifact is about 9.9 MiB uncompressed. This release is small enough to be stored in an ordinary Git repository without Git LFS, though future datasets may require different handling.
