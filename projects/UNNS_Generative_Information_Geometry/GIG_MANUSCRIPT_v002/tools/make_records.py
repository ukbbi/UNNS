#!/usr/bin/env python3
"""Generates records/THEOREM_CROSSWALK_v002.md and records/V001_TO_V002_MAP.md from the sources."""
import re, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = r"(theorem|lemma|proposition|corollary|definition|example|observation|remark|problem|conjecture)"
pat = re.compile(r"\\begin\{%s\}(?:\[((?:[^\[\]]|\[[^\]]*\])*)\])?\s*\\label\{([^}]+)\}" % ENV)
def scan(dirpath, prefix):
    out = {}
    for f in sorted(glob.glob(os.path.join(dirpath, "ch*.tex")) + glob.glob(os.path.join(dirpath, "appendices.tex"))):
        name = os.path.basename(f)
        t = open(f, encoding="utf-8").read()
        for m in pat.finditer(t):
            out[m.group(3)] = (m.group(1), (m.group(2) or "").replace("\n", " ").strip(), name)
    return out
v2 = scan(os.path.join(ROOT, "src"), "v2"); v1 = scan(os.path.join(ROOT, "tools", "v001_src"), "v1")
chap = {}
for f in sorted(glob.glob(os.path.join(ROOT, "src", "ch*.tex"))):
    n = int(re.search(r"ch(\d+)", f).group(1)); t = open(f, encoding="utf-8").read()
    m = re.search(r"\\chapter\{([^}]*)\}", t); chap[os.path.basename(f)] = (n, m.group(1) if m else "")
lines = ["# Theorem crosswalk, GIG_MANUSCRIPT_v002", "",
         "Every labelled statement of the monograph, in order of appearance, with its chapter, kind, title (the title carries the status tag) and, where the statement was preserved from GIG_MANUSCRIPT_v001, the v001 file it came from.", "",
         "| Label | Chapter | Kind | Title / status | v001 source |", "|---|---|---|---|---|"]
for lab, (env, title, fn) in v2.items():
    n, cn = chap.get(fn, ("-", fn))
    src = v1[lab][2] if lab in v1 else "new in v002"
    lines.append(f"| `{lab}` | {n} | {env} | {title.replace('|','/')} | {src} |")
open(os.path.join(ROOT, "records", "THEOREM_CROSSWALK_v002.md"), "w").write("\n".join(lines) + "\n")
lines = ["# v001 to v002 map", "",
         "Every labelled statement of v001 and where it stands in v002. `kept` = same label present; `absent` = not present as a labelled statement (removed, condensed into prose or recast; see the reason column).", "",
         "| v001 label | v001 file | v001 title | v002 |", "|---|---|---|---|"]
reasons = {"prob:": "open-problem statement: not a chapter in v002; scope stated in prose and Appendix A",
           "lem:cone": "classical fact, cited", "lem:gibbs": "classical fact, cited", "prop:faces": "classical fact, cited", "prop:ranknull": "elementary; used inline",
           "prop:diff": "folded into Theorem on face thresholds", "lem:lcmdiv": "folded into face-threshold theorem"}
for lab, (env, title, fn) in v1.items():
    if lab in v2: st = f"kept (ch{chap[v2[lab][2]][0]:02d})"
    else:
        r = next((v for k, v in reasons.items() if lab.startswith(k)), "condensed or recast in prose")
        st = "absent: " + r
    lines.append(f"| `{lab}` | {fn} | {title.replace('|','/')[:80]} | {st} |")
open(os.path.join(ROOT, "records", "V001_TO_V002_MAP.md"), "w").write("\n".join(lines) + "\n")
absent = [l for l in v1 if l not in v2]
print("v2 labels", len(v2), "v1 labels", len(v1), "absent", len(absent)); print(absent)
