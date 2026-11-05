"""Extract (label, uid, source_id, status, treatment, file) from Papers I-III v0.4 tex sources (prov may precede or follow its statement)."""
import re, glob, json, os

roots = {'I': R+'PAPER_I_TRANSPORT/v0.4/tex', 'II': R+'PAPER_II_HISTORIES/v0.4/tex', 'III': R+'PAPER_III_EVOLUTION/v0.4/tex'}
out = {}
for P, d in roots.items():
    for f in sorted(glob.glob(d+'/**/*.tex', recursive=True)):
        if 'main.' in f or 'appmap' in f: continue
        txt = open(f).read()
        labs = [(m.start(), m.group(1)) for m in re.finditer(r'\\label\{((?:thm|prop|lem|cor|def)[^}]*)\}', txt)]
        for m in re.finditer(r'\\prov\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}', txt):
            before = txt[max(0, m.start()-60):m.start()].rstrip()
            after = txt[m.end():m.end()+80].lstrip()
            follows = re.search(r'\\end\{(theorem|proposition|lemma|corollary|definition|example|counter|problem)\}\s*$', before) is not None
            if (not follows) and re.match(r'\\begin\{(theorem|proposition|lemma|corollary|definition|example|counter|problem)', after):
                nxt = [l for l in labs if l[0] > m.end()]
                lab = nxt[0][1] if nxt else None
            else:
                prv = [l for l in labs if l[0] < m.start()]
                lab = prv[-1][1] if prv else None
            if lab: out.setdefault(P, {})[lab] = dict(uid=m.group(1), sid=m.group(2), status=m.group(3), treat=m.group(4), file=os.path.basename(f))
json.dump(out, open('../results/prov_extract.json', 'w'), indent=1)
print({k: len(v) for k, v in out.items()})
