# TC_P01_C001 — Raw-Format Reconnaissance

## Source archive

`4T-DTC_upload.tar`

- SHA-256: `380f112980ac149a791b71f0553b776a82659da08dc60d69b242baf8c6712011`
- Size: 1,228,800 bytes
- TAR members: 42

The archive contains three practically distinct layers:

1. code / notebooks;
2. IBM raw-result JSON trajectories and readout-mitigation material;
3. tMPS finite-size trajectories for N = 8, 16, 24, 32.

## Primary experimental temporal evidence

The adapter uses eight IBM `Z_*.json` trajectories that are kept together in
the source archive as the recompilation-result experimental set:

- `Z_ibmq_guadalupe.json`
- `Z_ibmq_guadalupe2.json`
- `Z_ibmq_kolkata.json`
- `Z_ibmq_mumbai.json`
- `Z_ibm_cairo.json`
- `Z_ibm_cairo2.json`
- `Z_ibm_hanoi.json`
- `Z_ibm_hanoi2.json`

Each has 20 stroboscopic points.

They are stacked only as simultaneous **ensemble coordinates** of the same
reported observable and cycle index:

`X_t = (Z_run1(t), ..., Z_run8(t))`

No sign alignment, smoothing, Fourier filtering, interpolation, or target-period
information is supplied to the frozen temporal metric.

## Data deliberately excluded from the primary candidate

### No-recompilation traces

The seven `Z_no_recompilation*.json` files are kept as a separate negative /
hardware-control bundle:

`TC_P01_NRCTRL.zip`

They are **not** mixed into the candidate state vector.

### Mitigation traces

`Z_mit_*` and `Z_unmit_*` files are not mixed into the primary candidate,
because they are alternative mitigation representations of selected device
runs rather than independent state coordinates.

### tMPS trajectories

The N = 8, 16, 24, 32 tMPS files are preserved as a secondary theoretical
cross-check. They are not used to manufacture missing collective or spectral
TIME-CRYSTAL-I sectors.

## Blind chamber result — primary candidate

Candidate ID:

`TC_P01_C001`

Temporal status:

**SUPPORTED**

Detected recurrence depth:

**q0 = 4**

Frozen closure:

**C(q0) = 0.548297**

Recurrence-family contrast:

**F = 0.361657**

Frozen 200-shuffle p-value:

**p = 0.014925**

Final chamber verdict:

**TEMPORAL_RECURRENCE**

This is the key first prospective observation: the unchanged q=1..10 search
selects q0 = 4 from the new experimental ensemble.

## Blind hardware-control result

Candidate ID:

`TC_P01_NRCTRL`

Temporal status:

**NOT_SUPPORTED**

Automatic q candidate:

**q0 = 6**

Closure:

**C(q0) = 0.410906**

Family contrast:

**F = -0.003452**

Shuffle p-value:

**p = 0.995025**

Final chamber verdict:

**NO_TEMPORAL_ORDER**

The no-recompilation control therefore does not produce a supported recurrence
family under the frozen temporal gate.

## Evidence boundary

The public archive, in the form supplied here, does not contain the standardized
TIME-CRYSTAL-I evidence needed to claim all higher sectors without inventing new
adapter-specific definitions.

The primary bundle therefore contains only the experimentally grounded temporal
trajectory evidence.

Missing higher sectors remain `NOT_TESTED`.

This is intentional.
