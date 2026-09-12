from __future__ import annotations

ALLOWED_STATUS = {"SUPPORTED", "NOT_SUPPORTED", "PARTIAL", "NOT_TESTED", "N/A"}
ALLOWED_DOMAIN = {"quantum_many_body", "classical", "generic", "unknown"}

REQUIRED_SECTORS = ("temporal", "rigidity", "collective", "spectral")


def validate_record(record: dict) -> list[str]:
    errors = []

    for key in ("id", "label", "domain", "sectors"):
        if key not in record:
            errors.append(f"missing top-level field: {key}")

    if record.get("domain") not in ALLOWED_DOMAIN:
        errors.append(f"invalid domain: {record.get('domain')}")

    sectors = record.get("sectors", {})
    for name in REQUIRED_SECTORS:
        if name not in sectors:
            errors.append(f"missing sector: {name}")
            continue
        status = sectors[name].get("status")
        if status not in ALLOWED_STATUS:
            errors.append(f"{name}.status invalid: {status}")

    temporal = sectors.get("temporal", {})
    if temporal.get("status") == "SUPPORTED" and temporal.get("q0") is None:
        errors.append("temporal.status=SUPPORTED requires q0")

    if not isinstance(record.get("provenance", []), list):
        errors.append("provenance must be a list")

    return errors
