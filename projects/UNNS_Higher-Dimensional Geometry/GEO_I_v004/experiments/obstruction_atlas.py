"""E3/E5: obstruction atlas, validated against the exhaustive v003 polyhedral audit."""
import os, sys, itertools, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from obstruction_templates import Lattice, obstruction_atlas, embedded_by_templates
from realization import fibre_complex_data
from validation import cell_level_audit, edge_level_audit
import theorems as TH


def validate(res, b, boxes, atlas=None):
    """compare template prediction with the exhaustive audit on the given boxes.  returns (n, mismatches, n_nonembedded, atlas)."""
    lat = Lattice(res, b)
    ts, anti = atlas if atlas else obstruction_atlas(lat)
    n = bad = nn = 0; mism = []
    for q in boxes:
        fc = fibre_complex_data(res, q, b)
        if not fc['F']: continue
        a = cell_level_audit(fc['cells'], lp_budget=200000, stop_at_first=True)
        if a['status'] == 'resource_limited': continue
        n += 1; emb_audit = a['status'] == 'embedded'; nn += (not emb_audit)
        if emb_audit != embedded_by_templates(anti, q): bad += 1; mism.append(q)
    return n, bad, nn, (ts, anti), mism


def residue_classes(k, bs):
    for b in bs:
        us = [r for r in range(1, b) if gcd(r, b) == 1]
        for res in itertools.combinations_with_replacement(us, k):
            if len(set(res)) == 1 and res[0] == 1: continue
            yield b, res
