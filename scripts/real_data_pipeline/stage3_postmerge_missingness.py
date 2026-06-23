import pandas as pd
from pathlib import Path

root = Path(r"c:\Users\i1n23\OneDrive - University of Southampton\Desktop\New folder\NAHES_Dataset\platform_from_scratch_master_2026-02-24")
inp = root / "02_harmonize_merge" / "outputs" / "NHANES_stage2_merged_with_retinal_proxy_from_premerge_clean.csv"
out_dir = root / "03_missingness_postmerge" / "outputs"
out_dir.mkdir(parents=True, exist_ok=True)

threshold = 0.30

df = pd.read_csv(inp, low_memory=False)
base_protected = {"SEQN", "BPXSY1", "BPXDI1", "BPXPLS", "BPXPULS", "URXUMS", "LBXSBU", "LBDSTRSI"}
retinal_patterns = ["tortuosity", "curvature", "vessel_density", "fractal", "avr", "crae", "crve", "cup", "artery_", "vein_"]
retinal_cols = [c for c in df.columns if any(p in c.lower() for p in retinal_patterns)]
protected = set(base_protected).union(retinal_cols)

miss_df = df.isna().mean().rename("missing_rate").reset_index().rename(columns={"index":"column"})
high = miss_df[miss_df["missing_rate"] > threshold].copy()
high["protected"] = high["column"].isin(protected)

# Do not drop protected columns
drop_cols = high.loc[~high["protected"], "column"].tolist()
keep_cols = [c for c in df.columns if c not in set(drop_cols)]
filtered = df[keep_cols].copy()

filtered.to_csv(out_dir / "NHANES_stage3_postmerge_missingness_filtered.csv", index=False)
miss_df.to_csv(out_dir / "missing_rate_all_columns.csv", index=False)
high.to_csv(out_dir / "missing_above_30pct_with_protection_flag.csv", index=False)
pd.DataFrame({"column": sorted(protected)}).to_csv(out_dir / "protected_columns_missingness.csv", index=False)
pd.DataFrame({"column": keep_cols}).to_csv(out_dir / "kept_columns_after_missingness.csv", index=False)
pd.DataFrame({"column": drop_cols}).to_csv(out_dir / "dropped_columns_after_missingness.csv", index=False)

summary = [
    "STAGE-3 POSTMERGE MISSINGNESS SUMMARY",
    "="*70,
    f"Input shape: {df.shape}",
    f"Threshold: > {int(threshold*100)}%",
    f"Retinal columns protected: {len(retinal_cols)}",
    f"Protected columns total: {len(protected)}",
    f"Columns above threshold: {len(high)}",
    f"Dropped columns: {len(drop_cols)}",
    f"Kept columns: {len(keep_cols)}",
    f"Output shape: {filtered.shape}",
]
(out_dir / "stage3_postmerge_missingness_summary.txt").write_text("\n".join(summary), encoding="utf-8")
print("\n".join(summary))
