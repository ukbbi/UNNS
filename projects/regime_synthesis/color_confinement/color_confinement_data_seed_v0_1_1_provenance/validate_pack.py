from pathlib import Path
import csv, json
root = Path(__file__).resolve().parent
required = [
 'provenance/source_registry.csv',
 'data/01_core_static_potential/bulava2019_model_parameters_reported.csv',
 'data/02_core_string_breaking/bulava2019_string_breaking_thresholds_reported.csv',
 'data/03_core_flux_tube_profiles/baker2024_table1_simulation_summary.csv',
 'data/03_core_flux_tube_profiles/baker2024_table2_nonperturbative_integrals.csv',
 'data/03_core_flux_tube_profiles/baker2024_table3_full_field_integrals.csv',
 'extraction_queue/pointwise_data_acquisition_queue.csv',
]
missing=[p for p in required if not (root/p).exists()]
if missing:
    raise SystemExit('MISSING: '+str(missing))
for rel in required:
    if rel.endswith('.csv'):
        with open(root/rel, newline='', encoding='utf-8') as f:
            rows=list(csv.DictReader(f))
        if not rows:
            raise SystemExit('EMPTY CSV: '+rel)
print('VALIDATION PASSED: reported tables present; pointwise targets queued, not fabricated.')
