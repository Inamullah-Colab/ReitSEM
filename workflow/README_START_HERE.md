# START HERE

Canonical order:
1. 01_missingness_premerge
2. 02_harmonize_merge
3. 03_missingness_postmerge (retinal-protected)
4. 04_retinal_qc (negative penalize/fix)
5. 05_multicollinearity
6. 06_hemodynamics_completion
7. 07_transform_benchmark
8. 08_model_runs
9. 09_figures

Raw sources are in 00_raw_sources.

## Final Locked Run (Current)
- Collinearity rule: Spearman `|rho| <= 0.70` (strict prune).
- Transform decision: `z_standard` is final.
- Final model bootstrap: `2000`.
- Exposures: `URXUMA, URXCRS, LBXSBU, LBDSTRSI, LBDHDDSI, LBDTCSI`
- Mediators: `Fractal_dimension, Artery_Distance_tortuosity, Vein_Squared_curvature_tortuosity, AVR_Hubbard`
- Outcomes: `BPXSY1, BPXDI1, BPXPLS, BPXPULS`
- Covariates: `DMDHRAGE, RIAGENDR, RIDRETH1, DMDEDUC3, GREF_EUR, GREF_entropy`

## Final Outputs
- Main summary: `08_model_runs/final_z2000/summary_all_datasets.csv`
- Main table: `08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/mediation_table_all_combos.csv`
- Final top30 PNG: `08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie_top30.png`
- Full effects PNG: `08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie.png`
- Summary bar PNG: `08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_summary_te_nde_nie.png`
