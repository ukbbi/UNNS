# Local validation

Run from SIB_I_v003 with standard Python 3.10 or later:

    py -3 scripts\run_sib.py
    py -3 scripts\verify_sib.py

Generation checks: 1,106,745 PASS. Complete agreement for all 65,536 targets
between forward and inverse route enumeration, with 220,271 nonempty histories.
The source/content recurrence equals direct ordered-word aggregation at each target.

Expected verifier output with the unchanged release manifest present:

    {"status": "PASS", "export_checks": 1404247, "all_depth_targets": 65536}

Without a manifest the check count is 1,404,229. The extra 18 checks validate
the packaged file hashes. The verifier independently reconstructs routes by
inverse square-divisor enumeration, checks explicit pair classifications,
signature definitions, class metric ranges, counterexamples and case edges.
It also verifies the E3/Efull partition equality and the guaranteed truncated
depth profiles in this finite census.

These are assertion counts within overlapping validation tasks, not counts of
independent experiments. All scripts raise on failure. UTF-8/LF output permits
byte-identical regeneration on Windows without line-ending normalization.
