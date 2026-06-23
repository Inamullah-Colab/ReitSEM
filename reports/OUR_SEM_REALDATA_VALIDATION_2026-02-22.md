# RetiSEM Real-Data Validation Report (historical file, updated for accepted release)

## Status
This file path is retained for compatibility, but the accepted-paper final real-data result is anchored to the locked workflow under:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24`

The single merged exploratory run previously documented here is not the final accepted-paper reference result.

## Exact Model Formulation
The accepted real-data analysis follows the same constrained ordering used in the paper:
- `(G, Z) ≺ L ≺ R ≺ V`

Operational code mapping:
- `G`: ancestry or proxy-genetic variables
- `Z`: covariates
- `Lt` and `Lm`: exposure-side molecular or systemic variables
- `R`: retinal microvascular phenotype variables
- `V`: vascular outcomes

The real-data structure learning stage:
- builds an ordered model matrix,
- applies domain-constrained forbidden-edge masking,
- estimates a weighted adjacency matrix,
- thresholds the graph,
- exports adjacency and path summaries.

Primary implementation:
- `final_task/scripts/run_our_sem_on_nhanes_realdata.py`

## Accepted Final NHANES Workflow
Use:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/REPRODUCIBILITY_ONE_PAGE.md`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/REPRODUCIBILITY_REVIEWER.md`

Locked final mediation command settings:
- collinearity filter: `|rho| <= 0.70`
- transform: `z_standard`
- bootstrap: `2000`
- dataset: `NHANES_stage6_corr70_r4_z_standard`

## Accepted Final Results
From:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/summary_all_datasets.csv`

Expected final values:
- `n_pathways = 96`
- `nie_significant_count = 3`
- `nie_significant_rate = 0.03125`
- `mean_abs_nie = 0.0008293552683992055`
- `max_abs_nie = 0.0030195530065822603`

## Interpretation That Should Match The Paper
- Domain constraints improve structural recovery in the synthetic benchmark suite.
- In the fragmented NHANES analysis, retinal variables behave mainly as downstream biomarker-like indicators.
- Indirect effects are generally smaller than total or direct effects.
- A small subset of retina-hub pathways remains detectable, supporting limited mediator-like statistical signal rather than a dominant retinal causal role.

## Final Artifacts
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/summary_all_datasets.csv`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/mediation_table_all_combos.csv`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie_top30.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_summary_te_nde_nie.png`
