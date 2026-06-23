# Data Policy

Use code-based reproducibility for public release.

## Included
- Locked summary outputs in `results/main_locked/`
- Real-data figures in `figures/main/`
- Synthetic benchmark figures in `figures/synthetic/`
- NHANES source tables in `data/nhanes_xpt/`
- Prepared retinal trait table in `data/retinal_traits/macular_zone_b_imputed_with_seq.csv`
- Proxy-genetic adjustment table in `data/proxy_genetics/NHANES_1000G_proxy_only.csv`

## Real-Data Source Roots
- NHANES raw-source root: `data/nhanes_xpt/`
- Retinal feature source: `data/retinal_traits/macular_zone_b_imputed_with_seq.csv`
- Proxy-genetic source: `data/proxy_genetics/NHANES_1000G_proxy_only.csv`

## Main Locked Analysis Files
- Locked transformed dataset: `platform_from_scratch_master_2026-02-24/07_transform_benchmark/outputs/NHANES_stage6_corr70_r4_z_standard.csv`
- Locked run root: `platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/`
- Locked summary table: `results/main_locked/summary_all_datasets.csv`
- Locked mediation table: `results/main_locked/mediation_table_all_combos.csv`

## Connection Logic
- NHANES tables are merged by participant identifier `SEQN`
- retinal traits are linked onto the participant table by `SEQN`
- proxy-genetic adjustment variables are linked onto the same participant table by `SEQN`
- the merged dataset is then filtered, quality-checked, transformed, and passed to the final mediation scripts

Main merge script:
- `scripts/real_data_pipeline/stage2_harmonize_merge_from_preclean.py`

Staged preprocessing scripts included in this repo:
- `scripts/real_data_pipeline/stage1_premerge_missingness.py`
- `scripts/real_data_pipeline/stage2_harmonize_merge_from_preclean.py`
- `scripts/real_data_pipeline/stage3_postmerge_missingness.py`
- `scripts/real_data_pipeline/stage4_retinal_qc_penalize_then_fix.py`
- `scripts/real_data_pipeline/stage5_corr70_final.py`
- `scripts/real_data_pipeline/stage6_hemodynamics_check.py`
- `scripts/real_data_pipeline/stage6_hemodynamics_check_corr70.py`
- `scripts/real_data_pipeline/build_r4_transforms.py`

## Not Included
- Large/private real datasets
- A toy demo bundle

## Reuse Guidance
- point the scripts to your own prepared datasets
- use the workflow notes to reproduce the same staged order
- use the locked summary tables and figures as the main public reference outputs
