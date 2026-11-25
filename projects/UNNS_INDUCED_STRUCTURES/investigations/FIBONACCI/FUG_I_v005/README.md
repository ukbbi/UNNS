# FUG-I v005 — Unrestricted Structural Activation and History Classification

**UNNS_INDUCED_STRUCTURES · Local research release · 20 November 2026**

This is Phase 5 of **Fibonacci Geometry Induced by the UNNS Substrate**. It develops the *unrestricted positive-integer label* continuation grammar over the immutable founding arithmetic `M ⟂ N = M(N+1)^2/N`. Neither the substrate nor releases v001–v004 are modified.

## Main results

1. **Exact full-label activation decision:** an inverse-branch recursion decides the first new history depth for every fixed pair a|b, without enumerating a restricted alphabet.
2. **Fibonacci doubling law:** for each odd r, the full-label activation depth from F_(12r) to F_(24r) is 2 exactly when the odd integer L_(12r)/2 is squarefree; otherwise it is 1.
3. **Infinite obstruction:** for every odd s, the pair F_(84s) → F_(168s) acquires immediate label N=6. Thus the Phase 4 finite-alphabet result cannot be unrestricted without additional hypotheses.
4. **Unrestricted controls:** (144, 288p), prime p≥5, gives an infinite family of full-label depth-2 activation *outside Fibonacci*.
5. **Unbounded merger multiplicity:** for each t, t+1 distinct label-content histories generate the same endpoint from the same source; by the Fibonacci rank-of-apparition theorem the pattern lifts to a Fibonacci target.
6. **Exact census:** 307 proper index-divisibility transports through Fibonacci index 84 classify as 193 unchanged, 108 first-new depth 1, 6 first-new depth 2, confirmed using two independent algorithms.

See `theory/THEOREMS.md` for precise statements and proofs. The Lucas squarefreeness condition is a **criterion**, not a claim that infinitely many odd r satisfy it.

## Windows PowerShell — local use

Extract this folder beside (not inside) the frozen previous releases:

```text
UNNS_INDUCED_STRUCTURES\investigations\FIBONACCI\
  FUG_I_v001\
  FUG_I_v002\
  FUG_I_v003\
  FUG_I_v004\
  FUG_I_v005\
```

Open PowerShell in `FUG_I_v005` and run:

```powershell
py -3 scripts\run_p5.py
py -3 scripts\verify_p5.py
```

You should see `FUG-I v005 VERIFY PASS` at the end. If the `py` launcher is unavailable, substitute `python`.

**No `.bat`, third-party Python packages, installation, administrative rights, internet connection or GitHub operations are required.** The scripts write only under this v005 folder.

## Files

```text
FUG_I_v005/
  README.md
  README.txt
  RELEASE_NOTES.md
  SOURCE_PROVENANCE.md
  MANIFEST.json
  theory/
    SPEC.md
    THEOREMS.md
    LIMITS.md
  scripts/
    arith.py
    run_p5.py
    verify_p5.py
  baseline_v004/
    summary.json
    word_activation_84.csv
    transport_activation_84.csv
    merger_gate.json
    control_activation_84.json
  results/
    RESULTS.md
    summary.json
    all_label_pairs_84.csv
    unrestricted_delayed_84.csv
    odd_doubling_certificates.csv
    infinite_depth1_witnesses.csv
    matched_integer_controls.csv
    unbounded_merger_family.csv
  controls/
    CONTROL_PROTOCOL.md
  docs/
    REGISTER_PATCH.md
    NEXT_RESEARCH.md
```

## Scientific interpretation

This is a **mathematical investigation of an induced structure**. The Fibonacci recurrence is independently defined; the selected integer self-substitution grammar comes from the fixed UNNS nesting operation. The finite census, algebraic gate, restricted-vs-unrestricted obstruction, and merger families establish which mathematical configurations are possible and when. They do not justify a claim about physical laws, new electromagnetic mechanisms, substrate universality, or exceptional behavior of Fibonacci relative to matched nulls.

