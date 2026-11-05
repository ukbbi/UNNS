import sys
head = "\\begin{center}\\scriptsize\n\\begin{tabular}{@{}llllll@{}}\\toprule\nCW row & source id & status & treatment & section & number\\\\\\midrule\n"
tail = "\\bottomrule\\end{tabular}\n\\end{center}\n"
if "--placeholder" in sys.argv:
    body = "- & - & - & - & - & -\\\\\n"
else:
    import re
    seen = []
    for l in open("main.prov"):
        l = l.strip()
        if l and l not in seen: seen.append(l)
    seen.sort(key=lambda l: l.split("}")[0])
    rows = []
    for l in seen:
        m = re.match(r"\\provrow\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}\{(.*?)\}$", l)
        u, s, st, tr, sec, num = m.groups()
        rows.append("\\texttt{%s} & \\texttt{%s} & %s & %s & %s & %s\\\\\n" % (u, s, st, tr, sec, num))
    body = "".join(rows)
open("appmap_table.tex", "w").write(head + body + tail)
