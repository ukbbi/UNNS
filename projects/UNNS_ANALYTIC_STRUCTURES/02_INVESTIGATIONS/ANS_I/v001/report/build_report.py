"""Build the research report: proofs from ../PROOFS.md, tables from ../results/. Needs pandoc and pdflatex."""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R = lambda n: json.load(open(os.path.join(ROOT, "results", n)))
NAME = "History_Dirichlet_Series_of_the_Nesting_Grammar"
GH = "https://github.com/ukbbi/UNNS/tree/d3065a0b63889286a56b3149d7724e537bd6064e/projects/UNNS_INDUCED_STRUCTURES"
GHT = ("https://github.com/ukbbi/UNNS/blob/d3065a0b63889286a56b3149d7724e537bd6064e/"
       "projects/UNNS_INDUCED_STRUCTURES/THEOREM_INDEX.md")

LABEL = {"T03": "thm:evolution", "T04": "thm:prime", "T01": "thm:factor", "T14a": "thm:allhist",
         "T07": "thm:suff", "T15": "lem:saturation", "T09": "thm:sharp", "T14b": "thm:region",
         "T10": "thm:growth", "T12": "thm:fixed", "T05": "thm:depth2", "T06": "thm:euler",
         "T08": "thm:unit", "T11": "thm:criterion"}


def body():
    src = open(os.path.join(ROOT, "PROOFS.md"), encoding="utf-8").read()
    out, current, env, used = [], None, None, set()
    for block in src.split("\n\n"):
        block = block.strip()
        m = re.match(r"^## (T\d\d[ab]?)(?: and (T\d\d))?(?: \(partial\))? · (.*)$", block)
        if m:
            current = m.group(1)
            out.append("## " + m.group(3))
            continue
        m = re.match(r"^\*\*(Theorem|Lemma|Corollary)(?: \(([^)]*(?:\([^)]*\))?[^)]*)\))?\.\*\*\s*", block)
        if m:
            kind = m.group(1).lower()
            title = m.group(2)
            if kind == "theorem":
                lab = LABEL.get(current)
            elif kind == "lemma":
                lab = "lem:saturation" if title == "saturation" else "lem:primes"
            else:
                lab = {"histories ending at $n$": "cor:words", "abscissa": "cor:abscissa"}.get(title)
            head = "XXBEGIN%s" % kind
            tline = "XXLABEL{%s}" % lab if lab and lab not in used else ""
            used.add(lab)
            out.append(head + "\n\n" + ("XXTITLE " + title + "\n\n" if title else "") + tline)
            block = block[m.end():]
            env = kind
        if "*Proof.*" in block:
            a, b = block.split("*Proof.*", 1)
            if a.strip():
                out.append(a.strip())
            out.append("XXEND%s" % env)
            out.append("XXBEGINproof")
            block = b.strip()
        end = block.endswith(r"$\square$")
        if end:
            block = block[:-len(r"$\square$")].rstrip()
        out.append(block)
        if end:
            out.append("XXENDproof")
    md = "\n\n".join(out)
    tex = subprocess.run(["pandoc", "-f", "markdown", "-t", "latex"], input=md.encode(),
                         stdout=subprocess.PIPE, check=True).stdout.decode()
    # theorem environments with their titles and labels
    def head(m):
        kind, title, lab = m.group(1), m.group(2), m.group(3)
        s = "\\begin{%s}" % kind
        if title:
            title = title.strip()
            s += "[%s]" % (title[0].upper() + title[1:])
        if lab:
            s += "\\label{%s}" % lab
        return s
    tex = re.sub(r"XXBEGIN(theorem|lemma|corollary)\s*(?:XXTITLE ([^\n]*(?:\n[^\n]+)*?)\n\s*\n)?"
                 r"(?:XXLABEL\\\{([^\\]*)\\\}\s*)?", lambda m: head(m) + "\n", tex)
    tex = tex.replace("XXBEGINproof", "\\begin{proof}").replace("XXENDproof", "\\end{proof}")
    tex = re.sub(r"XXEND(theorem|lemma|corollary)", r"\\end{\1}", tex)
    tex = re.sub(r"\\hypertarget\{[^}]*\}\{%\n", "", tex)
    tex = re.sub(r"(\\(?:sub)*section\{(?:[^{}]|\{[^{}]*\})*\})\\label\{[^}]*\}\}", r"\1", tex)
    tex = tex.replace("\\subsection{", "\\subsection{").replace("\\subsubsection{", "\\subsubsection{")
    # pandoc maps '#' to section and '##' to subsection
    tex = re.sub(r"\bT(\d\d[ab]?)\b", lambda m: "\\cref{%s}" % LABEL["T" + m.group(1)], tex)
    cites = {
        "is monograph Lemma 4.2 for the nesting grammar": "is \\cite[Lemma~4.2]{monograph} for the nesting grammar",
        "of the monograph (Theorem 19.2)": "of \\cite[Theorem~19.2]{monograph}",
        "Delange's Tauberian theorem": "Delange's Tauberian theorem \\cite{delange,tenenbaum}",
        "(Landau)": "(Landau's theorem \\cite[Chapter~11]{apostol})",
    }
    flat = tex
    for old, new in cites.items():
        pat = re.escape(old).replace("\\ ", r"\s+").replace("'", "(?:'|’)")
        flat, n = re.subn(pat, lambda m: new, flat)
        assert n == 1, old
    return flat


def table(spec, header, rows, caption, label):
    return ("\\begin{table}[htbp]\\centering\\small\n\\begin{tabular}{%s}\\toprule\n%s\\\\\\midrule\n%s"
            "\\\\\\bottomrule\n\\end{tabular}\n\\caption{%s}\\label{%s}\n\\end{table}\n"
            % (spec, " & ".join(header), "\\\\\n".join(" & ".join(r) for r in rows), caption, label))


def num(n):
    return "{:,}".format(n).replace(",", "\\,")


def computations():
    cen = [R("census_stage_%s.json" % s) for s in "ABCDE"]
    ver, an, ctl = R("verification.json"), R("analytic.json"), R("controls.json")
    gen, ps = R("generation.json"), R("prime_coordinate_statistics.json")
    wit, tally = R("multiplicativity_witnesses.json"), R("coprime_pair_tally.json")
    assert ver["failed"] == 0
    pw = lambda X: "$10^{%d}$" % (len(str(X)) - 1)
    orb = {o["X"]: o for o in gen["source_one_orbit"]}
    t1 = table("rrrrrrr", ["$X$", "$A(X)$", "$C(X)$", "endpoints", "$N_1(X)$", "$\\frac{\\log A}{\\log X}$",
               "$\\frac{\\log C}{\\log X}$"],
               [[pw(c["X"]), num(c["A"]), num(c["C"]), num(c["distinct_endpoints"]),
                 num(orb[c["X"]]["histories_from_1"]), "%.4f" % c["log_A_over_log_X"],
                 "%.4f" % c["log_C_over_log_X"]] for c in cen],
               "Census of minimal-endpoint words, histories by endpoint, and histories from source $1$.",
               "tab:census")
    K = max(len(c["A_k"]) for c in cen)
    t2 = table("r" * 6, ["$k$"] + [pw(c["X"]) for c in cen],
               [[str(k)] + [num(c["A_k"][k]) if k < len(c["A_k"]) else "0" for c in cen] for k in range(K)],
               "Depth distribution $A_k(X)$.", "tab:depth")
    t3 = table("rrr", ["$n$ with largest $a(n)$", "$a(n)$", "$X$"],
               [[num(c["max_a"][0]), num(c["max_a"][1]), pw(c["X"])] for c in cen],
               "Largest endpoint multiplicities.", "tab:max")
    rows = []
    for key, v in wit.items():
        name = "$%s$" % key if "_" not in key else "$%s_{%s}$" % tuple(key.split("_"))
        rows.append([name, num(v["m"]), num(v["n"]), str(v["f(m)"]), str(v["f(n)"]), str(v["f(mn)"])])
    t4 = table("lrrrrr", ["$f$", "$m$", "$n$", "$f(m)$", "$f(n)$", "$f(mn)$"], rows,
               "Coprime witnesses of non-multiplicativity.", "tab:witness")
    t5 = table("rrr", ["$p$", "mean $v_p(E)$", "fraction with $p\\mid E$"],
               [[str(r["p"]), "%.3f" % r["mean_v_p"], "%.3f" % r["fraction_divisible"]] for r in ps["rows"]],
               "Prime coordinates of the %s words with $E\\le%d$." % (num(ps["words"]), ps["X"]), "tab:primes")
    t6 = table("rrrr", ["$X$", "$A_2(X)$", "gap to $c$", "gap $\\times X^{1/6}$"],
               [[pw(r["X"]), num(r["A_2"]), "%.4f" % r["residual_minus_c"],
                 "%.3f" % r["scaled_by_X^(1/6)"]] for r in an["A2"]],
               "Depth two: the gap is $A_2(X)/\\sqrt X-\\frac\\kappa2\\log X-c$ with $c=%.4f$."
               % an["second_constant"], "tab:A2")
    names = {"selected_nesting": "$N\\mapsto (N+1)^2/N$", "integer_scaling": "integer multipliers",
             "square_scaling": "square multipliers", "cubic_nesting": "$(N+1)^3/N$",
             "prime_scaling": "prime multipliers", "finite_2_3": "$\\{2,3\\}$", "empty": "no labels",
             "single_label_N1": "single label $N=1$", "consuming_3/2_9/4": "$\\{3/2,\\,9/4\\}$"}
    t7 = table("lrrrrl", ["grammar", "words", "endpoints", "max.\\ depth", "boundary", "$H$ witness $(m,n)$"],
               [[names[c["grammar"]], num(c["words"]), num(c["endpoints"]), str(c["max_depth"]),
                 "---" if c["sigma_c"] is None else "%.4f" % c["sigma_c"],
                 "none found" if not c["H_multiplicativity_witness"] else
                 "$(%d,%d)$" % tuple(c["H_multiplicativity_witness"][:2])] for c in ctl],
               "Control grammars, ceiling $%s$. The boundary is the abscissa of $\\mathcal G(s,1)$."
               % num(ctl[0]["X"]), "tab:controls")
    assert all(c["engine_mismatches"] == 0 for c in ctl)
    t5d = an["T05"]; kap = an["kappa"]
    sat = an["saturation"]
    text = r"""
\section{Exact computations}
Two engines were implemented independently. The forward engine enumerates words through
\cref{thm:evolution} and records the minimal endpoint of each. The backward engine uses the predecessor
recursion $H_{k+1}(n)=\sum_{m^2\mid n}H_k\big(n(m-1)/m^2\big)$ of \cref{cor:words} and never forms a
minimal endpoint. Their results satisfy $H_k=1*a_k$ for every depth and every $n\le10^7$.
A third routine, which tests admissibility directly from the definition, checks both engines on small ranges.
The verification run behind this report passed all %d checks (Python %s, %s). Finite agreement tests the
implementation; the infinite statements rest on the proofs.

""" % (ver["passed"], ver["python"], ver["platform"])
    text += t1 + t2 + t3
    text += "\\begin{figure}[htbp]\\centering\\includegraphics[width=.86\\textwidth]{fig_growth.pdf}\n" \
            "\\caption{Observed exponents against the limit of \\cref{thm:growth}. Convergence is slow: at " \
            "$X=10^7$ the three observed values are still well below $\\sigma_c$.}\\label{fig:growth}\\end{figure}\n"
    text += "\\begin{figure}[htbp]\\centering\\includegraphics[width=.86\\textwidth]{fig_depth.pdf}\n" \
            "\\caption{Normalized depth distributions.}\\label{fig:depth}\\end{figure}\n"
    text += ("The census file lists every word with $E\\le10^5$ with its record $(w,K,Q,E)$; all %s records "
             "replay from their least source. The longest word $w_p$ of \\cref{lem:primes} for $p<1000$ has "
             "%d letters.\n\n" % (num(gen["records_E_le_100000"]), gen["longest_prime_word_below_1000"]))
    text += ("\\subsection{Factorization and prime coordinates}\nAll %s coprime pairs of non-squarefree integers "
             "with $mn\\le10^5$ satisfy $H(mn)>H(m)H(n)$ (%d equalities, %d reversals).\n"
             % (num(tally["greater"]), tally["equal"], tally["less"])) + t4 + t5
    text += ("\\subsection{Depth two and boundaries}\nAt $s=%g$ the truncated double sum and the Hurwitz "
             "representation of \\cref{thm:depth2} agree to the accuracy of the tail bound $%.2g\\times10^{-7}$: "
             "$%.9f$. The partial Euler product with a tail correction gives $\\kappa\\approx%.5f$. "
             "Expanding the representation one order further at $s=\\tfrac12$ predicts\n"
             "\\[A_2(X)=\\sqrt X\\Big(\\frac\\kappa2\\log X+c+o(1)\\Big),\\qquad c=2\\gamma\\kappa+"
             "\\tfrac12F'(\\tfrac12)+S-1-\\kappa,\\]\nwhere $\\gamma$ is Euler's constant, "
             "$F(s)=\\sum_dJ_s(d)d^{-2s}c(d)^{-2s}$ and $S=\\sum_d\\frac{J_{1/2}(d)}{d\\,c(d)}"
             "\\big(-\\psi(1+\\tfrac1d)-\\gamma\\big)$. This second term is a computed prediction and is not "
             "part of \\cref{thm:depth2}; \\cref{tab:A2} compares it with exact counts.\n"
             % (t5d["s"], t5d["tail_bound"] * 1e7, t5d["direct"], kap["tail_corrected"])) + t6
    text += "\\begin{figure}[htbp]\\centering\\includegraphics[width=.86\\textwidth]{fig_A2.pdf}\n" \
            "\\caption{The gap in \\cref{tab:A2} and an $X^{-1/6}$ reference line.}\\label{fig:A2}\\end{figure}\n"
    a, b = sat[0], sat[1]
    text += ("The root $\\sigma_c$ lies in $[%.8f,\\,%.8f]$. In a sampled experiment on \\cref{lem:saturation} "
             "(%d words of length %d, labels $N\\le%d$), the fraction of admissible continuations rose from "
             "$%.3f$ with no initial word to $%.3f$ after an initial word of the largest tested size.\n"
             % (an["sigma_c"][0], an["sigma_c"][1] if an["sigma_c"][1] > an["sigma_c"][0] + 1e-8
                else an["sigma_c"][0] + 1e-8, a["samples"], a["length"], a["M"],
                a["rows"][0]["good_fraction"], a["rows"][-1]["good_fraction"]))
    text += "\\subsection{Control grammars}\nBoth engines agree on each of the following.\n" + t7
    return text


PRE = r"""\documentclass[11pt,a4paper]{article}
\usepackage{cmap}\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{lmodern}
\usepackage[margin=27mm]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,longtable,array,graphicx,microtype}
\usepackage[hidelinks]{hyperref}\usepackage{url}\usepackage[capitalise,noabbrev]{cleveref}
\graphicspath{{../figures/}}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem*{maintheorem}{Theorem}
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\allowdisplaybreaks\emergencystretch=2em
\title{\bfseries History Dirichlet Series of the Nesting Grammar\\[5pt]
\large Factorization, sharp convergence and the growth of generative histories}
\author{UNNS Research Collective}
\date{Research release v001 \quad 26 November 2026}
\begin{document}
\maketitle
\begin{abstract}
Starting from the operation $M\mapsto M(N+1)^2/N$, we study the integer sequences obtained by applying
$x\mapsto x(N+1)^2/N$ whenever $N$ divides $x$, with their ordered words of labels $N$. Each word is possible
exactly from the multiples of a least integer and ends exactly in the multiples of a least endpoint. The Dirichlet
series counting all histories ending at $n$ factors as $\zeta(s)$ times the generating series of least endpoints,
also when depth and source are weighted. Although every fixed depth converges for $\operatorname{Re}s>1/2$,
the full series has abscissa of absolute convergence $\sigma_c=1.5463810\ldots$, the root of
$\sum_{N\ge1}(N/(N+1)^2)^{\sigma}=1$. The histories issuing from any single integer already grow like
$X^{\sigma_c+o(1)}$ up to endpoint $X$. At depth two the series continues meromorphically to
$\operatorname{Re}s>1/3$ with a double pole at $1/2$, and the number of two-letter words with least endpoint
at most $X$ is asymptotic to $\frac{\kappa}{2}\sqrt X\log X$ for an explicit Euler product
$\kappa\approx1.8536$. The series admits no ordinary Euler product. Comparisons with other multiplicative
grammars show which arithmetic hypothesis drives the boundary.
\end{abstract}
\tableofcontents
\section{Introduction}
Fix the generating operation $M\perp N=M(N+1)^2/N$ and continue it on integers: the letter $N$ may be applied
to $x$ when $N\mid x$. From $x=1$ only the letter $1$ is possible and leads to $4$; from $4$ the letters
$1,2,4$ are possible, and so on. Two different words may reach the same integer, and the order of the letters
matters for the sources from which they are possible. The record of a word is
$\mathcal R(w)=(w,K(w),Q(w),E(w))$: the word, its least source, its multiplier and its least endpoint.
Dirichlet series appear here as summaries of these records; the records themselves, including the order of the
letters, remain the underlying object.

\begin{figure}[htbp]\centering\includegraphics[width=.92\textwidth]{fig_tree.pdf}
\caption{Words over the letters $1$ and $2$ up to length two, with least endpoint $E$ and least source $K$.
Edge labels are the letters.}\label{fig:tree}\end{figure}

\subsection*{Main results}
Write $\mathcal G(s,t)=\sum_wt^{|w|}E(w)^{-s}$ and $B(\sigma)=\sum_{N\ge1}(N/(N+1)^2)^{\sigma}$.
\begin{itemize}
\item \emph{Factorization} (\cref{thm:factor,thm:allhist}). The series of histories ending at $n$ equals
$\zeta(s)\mathcal G(s,t)$; the series over all histories weighted by source and endpoint is again a zeta factor
times a series over words.
\item \emph{Sharp boundary} (\cref{thm:sharp,thm:region}). The $k$-letter sum $G_k(\sigma)$ satisfies
$G_k(\sigma)^{1/k}\to B(\sigma)$; hence $\mathcal G(s,t)$ converges absolutely for $|t|B(\operatorname{Re}s)<1$,
$\operatorname{Re}s>1$, and not when the inequality is reversed.
\item \emph{Growth from one source} (\cref{thm:growth}). The number of histories from any fixed integer with
endpoint at most $X$ is $X^{\sigma_c+o(1)}$.
\item \emph{Fixed depth} (\cref{thm:fixed,thm:depth2}). Every $G_k$ with $k\ge1$ has abscissa $1/2$; $G_2$ has
an explicit continuation and a double pole there.
\end{itemize}

\subsection*{Relation to earlier work}
The least source and least endpoint of a word, the predecessor structure, and the decomposition of history sets
by endpoint are established in the monograph \cite{monograph}, in particular its Lemma~4.2, Proposition~5.5 and
Theorem~19.2; the surrounding source collection is public \cite{sources,index}. The present work adds the depth
and source weighted analytic series, their convergence boundaries, the growth theorem and the depth-two
analysis. The lemma that every prime is reached from the source $1$ proceeds by induction on primes, a device
also used for rational completeness in \cite{algebraic}. Priority with respect to the wider literature has not
been surveyed.

This report is release v001 of the investigation ANS-I of the research programme \emph{Analytic Structures of
the UNNS Substrate}; \cref{sec:register} relates its statements to the programme register. All statements called
theorems, lemmas or corollaries have proofs below; numerical statements are confined to \cref{sec:comp} and are
labelled as computations.
"""

POST = r"""
\section{Further mathematical directions}
\begin{enumerate}
\item Decide convergence on the surface $|t|B(\operatorname{Re}s)=1$ and describe the singularity of
$\mathcal G(s,1)$ at $s=\sigma_c$. Does it continue beyond that point?
\item Is $A(X)=\#\{w:E(w)\le X\}$ asymptotic to $cX^{\sigma_c}$, or is there a slowly varying factor?
\item Find the region of absolute convergence of $\mathcal F(s,u,t)$ when $\operatorname{Re}(s+u)<0$.
\item Prove the second term of $A_2(X)$ and continue $G_2$ beyond $\operatorname{Re}s=1/3$.
\item For depth $k\ge3$ we conjecture $(2\sigma-1)^kG_k(\sigma)\to\kappa_k$ as $\sigma\to\tfrac12^+$, where
$\kappa_k$ is the mean of $\prod_{i=2}^k\gcd(E(N_1\cdots N_{i-1}),N_i)^{1/2}$ over independent profinitely
uniform labels; the cases $k\le2$ are proved.
\item We conjecture $H(mn)>H(m)H(n)$ for all coprime non-squarefree $m,n$. Concatenating words does not give an
injective map from pairs: for $m=4$, $n=25$ the pairs $(\varepsilon,(1,4))$ and $((1),(4))$ have the same
concatenation.
\item Classify multiplicative grammars by the limit of $G_k^{1/k}$ when the saturation hypothesis of
\cref{thm:criterion} fails.
\item Determine which statements about zeros or cancellation, if any, the continued series support.
\end{enumerate}

\appendix
\section{Register and reproduction}\label{sec:register}
\begin{center}\small
\begin{tabular}{ll}\toprule
register & statement\\\midrule
ANS-T01, T02 & \cref{thm:factor}\\
ANS-T03 & \cref{thm:evolution,cor:words}\\
ANS-T04 & \cref{thm:prime}\\
ANS-T05, T13 & \cref{thm:depth2}\\
ANS-T06 & \cref{thm:euler}\\
ANS-T07 & \cref{thm:suff}\\
ANS-T08 & \cref{thm:unit}\\
ANS-T09 & \cref{thm:sharp,cor:abscissa}\\
ANS-T10 & \cref{thm:growth}\\
ANS-T11 (partial) & \cref{thm:criterion}\\
ANS-T12 & \cref{thm:fixed}\\
ANS-T14 & \cref{thm:allhist,thm:region}\\
ANS-T15 & \cref{lem:primes,lem:saturation,thm:growth}\\
\bottomrule
\end{tabular}
\end{center}
The release directory contains the engines, a definition-level test oracle, the census files and the record file.
\texttt{python verify.py --stage E} repeats the computations (standard library only; about 1 GB of memory);
\texttt{RUN\_WINDOWS.bat} runs the smaller default stage. The batch file has not yet been executed under Windows.

\begin{thebibliography}{9}
\bibitem{monograph} UNNS Research Collective, \emph{Induced Structures in the UNNS Substrate}, Chapters 1--42,
version 1.1 (workspace release).
\bibitem{sources} UNNS Research Collective, \emph{UNNS Substrate --- Induced Structures}, source collection,
\url{""" + GH + r"""}.
\bibitem{index} UNNS Research Collective, theorem index of the source collection,
\url{""" + GHT + r"""}.
\bibitem{algebraic} UNNS Research Collective, \emph{Algebraic and Topological Extensions of the UNNS
Generative Law}, version 1.1, November 2026 (workspace manuscript).
\bibitem{apostol} T.~M.~Apostol, \emph{Introduction to Analytic Number Theory}, Springer, 1976.
\bibitem{delange} H.~Delange, G\'en\'eralisation du th\'eor\`eme de Ikehara,
\emph{Ann.\ Sci.\ \'Ecole Norm.\ Sup.\ (3)} \textbf{71} (1954), 213--242.
\bibitem{tenenbaum} G.~Tenenbaum, \emph{Introduction to Analytic and Probabilistic Number Theory},
Cambridge University Press, 1995.
\end{thebibliography}
\end{document}
"""


def build():
    b = body()
    figs = {
        r"\end{proof}": None,
    }
    def after(label, fig):
        nonlocal b
        i = b.index("\\label{%s}" % label)
        j = b.index("\\end{proof}", i) + len("\\end{proof}")
        b = b[:j] + "\n" + fig + b[j:]
    after("cor:abscissa", "\\begin{figure}[htbp]\\centering\\includegraphics[width=.86\\textwidth]{fig_pressure.pdf}\n"
          "\\caption{The growth factor $B(\\sigma)$ per letter crosses $1$ at $\\sigma_c$, while a single "
          "letter, $G_1$, is finite for all $\\sigma>1/2$.}\\label{fig:pressure}\\end{figure}\n")
    after("thm:fixed", "\\begin{figure}[htbp]\\centering\\includegraphics[width=.74\\textwidth]{fig_region.pdf}\n"
          "\\caption{Source-weighted series at $t=1$, $a=\\operatorname{Re}s$, $b=\\operatorname{Re}(s+u)$. "
          "The full series changes behaviour at $a=\\sigma_c$ for $b\\ge0$; each fixed depth $k\\ge1$ "
          "converges, for $a>0$, $b>0$, exactly above the line $a+b=1$.}\\label{fig:region}\\end{figure}\n")
    comp = computations().replace("\\section{Exact computations}", "\\section{Exact computations}\\label{sec:comp}")
    tex = PRE + b + comp + POST
    open(os.path.join(HERE, NAME + ".tex"), "w", encoding="utf-8").write(tex)
    print("wrote", NAME + ".tex", len(tex))


if __name__ == "__main__":
    build()
