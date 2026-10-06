#!/usr/bin/env python3
from pathlib import Path
import fitz, hashlib, json, re
PUB_SHA="af40f084cf4f4624224af726d0bb4822e449b161b03ce38972077023cbd0ca7c"
ARX_SHA="f0eb6406bf49a00d376c0be25917173426c826050046a1bf0f32987895de23d0"
PRIMARY=(3.405,0.021)
ALT=(3.391,0.023)

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()

def text(p):
 d=fitz.open(p); s=' '.join(pg.get_text('text') for pg in d)
 s=s.replace('’',"'").replace('−','-').replace('–','-').replace('—','-').replace('ﬁ','fi').replace('ﬀ','ff').replace('ﬂ','fl').replace('ﬁ','fi').replace('ﬀ','ff').replace('ﬂ','fl')
 return re.sub(r'\s+',' ',s).strip()

root=Path(__file__).resolve().parent.parent
pub=root/'data'/'raw'/'at20'/'Athenodorou-Teper2020_Article_TheGlueballSpectrumOfSU3GaugeT.pdf'
arx=root/'data'/'raw'/'at20'/'2007.06422v2.pdf'
if not pub.exists() or not arx.exists(): raise SystemExit('Missing SPEC-I/A source PDFs in data/raw/at20/')
if sha(pub)!=PUB_SHA: raise SystemExit('Published PDF SHA-256 mismatch')
if sha(arx)!=ARX_SHA: raise SystemExit('arXiv v2 PDF SHA-256 mismatch')
pt=text(pub); at=text(arx)
phrases=['so that the vacuum energy is zero','the lightest state of interest is the first excited state above the vacuum',"The 0++ ground state is the lightest of all the glueballs and constitutes the theory's mass gap",'3.405(21)','3.391(23)','We shall employ the first value']
for ph in phrases:
 if ph not in pt or ph not in at: raise SystemExit('Required source phrase missing: '+ph)
pl=PRIMARY[0]-PRIMARY[1]; al=ALT[0]-ALT[1]
status='SPECTRAL-SCALE-POSITIVE' if pl>0 and al>0 else 'SPECTRAL-SCALE-INDETERMINATE'
out=root/'data'/'derived'/'at20'; out.mkdir(parents=True,exist_ok=True)
rec={'schema':'SPEC_I_A_EXTRACT_v1','status':status,'stage3_coexistence_verdict_issued':False,'source_hashes':{'published':PUB_SHA,'arxiv_v2':ARX_SHA},'primary':{'value':PRIMARY[0],'sigma':PRIMARY[1],'lower_1sigma':pl},'alternate':{'value':ALT[0],'sigma':ALT[1],'lower_1sigma':al},'independent_replication_count':0}
(out/'SPEC_I_A_EXTRACT.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
rep=root/'output'/'spec_i_a'; rep.mkdir(parents=True,exist_ok=True)
(rep/'SPEC_I_A_RESULT.md').write_text(f'# SPEC-I/A Result\n\n**Status:** **{status}**\n\nPrimary: `3.405 +/- 0.021`, lower 1-sigma = `{pl:.3f}`.\n\nAlternate: `3.391 +/- 0.023`, lower 1-sigma = `{al:.3f}`.\n\nStage-3 coexistence verdict: **NOT ISSUED**.\n',encoding='utf-8')
print('SPEC-I/A:',status)
print('primary lower 1-sigma =',pl)
print('alternate lower 1-sigma =',al)
print('No Stage-3 coexistence verdict issued.')
