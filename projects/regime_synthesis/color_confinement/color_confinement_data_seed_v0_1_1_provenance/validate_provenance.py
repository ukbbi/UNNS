#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
required_by_file = {
    'source_registry.csv': ['source_id','source_url','arxiv_id','doi','title','primary_use','source_status'],
    'static_QQbar_ensemble_metadata_seed.csv': ['source_id','source_url','arxiv_id','source_location','row_provenance'],
    'string_breaking_thresholds_seed.csv': ['source_id','source_url','arxiv_id','source_location','row_provenance'],
    'string_tension_seed.csv': ['source_id','source_url','arxiv_id','source_location','row_provenance'],
    'flux_tube_simulation_summary_seed.csv': ['source_id','source_url','arxiv_id','source_location','row_provenance'],
    'next_data_acquisition_queue.csv': ['source_id','source_url','arxiv_id','source_location','row_provenance'],
}
errors = []
for fname, cols in required_by_file.items():
    path = ROOT / fname
    if not path.exists():
        errors.append(f'missing file: {fname}')
        continue
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        missing = [c for c in cols if c not in (reader.fieldnames or [])]
        if missing:
            errors.append(f'{fname}: missing columns {missing}')
        for i, row in enumerate(reader, start=2):
            for c in cols:
                if c in row and row[c] is None:
                    errors.append(f'{fname}:{i}: null value in {c}')
            if 'source_id' in row and not row['source_id'].strip():
                errors.append(f'{fname}:{i}: empty source_id')
            if 'source_url' in row and not row['source_url'].strip():
                errors.append(f'{fname}:{i}: empty source_url')
            if 'row_provenance' in row and not row['row_provenance'].strip():
                errors.append(f'{fname}:{i}: empty row_provenance')

if errors:
    print('PROVENANCE VALIDATION FAILED')
    for e in errors:
        print('-', e)
    raise SystemExit(1)
print('PROVENANCE VALIDATION PASSED')
