#!/usr/bin/env python3
"""Generate the crosswalk, dependency, audit and check tables of Volume II from the registry
(registry.json), the manuscript sources (tex/*.tex) and the verification output.
Usage: python3 gen_tables.py [main.aux]   (the .aux file, if given, resolves numbers in the TSV files)"""
import json, re, sys, glob, csv, os
reg = json.load(open('registry.json'))['records']
V = [r for r in reg if str(r['vol']).startswith('II')]
ids = [r['id'] for r in V]
assert len(V) == 68
CH = {'ch1': 1, 'ch2': 2, 'ch3': 3, 'ch4': 4, 'ch5': 5, 'ch6': 6, 'ch7': 7, 'appF': 'F'}
WORD = {'theorem': 'Thm', 'proposition': 'Prop.', 'lemma': 'Lem.', 'corollary': 'Cor.', 'definition': 'Def.',
        'example': 'Ex.', 'remark': 'Rem.', 'problem': 'Prob.'}
loc = {}
for fn, c in CH.items():
    s = open(f'tex/{fn}.tex').read()
    for m in re.finditer(r'\\begin\{(theorem|proposition|lemma|corollary|definition|example|remark|problem)\}[^\n]*', s):
        line = m.group(0)
        env = m.group(1)
        found = re.findall(r'\\rec\{([^}]+)\}', line)
        for g in re.findall(r'\\record\{([^}]+)\}', line):
            found += [x.strip() for x in g.split(',')]
        for i in found:
            loc[i] = (env, c)
missing = [i for i in ids if i not in loc]
assert not missing, missing

def tex_escape(t):
    t = t.replace('\\', '\\textbackslash{}')
    for a, b in (('&', '\\&'), ('%', '\\%'), ('#', '\\#'), ('_', '\\_'), ('$', '\\$')):
        t = t.replace(a, b)
    t = t.replace('^', '\\^{}').replace('~', '\\~{}')
    return t.replace('>=', '$\\geq$').replace('<=', '$\\leq$')

# completeness classes
FULL, EXACT, DEF, SCOPE, CORR, OPEN = 'Full proof', 'Exact computation', 'Definition', 'Scope statement', 'Registered correction', 'Open problem'
cls = {}
rem = {}
for r in V:
    i = r['id']; k = r['kind']
    if k == 'Definition': cls[i] = DEF
    elif k in ('Erratum',): cls[i] = CORR
    elif k == 'Open problem': cls[i] = OPEN
    elif k in ('Problem', 'Statement'): cls[i] = SCOPE
    elif k == 'Example': cls[i] = EXACT
    else: cls[i] = FULL
rem.update({
 'F.CDEF': 'the selected collective rule; its consequences are the theorems of the volume',
 'F.T17p': 'scope A0',
 'F.T28': 'exact closed-form orbit, verified by exact iteration',
 'F.T30': 'scope A0',
 'F.T33': 'corrected form; see F.L5',
 'F.T34': 'proved together with F.L2 (Thm~\\ref{thm:G236}); also reproved by F.T45',
 'F.L2': 'proved together with F.T34',
 'F.L5': 'scope of F.T33 stated as Remark~\\ref{rem:L5}',
 'F.L6': 'resolved by F.T39: collapse is false',
 'F.T41': 'status remark; classification of persistent $g$ is open',
 'F.T38a': 'uses Dirichlet\'s theorem; F.T42 avoids it',
 'F.T48': 'universal statement is false; correct statement is F.T51',
 'F.T58': 'scope statements in Rem.~\\ref{rem:T58}',
 'F.T63': 'scope statement in Rem.~\\ref{rem:T63}',
 'F.T66': 'prime $g$, or no prime factor of $g\\le m^2$',
 'F.T68': 'part (a) proved for prime $g$; see F.T73',
 'F.T69': 'sharp; witnesses for $\\kappa\\le11$ (Table~\\ref{tab:kappa})',
 'F.T70': 'clause (c) for prime $g$',
 'F.T71': 'prime $g$, or whenever F.T67 applies',
 'F.T72': 'counts carry events; steps via plateau bound',
 'F.T73': 'scope of certification; effectiveness',
 'F.E71': 'numerical clause only',
 'O12.1': 'near-sharp transients', 'O12.2': 'composite/even certification', 'O12.3': 'composite $g$',
 'O12.4': 'closed form of $m_p$', 'O12.5': 'all $q$', 'O12.6': 'class closure at $q=11$',
 'O10.3': 'realisable triples', 'O10.4': 'composite/even sample',
})

def locstr(i):
    env, c = loc[i]
    return f"{WORD[env]}~\\ref{{th:{i}}}"

def bare(i):
    return i.replace('F.', '') if i.startswith('F.') else i

# crosswalk longtable
out = []
out.append('\\footnotesize\n\\begin{longtable}{@{}p{13mm}p{45mm}p{33mm}p{8mm}p{12mm}p{17mm}@{}}')
hdr = 'ID & Source record title & Source status & Scope & Reg.\\ chap. & Here\\\\\\midrule'
out.append('\\toprule ' + hdr + '\\endfirsthead')
out.append('\\toprule ' + hdr + '\\endhead')
for r in V:
    i = r['id']
    out.append(f"\\texttt{{{bare(i)}}} & {tex_escape(r['title'])} & {tex_escape(r['status'])} & {r['scope']} & {r['vol']} & {locstr(i)} \\\\")
out.append('\\bottomrule\n\\end{longtable}\n\\normalsize')
open('tex/crosswalk.tex', 'w', newline='\n').write('\n'.join(out) + '\n')

# dependencies longtable
out = ['\\footnotesize\n\\begin{longtable}{@{}p{14mm}p{108mm}@{}}']
h2 = 'Record & Depends on (registry dependency list)\\\\\\midrule'
out.append('\\toprule ' + h2 + '\\endfirsthead')
out.append('\\toprule ' + h2 + '\\endhead')
for r in V:
    deps = ', '.join(bare(d) for d in r['deps']) or '\\textemdash'
    out.append(f"\\texttt{{{bare(r['id'])}}} & \\texttt{{{deps}}} \\\\")
out.append('\\bottomrule\n\\end{longtable}\n\\normalsize')
open('tex/deps.tex', 'w', newline='\n').write('\n'.join(out) + '\n')

# checks mapping
chk = json.load(open('checks_volume_ii.json'))['results']
tag_of = {i: [] for i in ids}
exact = {bare(i): i for i in ids}
for c in chk:
    for part in c['tag'].split('/'):
        if part in exact:
            tag_of[exact[part]].append(c['tag']); continue
        m = re.match(r'^(.*?)([a-z])$', part)
        if m and m.group(1) in exact and part not in exact:
            tag_of[exact[m.group(1)]].append(c['tag'])
        else:
            m2 = re.match(r'^(L\d|T\d+[a-z]?)', part)
for i in ids: tag_of[i] = sorted(set(tag_of[i]))
# audit longtable
out = ['\\footnotesize\n\\begin{longtable}{@{}p{14mm}p{17mm}p{27mm}p{58mm}@{}}']
h3 = 'ID & Location & Completeness here & Remark; verification tag\\\\\\midrule'
out.append('\\toprule ' + h3 + '\\endfirsthead')
out.append('\\toprule ' + h3 + '\\endhead')
for r in V:
    i = r['id']
    note = rem.get(i, '')
    tg = ', '.join(tag_of[i])
    if tg: note = (note + '; ' if note else '') + 'check \\texttt{' + tex_escape(tg) + '}'
    out.append(f"\\texttt{{{bare(i)}}} & {locstr(i)} & {cls[i]} & {note} \\\\")
out.append('\\bottomrule\n\\end{longtable}\n\\normalsize')
open('tex/audit.tex', 'w', newline='\n').write('\n'.join(out) + '\n')

# checks table
out = ['\\footnotesize\n\\begin{longtable}{@{}p{13mm}p{100mm}p{11mm}@{}}']
h4 = 'Tag & Statement checked (exact arithmetic) & Result\\\\\\midrule'
out.append('\\toprule ' + h4 + '\\endfirsthead')
out.append('\\toprule ' + h4 + '\\endhead')
for c in chk:
    out.append(f"\\texttt{{{tex_escape(c['tag'])}}} & {tex_escape(c['statement'])} & {'pass' if c['pass'] else 'FAIL'} \\\\")
out.append('\\bottomrule\n\\end{longtable}\n\\normalsize')
open('tex/checks_table.tex', 'w', newline='\n').write('\n'.join(out) + '\n')

# counts for the text
from collections import Counter
cnt = Counter(cls.values())
json.dump({'n': len(V), 'classes': cnt, 'checks_passed': sum(1 for c in chk if c['pass']), 'checks_total': len(chk)}, open('tex/counts.json', 'w'))
print(len(V), dict(cnt), len(chk))

# TSVs (numbers resolved from the .aux file when given)
num = {}
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    for m in re.finditer(r'\\newlabel\{th:([^}]+)\}\{\{([^}]*)\}', open(sys.argv[1]).read()):
        num[m.group(1)] = m.group(2)
def plain(t):
    t = re.sub(r'\\ref\{[^}]*\}', '', t)
    t = t.replace('~', ' ').replace('\\textemdash', '-').replace('\\&', '&').replace('\\_', '_').replace('\\%', '%')
    t = re.sub(r'\$([^$]*)\$', r'\1', t)
    t = t.replace('\\leq', '<=').replace('\\geq', '>=').replace('\\le', '<=').replace('\\ge', '>=').replace('\\', '').replace('{', '').replace('}', '')
    return re.sub(r'\s+', ' ', t).strip()
with open('THEOREM_CROSSWALK.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['id', 'title', 'kind', 'status', 'scope', 'registry_chapter', 'manuscript_chapter', 'manuscript_location', 'depends_on', 'correction_status'])
    for r in V:
        i = r['id']; env, c = loc[i]
        n = num.get(i, '')
        w.writerow([i, r['title'], r['kind'], r['status'], r['scope'], r['vol'], c if c != 'F' else 'App. F',
                    f"{WORD[env]} {n}".strip(), ' '.join(r['deps']), r['corr']])
with open('AUDIT.tsv', 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['id', 'title', 'location', 'completeness_here', 'remark', 'verification_tags'])
    for r in V:
        i = r['id']; env, c = loc[i]
        w.writerow([i, r['title'], f"{WORD[env]} {num.get(i, '')}".strip(), cls[i], plain(rem.get(i, '')), ' '.join(tag_of[i])])
