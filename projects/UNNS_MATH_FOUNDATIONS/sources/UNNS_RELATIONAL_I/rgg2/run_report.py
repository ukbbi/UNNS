"""Produce exact RGG-2 examples and summary files (Python standard library only)."""
import csv, json
from pathlib import Path
from itertools import combinations
from math import log
from src.anchor_routes import Anchor, fibre
from src.joint_ops import j_join,j_mul
from src.relational_metric import lift_ratio, distance
from src.quotient import quotient_witness

ROOT=Path(__file__).resolve().parent
REPORTS=ROOT/'output/reports'; TABLES=ROOT/'output/tables'; FIGURES=ROOT/'output/figures'
for p in (REPORTS,TABLES,FIGURES): p.mkdir(parents=True,exist_ok=True)

F=fibre(72)
records=[]
for a,b in combinations(F,2):
    records.append({'value':72,'r':f'{a.k},{a.d}','s':f'{b.k},{b.d}',
      'join_value':j_join(a,b).value,'lift_ratio':lift_ratio(a,b),
      'distance_log':round(distance(a,b),12)})
with (TABLES/'fibre72.csv').open('w',newline='',encoding='utf-8') as file:
    w=csv.DictWriter(file,fieldnames=list(records[0]));w.writeheader();w.writerows(records)

routes=[r for m in range(1,401) for r in fibre(m)]
report={'scope':'positive-integer anchor routes; candidate J_join',
        'source':'UNNS nest formula plus explicitly proposed J_join; no physical claim',
        'routes_in_fibre_72':[{'k':r.k,'d':r.d,'value':r.value} for r in F],
        'fibre_72_pairwise':records,
        'finite_join_quotient_witness': quotient_witness(routes,j_join),
        'finite_mul_quotient_witness': quotient_witness(routes,j_mul),
        'status':{'T1':'proved','T2':'proved','T3':'proved','T4':'proved','T5':'proved on defined refinement domains'},
        'warning':'finite tests corroborate proofs but do not select J_join as an independently grounded interaction'}
(REPORTS/'rgg2_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# A self-contained, exact-label illustrative triangle; not an evidentiary scientific plot.
pts=[(125,80),(460,80),(293,298)]
labels=['(18,2)','(8,3)','(2,6)']
lines=[]
for i,j in [(0,1),(0,2),(1,2)]:
    a,b=F[i],F[j]
    x1,y1=pts[i]; x2,y2=pts[j]
    lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#59738c" stroke-width="2"/>')
    x,y=(x1+x2)/2,(y1+y2)/2
    lines.append(f'<text x="{x}" y="{y-10 if i+j==1 else y+17}" font-size="13" text-anchor="middle" fill="#243b53">lift ×{lift_ratio(a,b)}</text>')
for (x,y),lab in zip(pts,labels):
    lines.append(f'<circle cx="{x}" cy="{y}" r="34" fill="#edf3f8" stroke="#264861" stroke-width="2"/>')
    lines.append(f'<text x="{x}" y="{y+5}" font-size="13" text-anchor="middle" fill="#182d3c">{lab}</text>')
svg="""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="380" viewBox="0 0 600 380"><rect width="600" height="380" fill="#fff"/><text x="300" y="27" text-anchor="middle" font-size="18" font-family="Arial" fill="#1e3448">Fibre 72 — exact join lift</text><g font-family="Arial">"""+''.join(lines)+"""</g><text x="300" y="358" text-anchor="middle" font-size="12" font-family="Arial" fill="#4e5964">Node = (k,d), value 72. Edge = output / 72 (candidate J_join).</text></svg>"""
(FIGURES/'fibre72.svg').write_text(svg,encoding='utf-8')
print('RGG-2 report created: output/reports/rgg2_report.json; output/tables/fibre72.csv; output/figures/fibre72.svg')
