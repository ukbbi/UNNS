# UNNS-U3 v001 — Universal Sequence Embeddings and Structural Preservation
Independent release; U0–U2, TI, TI-DYN and RN releases are unchanged.
Contents: manuscript/ (tex, pdf), code/ (u3_graph, u3_exp, u3_register, verify_u3), frozen_RN/ (copied engines), data/ (config, registration, results, provenance), reports/verification_report.json, SHA256SUMS.
Verify: `python3 code/verify_u3.py reports/verification_report.json` (~40 s, ALL_PASSED).
Provenance: only RN and TI archives re-hashed here; other release hashes copied (NOT_RERUN).
Limitations: realizability searches are bounded ("not found" ≠ impossible, except triangles at r=1); entropy numerics corroborate, not prove; 2^(L-1) verified for L<=5 with proof sketch; FIELD-I/GIG (G8) not attempted; amendments A1–A3 disclosed in data/u3_config.json.
