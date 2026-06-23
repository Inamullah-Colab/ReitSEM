import pandas as pd
import numpy as np
from pathlib import Path

root = Path(r"c:\Users\i1n23\OneDrive - University of Southampton\Desktop\New folder\NAHES_Dataset\platform_from_scratch_master_2026-02-24")
inp = root / "03_missingness_postmerge" / "outputs" / "NHANES_stage3_postmerge_missingness_filtered.csv"
out_dir = root / "04_retinal_qc" / "outputs"
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(inp, low_memory=False)
patterns = ["tortuosity", "curvature", "vessel_density", "fractal", "avr", "crae", "crve", "cup", "artery_", "vein_"]
num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
retinal_cols = sorted([c for c in num_cols if any(p in c.lower() for p in patterns)])

def local_neighbor_mean(series: pd.Series, i: int, k: int = 3):
    vals = []
    n = len(series)
    for d in range(1, k + 1):
        j1, j2 = i - d, i + d
        if j1 >= 0:
            v1 = series.iat[j1]
            if pd.notna(v1) and v1 >= 0:
                vals.append(float(v1))
        if j2 < n:
            v2 = series.iat[j2]
            if pd.notna(v2) and v2 >= 0:
                vals.append(float(v2))
    if vals:
        return float(np.mean(vals))
    valid = pd.to_numeric(series, errors='coerce')
    valid = valid[(valid >= 0) & valid.notna()]
    return float(valid.median()) if len(valid) else np.nan

fixed = df.copy()
rows = []
for c in retinal_cols:
    s = pd.to_numeric(fixed[c], errors='coerce')
    neg_idx = np.where(s.values < 0)[0]
    neg_before = int(len(neg_idx))
    penalty_abs_sum = float(np.abs(s[s < 0]).sum()) if neg_before > 0 else 0.0
    for i in neg_idx:
        s.iat[i] = local_neighbor_mean(s, i, k=3)
    fixed[c] = s
    neg_after = int((pd.to_numeric(fixed[c], errors='coerce') < 0).sum())
    rows.append({"column": c, "neg_before": neg_before, "neg_after": neg_after, "penalty_abs_sum_before_fix": penalty_abs_sum})

rep = pd.DataFrame(rows).sort_values(["neg_before", "column"], ascending=[False, True])
fixed.to_csv(out_dir / "NHANES_stage4_retinal_qc_fixed.csv", index=False)
rep.to_csv(out_dir / "retinal_negative_penalty_and_fix_report.csv", index=False)

summary = [
    "STAGE-4 RETINAL QC SUMMARY",
    "="*70,
    f"Input shape: {df.shape}",
    f"Retinal columns detected: {len(retinal_cols)}",
    f"Columns with negatives before fix: {int((rep['neg_before'] > 0).sum()) if len(rep) else 0}",
    f"Total negative values before fix: {int(rep['neg_before'].sum()) if len(rep) else 0}",
    f"Total negative values after fix: {int(rep['neg_after'].sum()) if len(rep) else 0}",
    f"Output shape: {fixed.shape}",
]
(out_dir / "stage4_retinal_qc_summary.txt").write_text("\n".join(summary), encoding="utf-8")
print("\n".join(summary))
