from __future__ import annotations

VERDICT_LEVELS = {
    "NO_TEMPORAL_ORDER": 0,
    "TEMPORAL_RECURRENCE": 1,
    "RIGID_RECURRENCE": 2,
    "COLLECTIVE_TEMPORAL_ORDER": 3,
    "MANY_BODY_TIME_CRYSTAL_ADMISSIBLE": 4,
    "INSUFFICIENT_DOMAIN_EVIDENCE": 2,
    "INVALID_RECORD": -1,
}


def evaluate(record: dict) -> dict:
    sectors = record["sectors"]
    temporal = sectors["temporal"]
    rigidity = sectors["rigidity"]
    collective = sectors["collective"]
    spectral = sectors["spectral"]
    domain = record["domain"]

    path = []
    missing = []

    if temporal["status"] != "SUPPORTED":
        path.append("temporal recurrence/order not supported")
        return {
            "verdict": "NO_TEMPORAL_ORDER",
            "level": VERDICT_LEVELS["NO_TEMPORAL_ORDER"],
            "path": path,
            "missing": missing,
        }

    path.append(f"temporal recurrence supported at q0={temporal.get('q0')}")

    # Classical/generic systems are not failed for lacking Hilbert-space evidence.
    if domain != "quantum_many_body":
        if rigidity["status"] == "SUPPORTED":
            path.append("rigidity supported")
            path.append("many-body spectral admissibility not applicable to this domain")
            return {
                "verdict": "RIGID_RECURRENCE",
                "level": VERDICT_LEVELS["RIGID_RECURRENCE"],
                "path": path,
                "missing": missing,
            }

        path.append("higher recurrence rigidity not established")
        return {
            "verdict": "TEMPORAL_RECURRENCE",
            "level": VERDICT_LEVELS["TEMPORAL_RECURRENCE"],
            "path": path,
            "missing": missing,
        }

    # Quantum many-body branch.
    if rigidity["status"] != "SUPPORTED":
        path.append("quantum recurrence rigidity not supported")
        return {
            "verdict": "TEMPORAL_RECURRENCE",
            "level": VERDICT_LEVELS["TEMPORAL_RECURRENCE"],
            "path": path,
            "missing": missing,
        }

    path.append("quantum recurrence rigidity supported")

    if collective["status"] in {"NOT_TESTED", "N/A"}:
        missing.append("collective")
    if spectral["status"] in {"NOT_TESTED", "N/A"}:
        missing.append("spectral")

    if missing:
        path.append("required quantum many-body sector evidence is missing")
        return {
            "verdict": "INSUFFICIENT_DOMAIN_EVIDENCE",
            "level": VERDICT_LEVELS["INSUFFICIENT_DOMAIN_EVIDENCE"],
            "path": path,
            "missing": missing,
        }

    if collective["status"] != "SUPPORTED":
        path.append("collective many-body order not fully supported")
        return {
            "verdict": "RIGID_RECURRENCE",
            "level": VERDICT_LEVELS["RIGID_RECURRENCE"],
            "path": path,
            "missing": missing,
        }

    path.append("collective many-body order supported")

    if spectral["status"] != "SUPPORTED":
        path.append("many-body spectral/eigenstate breadth not fully supported")
        return {
            "verdict": "COLLECTIVE_TEMPORAL_ORDER",
            "level": VERDICT_LEVELS["COLLECTIVE_TEMPORAL_ORDER"],
            "path": path,
            "missing": missing,
        }

    path.append("many-body spectral/eigenstate breadth supported")
    path.append("all TIME-CRYSTAL-I quantum gates satisfied")

    return {
        "verdict": "MANY_BODY_TIME_CRYSTAL_ADMISSIBLE",
        "level": VERDICT_LEVELS["MANY_BODY_TIME_CRYSTAL_ADMISSIBLE"],
        "path": path,
        "missing": missing,
    }
