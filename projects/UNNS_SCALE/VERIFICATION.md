# Verification and reproducibility

## Fast, non-destructive integrity check

From the package root:

```bash
python tools/check_manifests.py
```

This checks the original root v001 `releases/SHA256SUMS.txt` and thirteen later per-release `SHA256SUMS_vNNN.txt` records. It requires only the Python standard library, writes no bytecode, and **does not alter research artifacts**. All 14 passed during packaging.

## Running computational verifiers

Each chamber has its own verifier in `releases/UNNS-SCALE-I[_vNNN]/code/`. Consult its `SPEC_vNNN.md` or release README for commands and dependencies. Selected verifiers use Python plus NumPy/SymPy; later experiments additionally require a C++ toolchain (including OpenMP on some platforms). The full v014 verifier is long-running and reconstructs C++ test slices; its historical output and original verification report are included.

**Reproduce in a separate writable copy of `releases/`.** In particular, the v001 verifier regenerates reports and the original root checksum list; running it directly in the immutable package can invalidate the manifest. Later verifiers may also write temporary or derived files. The check-manifests script is the safe default.

Three frozen auxiliary scripts contain development-environment-specific `/home/claude/...` input paths: v007 `run_famA.py`, v007 `run_v007.py`, and v008 `growth_scan.py`. These scripts need local input-path adaptation in a scratch copy; changing them in-place would invalidate the historical hashes. Their relevant data exist under v005 `results/`. Their paths do not affect the published theorem statements.

## Evidence definitions

- **PROVED:** mathematical derivation in a release's theory document.
- **CERTIFIED:** finite exact result with stored coverage, explicit paths and/or lower-bound certificates, subject to the stated computational audit.
- **EXPERIMENTAL:** observed on finite samples without a universal proof.
- **OPEN:** no proof or complete certification is claimed.

A full-graph route can leave the experiment's finite numerical window. The finite ambient four-step theorem does **not** assert a four-step route within the induced trillion-window graph. The confined upper bound of 18 is a certified construction, not the sharp maximum.

The computational reports document their actual independence levels. For example, v014's all-pairs sweep was computed in one C++ implementation and cross-checked on slices and samples, rather than independently reimplemented end-to-end.
