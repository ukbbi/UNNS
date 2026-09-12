from __future__ import annotations
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import re
MAIN_NS="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
def _ci(ref):
    n=0
    for ch in ref: n=n*26+(ord(ch)-64)
    return n-1
def _shared(z):
    try: root=ET.fromstring(z.read("xl/sharedStrings.xml"))
    except KeyError: return []
    return ["".join(t.text or "" for t in si.iter(f"{{{MAIN_NS}}}t")) for si in root.findall(f"{{{MAIN_NS}}}si")]
def _target(z,sheet):
    wb=ET.fromstring(z.read("xl/workbook.xml")); rels=ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rm={r.attrib["Id"]:r.attrib["Target"] for r in rels}
    for s in wb.find(f"{{{MAIN_NS}}}sheets"):
        if sheet is None or s.attrib["name"]==sheet:
            t=rm[s.attrib[f"{{{REL_NS}}}id"]]
            return ("xl/"+t.lstrip("/")) if not t.startswith("/") else t.lstrip("/")
    raise KeyError(sheet)
def extract(path, cols, sheet=None, start_row=2):
    out=[]
    with ZipFile(path) as z:
        ss=_shared(z); target=_target(z,sheet)
        with z.open(target) as f:
            for _,e in ET.iterparse(f,events=("end",)):
                if e.tag!=f"{{{MAIN_NS}}}row": continue
                rr=e.attrib.get("r");
                if rr is None:
                    e.clear(); continue
                r=int(rr); vals={}
                if r>=start_row:
                    for c in e.findall(f"{{{MAIN_NS}}}c"):
                        m=re.match(r"([A-Z]+)(\d+)",c.attrib.get("r",""));
                        if not m: continue
                        i=_ci(m.group(1)); typ=c.attrib.get("t"); v=c.find(f"{{{MAIN_NS}}}v"); val=None
                        if typ=="inlineStr":
                            q=c.find(f"{{{MAIN_NS}}}is"); val="".join(t.text or "" for t in q.iter(f"{{{MAIN_NS}}}t")) if q is not None else None
                        elif v is not None:
                            txt=v.text
                            if typ=="s": val=ss[int(txt)]
                            elif typ=="str": val=txt
                            else:
                                try: val=float(txt)
                                except: val=txt
                        vals[i]=val
                    row=[vals.get(i) for i in cols]
                    if all(v is not None for v in row): out.append(row)
                e.clear()
    return out
