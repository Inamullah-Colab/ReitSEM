#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def forest_triplet_png(
    df: pd.DataFrame,
    out_png: Path,
    title: str,
    top_n: int | None = None,
    pathway_prefix: str = "",
    pathway_suffix: str = " | Z,G",
) -> None:
    """Render the paper-style forest plot used to rank mediation pathways."""

    d = df.copy()
    # The paper ranks pathways by the magnitude of the indirect effect so the
    # strongest retina-hub mediation signals appear first.
    d["abs_nie"] = d["NIE_Estimate"].abs()
    d = d.sort_values("abs_nie", ascending=False).drop(columns=["abs_nie"]).reset_index(drop=True)
    if top_n is not None and top_n > 0:
        d = d.head(int(top_n)).reset_index(drop=True)

    # Offsetting the TE, NDE, and NIE markers keeps the three estimates
    # readable for each pathway on the same horizontal row.
    y = np.arange(len(d))
    y_te = y + 0.22
    y_nde = y
    y_nie = y - 0.22

    fig_h = max(8, 0.36 * len(d))
    fig, ax = plt.subplots(figsize=(13, fig_h))
    ax.axvline(0, color="gray", linestyle="--", linewidth=1)

    # TE
    x = d["TE_Estimate"].values
    lo = d["TE_CI_Lower"].values
    hi = d["TE_CI_Upper"].values
    xerr = np.vstack([x - lo, hi - x])
    ax.errorbar(x, y_te, xerr=xerr, fmt="o", color="#1f77b4", ecolor="#1f77b4", capsize=3, label="TE")

    # NDE
    x = d["NDE_Estimate"].values
    lo = d["NDE_CI_Lower"].values
    hi = d["NDE_CI_Upper"].values
    xerr = np.vstack([x - lo, hi - x])
    ax.errorbar(x, y_nde, xerr=xerr, fmt="s", color="#2ca02c", ecolor="#2ca02c", capsize=3, label="NDE")

    # NIE
    x = d["NIE_Estimate"].values
    lo = d["NIE_CI_Lower"].values
    hi = d["NIE_CI_Upper"].values
    xerr = np.vstack([x - lo, hi - x])
    ax.errorbar(x, y_nie, xerr=xerr, fmt="^", color="#d62728", ecolor="#d62728", capsize=3, label="NIE")

    for i, row in d.iterrows():
        if bool(row.get("NIE_Significant", False)):
            ax.text(row["NIE_CI_Upper"] + 0.002, y_nie[i], "*", color="#d62728", va="center", fontsize=10)

    ax.set_yticks(y)
    ax.set_yticklabels(pathway_prefix + d["Pathway"].astype(str) + pathway_suffix)
    ax.set_xlabel("Effect Size")
    ax.set_title(title)
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(out_png, dpi=320, bbox_inches="tight")
    plt.close(fig)


def summary_bar_png(df: pd.DataFrame, out_png: Path, title: str) -> None:
    """Aggregate pathway estimates into exposure-outcome summaries."""

    agg = df.copy()
    agg["Exposure"] = agg["Pathway"].str.split(" -> ").str[0]
    agg["Outcome"] = agg["Pathway"].str.split(" -> ").str[-1]
    g = (
        agg.groupby(["Exposure", "Outcome"], as_index=False)
        .agg(
            TE=("TE_Estimate", "mean"),
            NDE=("NDE_Estimate", "mean"),
            mean_abs_NIE=("NIE_Estimate", lambda s: s.abs().mean()),
        )
    )
    g["label"] = g["Exposure"] + " -> " + g["Outcome"]
    x = np.arange(len(g))
    w = 0.25

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(x - w, g["TE"], width=w, label="TE", color="#1f77b4")
    ax.bar(x, g["NDE"], width=w, label="NDE", color="#2ca02c")
    ax.bar(x + w, g["mean_abs_NIE"], width=w, label="Mean |NIE|", color="#d62728")
    ax.axhline(0, color="gray", linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(g["label"], rotation=20, ha="right")
    ax.set_ylabel("Effect")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_png, dpi=320, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Generate SEM paper-style PNGs from mediation tables.")
    ap.add_argument("--base-dir", required=True)
    ap.add_argument("--results-root", required=True, help="Relative path under base-dir to mediation results root.")
    ap.add_argument("--datasets", nargs="+", required=True, help="Dataset subfolder names under results-root.")
    ap.add_argument(
        "--pathway-prefix",
        default="",
        help="Prefix prepended to each pathway label (e.g., 'Z,G | ').",
    )
    ap.add_argument(
        "--pathway-suffix",
        default=" | Z,G",
        help="Suffix appended to each pathway label (default: ' | Z,G').",
    )
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    base = Path(args.base_dir)
    root = base / args.results_root

    for ds in args.datasets:
        fp = root / ds / "mediation_table_all_combos.csv"
        if not fp.exists():
            continue
        df = pd.read_csv(fp)
        # Full ranking across every pathway in the dataset.
        forest_triplet_png(
            df,
            root / ds / "sem_paper_forest_te_nde_nie.png",
            f"SEM Mediation Effects (TE/NDE/NIE) - {ds}",
            pathway_prefix=args.pathway_prefix,
            pathway_suffix=args.pathway_suffix,
        )
        # Compact ranking used when only the strongest mediator-like pathways
        # should be shown in the paper or on GitHub.
        forest_triplet_png(
            df,
            root / ds / "sem_paper_forest_te_nde_nie_top30.png",
            f"SEM Mediation Effects (Top 30 by |NIE|) - {ds}",
            top_n=30,
            pathway_prefix=args.pathway_prefix,
            pathway_suffix=args.pathway_suffix,
        )
        # Exposure-outcome summary view used to complement the detailed forest plot.
        summary_bar_png(
            df,
            root / ds / "sem_paper_summary_te_nde_nie.png",
            f"SEM Summary by Exposure-Outcome - {ds}",
        )


if __name__ == "__main__":
    main()
