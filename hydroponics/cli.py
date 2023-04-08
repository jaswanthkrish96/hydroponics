"""CLI entry point for NFT trial analysis."""

import argparse

from .analysis import load_trials, rank_trials, parameter_sensitivity


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="nft-analyze",
        description="Rank NFT hydroponics trials for Spinacia oleracea",
    )
    parser.add_argument("trials_csv", help="trial matrix CSV")
    parser.add_argument("--sensitivity", action="store_true",
                        help="print parameter sensitivity (yield correlation)")
    args = parser.parse_args(argv)

    ranked = rank_trials(load_trials(args.trials_csv))
    cols = ["trial_id", "total_score", "yield_g_per_plant"]
    print(ranked[cols].to_string(index=False))

    if args.sensitivity:
        print("\nParameter sensitivity (|corr| with yield):")
        for name, corr in parameter_sensitivity(ranked).items():
            print(f"  {name:24s} {corr:+.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
