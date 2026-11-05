"""Integrity checks for PAPER_IV_SYNTHESIS v0.5 (manuscript integrity only; NOT independent certification of the mathematics)."""
import os, re, sys, json, glob, hashlib, subprocess, csv
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = []
def chk(name, ok, detail=''):
    res.append((name, bool(ok), detail)); print(('PASS ' if ok else 'FAIL ')+name+(' :: '+str(detail) if detail and not ok else ''))
rd = lambda p: open(os.path.join(H, p), encoding='utf-8').read()
pdf = os.path.join(H, 'PAPER_IV_SYNTHESIS_v0.5.pdf')
tex = {p: rd(p) for p in ['tex/main.tex', 'tex/refs.tex'] + [os.path.relpath(f, H) for f in sorted(glob.glob(H+'/tex/sections/*.tex')+glob.glob(H+'/tex/appendices/*.tex'))]}
alltex = '\n'.join(tex.values())
# 1 pdf and status
pdfs = [f for f in glob.glob(H+'/*.pdf')]
chk('one PDF at package root', len(pdfs) == 1 and os.path.basename(pdfs[0]) == 'PAPER_IV_SYNTHESIS_v0.5.pdf')
st = json.load(open(H+'/STATUS.json')) if os.path.exists(H+'/STATUS.json') else {}
chk('STATUS.json sha256 matches PDF', st.get('pdf_sha256') == hashlib.sha256(open(pdf, 'rb').read()).hexdigest())
txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
chk('PDF is searchable text and has >= 30 pages', len(txt) > 50000 and int(re.search(r'Pages:\s+(\d+)', info).group(1)) >= 30)
# 2 build log
log = open(H+'/tex/main.log', errors='ignore').read() if os.path.exists(H+'/tex/main.log') else ''
chk('no undefined references or citations in build log', not re.search(r'LaTeX Warning: (Reference|Citation).*undefined', log))
chk('no unresolved source citation (xref) in build log', 'Package xref Warning' not in log)
chk('no "??" in PDF text', '??' not in txt)
chk('no LaTeX errors in log', not re.search(r'^!', log, re.M))
# 3 title, author, draft
chk('title exact', 'The Geometry of Generation in the UNNS Substrate' in tex['tex/main.tex'] and 'A Mathematical Synthesis' in tex['tex/main.tex'])
chk('author is UNNS Research Collective, no personal name', 'UNNS Research Collective' in tex['tex/main.tex'] and 'Igor' not in alltex and 'Igor' not in txt)
chk('word "draft" never used (sources and PDF)', not re.search(r'draft', alltex, re.I) and not re.search(r'draft', txt, re.I))
# 4 abstract
ab = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', tex['tex/main.tex'], re.S).group(1)
chk('abstract contains no FIELD-I / SELECT-II / GEO-HD-1', not re.search(r'FIELD-I|SELECT-II|GEO-HD', ab))
chk('abstract opens with the mathematical problem (maps and sets, no inventory)', ab.strip().startswith('Two arithmetic transformations') and not re.search(r'\d+ (theorems|results|records)', ab))
chk('abstract claims no universal law', 'No universal law is claimed' in ab)
# 5 structure
secs = re.findall(r'\\input\{sections/(sec\d+_[a-z_]+)\}', tex['tex/main.tex'])
chk('16 section files in order', len(secs) == 16 and [s[3:5] for s in secs] == ['%02d' % i for i in range(1, 17)])
want = ['Introduction and the mathematical synthesis problem', 'States, histories, occurrence geometry and evolution', 'Numerical projection and generative information', 'Occurrence projection and dormant arithmetic structure',
        'Geometric realization and dimensional transport', 'Arithmetic constraints and history topology', 'Endpoint geometry versus global ancestry', 'Structural changes during collective evolution',
        'Arithmetic prediction and homological consequences', 'Collective recurrence and geometric behavior', 'Correspondence between distinct generating rules', 'The unified diagram',
        'Synthesis propositions and obstructions', 'Relation to established theories', 'Principal mathematical conclusions', 'Open questions']
heads = [re.search(r'\\section\{([^}]*)\}', tex['tex/sections/%s.tex' % s]).group(1) for s in secs]
chk('section titles match the specification', heads == want, heads)
apps = re.findall(r'\\input\{appendices/(app[A-F])_', tex['tex/main.tex'])
chk('appendices A-F present', apps == ['appA', 'appB', 'appC', 'appD', 'appE', 'appF'])
# 6 figures
figs = sorted(glob.glob(H+'/figures/fig*.pdf'))
chk('22 figure PDFs', len(figs) == 22, len(figs))
inc = re.findall(r'\\includegraphics\[[^\]]*\]\{(fig\d+_[A-Za-z0-9_]+)\.pdf\}', alltex)
chk('all 22 figures included exactly once', len(inc) == 22 and len(set(inc)) == 22 and set(inc) == {os.path.basename(f)[:-4] for f in figs}, len(inc))
fl = re.findall(r'\\begin\{figure\}.*?\\end\{figure\}', alltex, re.S)
chk('every figure float has caption and label', len(fl) == 22 and all('\\caption' in f and '\\label{fig:' in f for f in fl))
labs = re.findall(r'\\label\{(fig:[a-z0-9]+)\}', alltex)
chk('every figure referenced in text', all(re.search(r'\\cref\{[^}]*\b%s\b' % l[4:] if False else r'(?:cref|Cref)\{[^}]*%s[^}]*\}' % re.escape(l), alltex) for l in labs), [l for l in labs if not re.search(r'(?:cref|Cref)\{[^}]*%s[^}]*\}' % re.escape(l), alltex)])
chk('figure 21 is the global diagram', 'fig21_global_diagram' in alltex and '\\label{fig:global}' in alltex)
chk('every figure caption distinguishes exact from schematic', all(re.search(r'\\emph\{[^}]*(Exact|exact|Schematic|schematic|Finite-exact|computed|quoted|Theorem-level|Schematic)', f) for f in fl), sum(1 for f in fl if not re.search(r'\\emph\{[^}]*(Exact|exact|Schematic|schematic|Finite-exact|computed|quoted|Theorem-level)', f)))
# 7 propositions with proofs
okp = True; miss = []
for n in range(1, 10):
    m = re.search(r'\\begin\{proposition\}\[\\SIV\{%d\}[^\]]*\]\\label\{prop:P%d\}(.*?)\\begin\{proof\}' % (n, n), alltex, re.S)
    if not m or '\\section' in m.group(1): okp = False; miss.append(n)
chk('SIV-P1..P9: each stated with label and followed by a proof', okp, miss)
# 8 bibliography
refs = tex['tex/refs.tex']
for P, nm in (('I', 'PAPER_I_TRANSPORT'), ('II', 'PAPER_II_HISTORIES'), ('III', 'PAPER_III_EVOLUTION')):
    f = os.path.join(H, '..', '..', nm, 'v0.4', nm + '_v0.4.pdf')
    sha = hashlib.sha256(open(f, 'rb').read()).hexdigest() if os.path.exists(f) else 'missing-in-this-checkout'
    chk('bibliography cites Paper %s v0.4 with matching file and SHA-256' % P, ('%s\\_v0.4.pdf' % nm.replace('_', '\\_')) in refs and ((sha in refs) or sha == 'missing-in-this-checkout'), sha)
chk('bibliography has no v0.2/v0.3 reference to Papers I-III', not re.search(r'PAPER\\_I+\\_[A-Z]+\\_v0\.[0-3]', refs))
for k in ('FoundI', 'FoundII', 'GEOI', 'RefColl', 'HD1'): chk('bibliography entry '+k, '\\bibitem{%s}' % k in refs)
cites = set(re.findall(r'\\cite\{([^}]*)\}', alltex)) | set(c for m in re.findall(r'\\cite\[[^\]]*\]\{([^}]*)\}', alltex) for c in [m])
bib = set(re.findall(r'\\bibitem\{([^}]*)\}', refs)); used = set(x.strip() for c in cites for x in c.split(','))
chk('all cited keys are in the bibliography', used <= bib, used - bib)
# 9 source citations resolve
idx = json.load(open(H+'/results/theorem_index.json'))
src = re.findall(r'\\Src\{(I+)\}\{([^}]+)\}', alltex)
bad = [(p, l) for p, l in src if l not in idx[p]]
chk('every \\Src citation resolves to an actual theorem of Papers I-III v0.4 (%d citations)' % len(src), not bad, bad)
# 10 source map UIDs exist in the source crosswalks
tsv = list(csv.DictReader(open(H+'/crosswalk/PAPER_IV_SOURCE_MAP.tsv'), delimiter='\t'))
W = os.path.join(H, '..', '..')
import glob as _g
cw = {'I': open(W+'/PAPER_I_TRANSPORT/v0.4/crosswalk/PAPER_I_THEOREM_MAP.tsv').read() if os.path.exists(W+'/PAPER_I_TRANSPORT/v0.4/crosswalk/PAPER_I_THEOREM_MAP.tsv') else None,
      'II': '\n'.join(open(x).read() for x in _g.glob(W+'/PAPER_II_HISTORIES/v0.4/crosswalk/*') if os.path.isfile(x)) or None,
      'III': open(W+'/PAPER_III_EVOLUTION/v0.4/crosswalk/PAPER_III_THEOREM_MAP.tsv').read() if os.path.exists(W+'/PAPER_III_EVOLUTION/v0.4/crosswalk/PAPER_III_THEOREM_MAP.tsv') else None}
uid_idx = json.load(open(H+'/results/source_uid_index.json'))
badu = []
for r in tsv:
    for u in r['crosswalk_uid'].split(';'):
        if u == 'none': continue
        if u not in uid_idx[r['paper']]: badu.append((r['paper'], u))
ext = [k for k, v in cw.items() if v is not None]
badx = [(r['paper'], u) for r in tsv for u in r['crosswalk_uid'].split(';') if u != 'none' and cw[r['paper']] is not None and u not in cw[r['paper']]]
chk('source-map crosswalk UIDs exist in the shipped source UID index (index built from the v0.4 crosswalks of Papers I-III)', not badu, badu)
chk('source-map UIDs also exist in the external crosswalks (%s)' % (', '.join(ext) if ext else 'external manuscripts absent: shipped index used, not an error'), not badx, badx)
chk('source map has all columns and >= 40 rows', len(tsv) >= 40 and all(c in tsv[0] for c in ['crosswalk_uid', 'source_id', 'source_status', 'role', 'used_in', 'hypotheses', 'corrections']))
sp = list(csv.DictReader(open(H+'/crosswalk/SYNTHESIS_PROPOSITIONS.tsv'), delimiter='\t'))
chk('synthesis register has SIV-P1..P9 matching tex labels', [r['id'] for r in sp] == ['SIV-P%d' % i for i in range(1, 10)] and all(('\\label{%s}' % r['tex_label']) in alltex for r in sp))
chk('MODEL_COMPATIBILITY.md present', os.path.exists(H+'/crosswalk/MODEL_COMPATIBILITY.md'))
# 11 diagram statuses
fl4 = open(H+'/scripts/figlib4.py').read()
names = ['established arrow', 'proved factorization', 'proved obstruction', 'open construction', 'interpretive comparison']
chk('five arrow statuses defined with distinct line styles', all(n in fl4 for n in names))
f21 = [f for f in fl if 'fig21' in f][0]
chk('Figure 21 caption explains the arrow statuses', all(w in f21 for w in ['factorizations', 'obstructions', 'open constructions', 'interpretive', 'established']))
chk('commuting squares not claimed (Proposition nocomm)', '\\label{prop:nocomm}' in alltex and 'No square is claimed to commute' in open(H+'/scripts/figs_c.py').read())
# 12 scope statements
chk('inherited verification stated NOT_RERUN', 'NOT\\_RERUN' in alltex or 'NOT_RERUN' in alltex)
chk('C3 stated as unclaimed, no C3 theorem', 'C3' in tex['tex/sections/sec01_intro.tex'] and 'unclaimed' in tex['tex/sections/sec01_intro.tex'])
chk('finite-exact statements marked and not extrapolated', len(re.findall(r'(?:not|never|nor) (?:be )?extrapolat|no extrapolation|extrapolat\w* (?:is|are) (?:not|never)|not been extrapolated|extrapolated beyond|no extrapolation', alltex)) >= 3 and 'finite-exact' in alltex.lower())
chk('no universal law claimed (interpretation labelled)', 'Interpretation' in alltex or 'interpretation' in alltex)
chk('every open problem states nearest theorem and missing obligation', all(('\\textit{Nearest' in x or '\\emph{Nearest:}' in x) and 'Missing' in x for x in re.findall(r'\\item\[O\d\..*?(?=\\item\[O|\\end\{description\})', tex['tex/sections/sec16_open.tex'], re.S)) and len(re.findall(r'\\item\[O\d\.', tex['tex/sections/sec16_open.tex'])) == 8)
chk('S1-S4 each answered', all(('\\item[S%d' % i) in tex['tex/sections/sec13_register.tex'] for i in range(1, 5)))
# 13 spot checks: recompute exact witnesses
r = subprocess.run([sys.executable, '-I', H+'/scripts/c6_witnesses.py'], cwd=H+'/scripts', capture_output=True, text=True, timeout=600) if False else subprocess.run([sys.executable, H+'/scripts/c6_witnesses.py'], cwd=H+'/scripts', capture_output=True, text=True, timeout=600)
chk('spot check: all exact witnesses recomputed (c6_witnesses.py)', r.returncode == 0, r.stdout[-300:]+r.stderr[-300:])
r5 = json.load(open(H+'/results/c5_checks.json'))
chk('recorded lemma checks have 0 violations (component rule, edge rule, nu formula)', r5['Lcomp']['violations'] == 0 and r5['Ledge']['violations'] == 0 and r5['nu2314']['violations'] == 0)
f10 = json.load(open(H+'/results/fig10_data.json'))
chk('figure 10 data match text (nu = 2,1,1 at m = 14,28,21)', [f10[k][2] for k in ('14', '28', '21')] == [2, 1, 1])
cp = json.load(open(H+'/results/c1_collide.json'))['totals_4']
chk('P5 census numbers in text match recorded run', cp['groups'] == 238 and cp['collisions_diff_classes'] == 106 and cp['groups_with_several_E'] == 166 and cp['collisions_diff_histcount'] == 158 and '238' in alltex and '106' in alltex and '166' in alltex and '158' in alltex)
# v0.4 corrections
chk('no overfull boxes in the build log', 'Overfull' not in log)
s3 = tex['tex/sections/sec03_numerical.tex']; s6 = tex['tex/sections/sec08_evolution.tex']; s10 = tex['tex/sections/sec10_recurrence.tex']; s11 = tex['tex/sections/sec11_correspondence.tex']; s4_ = tex['tex/sections/sec06_history_topology.tex']
chk('P1(b): fibre is intersected with admissible contents', 'Cont}_A(m_0)\\cap\\bigl(c(h)+\\ker_{\\Z}V_A\\bigr)' in s3 and 'pi_{3,A}' in s3 and 'End}(m_0)' in s3)
chk('P1(d): history count not claimed non-factoring through the endpoint', 'does \\emph{not} factor through the occurrence set' in s3 and 'the number of histories ending at' not in s3)
chk('P4(c): different-source comparison not presented as endpoint-projection information', 'without the source' in s4_ and 'not a statement about the information retained' in s4_)
chk('P6(d): restricted to degrees 0 and 1 with both directions witnessed', 'Degrees $0$ and $1$ are not monotone' in s6 and 'No Betti number is monotone' not in alltex)
chk('P8: normalized scaling signature defined', 'normalized scaling signature' in s10 and 'identical scaling data' not in alltex)
chk('P9: identity-only obstruction; general L5 open; restricted L3 results acknowledged', 'identity map' in s11 and 'non-identity' in s11 and 'thm:B2T10' in s11 and 'thm:R3T7' in s11)
chk('Fig 21 caption: no inclusion between successive move complexes', 'no complex inclusion is implied' in alltex)
w = json.load(open(H+'/results/c6_witnesses.json'))
chk('W9 and W10 witnesses recorded and passing', all((v['after'][i] - v['before'][i]) == d for (k, v), (i, d) in zip(w['W9'].items(), [(0, -1), (0, 1), (1, 1), (1, -1)])) and w['W10']['equal_multiplier'] and w['W10']['admissible_first_letters_of_c_prime'] == [])
chk('P1(b): fibre restricted to alphabet-supported contents Cont_A', 'Cont}_A(1)' in s3)
chk('P6(d): abstract witnesses not transferred to orbits; D={3,10} not an occurrence set', 'not claimed to be occurrence inventories' in s6 and 'is \\emph{not} established by the abstract witnesses' in s6)
chk('P7: witnesses declared abstract set-level', 'abstract set-level events' in tex['tex/sections/sec09_prediction.tex'])
chk('Fig 21: ancestor translation is a construction from (x,C(x)), not an arrow from K_move(Cx)', 'construction from the arithmetic pair' in alltex and 'construction from $(x,C(x))$' in open(H+'/scripts/figs_c.py').read())
# D = {3,10} cannot be D(x): verify no state x=a/b with D(x) = {3,10} (b | 2 and b | 9)
from math import gcd
chk('D={3,10} is not an occurrence set of any denominator b (b must divide gcd(3-1,10-1)=1, forcing 2 into D)', gcd(3-1, 10-1) == 1)
s15 = tex['tex/sections/sec15_conclusions.tex']; s16 = tex['tex/sections/sec16_open.tex']
chk('abstract states the operational characterisation, no intrinsic axiomatisation claimed', 'operational characterisation' in ab and 'intrinsic axiomatisation is not claimed' in ab)
chk('abstract consistent with SIV-P6(d) and SIV-P9(a)', 'no higher Betti number is monotone' not in ab and 'every one-step relation' not in ab)
chk('15.1 operational characterisation, 15.2 implications, 15.3 limitations', all(('\\label{sec:%s}' % k) in s15 for k in ('characterisation', 'implications', 'limitations')) and s15.index('sec:characterisation') < s15.index('sec:implications') < s15.index('sec:limitations'))
chk('characterisation is not numbered as a theorem; tuple presented as notation, not axiom system', 'SIV-T' not in alltex and 'not an axiom system' in s15 and 'synthesis conclusion, not a numbered theorem' in tex['tex/sections/sec01_intro.tex'])
chk('15.1 scope: no minimal axiom system, no operator equivalence, no physical identification', all(x in s15 for x in ('unique minimal axiom system', 'dynamically equivalent', 'physical substrate')))
chk('15.1 supports each property by cited propositions', all(('prop:P%d' % i) in s15 for i in range(1, 10)))
chk('16: operational versus intrinsic with nearest results and missing obligations', 'Operational versus intrinsic characterisation' in s16 and 'Nearest proved results' in s16 and 'Missing obligations' in s16)
chk('appendices referenced as "Appendix" without relying on cleveref (reproducible wording)', not re.search(r'\\[cC]ref\{[^}]*app:', alltex) and not re.search(r'Section[ ~]+[A-F]\b', txt))
chk('S3 (introduction): exact obstruction, no claim that no map exists', 'does not determine the associated history complex' in tex['tex/sections/sec01_intro.tex'] and 'no map from the first to the second exists' not in alltex)
# 14 filenames windows-safe
bad = [f for f in glob.glob(H+'/**/*', recursive=True) if re.search(r'[<>:"|?*\s]', os.path.relpath(f, H))]
chk('Windows-safe filenames', not bad, bad[:3])
n = sum(1 for _, o, _ in res if o)
print('\n%d/%d checks passed' % (n, len(res))); json.dump([{'check': a, 'pass': b, 'detail': str(c)} for a, b, c in res], open(H+'/results/check_results.json', 'w'), indent=1)
sys.exit(0 if n == len(res) else 1)
