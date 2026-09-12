#!/usr/bin/env python3
"""Download Baker et al. 2024 arXiv ancillary files and convert Grace .agr pointwise datasets to CSV.
Run from this pack root: python scripts/fetch_baker_ancillary.py
"""
from pathlib import Path
import re, csv, urllib.request

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "raw_ancillary" / "baker2024_arxiv_2409_20168v1"
OUT = BASE / "data" / "03_core_flux_tube_profiles" / "parsed_ancillary_csv"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
FILES = [
 'ENP_1064_0532.agr','EX_FULL-3d.dat','EX_FULL_vs_smearing_xl0.148_beta7.158.agr',
 'Ex_FULL-NP_beta7.158d10a.agr','Ex_FULL_d0.7fm_scaling_normfact.agr','Ex_FULL_d0.9fm_scaling_normfact.agr','Ex_FULL_d1.0fm_scaling_normfact.agr',
 'Ex_NP_d0.7fm_scaling_normfact.agr','Ex_NP_d0.9fm_scaling_normfact.agr','Ex_NP_d1.0fm_scaling_normfact.agr',
 'MC_1064_0532.agr','QCD_large_distances.agr','SU3_beta6.136dist16.agr','beta6.3942dist789.agr','beta6.3942dist789.eps','beta7.158dist13.agr',
 'sqrtstring_from_integral.agr','sqrtstring_from_integral.pdf','width_from_integral.agr'
]
BASE_URL = 'https://arxiv.org/src/2409.20168v1/anc/'

def download():
    for fn in FILES:
        dest = RAW / fn
        if dest.exists() and dest.stat().st_size > 0:
            continue
        print('downloading', fn)
        urllib.request.urlretrieve(BASE_URL + fn, dest)

def parse_agr(path: Path):
    text = path.read_text(errors='replace')
    # Grace datasets appear after @target G0.Sx @type xydy, ending at &
    pat = re.compile(r'@target\s+(G\d+\.S\d+)\s+@type\s+(\w+)\s+(.*?)(?=\s*&|\s*@target|\Z)', re.S)
    rows = []
    for m in pat.finditer(text):
        target, typ, body = m.group(1), m.group(2), m.group(3)
        nums = [float(x) for x in re.findall(r'[-+]?\d*\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+(?:[eE][-+]?\d+)?', body)]
        cols = 3 if typ.lower() == 'xydy' else 2
        for i in range(0, len(nums), cols):
            chunk = nums[i:i+cols]
            if len(chunk) == cols:
                rows.append({'source_file': path.name, 'target': target, 'type': typ, 'x': chunk[0], 'y': chunk[1], 'dy': chunk[2] if cols == 3 else ''})
    return rows

def convert():
    for p in RAW.glob('*.agr'):
        rows = parse_agr(p)
        if not rows:
            continue
        out = OUT / (p.stem + '.csv')
        with out.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=['source_file','target','type','x','y','dy'])
            w.writeheader(); w.writerows(rows)
        print('parsed', p.name, '->', out, len(rows), 'rows')

if __name__ == '__main__':
    download()
    convert()
