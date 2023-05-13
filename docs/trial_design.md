# NFT Trial Design - Spinacia oleracea

## Objective

Identify the operating window that maximizes fresh-weight yield of spinach in Nutrient Film Technique channels, using a structured parameter matrix.

## Setup

- 12 trial conditions (T01-T12), 8 plants per channel, randomized channel assignment
- NFT channels: 2% slope, ~5 L/min recirculation, 35-day harvest window
- Parameters varied: pH (5.4-7.0), EC (1.1-2.0 mS/cm), water temp (19-25 C), DO (5.8-8.1 mg/L), photoperiod (12-16 h), PPFD (250-400 umol/m2/s), nitrogen (140-210 ppm)
- Weekly destructive sampling on 3 plants per channel for fresh weight

## Measurements

- `nft_trial_matrix.csv`: condition matrix + harvest yield per plant
- `growth_measurements.csv`: weekly fresh-weight series for the top 4 trials
- `nutrient_schedule.csv`: 6-week fertigation schedule (N-P-K-Ca-Mg-Fe)

## Analysis

Run `python scripts/run_analysis.py` or `python -m hydroponics.cli data/nft_trial_matrix.csv --sensitivity`.
