# TokaMark Positive-Corridor Metadata Candidate Scanner

## Purpose

This report ranks public TokaMark/MAST shots by metadata-level suitability for a future UNNS-H Mode positive-corridor time-resolved probe.

The scanner only inspects `.zmetadata`; it does not download full arrays.

## Scan summary

- split file: `TokaMark_temporal_data_splits.csv`
- scanned shots: `200`
- successful metadata fetches: `200`
- failed metadata fetches: `0`
- campaign filter: `none`
- split filter: `none`
- max shots: `200`

## Candidate classes

- `CORE_DALPHA_GEOMETRY_CANDIDATE`: 110
- `FULL_PROFILE_EDGE_CANDIDATE`: 45
- `LOW_PRIORITY`: 6
- `PARTIAL_DALPHA_CANDIDATE`: 38
- `PROFILE_DALPHA_CANDIDATE`: 1

## Top candidates

| rank | shot_id | campaign | score | class | core | profile | soft-X | support |
|---:|---:|---|---:|---|---:|---:|---:|---:|
| 1 | 12063 | M5 | 97.143 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 10/14 |
| 2 | 12065 | M5 | 97.143 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 10/14 |
| 3 | 12069 | M5 | 97.143 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 10/14 |
| 4 | 12075 | M5 | 97.143 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 10/14 |
| 5 | 12076 | M5 | 97.143 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 10/14 |
| 6 | 12077 | M5 | 97.143 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 10/14 |
| 7 | 11823 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 8 | 11824 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 9 | 11825 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 10 | 11826 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 11 | 11827 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 12 | 11829 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 13 | 11939 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 14 | 11940 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 15 | 11941 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 16 | 11942 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 17 | 11943 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 18 | 11946 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 19 | 11996 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 20 | 11998 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 21 | 12004 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 22 | 12006 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 23 | 12007 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 24 | 12008 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |
| 25 | 12009 | M5 | 96.429 | `FULL_PROFILE_EDGE_CANDIDATE` | 8/8 | 2/2 | 2/2 | 9/14 |

## Interpretation

Preferred targets are `FULL_PROFILE_EDGE_CANDIDATE` or `PROFILE_DALPHA_SOFTX_PARTIAL_CANDIDATE` shots.

If no full candidate is found, `PROFILE_DALPHA_CANDIDATE` is still useful for a Thomson+D-alpha edge-response probe.

If only `CORE_DALPHA_GEOMETRY_CANDIDATE` shots are found, the source can support an event-level edge-response probe but not full profile-resolved `m_edge(t)`.

## Next step

After identifying a top candidate, build a small HTTP chunk/array reader or a controlled zarr loader for that one shot only.