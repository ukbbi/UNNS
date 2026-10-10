from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UPIResult:
    value: float
    band: str


def compute_upi(D: float, R: float, M: float, S: float) -> UPIResult:
    """
    Compute the foundational scalar UPI = (D * R) / (M + S).

    SCR-I status: diagnostic only. This function must not be wired into
    candidate pruning in the v0.1 protocol.
    """
    if D < 0 or not (0 <= R <= 1) or M < 0 or S < 0:
        raise ValueError("UPI inputs outside foundational domains.")
    denom = M + S
    if denom == 0:
        value = float("inf") if D * R > 0 else 0.0
    else:
        value = (D * R) / denom

    if value < 1:
        band = "SAFE"
    elif value <= 3:
        band = "CAUTION"
    else:
        band = "HIGH_RISK"
    return UPIResult(value=value, band=band)
