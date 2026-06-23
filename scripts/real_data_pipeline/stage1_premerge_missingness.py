import pandas as pd
from pathlib import Path

root = Path(r"c:\Users\i1n23\OneDrive - University of Southampton\Desktop\New folder\NAHES_Dataset\platform_from_scratch_master_2026-02-24")
out = root / "01_missingness_premerge" / "outputs"
(out / "nhanes_xpt_clean").mkdir(parents=True, exist_ok=True)
(out / "retinal_clean").mkdir(parents=True, exist_ok=True)
(out / "proxy_clean").mkdir(parents=True, exist_ok=True)

threshold = 0.30
# known key/model protection list (only applied if column exists)
protect_global = {
    "SEQN","BPXSY1","BPXDI1","BPXPLS","BPXPULS","URXUMS","LBXSBU","LBDSTRSI",
    "RIDAGEEX","RIDRETH1","INDFMPIR","DMDHRGND","DMDEDUC3",
    "GREF_AMR","GREF_EUR","GREF_SAS","GREF_entropy"
}

summary_rows = []

# NHANES XPT per-file premerge filtering
xpt_dir = root / "00_raw_sources" / "nhanes_xpt"
for fp in sorted(xpt_dir.glob("*.xpt")):
    df = pd.read_sas(str(fp), format="xport")
    cols = list(df.columns)
    id_col = cols[0] if cols else "SEQN"
    protect = set([id_col]).union({c for c in protect_global if c in df.columns})

    miss = df.isna().mean()
    drop_cols = [c for c, r in miss.items() if (r > threshold and c not in protect)]
    keep_cols = [c for c in df.columns if c not in set(drop_cols)]
    d2 = df[keep_cols].copy()

    d2.to_csv(out / "nhanes_xpt_clean" / f"{fp.stem}_premerge_missingness_filtered.csv", index=False)
    miss.rename("missing_rate").to_csv(out / "nhanes_xpt_clean" / f"{fp.stem}_missing_rate.csv", header=True)
    pd.DataFrame({"column": drop_cols}).to_csv(out / "nhanes_xpt_clean" / f"{fp.stem}_dropped_cols.csv", index=False)

    summary_rows.append({
        "source":"nhanes_xpt",
        "table":fp.stem,
        "rows":len(df),
        "cols_in":df.shape[1],
        "cols_out":d2.shape[1],
        "dropped":len(drop_cols),
        "protected_in_table":len(protect),
    })

# Retinal premerge filtering
ret_fp = root / "00_raw_sources" / "retinal_traits" / "macular_zone_b_imputed_with_seq.csv"
ret = pd.read_csv(ret_fp, low_memory=False)
ret_id = "SEQN" if "SEQN" in ret.columns else ret.columns[0]
protect = {ret_id}
miss = ret.isna().mean()
drop_cols = [c for c, r in miss.items() if (r > threshold and c not in protect)]
ret2 = ret[[c for c in ret.columns if c not in set(drop_cols)]].copy()
ret2.to_csv(out / "retinal_clean" / "retinal_premerge_missingness_filtered.csv", index=False)
miss.rename("missing_rate").to_csv(out / "retinal_clean" / "retinal_missing_rate.csv", header=True)
pd.DataFrame({"column": drop_cols}).to_csv(out / "retinal_clean" / "retinal_dropped_cols.csv", index=False)
summary_rows.append({"source":"retinal","table":"macular_zone_b_imputed_with_seq","rows":len(ret),"cols_in":ret.shape[1],"cols_out":ret2.shape[1],"dropped":len(drop_cols),"protected_in_table":len(protect)})

# Proxy premerge filtering
prx_fp = root / "00_raw_sources" / "proxy_genetics" / "NHANES_1000G_proxy_only.csv"
prx = pd.read_csv(prx_fp, low_memory=False)
prx_id = "SEQN" if "SEQN" in prx.columns else prx.columns[0]
protect = {prx_id}.union({c for c in ["GREF_AMR","GREF_EUR","GREF_SAS","GREF_entropy"] if c in prx.columns})
miss = prx.isna().mean()
drop_cols = [c for c, r in miss.items() if (r > threshold and c not in protect)]
prx2 = prx[[c for c in prx.columns if c not in set(drop_cols)]].copy()
prx2.to_csv(out / "proxy_clean" / "proxy_premerge_missingness_filtered.csv", index=False)
miss.rename("missing_rate").to_csv(out / "proxy_clean" / "proxy_missing_rate.csv", header=True)
pd.DataFrame({"column": drop_cols}).to_csv(out / "proxy_clean" / "proxy_dropped_cols.csv", index=False)
summary_rows.append({"source":"proxy","table":"NHANES_1000G_proxy_only","rows":len(prx),"cols_in":prx.shape[1],"cols_out":prx2.shape[1],"dropped":len(drop_cols),"protected_in_table":len(protect)})

summary = pd.DataFrame(summary_rows)
summary.to_csv(out / "stage1_premerge_missingness_summary.csv", index=False)

lines = [
    "STAGE-1 PREMERGE MISSINGNESS SUMMARY",
    "="*70,
    f"Threshold: > {int(threshold*100)}%",
    "",
    summary.to_string(index=False)
]
(out / "stage1_premerge_missingness_summary.txt").write_text("\n".join(lines), encoding="utf-8")

print(summary.to_string(index=False))
print(f"Saved summary: {out / 'stage1_premerge_missingness_summary.csv'}")
