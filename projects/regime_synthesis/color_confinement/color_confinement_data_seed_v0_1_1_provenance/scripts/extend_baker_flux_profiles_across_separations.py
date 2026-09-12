#!/usr/bin/env python3
"""Extend Baker et al. flux-tube profiles across source separations.

Run from the pack root:
    python scripts/extend_baker_flux_profiles_across_separations.py --download

Without --download, the script parses any ancillary files already present in:
    raw_ancillary/baker2024_arxiv_2409_20168v1/

Outputs:
    data/03_core_flux_tube_profiles/baker2024_extended_flux_profiles_long.csv
    data/03_core_flux_tube_profiles/baker2024_flux_profile_separation_summary.csv
    reports/03_flux_tube_separation_extension.md
    reports/fig_baker_flux_profiles_by_separation.png
    reports/fig_baker_flux_width_peak_vs_separation.png
"""
from __future__ import annotations
from pathlib import Path
import argparse, csv, json, math, re, sys, urllib.request
from typing import Dict, List, Tuple, Optional

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "raw_ancillary" / "baker2024_arxiv_2409_20168v1"
DATA = BASE / "data" / "03_core_flux_tube_profiles"
REPORTS = BASE / "reports"
RAW.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://arxiv.org/src/2409.20168v1/anc/"
PROFILE_FILES = [
    "Ex_FULL_d0.7fm_scaling_normfact.agr",
    "Ex_NP_d0.7fm_scaling_normfact.agr",
    "Ex_FULL_d0.9fm_scaling_normfact.agr",
    "Ex_NP_d0.9fm_scaling_normfact.agr",
    "Ex_FULL_d1.0fm_scaling_normfact.agr",
    "Ex_NP_d1.0fm_scaling_normfact.agr",
    "QCD_large_distances.agr",
    "beta6.3942dist789.agr",
    "beta7.158dist13.agr",
    "Ex_FULL-NP_beta7.158d10a.agr",
]

LONG_COLUMNS = [
    "source_id","source_url","ancillary_url","arxiv_id","source_file","target","series_index",
    "component","nominal_separation_group","lattice","beta","lattice_spacing_fm",
    "source_separation_lattice_units","source_separation_fm","x_t_fm","field_value_GeV2",
    "field_error_GeV2","data_status","series_legend","series_comment","notes"
]

def download_files(files: List[str]) -> List[str]:
    errors=[]
    for fn in files:
        dest = RAW / fn
        if dest.exists() and dest.stat().st_size > 0:
            continue
        try:
            print(f"downloading {fn}")
            urllib.request.urlretrieve(BASE_URL + fn, dest)
        except Exception as e:
            errors.append(f"{fn}: {e}")
    return errors

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def clean_grace(s: str) -> str:
    # remove a few Grace formatting escapes for readable legends
    s = s.replace('\\S4\\N', '^4')
    s = s.replace('\\xb\\f{}', 'beta')
    s = s.replace('\\st\\N', '_t')
    s = s.replace('\\N', '')
    s = s.replace('\\s', '_')
    return s

def parse_metadata(text: str) -> Tuple[Dict[str,str], Dict[str,str]]:
    legends: Dict[str,str] = {}
    comments: Dict[str,str] = {}
    for m in re.finditer(r'@\s*s(\d+)\s+legend\s+"(.*?)"', text):
        legends[f"G0.S{m.group(1)}"] = clean_grace(m.group(2))
    for m in re.finditer(r'@\s*s(\d+)\s+comment\s+"(.*?)"', text):
        comments[f"G0.S{m.group(1)}"] = clean_grace(m.group(2))
    return legends, comments

def infer_component(filename: str, target: str) -> str:
    if "FULL-NP" in filename:
        return "FULL" if target.endswith("S0") else "NP" if target.endswith("S1") else "UNKNOWN"
    if "Ex_FULL" in filename or "EX_FULL" in filename:
        return "FULL"
    if "Ex_NP" in filename or "ENP" in filename:
        return "NP"
    return "PAPER_DEFINED"

def infer_nominal_group(filename: str) -> str:
    for key in ["d0.7fm","d0.9fm","d1.0fm"]:
        if key in filename:
            return key.replace('d','').replace('fm',' fm')
    if "d10a" in filename:
        return "0.738309 fm"
    if "large" in filename.lower():
        return "large-distance group"
    if "dist789" in filename:
        return "dist7/8/9 group"
    if "dist13" in filename:
        return "dist13 group"
    return "unknown"

def infer_float(patterns: List[str], text: str) -> Optional[float]:
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            try: return float(m.group(1))
            except Exception: pass
    return None

def infer_int_text(patterns: List[str], text: str) -> str:
    for pat in patterns:
        m = re.search(pat, text)
        if m: return m.group(1)
    return ""

def parse_agr(path: Path) -> List[dict]:
    text = read_text(path)
    legends, comments = parse_metadata(text)
    pat = re.compile(r'@target\s+(G\d+\.S\d+)\s+@type\s+(\w+)\s+(.*?)(?=\s*&|\s*@target|\Z)', re.S)
    rows: List[dict] = []
    for m in pat.finditer(text):
        target, typ, body = m.group(1), m.group(2), m.group(3)
        nums = [float(x) for x in re.findall(r'[-+]?\d*\.\d+(?:[eE][-+]?\d+)?|[-+]?\d+(?:[eE][-+]?\d+)?', body)]
        cols = 3 if typ.lower() == 'xydy' else 2
        legend = legends.get(target, '')
        comment = comments.get(target, '')
        meta_text = " ".join([path.name, legend, comment])
        series_idx = target.split('S')[-1]
        beta = infer_float([r'beta\s*=\s*([0-9.]+)', r'beta([0-9.]+)', r'_beta([0-9.]+)'], meta_text)
        a_fm = infer_float([r'al([0-9.]+)', r'a\s*=\s*([0-9.]+)'], meta_text)
        d_fm = infer_float([r'd\s*=\s*\d+a\s*=\s*([0-9.]+)\s*fm', r'dist\d+a_([0-9.]+)fm', r'd(0\.[0-9]+)fm'], meta_text)
        dist_lu = infer_int_text([r'd\s*=\s*(\d+a)', r'dist(\d+a)', r'd(\d+a)'], meta_text)
        lattice = infer_int_text([r'(\d+\^4)', r'LAT_(\d+-\d+-\d+-\d+)'], meta_text)
        for i in range(0, len(nums), cols):
            chunk = nums[i:i+cols]
            if len(chunk) == cols:
                rows.append({
                    'source_id':'Baker2024_flux_tube_full_QCD',
                    'source_url':'https://arxiv.org/abs/2409.20168',
                    'ancillary_url':BASE_URL + path.name,
                    'arxiv_id':'2409.20168v1',
                    'source_file':path.name,
                    'target':target,
                    'series_index':series_idx,
                    'component':infer_component(path.name, target),
                    'nominal_separation_group':infer_nominal_group(path.name),
                    'lattice':lattice,
                    'beta':'' if beta is None else beta,
                    'lattice_spacing_fm':'' if a_fm is None else a_fm,
                    'source_separation_lattice_units':dist_lu,
                    'source_separation_fm':'' if d_fm is None else d_fm,
                    'x_t_fm':chunk[0],
                    'field_value_GeV2':chunk[1],
                    'field_error_GeV2':chunk[2] if cols == 3 else '',
                    'data_status':'AUTHOR_ANCILLARY_POINTWISE_DATA_PARSED_FROM_ARXIV',
                    'series_legend':legend,
                    'series_comment':comment,
                    'notes':'Parsed automatically from Grace .agr ancillary file; verify series interpretation before physics use.'
                })
    return rows

def load_existing_profile() -> List[dict]:
    p = DATA / 'baker2024_pointwise_Ex_FULL_NP_beta7_158_d10a_0_738fm.csv'
    rows=[]
    if not p.exists(): return rows
    import csv
    with p.open(newline='',encoding='utf-8') as f:
        for r in csv.DictReader(f):
            for comp, val_key, err_key in [('FULL','Ex_FULL_GeV2','Ex_FULL_error_GeV2'),('NP','Ex_NP_GeV2','Ex_NP_error_GeV2')]:
                if r.get(val_key,'')!='':
                    rows.append({
                        'source_id':r.get('source_id','Baker2024_flux_tube_full_QCD'),
                        'source_url':r.get('source_url','https://arxiv.org/abs/2409.20168'),
                        'ancillary_url':r.get('ancillary_url',''),
                        'arxiv_id':r.get('arxiv_id','2409.20168v1'),
                        'source_file':'Ex_FULL-NP_beta7.158d10a.agr',
                        'target':'G0.S0' if comp=='FULL' else 'G0.S1',
                        'series_index':'0' if comp=='FULL' else '1',
                        'component':comp,
                        'nominal_separation_group':'0.738309 fm',
                        'lattice':'32^4',
                        'beta':r.get('beta',''),
                        'lattice_spacing_fm':r.get('lattice_spacing_fm',''),
                        'source_separation_lattice_units':r.get('source_separation_lattice_units',''),
                        'source_separation_fm':r.get('source_separation_fm',''),
                        'x_t_fm':r.get('x_t_fm',''),
                        'field_value_GeV2':r.get(val_key,''),
                        'field_error_GeV2':r.get(err_key,''),
                        'data_status':'AUTHOR_ANCILLARY_POINTWISE_DATA_ALREADY_EMBEDDED',
                        'series_legend':'32^4, beta=7.158, d=10a=0.738 fm',
                        'series_comment':'Existing embedded FULL/NP control profile.',
                        'notes':'Loaded from existing pointwise CSV.'
                    })
    return rows

def write_csv(path: Path, rows: List[dict], columns: List[str]) -> None:
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        w.writeheader(); w.writerows(rows)

def fwhm_estimate(points: List[Tuple[float,float]]) -> Optional[float]:
    if not points: return None
    pts=sorted(points)
    ys=[y for _,y in pts]
    peak=max(ys)
    if peak <= 0: return None
    half=peak/2.0
    xs=[]
    for (x1,y1),(x2,y2) in zip(pts[:-1], pts[1:]):
        if (y1-half)==0: xs.append(x1)
        if (y1-half)*(y2-half)<0:
            if y2!=y1:
                xs.append(x1 + (half-y1)*(x2-x1)/(y2-y1))
    if len(xs)>=2: return max(xs)-min(xs)
    # fallback discrete width
    above=[x for x,y in pts if y>=half]
    if len(above)>=2: return max(above)-min(above)
    return None

def trapz(points: List[Tuple[float,float]]) -> Optional[float]:
    if len(points)<2: return None
    pts=sorted(points); s=0.0
    for (x1,y1),(x2,y2) in zip(pts[:-1], pts[1:]):
        s += 0.5*(y1+y2)*(x2-x1)
    return s

def summarize(rows: List[dict]) -> List[dict]:
    groups={}
    for r in rows:
        key=(r['source_file'],r['target'],r['component'],str(r.get('source_separation_fm','')),r.get('nominal_separation_group',''))
        try:
            x=float(r['x_t_fm']); y=float(r['field_value_GeV2'])
        except Exception: continue
        groups.setdefault(key,[]).append((x,y))
    out=[]
    for (source_file,target,component,d_fm,ng), pts in sorted(groups.items(), key=lambda kv: (str(kv[0][3]), kv[0][0], kv[0][1])):
        ys=[y for _,y in pts]
        xs=[x for x,_ in pts]
        out.append({
            'source_file':source_file,'target':target,'component':component,
            'source_separation_fm':d_fm,'nominal_separation_group':ng,
            'n_points':len(pts),'x_min_fm':min(xs),'x_max_fm':max(xs),
            'peak_field_GeV2':max(ys),'center_field_GeV2':next((y for x,y in pts if abs(x)<1e-12), ''),
            'fwhm_estimate_fm':'' if fwhm_estimate(pts) is None else fwhm_estimate(pts),
            'area_trapz_GeV2_fm':'' if trapz(pts) is None else trapz(pts),
            'data_status':'computed_from_pointwise_profile'
        })
    return out

def make_plots(rows: List[dict], summary: List[dict]) -> List[str]:
    made=[]
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return made
    # plot profiles by component and separation; limit number of series for readability
    groups={}
    for r in rows:
        try: x=float(r['x_t_fm']); y=float(r['field_value_GeV2'])
        except Exception: continue
        d=str(r.get('source_separation_fm') or r.get('nominal_separation_group'))
        key=(r['component'], d, r['source_file'], r['target'])
        groups.setdefault(key,[]).append((x,y))
    # sort by numeric d if possible
    def dnum(key):
        try: return float(key[1])
        except Exception:
            m=re.search(r'([0-9]+\.[0-9]+)', key[1])
            return float(m.group(1)) if m else 999
    selected=sorted(groups.items(), key=lambda kv: (kv[0][0], dnum(kv[0]), kv[0][2], kv[0][3]))
    if selected:
        plt.figure(figsize=(10,6))
        count=0
        for (comp,d,src,target), pts in selected:
            if count>=16: break
            pts=sorted(pts)
            label=f"{comp} d={d} {src}:{target}"
            plt.plot([x for x,_ in pts], [y for _,y in pts], marker='o', linewidth=1, markersize=3, label=label)
            count+=1
        plt.title('Baker flux-tube profiles across source separations')
        plt.xlabel('transverse distance x_t [fm]')
        plt.ylabel('longitudinal chromoelectric field [GeV^2]')
        plt.legend(fontsize=7)
        plt.tight_layout()
        p=REPORTS/'fig_baker_flux_profiles_by_separation.png'
        plt.savefig(p,dpi=180); plt.close(); made.append(str(p))
    # summary plot: peak and width vs distance for numeric d
    numeric=[]
    for s in summary:
        try: d=float(s['source_separation_fm'])
        except Exception: continue
        try: peak=float(s['peak_field_GeV2'])
        except Exception: continue
        try: width=float(s['fwhm_estimate_fm']) if s['fwhm_estimate_fm']!='' else math.nan
        except Exception: width=math.nan
        numeric.append((d, peak, width, s['component']))
    if numeric:
        plt.figure(figsize=(9,5))
        for comp in sorted(set(c for *_,c in numeric)):
            pts=sorted([(d,peak,width) for d,peak,width,c in numeric if c==comp])
            plt.plot([p[0] for p in pts],[p[1] for p in pts],marker='o',label=f'peak {comp}')
        plt.title('Flux-tube peak field vs source separation')
        plt.xlabel('source separation d [fm]')
        plt.ylabel('peak field [GeV^2]')
        plt.legend()
        plt.tight_layout()
        p=REPORTS/'fig_baker_flux_peak_vs_separation.png'
        plt.savefig(p,dpi=180); plt.close(); made.append(str(p))
        plt.figure(figsize=(9,5))
        for comp in sorted(set(c for *_,c in numeric)):
            pts=sorted([(d,width) for d,peak,width,c in numeric if c==comp and not math.isnan(width)])
            if pts:
                plt.plot([p[0] for p in pts],[p[1] for p in pts],marker='o',label=f'FWHM {comp}')
        plt.title('Flux-tube width estimate vs source separation')
        plt.xlabel('source separation d [fm]')
        plt.ylabel('FWHM estimate [fm]')
        plt.legend()
        plt.tight_layout()
        p=REPORTS/'fig_baker_flux_width_vs_separation.png'
        plt.savefig(p,dpi=180); plt.close(); made.append(str(p))
    return made

def write_report(rows: List[dict], summary: List[dict], missing: List[str], errors: List[str], figures: List[str]) -> None:
    profile_files=sorted(set(r['source_file'] for r in rows))
    sep_values=sorted(set(str(r.get('source_separation_fm') or r.get('nominal_separation_group')) for r in rows))
    md=[]
    md.append('# Baker Flux-Tube Separation Extension\n')
    md.append('This report extends the flux-tube part of the UNNS + color confinement dataset across increasing static-source separations where pointwise Baker ancillary files are available locally or downloadable from arXiv.\n')
    md.append('## Data status\n')
    md.append(f'- Parsed/loaded pointwise rows: {len(rows)}')
    md.append(f'- Pointwise source files represented: {len(profile_files)}')
    md.append(f'- Separation labels represented: {len(sep_values)}')
    if missing:
        md.append(f'- Ancillary files still missing locally: {len(missing)}')
    if errors:
        md.append(f'- Download/parse warnings: {len(errors)}')
    md.append('\n## Files represented\n')
    for fn in profile_files:
        md.append(f'- `{fn}`')
    if missing:
        md.append('\n## Missing ancillary files\n')
        for fn in missing: md.append(f'- `{fn}`')
    if errors:
        md.append('\n## Download/parse warnings\n')
        for e in errors: md.append(f'- {e}')
    md.append('\n## Separation-summary table\n')
    md.append('| source file | component | d [fm] | group | n | peak [GeV^2] | FWHM [fm] | area |')
    md.append('|---|---|---:|---|---:|---:|---:|---:|')
    for s in summary[:80]:
        md.append(f"| {s['source_file']} | {s['component']} | {s['source_separation_fm']} | {s['nominal_separation_group']} | {s['n_points']} | {s['peak_field_GeV2']} | {s['fwhm_estimate_fm']} | {s['area_trapz_GeV2_fm']} |")
    md.append('\n## UNNS interpretation target\n')
    md.append('The extended Baker profiles are intended to test whether localized route geometry changes as the static-source separation approaches larger distances. The intended UNNS object is:')
    md.append('\n```text\nsource separation d -> route-extension coordinate\ntransverse Ex(x_t) profile -> localized route geometry\npeak/area/width trends -> route-thickening or route-weakening indicators\nlarge-distance profile changes -> approach toward repair/window behavior\n```\n')
    md.append('## Boundary\n')
    md.append('Do not interpret missing profiles as negative evidence. If only the already embedded d=0.738309 fm profile is present, this report is a scaffold plus control profile; run with `--download` on a machine with internet access to populate the full arXiv ancillary profile set.\n')
    if figures:
        md.append('## Figures\n')
        for fig in figures:
            md.append(f'- `{Path(fig).name}`')
    (REPORTS/'03_flux_tube_separation_extension.md').write_text('\n'.join(md),encoding='utf-8')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--download', action='store_true', help='download Baker arXiv ancillary .agr files before parsing')
    args=ap.parse_args()
    errors=[]
    if args.download:
        errors += download_files(PROFILE_FILES)
    rows=[]
    for fn in PROFILE_FILES:
        p=RAW/fn
        if p.exists() and p.stat().st_size>0:
            try:
                rows.extend(parse_agr(p))
            except Exception as e:
                errors.append(f'parse failed {fn}: {e}')
    # Always include existing embedded profile as a control if present.
    embedded=load_existing_profile()
    existing_keys={(r['source_file'],r['target'],r['component'],str(r['x_t_fm'])) for r in rows}
    for r in embedded:
        k=(r['source_file'],r['target'],r['component'],str(r['x_t_fm']))
        if k not in existing_keys: rows.append(r)
    
    embedded_present = bool(embedded)
    missing=[]
    for fn in PROFILE_FILES:
        if (RAW/fn).exists():
            continue
        if fn == 'Ex_FULL-NP_beta7.158d10a.agr' and embedded_present:
            continue
        missing.append(fn)
    write_csv(DATA/'baker2024_extended_flux_profiles_long.csv', rows, LONG_COLUMNS)
    summary=summarize(rows)
    summary_cols=['source_file','target','component','source_separation_fm','nominal_separation_group','n_points','x_min_fm','x_max_fm','peak_field_GeV2','center_field_GeV2','fwhm_estimate_fm','area_trapz_GeV2_fm','data_status']
    write_csv(DATA/'baker2024_flux_profile_separation_summary.csv', summary, summary_cols)
    figures=make_plots(rows,summary)
    write_report(rows,summary,missing,errors,figures)
    metrics={'rows':len(rows),'profiles':len(summary),'source_files':sorted(set(r['source_file'] for r in rows)),'missing_files':missing,'errors':errors,'figures':[str(Path(f).relative_to(BASE)) for f in figures]}
    (REPORTS/'03_flux_tube_separation_extension_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
    print('BAKER FLUX-TUBE EXTENSION COMPLETE')
    print('rows:',len(rows),'profiles:',len(summary),'missing:',len(missing))
    print('report:', REPORTS/'03_flux_tube_separation_extension.md')

if __name__ == '__main__':
    main()
