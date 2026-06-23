import pandas as pd
from pathlib import Path

root = Path(r"c:\Users\i1n23\OneDrive - University of Southampton\Desktop\New folder\NAHES_Dataset\platform_from_scratch_master_2026-02-24")
in_xpt = root / "01_missingness_premerge" / "outputs" / "nhanes_xpt_clean"
in_ret = root / "01_missingness_premerge" / "outputs" / "retinal_clean" / "retinal_premerge_missingness_filtered.csv"
in_prx = root / "01_missingness_premerge" / "outputs" / "proxy_clean" / "proxy_premerge_missingness_filtered.csv"
out_dir = root / "02_harmonize_merge" / "outputs"
out_dir.mkdir(parents=True, exist_ok=True)

# same core table list as prior pipeline
file_names = ["BMX_D", "BPX_D", "DEMO_D", "HDL_D", "LEXABPI", "SLQ_D", "SMQ_D", "TCHOL_D", "TRIGLY_D"]

datasets = {}
for name in file_names:
    fp = in_xpt / f"{name}_premerge_missingness_filtered.csv"
    if not fp.exists():
        raise FileNotFoundError(f"Missing cleaned table: {fp}")
    datasets[name] = pd.read_csv(fp, low_memory=False)

# merge NHANES cleaned set
merged = datasets["DEMO_D"].copy()
id_col = "SEQN" if "SEQN" in merged.columns else merged.columns[0]
if id_col != "SEQN":
    merged = merged.rename(columns={id_col: "SEQN"})

for name in ["BMX_D", "BPX_D", "HDL_D", "LEXABPI", "SLQ_D", "SMQ_D", "TCHOL_D", "TRIGLY_D"]:
    df = datasets[name].copy()
    d_id = "SEQN" if "SEQN" in df.columns else df.columns[0]
    if d_id != "SEQN":
        df = df.rename(columns={d_id: "SEQN"})
    merged = merged.merge(df, on="SEQN", how="left", suffixes=("", f"_{name}"))

nh_out = out_dir / "NHANES_cleaned_stage2_merged.csv"
merged.to_csv(nh_out, index=False)

# merge retinal + proxy cleaned
ret = pd.read_csv(in_ret, low_memory=False)
prx = pd.read_csv(in_prx, low_memory=False)
for d in (ret, prx, merged):
    if "SEQN" not in d.columns:
        d.rename(columns={d.columns[0]: "SEQN"}, inplace=True)
    d["SEQN"] = pd.to_numeric(d["SEQN"], errors="coerce")

merged = merged.dropna(subset=["SEQN"]).drop_duplicates(subset=["SEQN"]).copy()
ret = ret.dropna(subset=["SEQN"]).drop_duplicates(subset=["SEQN"]).copy()
prx = prx.dropna(subset=["SEQN"]).drop_duplicates(subset=["SEQN"]).copy()

full = merged.merge(ret, on="SEQN", how="left", suffixes=("", "_ret"))
full = full.merge(prx, on="SEQN", how="left", suffixes=("", "_prx"))

full_out = out_dir / "NHANES_stage2_merged_with_retinal_proxy_from_premerge_clean.csv"
full.to_csv(full_out, index=False)

lines = [
    "STAGE-2 HARMONIZE/MERGE (USING PREMERGE-CLEAN SOURCES)",
    "="*70,
    f"NHANES cleaned merged shape: {merged.shape}",
    f"Retinal cleaned shape: {ret.shape}",
    f"Proxy cleaned shape: {prx.shape}",
    f"Final merged shape: {full.shape}",
    f"Retinal overlap with NHANES: {int(merged['SEQN'].isin(ret['SEQN']).sum())}",
    f"Proxy overlap with NHANES: {int(merged['SEQN'].isin(prx['SEQN']).sum())}",
]
(out_dir / "stage2_harmonize_merge_summary.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"Saved: {full_out}")
