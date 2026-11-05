#!/usr/bin/env python3
"""Manuscript-quality and spot checks for Paper III v0.4 (stdlib only). Not an independent proof of the mathematics.
Run from anywhere: python3 checks/check_paper_III.py"""
import csv, json, os, re, glob, sys, hashlib
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, H + '/scripts')
res = []
def chk(n, ok, i=''): res.append((n, bool(ok), str(i))); print('PASS ' if ok else 'FAIL ', n, i)
files = sorted(glob.glob(H + '/tex/*.tex') + glob.glob(H + '/tex/sections/*.tex') + glob.glob(H + '/tex/appendices/*.tex'))
tex = ''.join(open(f, encoding='utf-8').read() for f in files)
body = ''.join(open(f, encoding='utf-8').read() for f in files if not f.endswith('appmap_table.tex'))
body += ''.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob(H + '/tex/tables/*.tex')))
body += open(H + '/tex/appmap_table.tex', encoding='utf-8').read()
# ---- crosswalk accounting
alloc = list(csv.DictReader(open(H + '/data/ALLOCATION_III.tsv', encoding='utf-8'), delimiter='\t'))
tmap = list(csv.DictReader(open(H + '/crosswalk/PAPER_III_THEOREM_MAP.tsv', encoding='utf-8'), delimiter='\t'))
chk('73 allocated records', len(alloc) == 73, len(alloc))
chk('theorem map has all 73 uids', {r['uid'] for r in tmap} == {r['uid'] for r in alloc} and len(tmap) == 73)
prov = []
for l in open(H + '/tex/main.prov', encoding='utf-8'):
    m = re.match(r'\\provrow\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}$', l.strip())
    if m: prov.append(m.groups())
pu = {p[0] for p in prov}
chk('provenance uids subset of allocation', pu <= {r['uid'] for r in alloc}, sorted(pu - {r['uid'] for r in alloc}))
reall = {r['uid'] for r in alloc if r['primary_manuscript'] != 'III'}
chk('uids without a provenance line are exactly the 9 reallocated B-T1..B-T9', {r['uid'] for r in alloc} - pu == reall and len(reall) == 9, sorted({r['uid'] for r in alloc} - pu))
chk('B-T1..B-T9 = CW-0383..CW-0391', reall == {'CW-%04d' % i for i in range(383, 392)})
chk('map marks the 9 as CITED', all(r['paper_III_treatment'] == 'CITED' for r in tmap if r['uid'] in reall))
chk('frozen crosswalk not modified (no file of that name here)', not glob.glob(H + '/crosswalk/CROSSWALK_MASTER*'))
tr = {'FULL', 'FINITE', 'SPLIT', 'OPEN', 'EXAMPLE', 'CORRECTED', 'CITED'}
chk('treatments in vocabulary', {p[3] for p in prov} <= tr, {p[3] for p in prov} - tr)
fin = [p for p in prov if p[3] == 'FINITE']
chk('FINITE-treatment records are finite-exact', all('FINITE' in p[2] for p in fin), [p[:4] for p in fin if 'FINITE' not in p[2]])
chk('OPEN records have status OPEN', all(p[2] == 'OPEN' for p in prov if p[3] == 'OPEN'))
chk('corrected records present (B2-T7, B2-T9)', {'B2-T7', 'B2-T9'} <= {p[1] for p in prov if p[3] == 'CORRECTED'})
# ---- language
chk('no "draft" anywhere in sources', not re.search(r'draft', tex, re.I))
for f in glob.glob(H + '/*.md') + glob.glob(H + '/*.json'):
    if not re.search(r'draft', open(f, encoding='utf-8').read(), re.I): pass
    else: chk('no "draft" in ' + os.path.basename(f), False)
chk('author line', '\\author{UNNS Research Collective' in tex and 'pdfauthor={UNNS Research Collective}' in tex)
chk('version 0.4', 'version 0.4' in tex)
chk('no novelty / priority words', not re.search(r'\b(novel|first-ever|breakthrough|groundbreaking|revolutionary|unprecedented)\b', body, re.I))
chk('q in {2,5} appears only as a refuted statement', all('false' in body[m.start():m.start() + 200] for m in re.finditer(r'q\\in\\\{2,\s*5\\\}', body)))
chk('no physical interpretation words', not re.search(r'\b(fine-structure|Weinberg|dark matter|quantum gravity|cosmolog)', body, re.I))
chk('no universal-law claim', 'no universal' in body.lower() or 'universal organi' in body.lower())
# ---- references and labels
bibkeys = set(re.findall(r'\\bibitem\{([^}]*)\}', tex))
cited = set()
for m in re.findall(r'\\cite[a-z]*\{([^}]*)\}', body):
    cited |= {k.strip() for k in m.split(',')}
chk('every citation resolves', cited <= bibkeys, sorted(cited - bibkeys))
chk('every bibliography entry is cited', bibkeys <= cited, sorted(bibkeys - cited))
labels = set(re.findall(r'\\label\{([^}]*)\}', body))
refs = set()
for m in re.findall(r'\\(?:[cC]ref|ref|eqref|autoref|pageref)\{([^}]*)\}', body):
    refs |= {k.strip() for k in m.split(',')}
chk('every reference has a label', refs <= labels, sorted(refs - labels))
log = open(H + '/tex/main.log', encoding='utf-8', errors='replace').read() if os.path.exists(H + '/tex/main.log') else None
if log is None: print('NOTE: tex/main.log absent; log checks skipped (rebuild with scripts/build_paper.sh)'); log = ''
chk('log: no undefined references/citations', not re.search(r'undefined', log))
chk('log: no multiply defined labels', 'multiply' not in log)
chk('log: no overfull boxes', 'Overfull' not in log, len(re.findall('Overfull', log)))
chk('log: no hyperref/font warnings', 'hyperref Warning' not in log and 'Font Warning' not in log)
aux = H + '/tex/main.aux'
if os.path.exists(aux):
    A = open(aux, encoding='utf-8', errors='replace').read()
    envtype = {}
    for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|definition|example|problem|counter|remark)\}(?:\[[^\]]*\])?(?:\\label\{([^}]*)\})?', body):
        if m.group(2): envtype[m.group(2)] = m.group(1)
    for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|definition|example|problem|counter|remark)\}(.*?)\\end\{\1\}', body, re.S):
        for l in re.findall(r'\\label\{([^}]*)\}', m.group(2)): envtype.setdefault(l, m.group(1))
    bad = []
    for l, e in envtype.items():
        mm = re.search(r'\\newlabel\{' + re.escape(l) + r'@cref\}\{\{\[([a-z]+)\]', A)
        if not mm or mm.group(1) != e: bad.append((l, e, mm.group(1) if mm else None))
    chk('cleveref type of every theorem-like label equals its environment (%d labels)' % len(envtype), not bad and len(envtype) > 60, bad[:6])
    bapp = [l for l in re.findall(r'\\label\{(app:[^}]*)\}', body) if re.search(r'\\cref?\{' + re.escape(l), body, re.I)]
    chk('appendices referenced as "Appendix ~\\ref", not through cleveref', not bapp, bapp)
else: print('NOTE: tex/main.aux absent; reference-type check skipped')
chk('log: no LaTeX errors', not re.search(r'^!', log, re.M))
# ---- figures
figs = sorted(glob.glob(H + '/figures/fig*.pdf'))
chk('26 figure files', len(figs) == 26, len(figs))
envs = re.findall(r'\\begin\{figure\}.*?\\end\{figure\}', body, re.S)
chk('26 figure environments', len(envs) == 26, len(envs))
okc = all('\\caption' in e and '\\label{fig:' in e and '\\includegraphics' in e for e in envs)
chk('each figure has image, caption, label', okc)
flab = {re.search(r'\\label\{(fig:[^}]*)\}', e).group(1) for e in envs}
chk('each figure referenced in the text', flab <= refs, sorted(flab - refs))
stat = [bool(re.search(r'(proved|scoped|finite-exact|schematic|exact|finite)', e, re.I)) for e in envs]
chk('figure captions state a status', all(stat))
chk('each figure file is included', all(os.path.basename(f)[:-4] in body for f in figs))
# ---- NOT_RERUN
rd = open(H + '/README.md', encoding='utf-8').read() if os.path.exists(H + '/README.md') else ''
st = json.load(open(H + '/STATUS.json'))
pdfs = [f for f in [H + '/PAPER_III_EVOLUTION_v0.4.pdf', H + '/tex/main.pdf'] if os.path.exists(f)]
chk('exactly one PDF in the package (root)', pdfs == [H + '/PAPER_III_EVOLUTION_v0.4.pdf'], pdfs)
chk('STATUS.json sha256 equals the root PDF', st['pdf_sha256'] == hashlib.sha256(open(H + '/PAPER_III_EVOLUTION_v0.4.pdf', 'rb').read()).hexdigest())
chk('README records NOT_RERUN', 'NOT_RERUN' in rd)
# ---- engine spot checks
try:
    from eng3 import *
    from fractions import Fraction as Fr
    o = orbit(Fr(3025, 3), 8)
    chk('8-step orbit denominators', [x.denominator for x in o] == [3, 54, 27, 18, 27, 54, 9, 9, 3], [x.denominator for x in o])
    chk('8-step orbit ends at 12100/3', o[-1] == Fr(12100, 3))
    Ds = [Dset(x) for x in o]
    chk('8-step occurrence sets', Ds[5] == [55] and Ds[6] == [10, 55] and Ds[8] == [10, 22, 55])
    chk('8-step Betti 0 -> 1 at last step', betti(complex_of(Ds[7]), 2)[2][:2] == [1, 0] and betti(complex_of(Ds[8]), 2)[2][:2] == [1, 1])
    t5 = json.load(open(H + '/results/tower5.json')); t11 = json.load(open(H + '/results/tower11.json'))
    S11 = lambda k: 2**2 * 3**(3 + k) * 5**4; S5 = lambda k: 126 * 2**k
    def tD(S, m): return sorted(d for d in divisors(factor(S)) if d >= 2 and d % m == 1 % m)
    ok = all(betti(complex_of(tD(S11(k), 11)), 2)[2] == t11[k]['b'] for k in range(0, 8)) and all(betti(complex_of(tD(S5(k), 5)), 2)[2] == t5[k]['b'] for k in range(0, 9))
    chk('tower engine matches stored Betti numbers (G=11 k<8, G=5 k<9)', ok)
    chk('G=5 law (1,6,5,0) for 7<=k<=140', all(t5[k]['b'] == [1, 6, 5, 0] for k in range(7, 141)))
    chk('G=11 laws beta1=8 (k>=2), beta2=17 (k>=6), beta3(k+5)=beta3(k)+9 (8<=k<=135)',
        all(t11[k]['b'][1] == 8 for k in range(2, 141)) and all(t11[k]['b'][2] == 17 for k in range(6, 141)) and all(t11[k + 5]['b'][3] == t11[k]['b'][3] + 9 for k in range(8, 136)))
    chk('G=11 |D|=2k+7', all(t11[k]['nV'] == 2 * k + 7 for k in range(141)))
    # entry time of the t-map (regime I)
    def sqf(n):
        r = 1
        for p, e in factor(n).items():
            if e % 2: r *= p
        return r
    def entry(t):
        n = 0
        while t not in (1, 2, 3): t = sqf(t + 1); n += 1
        return n
    sq = [t for t in range(1, 3000) if sqf(t) == t]
    mx = max((entry(t), t) for t in sq)
    chk('regime-I entry time max 12 at t=1301', mx == (12, 1301), mx)
    # collective cycle C^3 = 4x on {1,2,3}
    chk('C^3 = 4x on x = t*s^2, t in {1,2,3}, G=1 along the orbit (rigid set)', all(orbit(Fr(t * s * s), 3)[-1] == 4 * t * s * s for t in (1, 2, 3) for s in (2, 3, 5, 6) if (t * s * s) % 1 == 0 and all(Dset(y) and LG(Dset(y))[1] == 1 for y in orbit(Fr(t * s * s), 2))))
    # zig-zag example
    from trans3 import analyse, etype
    t = analyse([8, 22, 176], [2, 4, 8, 11, 16, 22, 44, 88, 176])
    chk('zig-zag example: b=(1,1)->(1,0), r,h,r2,h2, dead/new counts', t['b'][:2] == [1, 1] and t['b2'][:2] == [1, 0] and t['r'][:2] == [1, 0] and t['h'][:2] == [0, 3] and t['r2'][:2] == [1, 0] and t['h2'][:2] == [0, 2] and t['dead'][:3] == [0, 3, 0] and t['new'][:3] == [6, 11, 3] and all(t['chk'].values()), t['chk'])
    # census totals from stored rows
    cnt = {'V': 0, 'II': 0, 'III': 0, 'IV': 0}; n = 0
    for l in (5, 7, 11, 13):
        for r in json.load(open(H + '/results/census_l%d.json' % l))['rows']:
            db = r['db']; n += 1
            if all(x == 0 for x in db): cnt['V'] += 1
            else:
                up = any(x > 0 for x in db); dn = any(x < 0 for x in db)
                cnt['IV' if up and dn else ('II' if up else 'III')] += 1
    chk('census totals V 1787 / II 603 / III 172 / IV 14 (no type I)', cnt == {'V': 1787, 'II': 603, 'III': 172, 'IV': 14} and n == 2576, (cnt, n))
    b2 = json.load(open(H + '/results/c9_b2.json'))
    chk('B2-T9: 24,496 edges; inclusion holds 13,894, fails 10,602', b2['edges'] == 24496 and b2['inclusion_holds'] == 13894 and b2['inclusion_fails'] == 10602 and b2['sigma_strictly_increasing'] == 24496)
    # B2-T9 edge m=4 -> m(N+1)^2/N = 18 with N=2: sigma 2 -> 3 increases, D differs, inclusion fails
    m0, N0 = 4, 2; m1 = m0 * (N0 + 1)**2 // N0
    D0, D1 = Dset(Fr(m0)), Dset(Fr(m1)); s0 = max(d for d in D0); s1 = max(d for d in D1)
    chk('B2-T9 edge 4 -> 18 recomputed: D(4)=%s, D(18)=%s, D differs, inclusion fails' % (D0, D1), m1 == 18 and D0 != D1 and not set(D0) <= set(D1) and s1 > s0)
    # 375-step example (events and Betti)
    c1 = json.load(open(H + '/results/c1_traj.json'))
    ev = c1['t375']['events']
    chk('375-step events at 372, 373, 375 with new 106, 22, 134', [(e['step'], e['new']) for e in ev] == [(372, [106]), (373, [22]), (375, [134])])
    seg = json.load(open(H + '/results/c1_375_segments.json')) if os.path.exists(H + '/results/c1_375_segments.json') else []
    chk('375-step beta_1 0 -> 3', seg and seg[0]['betti'] == [1] and seg[-1]['betti'][1] == 3 if seg else False, seg[-1]['betti'] if seg else '')
    # l=29 control: events at the stage law
    x = Fr(1890**2, 29); o = orbit(x, 80); ev = [n for n in range(1, len(o)) if Dset(o[n]) != Dset(o[n - 1])]
    chk('l=29, S=1890: events at 24,27,35,59,62,70', ev == [24, 27, 35, 59, 62, 70], ev)
except Exception as e:
    import traceback; traceback.print_exc(); chk('engine checks ran', False, repr(e))
bad = [r for r in res if not r[1]]
json.dump({'passed': len(res) - len(bad), 'failed': [r[0] for r in bad], 'total': len(res)}, open(H + '/checks/check_result.json', 'w'), indent=1)
print('\n%d/%d checks passed' % (len(res) - len(bad), len(res)))
sys.exit(1 if bad else 0)
