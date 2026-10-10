# Reference preflight v003

From the `structural_complexity_reduction` project root in Command Prompt:

```bat
set "PATH=C:\msys64\ucrt64\bin;%PATH%"
python scr_iii_b\reference_check\validate_v003.py
```

The PATH change lasts for this Command Prompt only. Smart App Control stays enabled. If Windows prevents launching the generated executable, the script reports `EXECUTION_BLOCKED_OR_FAILED` and writes diagnostic JSON. Never disable protections or whitelist broad folders to force a PASS.

This is **not** validation against the unmodified Dryad simulator: it checks a separate C++ transcription of pair interactions against the Python evaluator. The v001 non-ice ground-state diagnostic remains provisional. The frozen v001/v002 results remain unchanged; v003 outputs are written only under `output/validation/v003/`. C++ executable is a generated local test artifact and is not shipped in the archive.
