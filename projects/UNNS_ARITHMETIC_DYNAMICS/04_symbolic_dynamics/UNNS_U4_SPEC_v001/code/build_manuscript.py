import json,os,re
H=os.path.dirname(os.path.abspath(__file__));D=H+"/../data";R=json.load(open(D+"/registry.json"));C=json.load(open(H+"/../reports/spec_check_report.json"))
ids={x["id"]:x for x in R}
import re as _re
def eo(s):
    parts=s.split("$")
    return "$".join(p.replace("\\_","_").replace("_","\\_") if i%2==0 else p for i,p in enumerate(parts))
def e(s): return s.replace("_","\\_").replace("#","\\#").replace("&","\\&")
core=[x for x in R if x["stage"]!="U4.0"]
from collections import Counter
oc=Counter(x["origin"] for x in core)
lab={"U3_CONSEQUENCE":"consequence of U0--U3","STANDARD":"standard theory, specialised","NEW_ELEMENTARY":"new, elementary (proof obligation)","FROZEN_IMPORT":"frozen record, imported","OPEN":"open","DEFINITION":"definition"}
tri="\n".join(f"{lab[k]} & {oc[k]}\\\\" for k in ["U3_CONSEQUENCE","STANDARD","NEW_ELEMENTARY","FROZEN_IMPORT","DEFINITION","OPEN"])
def short(d): return ", ".join(d) if d else "---"
reg_rows="\n".join(f"\\texttt{{{e(x['id'])}}} & {e(x['title']) if '$' not in x['title'] else x['title']} & {lab[x['origin']]} & {x['status'].replace('_','\\_')} & {x['info_class']}\\\\" for x in R)
detail=""
for s,name in [("U4.1","U4.1 Representational universality"),("U4.2","U4.2 Dynamical correspondence"),("U4.3","U4.3 Intrinsic admissibility and obstruction"),("U4.4","U4.4 Generative information boundary"),("U4.5","U4.5 SELECT / FIELD / GIG correspondence"),("U4.6","U4.6 Synthesis targets")]:
    detail+=f"\\subsection{{{name}}}\n"
    for x in [y for y in R if y["stage"]==s]:
        detail+=f"\\paragraph{{\\texttt{{{x['id']}}} --- {eo(x['title'])}.}} \\emph{{{x['kind']}; {lab[x['origin']]}; class: {x['info_class']}.}} {eo(x['statement'])}"
        if x["hypotheses"]: detail+=f" \\textbf{{Hypotheses:}} {eo(x['hypotheses'])}"
        if x["proof_note"]: detail+=f" \\textbf{{Proof route:}} {eo(x['proof_note'])}"
        detail+=f" \\textbf{{Status:}} {eo(x['status'])}."
        if x["falsification_gate"]: detail+=f" \\textbf{{Refuted by:}} {eo(x['falsification_gate'])}."
        if x["deps"]: detail+=f" \\textbf{{Uses:}} {', '.join('\\texttt{'+d+'}' for d in x['deps'])}."
        if x["probe"]: detail+=f" \\textbf{{Probe:}} {x['probe']}."
        detail+="\n\n"
it=C["items"]
probe_rows="\n".join(f"\\texttt{{{e(k)}}} & {'PASS' if v['passed'] else 'FAIL'}\\\\" for k,v in it.items())
tex=r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}\usepackage{amsmath,mathtools,amssymb,amsthm,booktabs,longtable,array,hyperref,graphicx,xcolor}
\hypersetup{colorlinks=true,linkcolor=blue!50!black,urlcolor=blue!50!black}
\newtheorem{thm}{Theorem}
\title{UNNS-U4 Specification, version 001\\Universality and Structural Obstruction Theorems\\for the Reversible SELECT-II Arithmetic Graph}
\author{UNNS Research Collective}\date{10 November 2026}
\begin{document}\maketitle
\begin{abstract}
Let $G$ be the graph on the positive integers with edges $\{kN,k(N+1)^2\}$. We fix the claims a theory of its universality has to settle, with exact hypotheses: (i) which sequences are faithfully coded as marked walks, at what segmentation and routing cost; (ii) which dynamical properties survive the passage to the discrete suspension; (iii) which finite-type systems arise from rules that use only the graph metric, and which cannot (fixed-point dichotomy, real-spectrum obstruction, a triangle-free entropy gap); (iv) what must be declared as additional information. New elementary statements recorded here: finite alphabets embed at cost $\le2$ per transition; the suspension over a symmetric base with a loop has period $1$ or $2$ and period $2$ for every golden-mean embedding; the directed SELECT-II digraph represents no sequence with a descent. The document is a registry of """+str(len(core))+r""" claims with proof dependencies, counterexamples, a correspondence matrix and acceptance gates; it proves nothing beyond U0--U3 except where marked, and records for each claim whether it is already a consequence of earlier releases or needs a new proof.
\end{abstract}
\section{Scope, provenance and reproducibility}
Releases U0--U2, TI, TI-DYN, RN, U3 v001 and U3-COR v001 are unchanged; their hashes are in \texttt{data/provenance\_frozen\_sources.txt} (not re-run, per the project protocol). The frozen records read for \S\ref{sec:corr} are the SELECT-I record (v1.0.0, 21 October 2026, verifier hash $\texttt{cd2f3510}\ldots$ as stated in its \texttt{FREEZE.md}), SELECT-II (v001/v002a/v002b), FIELD-I (v001--v012) and GIG\_I v001, cited through the Master Theorem Registry (Reference Collection v001, commit \texttt{bb8b12d753c6\ldots}, \url{https://github.com/ukbbi/UNNS/tree/bb8b12d753c600c597feb00df17fe139c7cc65fa/projects/UNNS_MATH_FOUNDATIONS/sources}) and the GIG collection (commit \texttt{a115e4bc6b8e\ldots}, \url{https://github.com/ukbbi/UNNS/tree/a115e4bc6b8ee734e6146b3b17a6b121e65d31c3/projects/UNNS_Generative_Information_Geometry}). Nothing in the frozen collection was modified or re-fetched.

\textbf{Reproducibility limitation carried from U3-COR.} The U3-COR verifier located the U3 v001 registration through an absolute path (\texttt{/home/claude/UNNS\_U3}); it therefore runs only on the machine where it was built. This package ships its own copies of the engine files and of the U3 registration record and uses relative paths only; U3-COR itself is not altered.

\section{Vocabulary and the three strengths of universality}
\textbf{Representation} (R): a coding with a decoder; marks, alphabet embedding and routing convention are part of the code. \textbf{Dynamical equivalence} (D): a conjugacy or suspension relation between dynamics. \textbf{Intrinsic structural universality} (I): the structure arises from rules that use only the graph's own isomorphism-invariant data. The registry keeps these separate: a claim classed \emph{intrinsic} may not depend, even transitively, on a non-definitional claim classed representation or additional information (acceptance gate AG3, checked mechanically; see \S\ref{sec:gates}). Every property supplied by markers, embeddings, route tables, observers or controllers is classed as additional information.

\section{Triage: what is already known, what is new}
Of the """+str(len(core))+r""" claims in stages U4.1--U4.6:
\begin{center}\begin{tabular}{@{}lr@{}}\toprule Origin & Claims\\\midrule
"""+tri+r"""
\\\bottomrule\end{tabular}\end{center}
Representation universality (U4.1-T1, T3) and the first-return conjugacy and Abramov relation are consequences of U3 and classical tower theory. The \emph{new} content is elementary but not empty: bounded cost for finite alphabets (using unbounded degree and triangle-freeness), the parity-period theorem, the fixed-point dichotomy and spectral obstructions for metric rules, the triangle-free entropy gap, and the non-universality of the directed digraph. None of the new statements is deep; their value is that they fix the boundary exactly. Five items are open (\S\ref{sec:open}).

\begin{figure}[h]\centering\includegraphics[width=\textwidth]{../figures/dependency_graph.png}
\caption{Proof-dependency graph of the registry, by stage and origin. Orange nodes are new elementary claims whose proofs must be written and independently checked in the U4 body.}\end{figure}

\section{Registry}
\scriptsize
\begin{longtable}{@{}p{1.25cm}p{4.9cm}p{3.0cm}p{3.6cm}p{1.6cm}@{}}\toprule
ID & Title & Origin & Status & Class\\\midrule\endhead
"""+reg_rows+r"""
\\\bottomrule\end{longtable}
\normalsize

\section{Exact claims, hypotheses and proof routes}
Statements are given with the hypotheses under which they are intended, the clause that would refute them, and what they use. ``Sketch'' means a proof route is stated but the proof is a U4-body obligation.
"""+detail+r"""
\section{Counterexamples to unrestricted intrinsic universality}\label{sec:counter}
(a) \emph{Golden mean.} One fixed point, entropy $\log\varphi$; every finite-memory metric rule has $0$ or $|F|$ fixed points (U4.3-T2), so a conjugate metric shift has one letter and zero entropy. (b) \emph{The 3-cycle with loops}, matrix $\begin{psmallmatrix}1&1&0\\0&1&1\\1&0&1\end{psmallmatrix}$: eigenvalues $2,1+\omega,1+\bar\omega$ (checked, probe P3); memory-1 metric shifts have real spectrum (U4.3-T3). (c) \emph{Full $k$-shift, $k\ge3$, radius 1}: needs a triangle; $\rho(A+I)\le1+k/2<k$ for every triangle-free graph (exhaustively verified for $k\le7$, probe P3); realised at radius $2$ by a star (probe P1). (d) \emph{Non-SFT systems} (even shift, Sturmian). (e) \emph{Descents}: the directed SELECT-II digraph cannot carry the waypoint sequence $2,1$ (growth $\ge4$, checked for $x\le3000$, probe P5). Each is a theorem about the stated class only: grammars with unbounded memory, with vertex-naming (e.g.\ degree conditions, as used for primes), or with additional state are outside it and belong to the finite-control tier.

\section{SELECT / FIELD / GIG correspondence matrix}\label{sec:corr}
Definitions were read from the frozen records; terminology similarity was not taken as correspondence.
\begin{center}\small\begin{tabular}{@{}p{4.1cm}p{5.8cm}p{2.6cm}p{1.2cm}@{}}\toprule
Frozen structure & U3/U4 counterpart & Verdict & Claim\\\midrule
SELECT-II arrows $m\to m(N+1)^2/N$ & $G$ is the underlying simple graph (brute-force check $m<260$; $\sum R=3124$, $\sum H=8283$ to $5000$ reproduce frozen S2.12) & proven (identity) & S2a\\
SELECT-II degrees $\tau$, $R$ & $\deg=\tau+R$ ($x\le3000$) & proven (consequence) & S2b\\
SELECT-II orientation, acyclicity & orientation not shown graph-intrinsic; directed histories not universal & open / proven & S2c, S2d\\
SELECT-II Markov no-go (S2.13) & memory lives in marks = declared information & conditional & S2e\\
SELECT-I anchor routes $(k,d)$ & edges $k(d-1)\to kd^2$ (S2.5) & proven & S1\\
SELECT-I binary $J_{\mathrm{join}},J_{\mathrm{ref}}$ & no binary operation on $G$ & not addressed & S1\\
FIELD-I integer fibres (F.T1, $b=1$) & fibre size $=R(a)$ = indegree & consistent & F1\\
FIELD-I rational fibres, collective $C(x)$, regimes & vertices are integers only & unsupported & F1\\
FIELD-I leakage / nonselection & marks are label recovery & conditional & F2\\
GIG ambiguity $A(t)=\log_2|F_t|$ & different object from $M(w)$ & unsupported (no bridge) & G1\\
GIG hierarchy, history complexes & would need directed marked walks & open & G2\\
\bottomrule\end{tabular}\end{center}

\section{Prior-art obligations}
None of the following reviews has been done; the baseline entries are recalled from general knowledge and are unverified here. A claim may be labelled new only after its review.
\begin{center}\footnotesize\begin{tabular}{@{}p{2.6cm}p{6.7cm}p{3.2cm}@{}}\toprule
Area & Expected baseline (recalled) & Claims affected\\\midrule
Symbolic dynamics, SFTs & Lind--Marcus (1995), Kitchens (1998); sliding-block codes (Curtis--Hedlund--Lyndon); periodic-point and zeta invariants; Williams (1973) & U4.3-T2, T3, T5\\
Graph presentations; hom-shifts & $X_r(F)$ is the walk shift $\mathrm{Hom}(\mathbb Z,H)$ of a reflexive symmetric graph $H$; literature on hom-shifts (e.g.\ Chandgotia--Marcus) & U4.3 (all)\\
Discrete suspensions & Kakutani induced transformations; Ambrose--Kakutani; Abramov (1959); pressure equation (Bowen, Parry--Pollicott) & U4.2-T1--T6\\
Spectral graph bounds & Mantel; Nosal (spectral bound for triangle-free graphs) & U4.3-T4\\
Complexity, counting & Kolmogorov complexity, invariance theorem; counting arguments & U4.4-T1, T2\\
Graph powers, induced subgraphs & realisability of graphs inside powers of a fixed graph & U4.3-Cj1\\
Arithmetic graphs & graphs defined by multiplicative adjacency; degree--divisor formulas & U4.5-S2b, U4.4-P1\\\bottomrule\end{tabular}\end{center}
\textbf{What may be distinctive about this architecture} (to be tested against the above, not asserted): (D1) an explicit arithmetic graph that is triangle-free with odd girth $5$ and unbounded degree $\tau+R$; (D2) the consequence that every finite alphabet embeds at cost $\le2$ although radius-1 rules cannot reach full shifts; (D3) canonical lex-first routing with an exact segmentation ledger; (D4) the explicit separation of representation, finite control and intrinsic generation. The obstruction theorems themselves are specialisations of classical facts about shifts and hom-shifts; their novelty, if any, lies in their application to $G$ and in the accounting.

\section{Open problems}\label{sec:open}
\textbf{U4.1-C1} eccentricity growth of the identity embedding; \textbf{U4.3-Cj1} realisability of every finite graph in some power; \textbf{U4.3-Cj2} rigidity of $G$ (local probe: degree-coloured balls of radii 2, 3 have an order-2 automorphism group caused by boundary symmetry, so no evidence either way); \textbf{U4.5-S2c} intrinsic orientation; \textbf{U4.5-G2} a bridge to GIG. Obstructions for memory $\ge2$ metric rules beyond the fixed-point dichotomy are also open.

\section{Acceptance and falsification gates}\label{sec:gates}
\begin{description}\itemsep0pt
\item[AG0] engine files byte-identical to U3 v001 registration; frozen-source hashes recorded.
\item[AG1] every claim has origin, status, class, hypotheses (where applicable), dependencies that exist, a refutation clause; no dependency cycle.
\item[AG2] each new elementary claim receives a full written proof, an independent exact check by a second implementation, and an attempted falsification before it is labelled proved.
\item[AG3] no claim classed intrinsic depends on a representation/additional-information claim (mechanical).
\item[AG4] prior-art review for every non-frozen, non-U3 claim before any ``new'' label.
\item[AG5] no preservation claim for FIELD-I or GIG without the exact frozen statement and a hypothesis check; unsupported extensions stay labelled.
\item[AG6] verifiers use relative paths only; inherited verifications are \texttt{NOT\_RERUN} with hashes.
\item[AG7] every obstruction carries an explicit counterexample certificate; negative results are retained.
\end{description}
\textbf{Checker results} (\texttt{reports/spec\_check\_report.json}): \begin{center}\begin{tabular}{@{}lr@{}}\toprule Item & Result\\\midrule
"""+probe_rows+r"""
\\\bottomrule\end{tabular}\end{center}
The probes are bounded exact computations supporting sketches; they are not proofs. All results above are corroborations of the registry's hypotheses; in particular the reproduction of the frozen sums $3124$ and $8283$ (probe P4) is an independent confirmation that $G$ is the SELECT-II graph in the sense used by U3.

\section{Plan}
Stage 1 (this document). Stage 2: write and independently check the proofs of the new elementary claims (PO-1--PO-10), starting with U4.3-T2--T4 and U4.2-T4. Stage 3: prior-art review. Stage 4: import RN and complete the information-boundary chapter. Stage 5: the coordinated theorem pair U4.6-TU / TO and the boundary statement TB. No synthesis manuscript is written before stages 2--3 are complete.
\end{document}
"""
open(H+"/../manuscript/UNNS_U4_SPEC_v001.tex","w").write(tex);print("ok",len(tex))
