#!/usr/bin/env python3
"""Run the full NFT trial analysis: ranking + sensitivity + growth fits."""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from hydroponics.analysis import load_trials, rank_trials, parameter_sensitivity
from hydroponics.growth import fit_growth_curve

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, "..", "data")


def main() -> int:
    trials = load_trials(os.path.join(DATA, "nft_trial_matrix.csv"))
    ranked = rank_trials(trials)
    print("=== Trial ranking ===")
    print(ranked[["trial_id", "total_score", "yield_g_per_plant"]].to_string(index=False))

    print("\n=== Parameter sensitivity ===")
    for name, corr in parameter_sensitivity(ranked).items():
        print(f"  {name:24s} {corr:+.3f}")

    growth = pd.read_csv(os.path.join(DATA, "growth_measurements.csv"))
    print("\n=== Growth fits (top trials) ===")
    for tid, grp in growth.groupby("trial_id"):
        fit = fit_growth_curve(grp["day"].values, grp["mean_fresh_weight_g"].values)
        print(f"  {tid}: k={fit['k']:.1f}g r={fit['r']:.3f}/day t0={fit['t0']:.1f}d R2={fit['r2']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
