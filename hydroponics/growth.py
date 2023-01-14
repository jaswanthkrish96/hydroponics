"""Logistic growth modeling for NFT-grown Spinacia oleracea."""

import numpy as np


def logistic(t: np.ndarray, k: float, r: float, t0: float) -> np.ndarray:
    """Logistic growth curve: carrying capacity k, rate r, inflection t0."""
    return k / (1.0 + np.exp(-r * (t - t0)))


def _residual(days, fw, k, r, t0) -> float:
    return float(np.sum((logistic(days, k, r, t0) - fw) ** 2))


def fit_growth_curve(days: np.ndarray, fresh_weight_g: np.ndarray) -> dict:
    """Fit a logistic curve: coarse grid search, then joint coordinate descent.

    Returns fitted parameters {k, r, t0} and R^2 of the fit.
    """
    days = np.asarray(days, dtype=float)
    fw = np.asarray(fresh_weight_g, dtype=float)

    # stage 1: coarse grid for the basin of attraction
    best = (np.inf, fw.max() * 1.1, 0.2, days[len(days) // 2])
    for k in np.linspace(fw.max(), fw.max() * 1.5, 50):
        for r in np.linspace(0.05, 0.6, 50):
            for t0 in np.linspace(days.min(), days.max(), 15):
                resid = _residual(days, fw, k, r, t0)
                if resid < best[0]:
                    best = (resid, k, r, t0)

    # stage 2: joint coordinate descent with shrinking windows
    resid, k, r, t0 = best
    for span in (0.5, 0.25, 0.1, 0.05, 0.02):
        improved = True
        while improved:
            improved = False
            for k2 in np.linspace(k * (1 - span), k * (1 + span), 15):
                cand = _residual(days, fw, k2, r, t0)
                if cand < resid:
                    resid, k, improved = cand, k2, True
            for r2 in np.linspace(r * (1 - span), r * (1 + span), 15):
                cand = _residual(days, fw, k, r2, t0)
                if cand < resid:
                    resid, r, improved = cand, r2, True
            for t02 in np.linspace(t0 - span * 20, t0 + span * 20, 15):
                cand = _residual(days, fw, k, r, t02)
                if cand < resid:
                    resid, t0, improved = cand, t02, True

    ss_tot = float(np.sum((fw - fw.mean()) ** 2))
    r2 = 1.0 - resid / ss_tot if ss_tot > 0 else 0.0
    return {"k": float(k), "r": float(r), "t0": float(t0), "r2": float(r2)}


def growth_rate_at(fit: dict, day: float) -> float:
    """Instantaneous growth rate (g/day) at a given day."""
    k, r, t0 = fit["k"], fit["r"], fit["t0"]
    return k * r * np.exp(-r * (day - t0)) / (1.0 + np.exp(-r * (day - t0))) ** 2


def doubling_time(fit: dict) -> float:
    """Approximate mass doubling time (days) around the inflection point."""
    return float(np.log(2) / fit["r"]) if fit["r"] > 0 else float("inf")
