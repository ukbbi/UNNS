#!/usr/bin/env python3
"""IV-4B negative controls + positive twins on the REAL instance (frozen couplings), using the D0=14 frontier certificates.
Each tests/neg4b_*.lean MUST FAIL to compile (kernel: the claim is false); each tests/pos4b_*.lean (true twin of the same prefix) MUST compile.
usage: mk_neg4b.py ROOT CERTDIR"""
import sys, pathlib
sys.set_int_max_str_digits(0)
ROOT, CD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); D0 = 14; M = (1 << D0) - 1
(ROOT/"tests").mkdir(exist_ok=True)
cg = [int(x) for x in (CD/f"cert_ground_D{D0}.txt").read_text().split()]; cn = [int(x) for x in (CD/f"cert_nongT_D{D0}.txt").read_text().split()]
bg = 711243241830 & M; bn = 711243241766 & M
def toks(c): return [(c >> (2*k)) & 3 for k in range(c.bit_length()//2)]
H = "import SCR_IV_V4\nopen SCR_IV\n"
def neg(name, body): (ROOT/"tests"/f"neg4b_{name}.lean").write_text(H + "/-- NEGATIVE CONTROL on the real instance: this file MUST FAIL to compile. -/\n" + body + "\n")
def pos(name, body): (ROOT/"tests"/f"pos4b_{name}.lean").write_text(H + "/-- Positive twin: this file MUST compile. -/\n" + body + "\n")
G = "subOK Rreal 40 claimedGroundNum (fun _ => false) 14"; N = "subOK Rreal 40 claimedNonGTrue leafGrammar 14"
tg = toks(cg[bg]); assert tg[0] == 1, tg[:3]
pos("g", f"theorem t : {G} {bg} {cg[bg]} = true := by decide +kernel")
neg("g_Uplus1", f"theorem t : subOK Rreal 40 (claimedGroundNum + 1) (fun _ => false) 14 {bg} {cg[bg]} = true := by decide +kernel")
neg("g_tamper", f"theorem t : {G} {bg} {cg[bg] ^ 1} = true := by decide +kernel")                    # token 0: split -> prune-bound
neg("g_trunc", f"theorem t : {G} {bg} {cg[bg] >> 2} = true := by decide +kernel")
neg("g_trail", f"theorem t : {G} {bg} {cg[bg] | (1 << (cg[bg].bit_length() + 1))} = true := by decide +kernel")
neg("g_rows", f"theorem t : subOK (fun d => (Rreal d).map (fun x => x + 1)) 40 claimedGroundNum (fun _ => false) 14 {bg} {cg[bg]} = true := by decide +kernel")
neg("g_wrongpfx", f"theorem t : {G} {bg ^ 16383} {cg[bg]} = true := by decide +kernel")
# non-grammar: pick the witness prefix; if it has no leaf token, also pick any prefix that has one
tn = toks(cn[bn]); bl = next((b for b in range(1 << D0) if 2 in toks(cn[b])), None); assert bl is not None
pos("n", f"theorem t : {N} {bn} {cn[bn]} = true := by decide +kernel")
neg("n_frozenU", f"theorem t : subOK Rreal 40 claimedNonGNum leafGrammar 14 {bn} {cn[bn]} = true := by decide +kernel")   # the frozen (non-minimal) value
neg("n_Uplus1", f"theorem t : subOK Rreal 40 (claimedNonGTrue + 1) leafGrammar 14 {bn} {cn[bn]} = true := by decide +kernel")
neg("n_noleaf", f"theorem t : subOK Rreal 40 claimedNonGTrue (fun _ => false) 14 {bl} {cn[bl]} = true := by decide +kernel")
pos("n_leaf", f"theorem t : {N} {bl} {cn[bl]} = true := by decide +kernel")
print("neg/pos written; ground witness prefix", bg, "tokens", len(tg), "; nongT witness prefix", bn, "tokens", len(tn), "; leaf-token prefix", bl, "tokens", len(toks(cn[bl])))
