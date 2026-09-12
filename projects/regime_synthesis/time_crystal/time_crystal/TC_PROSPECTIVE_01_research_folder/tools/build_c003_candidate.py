from __future__ import annotations
import argparse,csv,json,shutil,struct,tempfile
from pathlib import Path

FREE=0xFFFFFFFF
ENDOF=0xFFFFFFFE
PHI_ROUNDED=1.618

def _rk_value(rk):
    if rk & 2:
        val=float(struct.unpack("<i",struct.pack("<I",rk))[0]>>2)
    else:
        val=struct.unpack("<d",struct.pack("<II",0,rk&0xFFFFFFFC))[0]
    return val/100.0 if rk&1 else val

class LegacyXls:
    def __init__(self,path):
        self.path=Path(path)
        self.data=self.path.read_bytes()
        if self.data[:8] != bytes.fromhex("d0cf11e0a1b11ae1"):
            raise RuntimeError("Not a legacy OLE XLS file")
        self.sec_size=1<<struct.unpack_from("<H",self.data,0x1E)[0]
        self.num_fat=struct.unpack_from("<I",self.data,0x2C)[0]
        self.first_dir=struct.unpack_from("<I",self.data,0x30)[0]
        difat=[x for x in struct.unpack_from("<109I",self.data,0x4C)
               if x not in (FREE,ENDOF)]
        self.fat=[]
        n=self.sec_size//4
        for sid in difat[:self.num_fat]:
            self.fat.extend(struct.unpack_from(f"<{n}I",self.data,(sid+1)*self.sec_size))
        self.workbook=self._workbook_stream()
        self.records=self._records(self.workbook)
        self.sst=self._sst()
        self.sheets=self._boundsheets()

    def _chain(self,start,size=None):
        out=bytearray();seen=set();sid=start
        while sid not in (FREE,ENDOF) and sid<len(self.fat) and sid not in seen:
            seen.add(sid)
            off=(sid+1)*self.sec_size
            out+=self.data[off:off+self.sec_size]
            sid=self.fat[sid]
        return bytes(out if size is None else out[:size])

    def _workbook_stream(self):
        db=self._chain(self.first_dir)
        for i in range(0,len(db),128):
            e=db[i:i+128]
            if len(e)<128: break
            nlen=struct.unpack_from("<H",e,64)[0]
            name=e[:max(0,nlen-2)].decode("utf-16le","ignore") if nlen>=2 else ""
            if e[66]==2 and name=="Workbook":
                start=struct.unpack_from("<I",e,116)[0]
                size=struct.unpack_from("<Q",e,120)[0]
                return self._chain(start,size)
        raise RuntimeError("Workbook stream not found")

    @staticmethod
    def _records(buf):
        out=[];pos=0
        while pos+4<=len(buf):
            rid,rlen=struct.unpack_from("<HH",buf,pos)
            end=pos+4+rlen
            if end>len(buf): break
            out.append((pos,rid,buf[pos+4:end]))
            pos=end
        return out

    def _sst(self):
        rec=next((r for r in self.records if r[1]==0x00FC),None)
        if rec is None: return []
        buf=rec[2];_,unique=struct.unpack_from("<II",buf,0);pos=8;out=[]
        for _ in range(unique):
            cch=struct.unpack_from("<H",buf,pos)[0];pos+=2
            flags=buf[pos];pos+=1
            rich=bool(flags&8);ext=bool(flags&4);high=bool(flags&1)
            crun=struct.unpack_from("<H",buf,pos)[0] if rich else 0
            if rich: pos+=2
            cbext=struct.unpack_from("<I",buf,pos)[0] if ext else 0
            if ext: pos+=4
            nbytes=cch*(2 if high else 1)
            raw=buf[pos:pos+nbytes];pos+=nbytes
            out.append(raw.decode("utf-16le" if high else "latin1","replace"))
            pos+=crun*4+cbext
        return out

    def _boundsheets(self):
        out=[]
        for _,rid,pay in self.records:
            if rid!=0x0085: continue
            off=struct.unpack_from("<I",pay,0)[0];cch=pay[6];flags=pay[7]
            name=(pay[8:8+2*cch].decode("utf-16le","ignore") if flags&1
                  else pay[8:8+cch].decode("latin1","ignore"))
            out.append((name,off))
        return out

    def cells(self,sheet):
        try: off=next(o for n,o in self.sheets if n==sheet)
        except StopIteration: raise RuntimeError(f"Missing sheet {sheet}")
        cells={};pos=off
        while pos+4<=len(self.workbook):
            rid,rlen=struct.unpack_from("<HH",self.workbook,pos)
            pay=self.workbook[pos+4:pos+4+rlen]
            if rid==0x000A: break
            if rid==0x0203:
                r,c,_=struct.unpack_from("<HHH",pay,0)
                cells[(r,c)]=struct.unpack_from("<d",pay,6)[0]
            elif rid==0x027E:
                r,c,_,rk=struct.unpack_from("<HHHI",pay,0)
                cells[(r,c)]=_rk_value(rk)
            elif rid==0x00BD:
                r,fc=struct.unpack_from("<HH",pay,0);n=(len(pay)-6)//6
                for i in range(n):
                    _,rk=struct.unpack_from("<HI",pay,4+i*6)
                    cells[(r,fc+i)]=_rk_value(rk)
            elif rid==0x00FD:
                r,c,_,idx=struct.unpack_from("<HHHI",pay,0)
                cells[(r,c)]=self.sst[idx]
            pos+=4+rlen
        return cells

def section(cells,title):
    hits=[rc for rc,v in cells.items() if v==title]
    if len(hits)!=1: raise RuntimeError(f"Expected one {title} section")
    r0,c0=hits[0]
    if cells.get((r0+1,c0))!="x" or cells.get((r0+1,c0+1))!="y":
        raise RuntimeError(f"Unexpected headers for {title}")
    rows=[];r=r0+2
    while (r,c0) in cells and (r,c0+1) in cells:
        x=float(cells[(r,c0)]);y=float(cells[(r,c0+1)])
        err=cells.get((r,c0+2))
        rows.append((x,y,float(err) if isinstance(err,(int,float)) else None))
        r+=1
    return rows

def dual_clock(rows):
    # The raw source time axis is expressed in units of tau1 and includes the
    # union of pulse-event times n1*tau1 and n2*tau2, with tau2/tau1=1.618
    # rounded to three decimals in the source workbook.
    c1={};c2={}
    for t,y,e in rows:
        n1=round(t)
        if abs(t-n1)<1e-12:
            c1[int(n1)]=(y,e,t)
        n2=int(round(t/PHI_ROUNDED))
        if abs(t-round(n2*PHI_ROUNDED,3))<5e-7:
            c2[n2]=(y,e,t)
    common=sorted(set(c1)&set(c2))
    if len(common)<20:
        raise RuntimeError("Too few paired dual-clock events")
    return [(n,c1[n],c2[n]) for n in common]

def build(source,title,candidate_id,outzip):
    book=LegacyXls(source)
    rows=section(book.cells("Fig. 1"),title)
    paired=dual_clock(rows)
    with tempfile.TemporaryDirectory(prefix="tc_p01_c003_") as td:
        td=Path(td);root=td/candidate_id;(root/"temporal").mkdir(parents=True)
        (root/"manifest.json").write_text(json.dumps({
            "candidate_id":candidate_id,
            "label":candidate_id,
            "domain":"quantum_many_body",
            "protocol":"quantum_dtc_v1_1_0"
        },indent=2),encoding="utf-8")
        with (root/"temporal"/"trajectories.csv").open("w",newline="",encoding="utf-8") as f:
            w=csv.writer(f);w.writerow(["event_index","clock_A","clock_B"])
            for n,a,b in paired:
                w.writerow([n,format(a[0],".15g"),format(b[0],".15g")])
        with (root/"temporal"/"sampling_provenance.csv").open("w",newline="",encoding="utf-8") as f:
            w=csv.writer(f);w.writerow(["event_index","time_clock_A","time_clock_B","error_A","error_B"])
            for n,a,b in paired:
                w.writerow([n,format(a[2],".15g"),format(b[2],".15g"),
                            "" if a[1] is None else format(a[1],".15g"),
                            "" if b[1] is None else format(b[1],".15g")])
        (root/"ADAPTER_RECORD.json").write_text(json.dumps({
            "candidate_id":candidate_id,
            "source_kind":"experimental signed polarization under two incommensurate drive clocks",
            "paired_event_count":len(paired),
            "clock_ratio_used_from_source_protocol":PHI_ROUNDED,
            "operation":(
                "Pair only experimentally stored polarization samples at the nth event of "
                "each of the two documented incommensurate drive clocks. No interpolation "
                "or synthetic signal values are created. The two measured clock-event "
                "sequences become the two chamber coordinates."
            ),
            "forbidden_operations_confirmed_absent":[
                "uniform resampling","Fourier filtering","target response frequency input",
                "sign alignment","favorable sub-window selection","chamber threshold tuning"
            ]
        },indent=2),encoding="utf-8")
        if outzip.exists(): outzip.unlink()
        shutil.make_archive(str(outzip.with_suffix("")),"zip",root.parent,root.name)
    return rows,paired

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("rawdata_xls")
    ap.add_argument("project_root")
    a=ap.parse_args()
    src=Path(a.rawdata_xls).resolve();root=Path(a.project_root).resolve()
    cands=root/"candidates";cands.mkdir(parents=True,exist_ok=True)
    _,pc=build(src,"Fig. 1d","TC_P01_C003",cands/"TC_P01_C003.zip")
    _,pk=build(src,"Fig. 1b","TC_P01_C003_CTRL",cands/"TC_P01_C003_CTRL.zip")
    print("C003 ADAPTER STATUS: COMPLETE")
    print("Candidate paired events:",len(pc))
    print("Control paired events:",len(pk))
    print("Candidate:",cands/"TC_P01_C003.zip")
    print("Control:",cands/"TC_P01_C003_CTRL.zip")

if __name__=="__main__":
    main()
