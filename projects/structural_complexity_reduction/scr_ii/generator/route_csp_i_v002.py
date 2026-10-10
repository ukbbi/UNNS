from __future__ import annotations
import copy, hashlib, json, math, random
from typing import Dict, List, Mapping

from grammar.route_grammar import ALPHABET, DEFAULT_TRANSITIONS
from solver.exact_solver import solve_baseline

CHECKSUM_MODULUS=5
COST_MIN=1
COST_MAX=1000
DENSITY_MIN=0.02
DENSITY_MAX=0.04
COST_HALF_WIDTH_FACTOR=0.025
MAX_ATTEMPTS=64

def _sha(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def _structure(seed:int, depth:int):
    rng=random.Random(int(seed))
    initial_symbol=rng.choice(ALPHABET)
    initial_phase=rng.randrange(3)
    prev_symbol=initial_symbol
    prev_phase=initial_phase
    last_disc=[]
    layers=[]
    for i in range(depth):
        backbone_bit=rng.randrange(2)
        symbol=rng.choice(DEFAULT_TRANSITIONS[prev_symbol])
        phase=(prev_phase+rng.choice((0,1)))%3
        may_disc=sum(last_disc[-3:])==0
        disc=1 if may_disc and rng.random()<0.12 else 0
        good={"symbol":symbol,"phase":phase,"discontinuity":disc,"branch_id":backbone_bit}
        other_bit=1-backbone_bit
        decoy={
            "symbol":rng.choice(ALPHABET),
            "phase":rng.randrange(3),
            "discontinuity":1 if rng.random()<0.35 else 0,
            "branch_id":other_bit
        }
        opts=[None,None]
        opts[backbone_bit]=good
        opts[other_bit]=decoy
        layers.append({"index":i,"options":opts})
        prev_symbol=symbol
        prev_phase=phase
        last_disc=(last_disc+[disc])[-3:]
    return {"initial_symbol":initial_symbol,"initial_phase":initial_phase,"layers":layers}

def _arith_rng(seed:int, attempt:int):
    return random.Random((int(seed)*1000003 + int(attempt)*9176) & ((1<<63)-1))

def _merge_attempt(seed:int, depth:int, structure:Mapping, attempt:int):
    rng=_arith_rng(seed,attempt)
    arithmetic=[]
    for i in range(depth):
        arithmetic.append([
            {"cost":rng.randint(COST_MIN,COST_MAX),"checksum_weight":rng.randrange(CHECKSUM_MODULUS)},
            {"cost":rng.randint(COST_MIN,COST_MAX),"checksum_weight":rng.randrange(CHECKSUM_MODULUS)}
        ])
    anchor=[rng.randrange(2) for _ in range(depth)]
    anchor_cost=sum(arithmetic[i][anchor[i]]["cost"] for i in range(depth))
    anchor_checksum=sum(arithmetic[i][anchor[i]]["checksum_weight"] for i in range(depth))%CHECKSUM_MODULUS
    seal=int(anchor[-1])
    half=max(2,round(COST_HALF_WIDTH_FACTOR*depth*COST_MAX))
    layers=[]
    for i in range(depth):
        opts=[]
        for b in (0,1):
            o=dict(structure["layers"][i]["options"][b])
            o.update(arithmetic[i][b])
            opts.append(o)
        layers.append({"index":i,"options":opts})
    inst={
        "benchmark":"ROUTE_CSP_I",
        "version":"v002",
        "seed":int(seed),
        "depth":int(depth),
        "attempt":int(attempt),
        "initial_symbol":structure["initial_symbol"],
        "initial_phase":int(structure["initial_phase"]),
        "layers":layers,
        "checksum_modulus":CHECKSUM_MODULUS,
        "checksum_target":anchor_checksum,
        "cost_min":anchor_cost-half,
        "cost_max":anchor_cost+half,
        "terminal_seal":seal,
        "generator_provenance":{
            "structure_stream":"seed",
            "arithmetic_stream":"seed+attempt",
            "target_selection":"arithmetic_anchor_only",
            "structural_filter_consulted_for_acceptance":False
        }
    }
    inst["instance_sha256"]=_sha(inst)
    return inst

def generate_instance(seed:int, depth:int):
    structure=_structure(seed,depth)
    attempts=[]
    for attempt in range(MAX_ATTEMPTS):
        inst=_merge_attempt(seed,depth,structure,attempt)
        baseline=solve_baseline(inst)
        density=baseline["solution_count"]/(1<<depth)
        attempts.append({"attempt":attempt,"solution_count":baseline["solution_count"],"density":density})
        if DENSITY_MIN <= density <= DENSITY_MAX:
            inst["multiplicity_acceptance"]={
                "solution_count":baseline["solution_count"],
                "solution_density":density,
                "accepted_attempt":attempt,
                "acceptance_uses_structural_filter":False
            }
            inst["instance_sha256"]=_sha({k:v for k,v in inst.items() if k!="instance_sha256"})
            return inst, baseline, attempts
    raise RuntimeError(f"No in-band arithmetic attempt for seed={seed} depth={depth} within {MAX_ATTEMPTS} attempts")

def structural_view(instance:Mapping):
    return {
        "depth":int(instance["depth"]),
        "initial_symbol":instance["initial_symbol"],
        "initial_phase":int(instance["initial_phase"]),
        "layers":[{
            "index":int(layer["index"]),
            "options":[{
                "symbol":opt["symbol"],
                "phase":int(opt["phase"]),
                "discontinuity":int(opt["discontinuity"]),
                "branch_id":int(opt["branch_id"])
            } for opt in layer["options"]]
        } for layer in instance["layers"]]
    }
