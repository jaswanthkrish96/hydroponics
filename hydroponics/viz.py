"""Plotting helpers for NFT trial analysis."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .growth import logistic


def plot_growth_curves(fits: dict[str, dict], days: np.ndarray, out_path: str):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    t = np.linspace(days.min(), days.max(), 200)
    for label, fit in fits.items():
        ax.plot(t, logistic(t, fit["k"], fit["r"], fit["t0"]), label=label)
    ax.set_xlabel("Days after transplant")
    ax.set_ylabel("Fresh weight (g)")
    ax.set_title("Spinacia oleracea - NFT growth curves")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_parameter_bars(ranked, out_path: str):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(ranked["trial_id"], ranked["total_score"], color="#059669")
    ax.set_xlabel("Trial")
    ax.set_ylabel("Total score (0-100)")
    ax.set_title("NFT trial ranking")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
