import os

import pandas as pd

from hydroponics.analysis import load_trials, rank_trials, parameter_sensitivity

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "nft_trial_matrix.csv")


def test_load_trials_columns():
    df = load_trials(DATA)
    assert "trial_id" in df.columns
    assert len(df) == 12


def test_rank_trials_sorted_desc():
    ranked = rank_trials(load_trials(DATA))
    scores = ranked["total_score"].tolist()
    assert scores == sorted(scores, reverse=True)


def test_best_trial_is_t10():
    ranked = rank_trials(load_trials(DATA))
    assert ranked.iloc[0]["trial_id"] == "T10"


def test_scores_bounded():
    ranked = rank_trials(load_trials(DATA))
    assert ranked["total_score"].between(0, 100).all()


def test_sensitivity_keys():
    sens = parameter_sensitivity(rank_trials(load_trials(DATA)))
    assert "ph" in sens and "ec_ms_cm" in sens
    assert all(-1.0 <= v <= 1.0 for v in sens.values())
