from __future__ import annotations
import operator
import pandas as pd

OPS = {
    ">=": operator.ge,
    ">": operator.gt,
    "<=": operator.le,
    "<": operator.lt,
    "==": operator.eq,
    "!=": operator.ne,
}

def apply_relation_rule(df: pd.DataFrame, rule: dict | None) -> pd.DataFrame:
    """Return only edges satisfying the preregistered relation rule."""
    if not rule:
        return df.copy()
    mode = str(rule.get("mode", "all")).lower()
    conditions = rule.get("conditions", []) or []
    if not conditions:
        return df.copy()
    masks = []
    for cond in conditions:
        col = cond["column"]
        op_name = cond["op"]
        value = cond["value"]
        if col not in df.columns:
            raise ValueError(f"Relation rule refers to missing column: {col}")
        if op_name not in OPS:
            raise ValueError(f"Unsupported relation operator: {op_name}")
        masks.append(OPS[op_name](df[col], value))
    mask = masks[0]
    for m in masks[1:]:
        mask = (mask & m) if mode == "all" else (mask | m)
    if mode not in ("all", "any"):
        raise ValueError("relation_rule.mode must be 'all' or 'any'")
    return df.loc[mask].copy()
