# Reproducibility One-Page (Reviewer Quick Run)

## Goal
Reproduce final NHANES mediation results and final PNGs from raw inputs to end outputs.

## Input placement
- NHANES XPT files -> `00_raw_sources/nhanes_xpt/`
- Retinal CSV -> `00_raw_sources/retinal_traits/macular_zone_b_imputed_with_seq.csv`
- Proxy genetics CSV -> `00_raw_sources/proxy_genetics/NHANES_1000G_proxy_only.csv`

## Run pipeline (in order)
```powershell
python "platform_from_scratch_master_2026-02-24\01_missingness_premerge\stage1_premerge_missingness.py"
python "platform_from_scratch_master_2026-02-24\02_harmonize_merge\stage2_harmonize_merge_from_preclean.py"
python "platform_from_scratch_master_2026-02-24\03_missingness_postmerge\stage3_postmerge_missingness.py"
python "platform_from_scratch_master_2026-02-24\04_retinal_qc\stage4_retinal_qc_penalize_then_fix.py"
python "platform_from_scratch_master_2026-02-24\05_multicollinearity\stage5_corr70_final.py"
python "platform_from_scratch_master_2026-02-24\06_hemodynamics_completion\stage6_hemodynamics_check_corr70.py"
python "platform_from_scratch_master_2026-02-24\07_transform_benchmark\build_r4_transforms.py"
```

## Final locked model run
```powershell
python "platform_from_scratch_master_2026-02-24\08_model_runs\run_mediation_te_nde_nie_realdata.py" `
  --base-dir "platform_from_scratch_master_2026-02-24" `
  --inputs "07_transform_benchmark/outputs/NHANES_stage6_corr70_r4_z_standard.csv" `
  --out-dir "08_model_runs/final_z2000" `
  --bootstrap 2000 --seed 2026 --min-complete-rows 300 `
  --exposures URXUMA URXCRS LBXSBU LBDSTRSI LBDHDDSI LBDTCSI `
  --outcomes BPXSY1 BPXDI1 BPXPLS BPXPULS `
  --mediators Fractal_dimension Artery_Distance_tortuosity Vein_Squared_curvature_tortuosity AVR_Hubbard `
  --covars DMDHRAGE RIAGENDR RIDRETH1 DMDEDUC3 GREF_EUR GREF_entropy
```

## Generate final figures
```powershell
python "platform_from_scratch_master_2026-02-24\08_model_runs\make_sem_paper_png_results.py" `
  --base-dir "platform_from_scratch_master_2026-02-24" `
  --results-root "08_model_runs/final_z2000" `
  --datasets "NHANES_stage6_corr70_r4_z_standard" `
  --pathway-suffix " | Z,G (CC)"
```

## Verify final result
Check:
- `08_model_runs/final_z2000/summary_all_datasets.csv`

Expected:
- `n_pathways=96`
- `nie_significant_count=3`
- `nie_significant_rate=0.03125`
- `mean_abs_nie=0.0008293552683992055`
- `max_abs_nie=0.0030195530065822603`

Final PNGs:
- `08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie.png`
- `08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie_top30.png`
- `08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_summary_te_nde_nie.png`

For full detail, see:
- `10_docs/REPRODUCIBILITY_REVIEWER.md`
