import pandas as pd
from pathlib import Path

root = Path(r"c:\Users\i1n23\OneDrive - University of Southampton\Desktop\New folder\NAHES_Dataset\platform_from_scratch_master_2026-02-24")
inp = root / "05_multicollinearity" / "final" / "pruned_corr70.csv"
out_dir = root / "06_hemodynamics_completion" / "corr70_outputs"
out_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(inp, low_memory=False)
required_y = ["BPXSY1", "BPXDI1", "BPXPLS", "BPXPULS"]
missing_y = [c for c in required_y if c not in df.columns]
if missing_y:
    bpx = pd.read_csv(root / "01_missingness_premerge" / "outputs" / "nhanes_xpt_clean" / "BPX_D_premerge_missingness_filtered.csv", low_memory=False)
    if "SEQN" not in bpx.columns:
        bpx = bpx.rename(columns={bpx.columns[0]: "SEQN"})
    add_cols = ["SEQN"] + [c for c in required_y if c in bpx.columns]
    df = df.merge(bpx[add_cols], on="SEQN", how="left", suffixes=("", "_restore"))

roles = {
    "X_exposures": ["URXUMS", "LBXSBU", "LBDSTRSI"],
    "Y_outcomes_hemo": required_y,
    "M_mediators": ["Artery_Squared_curvature_tortuosity", "Squared_curvature_tortuosity", "Vein_Distance_tortuosity", "Vein_Squared_curvature_tortuosity"],
    "Z_covars": ["RIDAGEEX", "RIDRETH1", "INDFMPIR", "DMDHRGND", "DMDEDUC3"],
    "G_covars": ["GREF_AMR", "GREF_EUR", "GREF_SAS", "GREF_entropy"],
}
rows=[]
for role, cols in roles.items():
    present=[c for c in cols if c in df.columns]
    missing=[c for c in cols if c not in df.columns]
    rows.append({"role":role,"required":len(cols),"present":len(present),"missing":len(missing),"present_cols":"|".join(present),"missing_cols":"|".join(missing)})
rep=pd.DataFrame(rows)
rep.to_csv(out_dir / "model_role_compatibility_stage6_corr70.csv", index=False)
df.to_csv(out_dir / "NHANES_stage6_hemodynamics_checked_corr70.csv", index=False)

lines=[
"STAGE-6 HEMODYNAMICS CHECK (corr70 path)",
"="*70,
f"Input shape: {pd.read_csv(inp, low_memory=False).shape}",
f"Output shape: {df.shape}",
f"Y present: {sum(c in df.columns for c in required_y)}/{len(required_y)}"
]
(out_dir / "stage6_hemodynamics_summary_corr70.txt").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
