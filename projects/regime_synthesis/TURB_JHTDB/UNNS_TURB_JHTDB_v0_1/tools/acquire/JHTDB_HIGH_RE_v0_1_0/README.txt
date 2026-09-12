JHTDB_HIGH_RE_v0_1_0

PURPOSE
  Extract the preregistered central 256^3 native-grid cubes directly from the
  SciServer-mounted JHTDB Ceph Zarr arrays. No JHTDB authorization token is used.

FROZEN SAMPLES
  isotropic8192  : x/y/z 3969:4224, snapshots 0..5
  isotropic32768 : x/y/z 16257:16512, snapshot 0

IMPORTANT
  The isotropic8192 snapshots are not treated as a time sequence.
  The parent DNS is periodic; extracted cubes are analyzed as nonperiodic cutouts.

SCISERVER
  1. Upload INSPECT_SCISERVER.py and EXTRACT_SCISERVER.py into your running container.
  2. Terminal:
       python INSPECT_SCISERVER.py
  3. If PASS:
       python EXTRACT_SCISERVER.py
  4. The script auto-selects a writable Temporary/scratch or Storage/persistent volume.
     To force a destination:
       python EXTRACT_SCISERVER.py --output /home/idies/workspace/Temporary/<user>/<volume>/HIGH_RE_EXPORT
  5. Download the complete HIGH_RE_EXPORT folder.

Do not alter coordinates or snapshots after seeing field values.
