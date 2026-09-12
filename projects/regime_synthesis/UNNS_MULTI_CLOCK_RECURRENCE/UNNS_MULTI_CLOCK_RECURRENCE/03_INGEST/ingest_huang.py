from pathlib import Path
import csv
from xlsx_min import extract
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'02_RAW'/'HUANG_2025'/'41467_2025_64413_MOESM3_ESM.xlsx'
OUT=Path(__file__).resolve().parent/'HUANG'; OUT.mkdir(exist_ok=True)
for fn,cols,names in [('HUANG_LC.csv',[0,1],['time','intensity']),('HUANG_QP.csv',[6,7],['time','intensity']),('HUANG_CHAOS.csv',[16,17],['time','intensity'])]:
    rows=extract(SRC,cols,'Figure2',3)
    with (OUT/fn).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['sample_index']+names)
        for i,r in enumerate(rows): w.writerow([i]+r)
