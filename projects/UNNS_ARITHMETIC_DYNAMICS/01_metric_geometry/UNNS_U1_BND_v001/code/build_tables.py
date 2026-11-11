#!/usr/bin/env python3
"""Generate the LaTeX tables and a machine-readable record of the nine identities
directly from the symbolic certificates (so the manuscript cannot drift from them)."""
import json
import sys

import sympy as sp

import u1_bnd_lib as L

T = L.T


def tx(e):
    return sp.latex(sp.factor(e)) if not isinstance(e, (int, sp.Integer)) else str(e)


def lab(d, N):
    s = tx(N)
    if any(ch in s for ch in "+-") and not s.startswith("("):
        s = f"({s})"
    return ("+" if d == "+" else "-") + s


def main(out_dir, data_dir):
    certs = [L.certify(i) for i in L.IDENTITIES]
    assert all(c["ok"] for c in certs)
    # ---- summary table
    lines = [r"\begin{tabular}{@{}clcl@{}}", r"\toprule",
             r"class & $n$ & steps & labels (forward $+N$, inverse $-N$) \\ \midrule"]
    for c, ident in zip(certs, L.IDENTITIES):
        nform = f"{ident['M']}t+{ident['r']}" if ident["r"] else f"{ident['M']}t"
        rng = rf"\,($t\ge {c['t0']}$)"
        labs = r",\ ".join(f"${lab(d, N)}$" for d, N in ident["steps"])
        lines.append(rf"{c['name']} & $n={nform}${rng} & {c['length']} & {labs} \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    open(f"{out_dir}/identities_summary.tex", "w").write("\n".join(lines) + "\n")
    # ---- certificate tables
    out = []
    for c, ident in zip(certs, L.IDENTITIES):
        nform = f"{ident['M']}t+{ident['r']}" if ident["r"] else f"{ident['M']}t"
        out.append(rf"\paragraph{{Identity {c['name']}: $n={nform}$, $t\ge {c['t0']}$ ({c['length']} steps).}}")
        out.append(r"\begin{center}\footnotesize")
        out.append(r"\begin{tabular}{@{}clcccc@{}}\toprule")
        out.append(r"step & type & $N$ & cofactor $k$ & state before & state after \\ \midrule")
        for row in c["rows"]:
            typ = "forward" if row["dir"] == "+" else "inverse"
            out.append(rf"{row['step']} & {typ} & ${tx(row['N'])}$ & ${tx(row['k'])}$ & "
                       rf"${tx(row['before'])}$ & ${tx(row['after'])}$ \\")
        out.append(r"\bottomrule\end{tabular}\end{center}")
    open(f"{out_dir}/identities_certificates.tex", "w").write("\n".join(out) + "\n")
    # ---- machine-readable
    rec = []
    for c, ident in zip(certs, L.IDENTITIES):
        rec.append(dict(name=c["name"], modulus=c["M"], residue=c["r"], t_min=c["t0"], length=c["length"],
                        n="%d*t+%d" % (c["M"], c["r"]),
                        steps=[dict(step=r["step"], direction="forward" if r["dir"] == "+" else "inverse",
                                    N=str(sp.factor(r["N"])), cofactor=str(sp.factor(r["k"])),
                                    state_before=str(sp.factor(r["before"])),
                                    state_after=str(sp.factor(r["after"]))) for r in c["rows"]]))
    json.dump(rec, open(f"{data_dir}/identities.json", "w"), indent=2, sort_keys=True)
    print("wrote identity tables:", len(rec))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
