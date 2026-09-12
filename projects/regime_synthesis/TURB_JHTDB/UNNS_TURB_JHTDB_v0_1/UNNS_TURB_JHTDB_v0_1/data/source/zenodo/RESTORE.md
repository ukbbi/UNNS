# Restore the local raw layer from Zenodo

Published source record:

`https://zenodo.org/records/22650769`

Version DOI:

`10.5281/zenodo.22650769`

If a local heavy source is lost, download the corresponding file from Zenodo and restore it to the path below.

| Zenodo file | Restore to local project path | SHA-256 |
|---|---|---|
| `isotropic1024-coarse-velocity.h5` | `data/raw/jhtdb/isotropic1024coarse/cutouts/isotropic1024-coarse-velocity.h5` | `e32c9225af656a2f0fa0a704be7dcd78fa12efc1a01b880af23eb45e02108a46` |
| `isotropic1024-coarse-pilot-b-velocity.h5` | `data/raw/jhtdb/pilot_b/isotropic1024-coarse-pilot-b-velocity.h5` | `977e6ab3c437252395dc7f7185af1829619fe1eec754f59f5f3ceae2ca0b969f` |
| `HIGH_RE_EXPORT.tar` | `data/raw/jhtdb/high_re/HIGH_RE_EXPORT.tar` | `bbda6ab3fe3b22679a0bccdaad4287cca7f0f0f06e28caa1f9692d92298c105f` |
| `HIGH_RE_EXPORT.tar.sha256` | `data/raw/jhtdb/high_re/HIGH_RE_EXPORT.tar.sha256` | use the native checksum companion as deposited |

After downloading, verify SHA-256 before allowing any downstream adapter/chamber stage to use the restored file.

Do not silently substitute a newer Zenodo version into a frozen analysis. A newer archive version must be treated as a distinct source release unless byte identity is proven.
