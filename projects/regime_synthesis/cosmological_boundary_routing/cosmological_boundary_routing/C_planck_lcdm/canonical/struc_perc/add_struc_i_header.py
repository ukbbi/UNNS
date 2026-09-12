#!/usr/bin/env python3
from pathlib import Path

source = Path("planck_lcdm_response_ladder_preliminary.csv")
output = Path("planck_lcdm_response_ladder_preliminary_struc_i.csv")

if not source.is_file():
    raise FileNotFoundError(f"Source file not found: {source.resolve()}")

lines = source.read_text(encoding="utf-8").splitlines()
output.write_text("value\n" + "\n".join(lines) + "\n", encoding="utf-8")

print(f"Created: {output.resolve()}")
print(f"Data rows: {len(lines)}")
