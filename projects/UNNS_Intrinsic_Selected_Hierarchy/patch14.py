import re
s=open('UNNS_Intrinsic_Selected_v1_3.tex',encoding='utf8').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:60]); s=s.replace(a,b)
# --- item 1: explicit cross-reference words (robust to cleveref/newtx differences)
M={'cor:nonhom':'Corollary~\\ref{cor:nonhom}','def:G':'Definition~\\ref{def:G}',
 'prop:selectorfree':'Proposition~\\ref{prop:selectorfree}','prop:nonexpanding':'Proposition~\\ref{prop:nonexpanding}',
 'prop:legality':'Proposition~\\ref{prop:legality}','thm:bookentropy':'Theorem~\\ref{thm:bookentropy}',
 'thm:valuation':'Theorem~\\ref{thm:valuation}','sec:projection':'Section~\\ref{sec:projection}',
 'sec:selection':'Section~\\ref{sec:selection}','sec:primefire':'Section~\\ref{sec:primefire}',
 'eq:G':'Equation~\\eqref{eq:G}','eq:balls':'Equation~\\eqref{eq:balls}','fig:hierarchy':'Figure~\\ref{fig:hierarchy}',
 'prop:bookrank,thm:bookentropy':'Proposition~\\ref{prop:bookrank} and Theorem~\\ref{thm:bookentropy}',
 'fig:e8view,fig:collision':'Figures~\\ref{fig:e8view} and~\\ref{fig:collision}'}
def f(m):
    k=m.group(1); assert k in M,k; return M[k]
s=re.sub(r'\\Cref\{([^}]*)\}',f,s)
assert 'Cref' not in s
rep(r'\usepackage{cleveref}'+'\n','')
# --- item 2: \vv works with or without newtx
rep(r'\renewcommand{\vv}{\mathbf v}', r'\providecommand{\vv}{}'+'\n'+r'\renewcommand{\vv}{\mathbf v}')
# --- item 3: complete CC BY-SA attribution
old=s[s.index('(image: Misaki Ohta; user-supplied reproduction'):]
old=old[:old.index('CC BY-SA 4.0}')+len('CC BY-SA 4.0}')]+')'
new=r'(image: \emph{A two-dimensional projection of the shortest vectors of an $E_8$ lattice}, by Misaki Ohta, licensed under \href{https://creativecommons.org/licenses/by-sa/4.0/}{CC BY-SA 4.0}; cropped to remove the web caption, otherwise unmodified)'
rep(old,new)
rep(r'The E8 image is reproduced from the user-provided image with credit to Misaki Ohta under CC BY-SA 4.0;',
    r'The $E_8$ image is by Misaki Ohta, licensed under CC BY-SA 4.0, and is reproduced cropped to remove the web caption; it remains subject to that licence;')
# --- item 4: the "27" label above-right of its point
rep(r'\node[above left] at (dsttwo) {\scriptsize $27$};', r'\node[above right] at (dsttwo) {\scriptsize $27$};')
# --- version / note
rep(r'Version 1.3 \quad $\cdot$ \quad 14 November 2026', r'Version 1.4 \quad $\cdot$ \quad 14 November 2026')
rep(r'\textbf{Revision note (v1.3).} This release supplies',
    r'\textbf{Revision note (v1.4).} This release is typographical and editorial: cross-reference labels are written explicitly so that definitions, propositions and corollaries are named correctly in every build; the image attribution is completed; and one plot label is moved. No mathematical statement changes. Version 1.3 supplied')
open('UNNS_Intrinsic_Selected_v1_4.tex','w',encoding='utf8').write(s); print('ok')
