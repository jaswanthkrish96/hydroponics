"""Trial analysis: score NFT condition matrices against harvest yield."""

import numpy as np
import pandas as pd

from .parameters import NFTParameters, OPTIMAL_RANGES, compliance_score


def load_trials(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"trial_id", "ph", "ec_ms_cm", "water_temp_c",
                "dissolved_oxygen_mg_l", "photoperiod_h", "ppfd_umol_m2_s",
                "nitrogen_ppm", "yield_g_per_plant"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"trial matrix missing columns: {sorted(missing)}")
    return df


def score_trial(row: pd.Series) -> float:
    """Score a trial 0-100: 60% parameter compliance + 40% yield vs cohort max."""
    params = NFTParameters(
        ph=row.ph, ec_ms_cm=row.ec_ms_cm, water_temp_c=row.water_temp_c,
        dissolved_oxygen_mg_l=row.dissolved_oxygen_mg_l,
        photoperiod_h=row.photoperiod_h, ppfd_umol_m2_s=row.ppfd_umol_m2_s,
        nitrogen_ppm=row.nitrogen_ppm,
    )
    return round(compliance_score(params) * 60.0, 2)


def rank_trials(df: pd.DataFrame) -> pd.DataFrame:
    """Attach compliance and total scores; return sorted descending."""
    out = df.copy()
    out["param_score"] = out.apply(score_trial, axis=1)
    ymax = out["yield_g_per_plant"].max()
    out["yield_score"] = (out["yield_g_per_plant"] / ymax * 40.0).round(2)
    out["total_score"] = (out["param_score"] + out["yield_score"]).round(2)
    return out.sort_values("total_score", ascending=False).reset_index(drop=True)
