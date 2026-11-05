"""Writes crosswalk/PAPER_IV_SOURCE_MAP.tsv, crosswalk/SYNTHESIS_PROPOSITIONS.tsv, tex/tables/register.tex, tex/tables/provenance.tex"""
import json, os, re, glob
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
idx = json.load(open(H+'/results/theorem_index.json'))
OVR = {('II', 'thm:cube'): [('CW-0340', 'D-T3', 'PROVED', 'FULL')], ('II', 'thm:R3T3'): [('CW-0413', 'R3-T3', 'PROVED-SCOPED', 'CITED')],
       ('III', 'prop:onestep'): [], ('II', 'def:select'): [], ('III', 'def:KD'): [], ('III', 'def:collective'): []}
# (paper, label, role, used_in, hypotheses, corrections)
S = [
 ('II','def:select','definition (cited)','Sec.2','source Foundations Vol. I','none'),
 ('II','def:history','definition (cited)','Sec.2','','none'),
 ('II','thm:predecessors','proved again (self-contained proof in SIV-P2(a))','SIV-P2,SIV-P5,SIV-P9','integer t','none'),
 ('II','thm:kernel','cited as ingredient','SIV-P1','fixed source, finite alphabet','none'),
 ('II','thm:faith','cited','SIV-P5 (d), S2','fixed source','none'),
 ('II','thm:2314','used to derive','SIV-P1, SIV-P4','content {2,3,14}','none'),
 ('II','thm:R3T3','cited','SIV-P4 context','source 4, A disjoint from {1,2,4}; proved-scoped','scope as in Paper II'),
 ('II','thm:cube','used to derive','SIV-P4(d)','r=2 used','none'),
 ('II','thm:block','cited','O1','scoped block rewrites','none'),
 ('II','thm:sphere','cited','Sec.6','scoped','none'),
 ('II','thm:dual','cited','Sec.6','','none'),
 ('III','def:collective','definition (cited)','Sec.2','source Foundations Vol. II','none'),
 ('III','lem:M','used to derive','SIV-P3,P6,P9','all reduced rationals with D nonempty','none'),
 ('III','def:KD','definition (cited)','Sec.2','','none'),
 ('III','thm:R3T1a','used to derive','SIV-P2(b), Fig.20','reduced rational states','none'),
 ('III','thm:R3T1','cited (obstruction)','SIV-P2(c)','r>=13 prime, r=5 mod 8','none'),
 ('III','thm:B2T1','cited','SIV-P2(b)','integer m with sigma>1','none'),
 ('III','thm:A5T31','used to derive','SIV-P3,P6; Lemma comp','any finite D','none'),
 ('III','thm:A4T1','cited (example)','SIV-P3(c)','k>=2, l prime with k|l-1, ...','none'),
 ('III','thm:A5T24','cited','Sec.9','activation family before first event','none'),
 ('III','thm:sieve','cited','Sec.9, Fig.13','stage Y_j','none'),
 ('III','cor:event','cited','Sec.9','','none'),
 ('III','thm:zigzag','cited','SIV-P7 remark, Sec.9','any event K <- K0 -> K\'','none'),
 ('III','thm:nested','cited','Sec.9','Dead empty','none'),
 ('III','thm:cause','cited','SIV-P6','','none'),
 ('III','thm:A5T7','cited (finite-exact census)','SIV-P6(d)','l in {5,7,11,13}, S<1500, 24 steps','mixed record; census only'),
 ('III','thm:R3T5c','cited','SIV-P8, Sec.10','l=5 tower','none'),
 ('III','thm:R3T5bp','cited','Sec.10','l=11 tower','none'),
 ('III','thm:A5T53','cited','Sec.10, O5','qualitative; no effective threshold','proved-scoped'),
 ('III','thm:A5T6','cited (finite-exact)','SIV-P8','k<=140','finite-exact; not extrapolated'),
 ('III','prop:onestep','cited (derived in Paper III; no separate crosswalk row)','SIV-P9(a)','D(x) nonempty','none'),
 ('III','thm:R3T7','cited','SIV-P9(b)','towers','none'),
 ('III','thm:B2T3','cited','Remark after SIV-P1','','none'),
 ('I','thm:P2T1','cited','Sec.2','','none'),
 ('I','thm:P2T2','used to derive (instance of minimality lemma)','SIV-P3, Cor. S4','','none'),
 ('I','thm:cell-transport','cited','Sec.2','','none'),
 ('I','thm:laws','cited (counterexamples)','SIV-P3(d)','','none'),
 ('I','thm:planar','cited','Sec.5, Fig.8','rank 2, any box','none'),
 ('I','thm:C1','cited','Sec.5, Fig.8','E3, box (2,4,2)','none'),
 ('I','thm:corner','cited','Sec.5','','none'),
 ('I','thm:slab-i','cited','Sec.5','free coordinate','none'),
 ('I','prop:topology','cited (finite-exact)','Sec.5, Fig.9','specimen 21^8/5 -> 21^8/4','finite-exact; not recomputed'),
]
rows = []
for P, lab, role, used, hyp, corr in S:
    e = idx[P][lab]; pv = OVR.get((P, lab), [(p['uid'], p['sid'], p['status'], p['treat']) for p in e['prov']])
    uid = ';'.join(p[0] for p in pv) or 'none'; sid = ';'.join(p[1] for p in pv) or '-'; st = ';'.join(p[2] for p in pv) or '-'
    rows.append(dict(ref=f'Paper {P} {e["kind"]} {e["number"]}', paper=P, label=lab, number=e['number'], uid=uid, sid=sid, status=st, role=role, used=used, hyp=hyp, corr=corr))
hdr = ['ref', 'paper', 'label', 'number', 'crosswalk_uid', 'source_id', 'source_status', 'role', 'used_in', 'hypotheses', 'corrections']
with open(H+'/crosswalk/PAPER_IV_SOURCE_MAP.tsv', 'w') as f:
    f.write('\t'.join(hdr)+'\n')
    for r in rows: f.write('\t'.join([r['ref'], r['paper'], r['label'], r['number'], r['uid'], r['sid'], r['status'], r['role'], r['used'], r['hyp'], r['corr']])+'\n')
def tx(s): return s.replace(';', '; ').replace('  ', ' ').replace('_', r'\_').replace('&', r'\&').replace('^', r'\^{}').replace('#', r'\#').replace("'", "'")
with open(H+'/tex/tables/provenance.tex', 'w') as f:
    f.write('{\\scriptsize\\setlength{\\tabcolsep}{3pt}\\begin{longtable}{@{}p{2.9cm}p{1.5cm}p{1.2cm}p{3.1cm}p{3.1cm}p{2.2cm}@{}}\\toprule\nSource & UID & ID & Status & Role in Paper IV & Hypotheses / corrections\\\\\\midrule\\endhead\n')
    for r in rows:
        f.write(f"{tx(r['ref'])} & {tx(r['uid'])} & {tx(r['sid'])} & {tx(r['status'])} & {tx(r['role'])} ({tx(r['used'])}) & {tx(r['hyp'])}{'; ' if r['hyp'] and r['corr']!='none' else ''}{tx(r['corr']) if r['corr']!='none' else ''}\\\\\n")
    f.write('\\bottomrule\\end{longtable}}\n')
P = [
 ('SIV-P1','Endpoint projection and retained information','NEW-PROVED','prop:P1','II thm:kernel;II thm:faith;II thm:2314','W1 (32:(2,2,2,2) vs (1,8,8)); W4 (nu(14)=2); W10 (admissibility of the kernel coset)','c6_witnesses.py'),
 ('SIV-P2','Occurrence projection and primitive-relation information','NEW-PROVED (a); CITED (b),(c)','prop:P2','II thm:predecessors;III thm:R3T1a;III thm:R3T1;III thm:B2T1','W7 (N+1 in D(T_N m)); D(x13)=D(y13)','c6_witnesses.py'),
 ('SIV-P3','Arithmetic availability versus geometric realization','NEW-PROVED (a),(b); CITED (c),(d)','prop:P3','III lem:M;III thm:A5T31;III thm:A4T1;I thm:laws;I thm:P2T2','Lemma minimal (abstract); edge windows','c5_checks.py (L-edge, 28179 pairs)'),
 ('SIV-P4','Arithmetic constraints and global history connectivity','NEW-PROVED from cited theorems; FINITE check','prop:P4','II thm:2314;II thm:R3T3;II thm:cube','nu(7,14,28,70)=(0,2,1,2); 16 histories 1->5184','c5_checks.py; c6_witnesses.py'),
 ('SIV-P5','Limits of endpoint geometry as a history invariant','NEW-PROVED (exhaustive recursion); FINITE-EXACT census','prop:P5','II thm:predecessors;II thm:faith;III thm:R3T1a','W3 (900 vs 9000), W3b (288 vs 4320)','c6_witnesses.py; c1_collide.py'),
 ('SIV-P6','Hierarchy of structural persistence under evolution','NEW-PROVED; (d) quotes finite-exact census','prop:P6','III lem:M;III thm:A5T31;III thm:A5T7;III thm:cause','Lemma comp (3000 random sets); W9 (four set-level Betti-change witnesses)','c5_checks.py'),
 ('SIV-P7','Information requirements for topological prediction','NEW-PROVED (a)-(d); (e) search outcome only','prop:P7','III thm:zigzag;III thm:sieve;III thm:A5T7','W5 pairs A,B','c6_witnesses.py; c7_dim2.py'),
 ('SIV-P8','Scaling information versus geometric structure','NEW; FINITE-EXACT (k<=14, 12 periods)','prop:P8','III thm:R3T5c;III thm:A5T6','W8 (126 vs 3094); normalized scaling signature','c4_pair.py; c6_witnesses.py'),
 ('SIV-P9','Correspondence levels for distinct arithmetic dynamics','NEW-PROVED (c); ASSEMBLED (a),(b),(d)','prop:P9','III prop:onestep;III thm:R3T7;III lem:M;II thm:predecessors','W6 (1008 integer states); L3 restricted results quoted from III B2T10, R3T7; identity-only obstruction','c6_witnesses.py'),
]
with open(H+'/crosswalk/SYNTHESIS_PROPOSITIONS.tsv', 'w') as f:
    f.write('id\ttitle\tstatus\ttex_label\tinherited_sources\twitnesses_or_checks\tscript\n')
    for r in P: f.write('\t'.join(r)+'\n')
with open(H+'/tex/tables/register.tex', 'w') as f:
    f.write('\\begin{table}[t]\\centering\\footnotesize\\setlength{\\tabcolsep}{3pt}\\begin{tabular}{@{}p{1.3cm}p{4.6cm}p{4.6cm}p{2.5cm}@{}}\\toprule\nID & Subject & Status & Statement \\\\\\midrule\n')
    for r in P:
        n = r[3].split(':')[1]
        f.write(f"{r[0].replace('SIV-','SIV-')} & {tx(r[1])} & {tx(r[2])} & \\cref{{prop:{n}}}\\\\\n")
    f.write('\\bottomrule\\end{tabular}\\caption{\\textbf{Register of the synthesis propositions.} New results are proved in the text or in Appendix~\\ref{app:proofs}; inherited ingredients are cited by theorem number (Appendix~\\ref{app:prov}); finite-exact statements are labelled with their checked ranges.}\\label{tab:register}\\end{table}\n')
print(len(rows), 'source rows;', len(P), 'propositions')
