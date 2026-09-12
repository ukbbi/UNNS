# Changelog

## v0.1.1

- Fixed real-data failure in `_axis_edge_aggregate`.
- Both aggregate tables now expose the common merge key `node_id`.
- Added one-to-one merge validation.
- Hardened branch/merge flag creation when optional metric columns are absent.
- Added an explicit mechanism-table regression test that reproduces the real
  source-edge aggregation path.
- Scientific null definitions, thresholds, frozen input, and outputs are unchanged.

## v0.1.0

- Initial STITCH-MECH Pilot-A mechanism/null hierarchy build.
