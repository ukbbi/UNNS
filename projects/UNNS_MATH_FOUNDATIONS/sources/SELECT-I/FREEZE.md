# SELECT-I — frozen independent research result

Frozen release **v1.0.0**, 21 October 2026. Project home in the user's local directory: `UNNS_ENTANGLE_I/SELECT-I/` (sibling of `UNNS_RELATIONAL_I/`).

Original supplied `select1.py`, `SELECT1_note.md`, and `select1_output.txt` are copied byte-for-byte into this archive.
The recorded verifier returns **26/26 checks PASS** plus **4 unasserted DATA rows**; its SHA-256 is `cd2f3510dbf28f00b2958a0d69d94c95fe93f2638eb01e8622f9c4aabaa72095`.
A fresh run was performed without modifying the source and generated `select1_report.json`; see `replay_output.txt`. The supplied output ends with an external `done 0` line not printed by the bare Python script. Aside from that wrapper line, the supplied output matches the fresh script output.

**Frozen research verdict:** For the specified anchor-route model, selecting a commutative/associative/idempotent binary continuation is selecting its induced order; the factor-amplification order selects `J_join`, whereas admitting forward refinements as continuation steps selects `J_ref`. The nest rule plus `T_q` does not itself impose factor-amplification. With inverse refinements as steps, equivalent-value routes can lead to multiple minimal representatives.

**Scope:** These are statements about the indicated mathematical model. Intrinsic generative semantics for a broader UNNS grammar, physics, field occurrences and entanglement remain open. The source files and earlier RGG work are not changed.

Next stage: separate `UNNS_ENTANGLE_I/SELECT-II/` investigation. Do not alter this frozen package when working on SELECT-II.

Reproduce (Windows PowerShell in SELECT-I):

    python select1.py

The script writes `select1_report.json` locally. This frozen archive retains the report from a verified replay as a read-only record.
