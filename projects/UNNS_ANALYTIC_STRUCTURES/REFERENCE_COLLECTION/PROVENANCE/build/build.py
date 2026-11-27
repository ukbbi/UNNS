#!/usr/bin/env python3
"""Builds the ASUNNS reference collection v003 from the frozen release files, catalog.txt and openlist.txt.
Statements are copied verbatim from the sources; nothing is retyped. Run from this folder: python3 -B build.py"""
import csv, hashlib, json, re, shutil, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
def load(name):
    exec((HERE / name).read_text(encoding='utf-8'), globals())
load('labels.py'); load('build_data.py')
COL = HERE.parents[1]; W = COL.parent; INV = W / '02_INVESTIGATIONS'
REL = {f'I{i}': f'ANS_I/v{i:03d}' for i in range(1, 16)}
REL.update({'II1': 'ANS_II/v001', 'II2': 'ANS_II/v002', 'N1': 'ANS_II/ND/v001', 'N2': 'ANS_II/ND/v002', 'N3': 'ANS_II/ND/v003'})
def relname(a):
    if a == 'B': return 'Initial analytic baseline'
    return REL[a].replace('ANS_II/ND/', 'ANS-II-ND ').replace('ANS_II/', 'ANS-II ').replace('ANS_I/', 'ANS-I ')
def srcpath(a): return W / '01_THEORY/BASELINE.md' if a == 'B' else INV / REL[a] / 'PROOFS.md'
def copyname(a): return 'sources/BASELINE.md' if a == 'B' else f'sources/{REL[a]}/PROOFS.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def full(i): return i if i.startswith(('ANS', 'AS-')) else ('ANS-' + i)
def put(rel, text):
    p = COL / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text.rstrip() + '\n', encoding='utf-8', newline='\n')
def datalines(name):
    return [l for l in (HERE / name).read_text(encoding='utf-8').split('\n') if l.strip() and not l.startswith('#')]

E = []
for l in datalines('catalog.txt'):
    i, reg_, status, rev, src, deps, cls, title = l.split('|')
    a, rs = src.split(':'); L = srcpath(a).read_text(encoding='utf-8').split('\n')
    parts, ranges = [], []
    for r in rs.split(','):
        s, e = map(int, r.split('-')); assert 1 <= s <= e <= len(L), (i, r)
        t = '\n'.join(x for x in L[s-1:e] if not x.startswith('#')).strip('\n'); assert t.strip(), (i, r)
        parts.append(t); ranges.append([s, e])
    scope = ('Integral-image grammars (see statement)' if i in ('T01', 'T02', 'T08', 'T11', 'T14', 'T03') else
             'Extended grammar with torsion multipliers' if i.startswith('ANS2') else 'Selected nesting grammar')
    prio = ('Classical content' if i.startswith('AS-') else 'Underlying structure classical; otherwise unreviewed' if i == 'T47'
            else 'Classical shifted divisor sum; no novelty claimed' if i == 'T46c' else 'Unreviewed')
    E.append(dict(id=full(i), short=i, region=reg_, status=status, review_code=rev, review=REVIEW[rev], qualification=QUAL.get(i, ''),
        title=title, source=copyname(a), release=relname(a), lines=ranges, statement=relabel('\n\n'.join(parts)),
        review_record=('UNNS Research Collective review, 27 November 2026 (PROVENANCE/REVIEWS)' if i in V003_IDS else 'Foundational audit, 27 November 2026 (PROVENANCE/REVIEWS)' if i in AUDIT_IDS else
            'Release review records' if rev in ('V', 'VQ', 'A') else 'None'),
        acceptance=('Release not frozen: Windows acceptance pending' if a == 'I1' else 'Release has no archive of its own' if a == 'I4' else
            'Baseline note' if a == 'B' else 'Archived release') + ('; certificate not independently rerun' if status == 'CERTIFIED' else
            '; floating-point computation' if status == 'COMPUTED' else ''),
        depends_on=[full(d) for d in deps.split()], classical_inputs=cls.strip(), note=NOTES.get(i, ''), scope=scope, literature_priority=prio))
ids = [e['id'] for e in E]; assert len(ids) == len(set(ids)); byid = {e['id']: e for e in E}
for e in E:
    for d in e['depends_on']: assert d in byid, (e['id'], d)

tables = ['ANS_I/v%03d' % i for i in range(1, 16)] + ['ANS_II/v001', 'ANS_II/v002', 'ANS_II/ND/v001', 'ANS_II/ND/v002', 'ANS_II/ND/v003']
rows = {}
for t in tables:
    for l in (INV / t / 'THEOREMS.md').read_text(encoding='utf-8').split('\n'):
        if l.startswith('|'):
            c = [x.strip() for x in l.strip().strip('|').split(' | ')]
            if len(c) > 1 and re.match(r'(?:ANS2?N?-[A-Z]?\d+[a-z]?(?:-i)?|ANS-C\d)$', c[0]): rows[c[0]] = (t, c[1])
reg = {r['id']: r for r in csv.DictReader((W / '01_THEORY/REGISTER.csv').open(encoding='utf-8', newline=''))}
for e in E:
    r = rows.get(e['id']); e['release_summary'] = r[1] if r else ''; e['release_summary_from'] = r[0] if r else ''
    g = reg.get(e['id']); e['register'] = {k: g[k] for k in ('evidence', 'review', 'crosswalk')} if g else None

used = collections.defaultdict(list)
for e in E:
    for d in e['depends_on']: used[d].append(e['id'])
def closure(i, nxt, acc):
    for d in nxt(i):
        if d not in acc: acc.add(d); closure(d, nxt, acc)
    return acc
up = {i: closure(i, lambda x: byid[x]['depends_on'], set()) for i in ids}
down = {i: closure(i, lambda x: used.get(x, []), set()) for i in ids}
assert all(i not in up[i] for i in ids), 'cycle'
reviewed = [i for i in ids if byid[i]['review_code'] in ('V', 'VQ') and byid[i]['status'].startswith(('PROVED', 'CERTIFIED'))]
exposed = {i: sorted(d for d in up[i] if byid[d]['review_code'] not in ('V', 'VQ')) for i in reviewed}
exposed = {i: v for i, v in exposed.items() if v}
for e in E:
    e['used_by'] = sorted(used.get(e['id'], [])); e['unreviewed_ancestors'] = exposed.get(e['id'], [])
    e['related'] = [f'{full(a)} {k} {full(b)}' for a, b, k in RELATIONS if e['short'] in (a, b)]
def cat(e):
    if e['status'] in ('COMPUTED', 'CERTIFIED'): return e['status'].lower()
    if e['status'].startswith('CONJECTURE') or e['id'] == 'ANS-T46b': return 'conjecture'
    return {'V': 'reviewed', 'VQ': 'reviewed', 'A': 'reciprocal', 'P': 'unreviewed', 'B': 'baseline'}[e['review_code']]
count = collections.Counter(cat(e) for e in E)
opens = [dict(zip(('id', 'region', 'text'), l.split('|'))) for l in datalines('openlist.txt')]
load('build_out.py')
