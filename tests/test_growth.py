import numpy as np

from hydroponics.growth import logistic, fit_growth_curve, growth_rate_at, doubling_time


def test_logistic_endpoints():
    t = np.array([0.0, 100.0])
    y = logistic(t, k=50.0, r=0.2, t0=20.0)
    assert y[0] < 1.0
    assert abs(y[1] - 50.0) < 1.0


def test_fit_recovers_params():
    days = np.array([7, 14, 21, 28, 35, 42], dtype=float)
    true = logistic(days, k=45.0, r=0.18, t0=22.0)
    fit = fit_growth_curve(days, true)
    assert abs(fit["k"] - 45.0) < 5.0
    assert fit["r"] > 0.05
    assert fit["r2"] > 0.95


def test_growth_rate_peaks_near_inflection():
    fit = {"k": 45.0, "r": 0.18, "t0": 22.0, "r2": 0.99}
    assert growth_rate_at(fit, 22.0) > growth_rate_at(fit, 5.0)


def test_doubling_time_positive():
    fit = {"k": 45.0, "r": 0.18, "t0": 22.0, "r2": 0.99}
    assert 0 < doubling_time(fit) < 30
