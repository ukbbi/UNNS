#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re
import pymupdf

PDF_SHA = '66973cf81063071cf5c58d93cff86d4778b7d8f11e83eb1f3b89a21be3047f22'
VALUE = 4.16
SIGMA_STAT = 0.11
SIGMA_ANISO = 0.04
HIST_VALUE = 4.21
HIST_SIGMA = 0.11

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()

def text_from_pdf(path):
    doc=pymupdf.open(path)
    s=' '.join(p.get_text('text') for p in doc)
    s=s.replace('−','-').replace('–','-').replace('—','-')
    return re.sub(r'\s+',' ',s)

def require(text,label,pattern):
    if not re.search(pattern,text,re.I):
        raise SystemExit('Missing required source phrase/value: '+label)

root=Path(__file__).resolve().parent.parent
src=root/'data'/'raw'/'chen06'/'chen06.pdf'
if not src.exists():
    raise SystemExit('Missing canonical Chen06 PDF: '+str(src))
if sha256(src)!=PDF_SHA:
    raise SystemExit('Chen06 PDF SHA-256 mismatch')

text=text_from_pdf(src)
require(text,'title',r'Glueball Spectrum and Matrix Elements on Anisotropic Lattices')
require(text,'continuum',r'continuum limits are reliably extrapolated')
require(text,'Table VIII',r'4\.16\(11\).*?4\.21\(11\)')
require(text,'Table XXI',r'0\+\+.*?4\.16\(11\)\(4\).*?1710\(50\)\(80\)')
require(text,'pure SU(3)',r'pure SU\(3\) gauge theory')
require(text,'vacuum subtraction',r'vacuum subtraction')

lower=VALUE-SIGMA_STAT-SIGMA_ANISO
sigma_quad=(SIGMA_STAT**2+SIGMA_ANISO**2)**0.5
lower_quad=VALUE-sigma_quad
hist_lower=HIST_VALUE-HIST_SIGMA
status='SPECTRAL-SCALE-POSITIVE' if lower>0 else 'SPECTRAL-SCALE-INDETERMINATE'

out=root/'data'/'derived'/'chen06'
out.mkdir(parents=True,exist_ok=True)
record={
 'schema':'SPEC_I_B_EXTRACT_v1',
 'status':status,
 'stage3_coexistence_verdict_issued':False,
 'source':{'path':'data/raw/chen06/chen06.pdf','sha256':PDF_SHA},
 'theory':'pure SU(3) gauge theory',
 'state':'0++ scalar glueball',
 'coordinate':'r0*M_0++',
 'primary':{
   'value':VALUE,
   'sigma_stat':SIGMA_STAT,
   'sigma_anisotropy':SIGMA_ANISO,
   'lower_conservative_linear':lower,
   'sigma_quadrature_provenance_only':sigma_quad,
   'lower_quadrature_provenance_only':lower_quad
 },
 'historical_source_check':{
   'value':HIST_VALUE,
   'sigma':HIST_SIGMA,
   'lower_1sigma':hist_lower,
   'counts_as_stage3_independent_branch':False
 }
}
(out/'SPEC_I_B_EXTRACT.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')

rep=root/'output'/'spec_i_b'
rep.mkdir(parents=True,exist_ok=True)
report = '# SPEC-I/B Result\n\n'
report += '**Status:** **'+status+'**  \n'
report += '**Stage-3 coexistence verdict issued:** **NO**\n\n'
report += 'Primary independent continuum coordinate:\n\n```text\nr0 M_0++ = 4.16(11)(4)\n```\n\n'
report += 'Frozen conservative lower bound:\n\n```text\n4.16 - 0.11 - 0.04 = %.3f\n```\n\n' % lower
report += 'This remains strictly above zero.\n\n'
report += 'Historical source comparison:\n\n```text\nRef. [4] quoted in Table VIII: r0 M_0++ = 4.21(11)\n```\n\n'
report += 'It is not counted as another Stage-3 branch.\n\nBRIDGE-III has not yet been issued.\n'
(rep/'SPEC_I_B_RESULT.md').write_text(report,encoding='utf-8')

print('SPEC-I/B:',status)
print('conservative lower bound =',lower)
print('No BRIDGE-III verdict issued.')
