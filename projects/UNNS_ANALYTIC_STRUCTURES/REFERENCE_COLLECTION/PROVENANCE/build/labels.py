"""Review attribution wording used in displayed statements. Proof files themselves are not edited."""
import re
N='UNNS Research Collective'
RULES=[
 (r"(?i)\bworkspace owner(?=['’]s)", N),
 (r"\b([Aa])n owner\b", r"\1 owner"),
 (r"\bowner['’]s review", N+" review"),
 (r"\b[Oo]wner review", N+" review"),
 (r"\bowner: (?=\S)(?=valid|retain|conjectur|k |k=|positivity|proved)", N+" review: "),
 (r"\bOwner proposed\b", "Proposed by "+N),
 (r"\bowner proposed\b(?! (?:bounds|proof|pair))", "proposed by "+N),
 (r"\b[Oo]wner(?=\b)", N),
]
def relabel(t):
    for a,b in RULES: t=re.sub(a,b,t)
    # article agreement before the new name
    t=re.sub(r"\b([Aa])n (?="+N+")", r"\1 ", t)
    return t
