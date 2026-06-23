import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import yeojohnson


ROOT = Path(r"c:\Users\i1n23\OneDrive - University of Southampton\Desktop\New folder\NAHES_Dataset\platform_from_scratch_master_2026-02-24")
INP = ROOT / "06_hemodynamics_completion" / "corr70_outputs" / "NHANES_stage6_hemodynamics_checked_corr70.csv"
OUT = ROOT / "07_transform_benchmark" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

EXPOSURES = ["URXUMA", "URXCRS", "LBXSBU", "LBDSTRSI"]
OUTCOMES = ["BPXSY1", "BPXDI1", "BPXPLS", "BPXPULS"]
MEDIATORS = ["Fractal_dimension", "Artery_Distance_tortuosity", "Vein_Squared_curvature_tortuosity", "AVR_Hubbard"]
TRANSFORM_COLS = [c for c in (EXPOSURES + OUTCOMES + MEDIATORS)]


def z_standard(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            continue
        s = pd.to_numeric(out[c], errors="coerce")
        mu = s.mean(skipna=True)
        sd = s.std(skipna=True)
        if pd.isna(sd) or sd == 0:
            continue
        out[c] = (s - mu) / sd
    return out


def yeojohnson_winsor(df: pd.DataFrame, cols: list[str], q_lo: float = 0.01, q_hi: float = 0.99) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            continue
        s = pd.to_numeric(out[c], errors="coerce")
        mask = s.notna()
        if int(mask.sum()) < 10:
            continue
        x = s.loc[mask].to_numpy(dtype=float)
        x_t, lam = yeojohnson(x)
        lo = float(np.quantile(x_t, q_lo))
        hi = float(np.quantile(x_t, q_hi))
        x_tw = np.clip(x_t, lo, hi)
        out.loc[mask, c] = x_tw
    return out


def main() -> None:
    df = pd.read_csv(INP, low_memory=False)
    cols = [c for c in TRANSFORM_COLS if c in df.columns]

    z_df = z_standard(df, cols)
    yj_df = yeojohnson_winsor(df, cols)

    z_fp = OUT / "NHANES_stage6_corr70_r4_z_standard.csv"
    yj_fp = OUT / "NHANES_stage6_corr70_r4_yeojohnson_winsor.csv"
    z_df.to_csv(z_fp, index=False)
    yj_df.to_csv(yj_fp, index=False)

    summary = {
        "input": str(INP),
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "transformed_cols": cols,
        "z_standard_file": str(z_fp),
        "yeojohnson_winsor_file": str(yj_fp),
        "winsor_quantiles": [0.01, 0.99],
    }
    (OUT / "r4_transform_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
