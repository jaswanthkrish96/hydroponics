"""NFT system parameter definitions and validation for leafy greens."""

from dataclasses import dataclass, asdict


@dataclass
class NFTParameters:
    """Operating parameters for a Nutrient Film Technique channel."""

    ph: float
    ec_ms_cm: float
    water_temp_c: float
    dissolved_oxygen_mg_l: float
    photoperiod_h: float
    ppfd_umol_m2_s: float
    nitrogen_ppm: float

    def to_dict(self) -> dict:
        return asdict(self)


# Literature-informed optimal windows for Spinacia oleracea in NFT.
OPTIMAL_RANGES = {
    "ph": (5.8, 6.5),
    "ec_ms_cm": (1.4, 1.9),
    "water_temp_c": (18.0, 23.0),
    "dissolved_oxygen_mg_l": (6.0, 9.0),
    "photoperiod_h": (12.0, 16.0),
    "ppfd_umol_m2_s": (250.0, 400.0),
    "nitrogen_ppm": (150.0, 200.0),
}


def in_range(params: NFTParameters, name: str) -> bool:
    lo, hi = OPTIMAL_RANGES[name]
    return lo <= getattr(params, name) <= hi


def validate(params: NFTParameters) -> list[str]:
    """Return names of parameters outside their optimal window."""
    return [name for name in OPTIMAL_RANGES if not in_range(params, name)]


def compliance_score(params: NFTParameters) -> float:
    """Fraction of parameters inside their optimal window (0.0 - 1.0)."""
    violations = validate(params)
    return 1.0 - len(violations) / len(OPTIMAL_RANGES)
