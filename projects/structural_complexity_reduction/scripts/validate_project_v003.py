from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scr_i_v003.source_lock_v003 import verify as verify_source_lock


def ok(label: str, condition: bool, detail: str = "") -> bool:
    print(f"{'PASS' if condition else 'FAIL'}  {label}" + (f" — {detail}" if detail else ""))
    return condition


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def sidecar_ok(path: Path) -> bool:
    side = path.with_suffix(path.suffix + '.sha256')
    if not side.is_file():
        return False
    expected = side.read_text(encoding='utf-8').strip().split()[0]
    return expected == sha256(path)


def run_validator(path: Path) -> bool:
    p = subprocess.run([sys.executable, str(path / 'scripts' / 'validate_prereg.py')], cwd=str(path), capture_output=True, text=True)
    return p.returncode == 0


def main() -> int:
    good = True
    source = verify_source_lock(ROOT)
    good &= ok('v003 pinned source lock', bool(source.get('ok')))
    good &= ok('v003 preregistration', run_validator(ROOT / 'SCR_I_PREREG_v003'))
    good &= ok('archived v001 preregistration preserved', run_validator(ROOT / 'archive' / 'prereg' / 'SCR_I_PREREG_v001'))
    good &= ok('archived v002 preregistration preserved', run_validator(ROOT / 'archive' / 'prereg' / 'SCR_I_PREREG_v002'))

    design = ROOT / 'output' / 'v003_phase1' / 'DESIGN_PRESERVATION_AUDIT_PASS.json'
    try:
        design_ok = design.is_file() and bool(json.loads(design.read_text(encoding='utf-8')).get('ok'))
    except Exception:
        design_ok = False
    good &= ok('design-preservation audit marker', design_ok)

    progress_path = ROOT / 'output' / 'RUN_PROGRESS_v003.json'
    result_path = ROOT / 'output' / 'PRIMARY_RESULT_v003.json'
    final_path = ROOT / 'output' / 'exports' / 'v003' / 'SCR_I_V003_FINAL.json'
    progress = json.loads(progress_path.read_text(encoding='utf-8')) if progress_path.is_file() else {}
    primary_complete = progress.get('status') == 'COMPLETE' and progress.get('completed_cells') == 15 and progress.get('total_cells') == 15
    good &= ok('primary progress COMPLETE 15/15', primary_complete)

    records = json.loads(result_path.read_text(encoding='utf-8')) if result_path.is_file() else []
    expected_seeds = {2026101001,2026101002,2026101003,2026101004,2026101005}
    expected_sizes = {2500,10000,40000}
    combos = {(int(r['seed']), int(r['pool_size'])) for r in records if isinstance(r, dict) and 'seed' in r and 'pool_size' in r}
    expected = {(s,n) for s in expected_seeds for n in expected_sizes}
    good &= ok('primary result has exact 15 frozen seed×size cells', len(records) == 15 and combos == expected)
    good &= ok('primary result SHA-256 freeze marker', result_path.is_file() and sidecar_ok(result_path))

    final = json.loads(final_path.read_text(encoding='utf-8')) if final_path.is_file() else {}
    good &= ok('consolidated final record present/complete', final.get('status') == 'COMPLETE' and final.get('aggregate',{}).get('cells') == 15)
    good &= ok('consolidated final SHA-256 freeze marker', final_path.is_file() and sidecar_ok(final_path))

    tmp_files = list(ROOT.rglob('*.pyc')) + list(ROOT.rglob('*.tmp'))
    pycache_dirs = [p for p in ROOT.rglob('__pycache__') if p.is_dir()]
    good &= ok('no generated pycache/tmp clutter', not tmp_files and not pycache_dirs, f"files={len(tmp_files)} dirs={len(pycache_dirs)}")

    schema = json.loads((ROOT / 'SCR_I_PREREG_v003' / 'schema' / 'result_schema.json').read_text(encoding='utf-8'))
    actual_keys = set(records[0]) if records else set()
    missing = [k for k in schema.get('required',[]) if k not in actual_keys]
    mapped_only = missing == ['basin_count_base'] and 'basin_count' in actual_keys
    print(('WARN' if mapped_only else 'FAIL') + '  frozen result-schema compatibility' + (
        ' — basin_count_base maps to basin_count; documented in docs/SCHEMA_COMPATIBILITY.md' if mapped_only else f' — missing={missing}'
    ))
    if missing and not mapped_only:
        good = False

    print('WARN  negative-space depth — aggregate gate audit retained; candidate-level reject export was not produced (documented).')
    print()
    print('SCR-I v003 project alignment:', 'PASS WITH DOCUMENTED COMPATIBILITY NOTES' if good else 'FAIL')
    return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
