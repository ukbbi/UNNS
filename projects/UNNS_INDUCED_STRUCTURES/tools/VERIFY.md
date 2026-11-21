# Read-only integrity and targeted scientific verification

## Check the GitHub-ready collection

From `projects/UNNS_INDUCED_STRUCTURES/` in Ubuntu/WSL:

```bash
python3 tools/verify_reference.py
```

The command checks SHA-256 hashes of **every file in this curated collection** and flags missing or unlisted files. It does not validate mathematical correctness; it is an integrity check.

## Selected scientific verifiers

Run from the named release directory. Standard Python 3 is sufficient for most exact arithmetic FUG and SIB verification scripts. Some physical-model or QTI verifiers require `numpy`, `scipy` or original upstream detector data; check each release README first.

```bash
cd investigations/SEQUENCES/SIB_I_v002
python3 scripts/verify_sib.py
```

```bash
cd investigations/SEQUENCES/SIB_I_v003
python3 scripts/verify_sib.py
```

```bash
cd investigations/SEQUENCES/SIB_I_v004
python3 scripts/verify_sib.py
```

```bash
cd investigations/SEQUENCES/SIB_I_v005
python3 scripts/verify_sib.py
```

**Note on paths:** These are separate invocations from the collection root; `cd` back to the root between examples. Use forward slashes and `python3` under Ubuntu, not PowerShell's `py -3`.

The per-release historical manifest may include files removed during curation (e.g. `.pyc`), and some FUG/Maxwell historical digests already mismatch the user-supplied archive. The `CHECKSUMS.sha256` index is the authoritative byte-integrity record **for this curated collection**. When a scientific verifier checks its historical MANIFEST and a missing generated file is explicitly excluded, consult `CURATION_AUDIT.md` rather than editing theorem claims or restoring redundant binaries.

## Reproducibility distinctions

- **Source and verification code retained:** theorem files, scripts, registration/protocol JSON, key output tables and counterexamples.
- **Complete external replay requires outside data:** QTI `.pt` source files and some experimental inputs are not in this package. The cached parts are evidence of prior computation, not a substitute for original raw-data processing.
- **Not rerun by this packaging pass:** all large experiments; it verifies file integrity, original inventories and script importability for the checked subset, not 100% of the scientific claims.
