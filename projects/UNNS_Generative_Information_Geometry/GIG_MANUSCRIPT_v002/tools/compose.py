#!/usr/bin/env python3
"""Authoring tool (not part of the build): lifts theorem/proof environments from the preserved v001
sources into the v002 chapter templates in tpl/, stripping v001 provenance annotations.
Template syntax:  @@label@@  or  @@label+tag@@  (tag is appended to the environment title)."""
import re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "v001_src")
ENVS = ["theorem","lemma","proposition","corollary","definition","example","observation","remark","conjecture","problem"]
files = {f: open(os.path.join(SRC, f), encoding="utf-8").read() for f in os.listdir(SRC) if f.endswith(".tex")}
tok = re.compile(r"\\(begin|end)\{(%s)\}" % "|".join(ENVS))
def spans(text):
    st, out = [], []
    for m in tok.finditer(text):
        if m.group(1) == "begin": st.append((m.start(), m.group(2)))
        else:
            s, e = st.pop(); out.append((s, m.end(), e))
    return out
def find_env(label):
    for fn, text in files.items():
        for m in re.finditer(r"\\label\{%s\}" % re.escape(label), text):
            c = [(s, e, n) for s, e, n in spans(text) if s < m.start() < e]
            if c:
                s, e, n = min(c, key=lambda x: x[1]-x[0])
                rest = text[e:]
                pm = re.match(r"\s*\\begin\{proof\}", rest)
                if pm:
                    pe = rest.index("\\end{proof}") + len("\\end{proof}")
                    e = e + pe
                return text[s:e]
    raise KeyError(label)
def strip_macro(text, name):
    out, i = [], 0
    pat = "\\" + name + "{"
    while True:
        j = text.find(pat, i)
        if j < 0: out.append(text[i:]); break
        out.append(text[i:j].rstrip(" \t"))
        k = j + len(name) + 1; nargs = 2 if name == "status" else 1
        for _ in range(nargs):
            while text[k] != "{": k += 1
            d = 0
            while True:
                if text[k] == "{": d += 1
                elif text[k] == "}":
                    d -= 1
                    if d == 0: k += 1; break
                k += 1
        i = k
    return "".join(out)
REPL = [
 (r"\n\s*\n(\s*\n)+", "\n\n"),
]
def tag_env(block, tag):
    m = re.match(r"\\begin\{(\w+)\}(\[(.*?)\])?", block, flags=re.S)
    env = m.group(1)
    if m.group(2):
        title = m.group(3)
        # titles may contain nested brackets rarely; accept simple case
        return block.replace(m.group(0), "\\begin{%s}[%s; %s]" % (env, title, tag), 1)
    return block.replace(m.group(0), "\\begin{%s}[%s]" % (env, tag), 1)
import json
REPL_PATH = os.path.join(HERE, "repl.json")
def apply_repl(t):
    t = re.sub(r"(\\label\{[^}]+\})[ \t]*\n[ \t]*(\\begin\{(?:itemize|enumerate)\})", r"\1\\leavevmode\n\2", t)
    if os.path.exists(REPL_PATH):
        for a, b in json.load(open(REPL_PATH, encoding="utf-8")):
            t = t.replace(a, b)
    return t
def lift(label, tag=None):
    b = find_env(label)
    b = strip_macro(b, "status")
    b = apply_repl(b)
    if tag: b = tag_env(b, tag)
    return b.strip()
def raw(fn, a, b):
    a = a.replace("\\n\\", "\n\\"); b = b.replace("\\n\\", "\n\\")
    t = files[fn]; i = t.index(a); j = t.index(b, i) + len(b)
    return apply_repl(strip_macro(t[i:j], "status")).strip()
def render(tpl):
    def subraw(m):
        fn, a, b = m.group(1).split("::")
        return raw(fn, a, b)
    tpl = re.sub(r"^@@RAW:([^\n]+?)@@[ \t]*$", subraw, tpl, flags=re.M)
    def sub(m):
        spec = m.group(1)
        tag = None
        if "+" in spec: spec, tag = spec.split("+", 1)
        return lift(spec, tag)
    return re.sub(r"^@@([^@\n]+)@@[ \t]*$", sub, tpl, flags=re.M)
def type_labels(t):
    """Give every label inside a theorem-like environment an explicit cleveref type, so that
    \\cref names do not depend on how a TeX distribution resolves shared counters."""
    ss = spans(t)
    labs = [(m.start(), m.end(), m.group(1)) for m in re.finditer(r"\\label\{([^}]+)\}", t)]
    for a, b, name in reversed(labs):
        c = [(s, e, n) for s, e, n in ss if s < a < e]
        if not c: continue
        env = min(c, key=lambda x: x[1]-x[0])[2]
        t = t[:a] + "\\label[%s]{%s}" % (env, name) + t[b:]
    t = re.sub(r"\\chapter\{([^}]*)\}\\label\{(app:[^}]+)\}", r"\\chapter{\1}\\label[appendix]{\2}", t)
    return t
if __name__ == "__main__":
    for fn in sorted(os.listdir(os.path.join(ROOT, "tpl"))):
        if not fn.endswith(".tex"): continue
        t = open(os.path.join(ROOT, "tpl", fn), encoding="utf-8").read()
        out = type_labels(render(t))
        open(os.path.join(ROOT, "src", fn), "w", encoding="utf-8").write(out)
        print("composed", fn, len(out.split()), "words")
