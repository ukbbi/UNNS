from __future__ import annotations

from .schema import validate_record
from .verdict import evaluate


def run_record(record: dict) -> dict:
    errors = validate_record(record)
    if errors:
        return {
            "id": record.get("id", "unknown"),
            "label": record.get("label", "unknown"),
            "domain": record.get("domain", "unknown"),
            "verdict": "INVALID_RECORD",
            "level": -1,
            "errors": errors,
            "path": [],
            "missing": [],
            "record": record,
        }

    result = evaluate(record)
    return {
        "id": record["id"],
        "label": record["label"],
        "domain": record["domain"],
        **result,
        "record": record,
    }
