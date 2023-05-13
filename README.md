# hydroponics

NFT (Nutrient Film Technique) hydroponics parameter optimization toolkit for **Spinacia oleracea** (spinach), built from doctoral trial work on controlled-environment cultivation.

## What it does

- Defines NFT operating parameters (pH, EC, water temperature, dissolved oxygen, photoperiod, PPFD, nitrogen) with literature-informed optimal windows
- Scores and ranks trial conditions against harvest yield (parameter compliance + yield contribution)
- Fits logistic growth curves to weekly fresh-weight series
- Reports parameter sensitivity (yield correlation) across a trial matrix

## Layout

| Path | Contents |
| --- | --- |
| `hydroponics/` | Python package: `parameters`, `growth`, `analysis`, `viz`, `cli` |
| `data/` | Trial condition matrix, weekly growth measurements, nutrient schedule |
| `tests/` | pytest suite |
| `docs/` | Trial design and results summary |
| `scripts/run_analysis.py` | End-to-end analysis entry point |

## Usage

```bash
pip install -r requirements.txt
python -m hydroponics.cli data/nft_trial_matrix.csv --sensitivity
python scripts/run_analysis.py
pytest -q
```

## Validated optimal window (Spinacia, NFT)

pH 6.0-6.4 | EC 1.5-1.8 mS/cm | water 19-22 C | DO >7.5 mg/L | 14-16 h photoperiod | PPFD 330-380 umol/m2/s | N 175-195 ppm

See `docs/results_summary.md` for the full findings.
