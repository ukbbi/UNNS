README_tokamark_one_shot_array_probe.txt

UNNS-H Mode Project
Component: tokamark_one_shot_array_probe.py

============================================================
PURPOSE
============================================================

This component performs a controlled one-shot array probe for a public
TokaMark/MAST candidate discharge.

It is designed for the next step after:

  docs/17_TOKAMARK_METADATA_CANDIDATE_SCAN_REPORT.md

The metadata scan identified shot 12063 as the top-ranked:

  FULL_PROFILE_EDGE_CANDIDATE

This script checks whether the actual selected arrays for that shot can be
downloaded by direct HTTPS chunk requests.

It does not compute final m_edge(t).
It does not decide whether the shot is physically positive-corridor.
It only verifies and summarizes the data needed for that later step.


============================================================
WHERE TO PLACE IT
============================================================

Place the script here:

  unns_hmode_project/
    components/
      tokamark_one_shot_array_probe.py

Place this README here:

  unns_hmode_project/
    components/
      README_tokamark_one_shot_array_probe.txt


============================================================
INSTALL DEPENDENCIES
============================================================

Run:

  python -m pip install requests numpy pandas numcodecs

This script intentionally avoids zarr and s3fs because the direct zarr/s3fs
route caused hanging / async shutdown problems on Windows.

It reads Zarr v2 arrays directly through:

  HTTPS metadata request
  HTTPS chunk requests
  numcodecs decompression


============================================================
DEFAULT TARGET
============================================================

Default shot:

  12063

Reason:

  It ranked first in the 200-shot TokaMark metadata candidate scan.

Candidate properties:

  campaign: M5
  split: val
  class: FULL_PROFILE_EDGE_CANDIDATE
  score: 97.143
  core signals: 8/8
  Thomson profile signals: 2/2
  soft-X edge/activity signals: 2/2
  support signals: 10/14


============================================================
RUN COMMAND
============================================================

From the project root:

  python components\tokamark_one_shot_array_probe.py --shot-id 12063 --out-dir outputs\reports

Optional faster test without preview CSV:

  python components\tokamark_one_shot_array_probe.py --shot-id 12063 --out-dir outputs\reports --skip-preview


============================================================
INPUT SOURCE
============================================================

The script reads from the public TokaMark/MAST Zarr store:

  https://s3.echo.stfc.ac.uk/mast/tokamark/v1/<shot_id>.zarr/

Metadata file:

  https://s3.echo.stfc.ac.uk/mast/tokamark/v1/<shot_id>.zarr/.zmetadata

For shot 12063:

  https://s3.echo.stfc.ac.uk/mast/tokamark/v1/12063.zarr/.zmetadata


============================================================
TARGET ARRAYS
============================================================

The script attempts to read:

Power / density:
  summary/power_nbi
  summary/ip
  interferometer/n_e_line

Edge response:
  spectrometer_visible/filter_spectrometer_dalpha_voltage
  soft_x_rays/horizontal_cam_lower
  soft_x_rays/horizontal_cam_upper

Profiles:
  thomson_scattering/t_e
  thomson_scattering/n_e

Geometry / equilibrium:
  equilibrium/q95
  equilibrium/elongation
  equilibrium/triangularity_upper
  equilibrium/triangularity_lower
  equilibrium/minor_radius
  equilibrium/beta_normal
  equilibrium/beta_pol
  equilibrium/whmd


============================================================
OUTPUT FILES
============================================================

The script writes:

  outputs/reports/tokamark_shot_12063_signal_probe.csv
  outputs/reports/tokamark_shot_12063_signal_probe.json
  outputs/reports/tokamark_shot_12063_signal_probe.md
  outputs/reports/tokamark_shot_12063_proxy_timeseries_preview.csv

CSV:
  compact signal-level summary

JSON:
  full probe summary, read information, failure notes, proxy summaries

Markdown:
  human-readable report

Preview CSV:
  first 250 samples of selected raw proxies, each kept on its native time base


============================================================
RAW PROXIES COMPUTED
============================================================

The script computes first-pass summaries for:

  D-alpha median across channels
  soft-X lower median across channels
  soft-X upper median across channels
  Thomson Te edge median
  Thomson Te profile-gradient proxy
  Thomson ne edge median
  Thomson ne profile-gradient proxy

Important assumption:

  The Thomson profile edge proxy assumes the last 20% of profile indices
  represent the outer edge. This is a raw probe only. A later version should
  use explicit radial / flux coordinates if available.


============================================================
WHAT THIS COMPONENT CAN CLAIM
============================================================

If successful, this component can claim:

  The selected public MAST/TokaMark candidate shot can be read at array level,
  and the required diagnostic families for a future m_edge(t) probe are present
  and extractable.

It can also identify which signals fail to load, if any.


============================================================
WHAT THIS COMPONENT CANNOT CLAIM
============================================================

Do not claim:

  shot 12063 is a positive-corridor discharge
  H-mode has been validated
  m_edge(t) has been constructed
  an L-H transition time has been identified
  the D-alpha / soft-X / Thomson traces prove edge confinement

This is only a controlled one-shot array extraction and diagnostic summary.


============================================================
NEXT STEP
============================================================

After this script succeeds, create:

  components/
    tokamark_m_edge_t_probe.py

That next component should:

  1. align selected diagnostics onto a common time base;
  2. compute S_power_balance(t);
  3. compute S_transport(t);
  4. compute S_edge_response(t);
  5. compute C_edge_capacity(t);
  6. compute F_route_fragmentation(t);
  7. compute m_edge(t);
  8. identify candidate edge-response intervals.

The one-shot array probe must come first.
