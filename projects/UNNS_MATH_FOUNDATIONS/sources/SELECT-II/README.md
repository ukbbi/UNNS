# SELECT-II v001 — Intrinsic Generative Reachability

**Status:** ACTIVE INVESTIGATION — first exact results and reproducible tests, 21 October 2026.  
**Prior work:** SELECT-I frozen independently; RGG-1/2/2.1 and the relational-invariants manuscript remain unchanged.

## Precise scope

This project studies **one explicitly declared interpretation** of self-iteration of the nest rule:
start with positive integer `m`, choose positive integer `N`, and substitute the current output as the next first argument,

    m -> m ⊥ N = m*(N+1)^2/N.

**Only integer successors are kept**; equivalently `N | m`. A directed edge is labelled by `N`.
This construction is derived from the nest arithmetic plus a **chosen self-substitution convention**.
It does **not** assert that all UNNS recursion has this interpretation, or that a binary joint operation is thereby prescribed.

## First exact results

1. All edges strictly increase the value, by a factor >= 4; the graph is acyclic.
2. Every source `m` has exactly `tau(m)` distinct outgoing edges, one per positive divisor `N | m`.
3. A target `t` has exactly `R(t)` distinct immediate predecessors, one per `d >= 2` with `d^2 | t`.
4. Targets are exactly nonsquarefree positive integers. Thus graph vertices with no incoming edges are exactly the squarefree integers; every integer has at least one squarefree ancestor.
5. An edge `m -> t` determines its parameter exactly: `g=gcd(m,t)`, `N=m/g`, and `t=g*(N+1)^2`. No parameter ambiguity is possible given the two endpoint values.
6. Reachability has **no universal least common future**: 1 and 2 both reach 81 and 100, and these are distinct incomparable minimal common futures. Consequently this reachability order is not a join-semilattice.
7. A fixed-target reachability query is decidable by finite exact bounded traversal: edges strictly increase and paths exceeding the target can be discarded.

Proofs and explicit witness paths are in `RESULTS.md`. These are **mathematical consequences of the explicitly declared one-step model**, not physical observations.

## Run on Windows

Double-click `RUN_TESTS.bat`, or open a terminal inside this folder and run:

    python select2.py

Python 3.10+; standard library only. The script generates `select2_report.json` and prints its checks.
The included `select2_output.txt` is the recorded first run. **23/23 asserted checks passed and 3 DATA rows were reported**. Repeat execution matched the recorded output and report bytes in our environment.

The script uses exhaustive finite checks to corroborate proofs, plus bounded reachability searches for the explicit counterexample. It does not prove general claims by enumeration alone.

## Project boundary

Do not change the SELECT-I frozen bundle, manuscript v3, or prior RGG sources. Do not modify GitHub until the local investigation is complete.
No rule for field (non-integer) occurrences, physical correlations, or quantum entanglement is asserted here.
