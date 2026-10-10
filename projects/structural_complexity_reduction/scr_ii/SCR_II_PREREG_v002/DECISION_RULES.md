# SCR-II v002 Decision Rules

## Integrity failure

`INVALID_RUN` if any frozen hash, seed-separation check, deterministic-generation check, multiplicity acceptance rule, arithmetic/filter firewall, or exact baseline solver check fails.

## Primary D1 — Preservation

If any primary instance has:

\[
S_{SCR}\neq S_{baseline},
\]

the primary verdict is `PRESERVATION_FAIL`.

## D2 — Search reduction

If D1 passes but median `R_node < 0.25` at any primary depth:

`NO_MATERIAL_REDUCTION`.

## D3 — Net gain

If D1–D2 pass but median `G_time < 1.10` at depth 16 or 18:

`REDUCTION_WITHOUT_NET_GAIN`.

## D4

If D1–D3 pass:

`COMPUTATIONAL_TRANSFER_CONFIRMED`.

## D5 — exploratory scaling

May be evaluated only after D4. It is empirical and is not a complexity-class claim.

## Anti-tuning rule

Calibration/design preservation outcomes may not be used to alter the multiplicity band, grammar, filter, primary seeds, or success thresholds after this preregistration is frozen.
