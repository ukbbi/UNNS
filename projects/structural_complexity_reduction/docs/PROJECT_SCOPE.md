# SCR Project Scope

Structural Complexity Reduction (SCR) tests whether a frozen structural filter can reduce an effective candidate/search space **before** downstream computation, while preserving the independently defined structural object required by the benchmark.

SCR separates four questions:

1. Does the candidate universe contract?
2. Is the benchmark's required solution/class/basin representation preserved?
3. Does downstream work decrease after including filter cost?
4. Is the effect structurally selective relative to matched nulls?

The preservation unit is benchmark-specific and must be preregistered. It may be a complete solution set, trajectory family, basin/class, or another independently justified object. SCR-I-A v003 uses viable mechanism-basin/class geometry.

SCR does not infer P=NP, complexity-class collapse, universal asymptotic speedup, or quantum-computing obsolescence from empirical contraction.

Current completed tier: controlled mechanism-space calibration (`SCR-I-A v003`). The next substantive step should be a domain-shift benchmark rather than further tuning of the frozen calibration.
