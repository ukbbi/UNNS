from pathlib import Path
from zipfile import ZipFile
import csv, tempfile
from xlsx_min import extract
ROOT=Path(__file__).resolve().parents[1]
ARC=ROOT/'02_RAW'/'LUO_2026'/'18396452.zip'
OUT=Path(__file__).resolve().parent/'LUO'; OUT.mkdir(exist_ok=True)
specs=[('Fig2b1Data.xlsx','LUO_M_N12.csv',1,'m'),('Fig2b1Data.xlsx','LUO_M_N32.csv',2,'m'),('Fig2c1Data.xlsx','LUO_F_N12.csv',1,'F'),('Fig2c1Data.xlsx','LUO_F_N40.csv',2,'F'),('Fig3a1Data.xlsx','LUO_EE_LOW_N12.csv',1,'S'),('Fig3a1Data.xlsx','LUO_EE_LOW_N32.csv',2,'S'),('Fig3a2Data.xlsx','LUO_EE_DTQC_N12.csv',1,'S'),('Fig3a2Data.xlsx','LUO_EE_DTQC_N32.csv',2,'S'),('Fig3a3Data.xlsx','LUO_EE_HIGH_N12.csv',1,'S'),('Fig3a3Data.xlsx','LUO_EE_HIGH_N32.csv',2,'S')]
with tempfile.TemporaryDirectory() as td:
    with ZipFile(ARC) as z:
        needed=sorted(set(s[0] for s in specs))
        for n in needed: z.extract(n,td)
    for src,fn,col,name in specs:
        rows=extract(Path(td)/src,[0,col],None,2)
        with (OUT/fn).open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f); w.writerow(['sample_index','time',name])
            for i,r in enumerate(rows): w.writerow([i]+r)
