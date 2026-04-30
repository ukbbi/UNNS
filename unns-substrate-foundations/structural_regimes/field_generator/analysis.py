def normalize_result(R):
    """
    Normalize engine output schema (JS ↔ Python compatibility).
    Supports both snake_case and camelCase.
    """

    return {
        "giant_ratio": R.get("giant_ratio") or R.get("giantRatio") or 0,
        "kappa_connect": R.get("kappa_connect") or R.get("kappaConnect") or 0,
        "verdict": R.get("verdict") or "UNKNOWN",
    }


def compute_commutator(R1, R2):
    R1n = normalize_result(R1)
    R2n = normalize_result(R2)

    return {
        "delta_giant": R1n["giant_ratio"] - R2n["giant_ratio"],
        "delta_kappa": R1n["kappa_connect"] - R2n["kappa_connect"],
        "different_verdict": R1n["verdict"] != R2n["verdict"],
    }


def detect_transition(mu_values, results):
    transitions = []

    if not results:
        return transitions

    prev = normalize_result(results[0])["verdict"]

    for mu, res in zip(mu_values, results):
        current = normalize_result(res)["verdict"]

        if current != prev:
            transitions.append((mu, prev, current))
            prev = current

    return transitions