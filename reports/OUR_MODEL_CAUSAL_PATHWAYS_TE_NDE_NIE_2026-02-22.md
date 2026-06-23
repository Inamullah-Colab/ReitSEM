# RetiSEM Pathway Report (supersedes older exploratory note)

## Status
This file is retained for path compatibility, but the accepted-paper interpretation should follow the locked final workflow under:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000`

The older `2026-02-22` exploratory NHANES note is not the final accepted-paper result and should not be cited as such.

## Exact Methodology Used In The Accepted Paper
The accepted paper uses a domain-constrained SEM plus mediation formulation over ordered blocks:
- `(G, Z) ≺ L ≺ R ≺ V`

Meaning:
- `G`: genetic or ancestry-proxy variables
- `Z`: covariates
- `L`: molecular or systemic exposure variables
- `R`: retinal microvascular phenotype variables
- `V`: vascular outcomes

Linear SEM approximation:
- `L = f_L(G, Z) + e_L`
- `R = f_R(L, G, Z) + e_R`
- `V = f_V(R, L, G, Z) + e_V`

Linear mediation decomposition used in code:
- single mediator: `NIE = alpha * beta`, `NDE = c'`, `TE = c' + alpha * beta`
- multi-mediator retinal block: `NIE = sum_j alpha_j * beta_j`

Repository implementation:
- `final_task/scripts/run_mediation_te_nde_nie_realdata.py`
- `final_task/scripts/make_sem_paper_png_results.py`

## Exact Locked NHANES Result
Final locked run:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/summary_all_datasets.csv`

Dataset:
- `NHANES_stage6_corr70_r4_z_standard`

Summary values:
- `n_pathways = 96`
- `nie_significant_count = 3`
- `nie_significant_rate = 0.03125`
- `mean_abs_nie = 0.0008293552683992055`
- `max_abs_nie = 0.0030195530065822603`

## Accepted-Paper Interpretation
- Retinal variables are not presented as dominant causal drivers.
- Most pathways are dominated by direct or biomarker-like behavior.
- A smaller subset shows detectable mediator-like indirect effects.

This is the interpretation that should remain consistent between the online paper and the repository.

## Significant Retina-Hub Pathways In The Locked Run
- `URXUMA -> Artery_Distance_tortuosity -> BPXPULS`
  - `NIE = 0.001839`
  - `95% CI = [0.000361, 0.004205]`
- `URXUMA -> Vein_Squared_curvature_tortuosity -> BPXPULS`
  - `NIE = 0.001996`
  - `95% CI = [0.000439, 0.004449]`
- `LBXSBU -> Vein_Squared_curvature_tortuosity -> BPXPULS`
  - `NIE = 0.002231`
  - `95% CI = [0.000059, 0.005723]`

## Final Artifacts To Cite
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/mediation_table_all_combos.csv`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie_top30.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_summary_te_nde_nie.png`
