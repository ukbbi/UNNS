# Revisions

## Reference Collection v001
Commit `bb8b12d753c600c597feb00df17fe139c7cc65fa` (23 October 2026). Immutable reference; cite this commit for the original publication.

## Documentation and verification maintenance (separate commit, descends from v001)
No research source file, theorem label, proof, result, or experimental script is changed.

- `README.md`, `PRESERVATION.md`, `CITATION.md`, `BASELINE.md`: removed stale references to `archives/ORIGINAL_USER_UPLOAD.zip` (not part of the repository), replaced the citation placeholder with the v001 commit SHA, and replaced "byte-for-byte" wording by the accurate statement (401 files byte-identical; 39 text files stored with LF line endings).
- `NEWLINE_LEDGER.tsv` (new): original newline form (`lf`, `crlf`, `binary`) and original SHA-256 of every source file; 342 lf, 39 crlf, 59 binary.
- `verify_sources.py`: a file passes if its SHA-256 matches exactly, or after converting only its line endings to the form recorded in `NEWLINE_LEDGER.tsv`. Binary files are never normalised. The original source ledger `SHA256_SOURCES.sha256` and `SOURCE_MAP.tsv` are unchanged.

Tested from fresh checkouts of v001 with `core.autocrlf=true`, `input` and `false`: the v001 verifier fails in all three; the revised verifier passes in all three (autocrlf=true: 100 byte-exact, 340 after newline normalisation; input/false: 401 byte-exact, 39 after normalisation). Negative tests: a one-character content change, an appended line, and a modified binary file all fail.
