import os

from hydroponics.cli import main

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "nft_trial_matrix.csv")


def test_cli_runs(capsys):
    assert main([DATA]) == 0
    out = capsys.readouterr().out
    assert "trial_id" in out and "T10" in out


def test_cli_sensitivity(capsys):
    assert main([DATA, "--sensitivity"]) == 0
    out = capsys.readouterr().out
    assert "Parameter sensitivity" in out
