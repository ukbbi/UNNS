# Generator

This module will implement the deterministic `ROUTE_CSP_I` instance generator defined by the frozen SCR-II preregistration.

It must:
- accept only a config object and an integer seed;
- produce identical instances for identical config+seed;
- generate structural metadata before arithmetic solution targets;
- guarantee one backbone exact solution;
- permit accidental additional exact solutions;
- emit an instance hash and provenance record.
