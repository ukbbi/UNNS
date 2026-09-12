# TC_P01 Campaign Shell v001

Dedicated HTML/JavaScript shell for:

`TC_PROSPECTIVE_01_research_folder`

## Purpose

This shell is separate from `TIME-CRYSTAL-I.html`.

- `TIME-CRYSTAL-I.html` = the **instrument / chamber**.
- `TC_P01.html` = the **prospective campaign registry / record**.

The campaign shell shows:

- C001, C002, future candidates;
- controls;
- blind/reveal stage;
- chamber verdict and level;
- q0, C(q0), family contrast, shuffle p;
- all four sector statuses;
- analysis-lock hashes;
- evidence audit links;
- posthoc physical identity **only after** `posthoc_comparison.json` exists;
- matched-control comparison;
- campaign progression;
- JSON and CSV export.

## Install

Copy the contents of this ZIP directly into:

`TC_PROSPECTIVE_01_research_folder\`

Do not put them in another wrapper folder.

The files should sit beside:

`candidates\`, `ground_truth\`, `locked_runs\`, `registry\`, `reports\`, `tools\`.

## Open / refresh

Double-click:

`OPEN_TC_P01.bat`

It first runs:

`tools\build_tc_p01_data.py`

which scans the local `locked_runs\` directory and rebuilds:

`TC_P01_DATA.js`

Then it opens:

`TC_P01.html`

## Blindness firewall

The data builder does **not** read files from `ground_truth\`.

A physical identity appears in the campaign shell only when the relevant locked-run folder contains:

`posthoc_comparison.json`

Thus a blind-locked C002 remains visually marked:

`BLIND LOCKED — NOT REVEALED`

until the reveal has actually occurred.

## Canonical data

The HTML/JS shell is a viewing/export layer.

Canonical scientific records remain under:

`locked_runs\<candidate>\`
