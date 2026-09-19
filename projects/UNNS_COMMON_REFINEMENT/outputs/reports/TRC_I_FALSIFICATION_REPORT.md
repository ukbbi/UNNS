# TRC-I FALSIFICATION REPORT

## Result

Five explicit countermodels were constructed.

Each countermodel retains four TRC-I roles, removes exactly one, and loses route closure
inside the formal test framework.

\[
\begin{array}{c|ccccc|c}
& I&P&D&L&R&\text{closure}\\
\hline
CM_I&0&1&1&1&1&0\\
CM_P&1&0&1&1&1&0\\
CM_D&1&1&0&1&1&0\\
CM_L&1&1&1&0&1&0\\
CM_R&1&1&1&1&0&0
\end{array}
\]

## Most important findings

### 1. I and P really can be separated

A densified atomless algebraic construction makes `P` vacuously true while a projected
atomic relation destroys `I` and route closure.

Conversely, `<2,3>` can be locally stratified into independent rank-one pieces while the
atom `2` remains nonprime globally, isolating `P`.

### 2. D and L are distinct

`CM_L` is decisive here.

All finite stages and the ordinal induction structure are well founded, but the compatible
family has no limit witness.

So:

\[
D\not\Rightarrow L.
\]

This justifies the Conway bridge's use of both support-order descent and common-tail
Cauchy completeness.

### 3. R is genuinely local-to-global

Even perfect local solutions need not assemble into a global witness.

That makes reconstruction a separate structural requirement, not bookkeeping.

## Current state of TRC-I

We now have evidence for **independent load-bearing necessity inside the abstract test
framework**.

What remains completely open is sufficiency:

\[
I+P+D+L+R
\stackrel{?}{\Longrightarrow}
\text{route closure}.
\]

The next research task is to formulate a precise category of stratified refinement systems
and prove or falsify this implication there.
