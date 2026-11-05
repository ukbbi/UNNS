"""Builds tex/appmap_table.tex and crosswalk/PAPER_III_THEOREM_MAP.tsv from main.prov and data/ALLOCATION_III.tsv.
Usage (from tex/): make_appmap.py [--placeholder]"""
import sys, re, csv, os
HEAD = "CW row & source id & status & treatment & section & number & owner\\\\\\midrule\n"
H = ("\\begin{center}\\scriptsize\n\\begin{longtable}{@{}lllllll@{}}\\caption{Theorem map: the 73 allocated records, their status and treatment in this paper, and where they appear.}\\label{tab:map}\\\\\\toprule\n" + HEAD + "\\endfirsthead\n\\toprule\n" + HEAD + "\\endhead\n")
T = "\\bottomrule\\end{longtable}\n\\end{center}\n"
alloc = list(csv.DictReader(open('../data/ALLOCATION_III.tsv'), delimiter='\t'))
if '--placeholder' in sys.argv:
    open('appmap_table.tex', 'w').write(H + "- & - & - & - & - & - & -\\\\\n" + T); sys.exit()
prov = {}
for l in open('main.prov'):
    l = l.strip().replace("\\protect \\unhbox \\voidb@x \\kern .06em\\vbox {\\hrule width.3em}", "\\_")
    m = re.match(r"\\provrow\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}$", l)
    if not m: continue
    u, s, st, tr, sec, num = m.groups()
    prov.setdefault(u, []).append((s, st, tr, sec, num))
tsv = ['uid\tsource_id\tinitial_owner\tprimary_manuscript\tallocation_treatment\tpaper_III_status\tpaper_III_treatment\tpaper_III_locations\treallocation_note']
tex = []
for r in alloc:
    u = r['uid']; own = r['initial_owner'] + '$\\to$' + r['primary_manuscript'] if r['initial_owner'] != r['primary_manuscript'] else r['primary_manuscript']
    if u in prov:
        p = prov[u]; st = p[0][1]; tr = p[0][2]; loc = '; '.join('%s.%s' % (a[3], a[4]) for a in p)
        tex.append("\\texttt{%s} & \\texttt{%s} & %s & %s & %s & %s & %s\\\\\n" % (u, r['source_id'], st, tr, p[0][3], p[0][4], own))
    else:
        st = r['status']; tr = 'CITED'; loc = '-'
        tex.append("\\texttt{%s} & \\texttt{%s} & %s & %s & - & - & %s\\\\\n" % (u, r['source_id'], st, tr, own))
    note = 'reallocated to Paper II: proved there, cited here' if r['initial_owner'] != r['primary_manuscript'] else ''
    tsv.append('\t'.join([u, r['source_id'], r['initial_owner'], r['primary_manuscript'], r['proof_treatment'], st, tr, loc, note]))
tex.sort(key=lambda s: s.split('}')[0])
open('appmap_table.tex', 'w').write(H + ''.join(tex) + T)
open('../crosswalk/PAPER_III_THEOREM_MAP.tsv', 'w').write('\n'.join(tsv) + '\n')
print('map rows', len(alloc), 'with prov', sum(1 for r in alloc if r['uid'] in prov))
