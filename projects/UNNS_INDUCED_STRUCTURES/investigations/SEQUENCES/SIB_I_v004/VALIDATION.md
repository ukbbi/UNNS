# Local validation

Run in SIB_I_v004:

    py -3 scripts\run_sib.py
    py -3 scripts\verify_sib.py

Expected verifier output for the unchanged archive:

    {"status": "PASS", "checks": 620714, "sequences": 4, "indexed_observations": 200, "gcd_identity": "verified", "permutation_counts": [94, 113]}

Without MANIFEST.json, the verifier performs 620687 assertions. With the release
manifest present it adds 27 file-hash checks. Counts describe assertions within
overlapping validation tasks, not independent statistical experiments.

The verifier reconstructs complete explicit word sets from certified prime
factorizations and compares every sequence-pair intersection with the corresponding
GCD word set. It checks kernel CSVs, directed inclusion, exact permutation
expectations, witness words and all sampled controls by deterministic replay.
Prime certificates use the inherited deterministic 64-bit primality routine;
word-set enumeration is independent of the generator's aggregate count recursion.

A direct-forward arithmetic fixture through 256 checks the endpoint-modulus rule
and GCD intersections without using factorization or backward predecessor formulas.
This validation bound is below the already completed baseline census.

The kernel SVG contains exactly 14786 data cells, matching the four square
matrix dimensions. XML structure and cell titles are checked during packaging.
Output uses UTF-8/LF; regeneration is required to match the release hashes.

Fibonacci/Lucas observed exclusion is theorem-implied. Permutation frequencies
and rewiring proportions are descriptive controls, not independent discoveries
of an unexplained anomaly. See REGISTER.md for the scope of each proof.
