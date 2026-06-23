import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

root = Path(r"c:\Users\i1n23\OneDrive - University of Southampton\Desktop\New folder\NAHES_Dataset\platform_from_scratch_master_2026-02-24")
inp = root / "04_retinal_qc" / "outputs" / "NHANES_stage4_retinal_qc_fixed.csv"
out = root / "05_multicollinearity" / "final"
out.mkdir(parents=True, exist_ok=True)

rho = 0.70

df = pd.read_csv(inp, low_memory=False)
num = df.select_dtypes(include=[np.number]).copy()
if "SEQN" in num.columns:
    num = num.drop(columns=["SEQN"])

# remove unusable numeric cols
all_missing = [c for c in num.columns if num[c].isna().all()]
num = num.drop(columns=all_missing)
const = [c for c in num.columns if num[c].nunique(dropna=True) <= 1]
num = num.drop(columns=const)

# impute for stable correlation
num_imp = num.copy()
for c in num_imp.columns:
    med = pd.to_numeric(num_imp[c], errors='coerce').median(skipna=True)
    num_imp[c] = pd.to_numeric(num_imp[c], errors='coerce').fillna(0.0 if pd.isna(med) else med)

keep = list(num_imp.columns)
dropped = []

# strict global pruning to enforce max |rho| <= 0.70
while True:
    corr = num_imp[keep].corr(method="spearman").abs()
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    max_corr = upper.max().max()
    if pd.isna(max_corr) or max_corr <= rho:
        break

    ij = np.where(upper.values == max_corr)
    i, j = int(ij[0][0]), int(ij[1][0])
    a, b = upper.index[i], upper.columns[j]

    mean_abs = corr.mean(axis=0)
    drop_col = a if mean_abs[a] >= mean_abs[b] else b
    keep.remove(drop_col)
    dropped.append({"dropped_feature": drop_col, "trigger_pair_a": a, "trigger_pair_b": b, "trigger_corr": float(max_corr)})

pruned = df[[c for c in df.columns if (c not in num.columns) or (c in set(keep))]].copy()
pruned.to_csv(out / "pruned_corr70.csv", index=False)
pd.DataFrame(dropped).to_csv(out / "dropped_by_corr70.csv", index=False)

# verify residual > 0.70
corr_after = num_imp[keep].corr(method="spearman")
up_after = corr_after.abs().where(np.triu(np.ones(corr_after.shape), k=1).astype(bool))
max_after = float(up_after.max().max()) if corr_after.shape[0] > 1 else 0.0
resid = []
if corr_after.shape[0] > 1:
    for c in up_after.columns:
        rows = up_after.index[up_after[c] > rho].tolist()
        for r in rows:
            resid.append({"feature_a": r, "feature_b": c, "abs_corr": float(up_after.loc[r, c])})
pd.DataFrame(resid).to_csv(out / "residual_pairs_gt_0p70.csv", index=False)

# polished low-density clustermap (display subset only for readability)
plot_df = num_imp[keep].copy()
if plot_df.shape[1] > 22:
    vars_ = plot_df.var().sort_values(ascending=False)
    plot_cols = vars_.head(22).index.tolist()
    plot_df = plot_df[plot_cols]

corr_plot = plot_df.corr(method="spearman")

sns.set_theme(style="white")
g = sns.clustermap(
    corr_plot,
    cmap="RdBu_r",
    center=0,
    vmin=-1,
    vmax=1,
    linewidths=0.30,
    linecolor="white",
    annot=False,
    figsize=(14, 12),
    cbar_kws={"label": "Spearman $\\rho$"},
)
g.ax_heatmap.set_title("Correlation After Pruning ($\\rho \\leq 0.70$)", pad=16, fontsize=14)
g.ax_heatmap.tick_params(axis='x', labelrotation=45, labelsize=8)
g.ax_heatmap.tick_params(axis='y', labelsize=8)
g.fig.savefig(out / "correlation_clustermap_corr70_final.png", dpi=320, bbox_inches="tight")
plt.close(g.fig)

pd.DataFrame({"plotted_feature": corr_plot.columns.tolist()}).to_csv(out / "clustermap_plotted_features.csv", index=False)

summary = pd.DataFrame([{
    "rows": int(df.shape[0]),
    "cols_total_before": int(df.shape[1]),
    "numeric_cols_before": int(num.shape[1]),
    "dropped_all_missing": int(len(all_missing)),
    "dropped_constant": int(len(const)),
    "dropped_by_corr70": int(len(dropped)),
    "numeric_cols_after": int(len(keep)),
    "cols_total_after": int(pruned.shape[1]),
    "max_abs_corr_after": max_after,
    "residual_pairs_gt_0p70": int(len(resid)),
    "displayed_in_clustermap": int(corr_plot.shape[0]),
}])
summary.to_csv(out / "summary_corr70_final.csv", index=False)
print(summary.to_string(index=False))
print(f"Saved final folder: {out}")
