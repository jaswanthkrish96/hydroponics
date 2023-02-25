from hydroponics.parameters import (
    NFTParameters, OPTIMAL_RANGES, validate, compliance_score,
)


def optimal():
    return NFTParameters(
        ph=6.1, ec_ms_cm=1.6, water_temp_c=20.5,
        dissolved_oxygen_mg_l=7.5, photoperiod_h=14.0,
        ppfd_umol_m2_s=330.0, nitrogen_ppm=180.0,
    )


def test_optimal_params_pass_validation():
    assert validate(optimal()) == []


def test_out_of_range_flagged():
    p = optimal()
    p.ph = 7.5
    assert "ph" in validate(p)


def test_compliance_score_full():
    assert compliance_score(optimal()) == 1.0


def test_compliance_score_partial():
    p = optimal()
    p.ph = 7.5
    p.water_temp_c = 28.0
    expected = 1.0 - 2.0 / len(OPTIMAL_RANGES)
    assert abs(compliance_score(p) - expected) < 1e-9


def test_boundaries_inclusive():
    p = optimal()
    p.ph = 5.8
    assert "ph" not in validate(p)
    p.ph = 6.5
    assert "ph" not in validate(p)
