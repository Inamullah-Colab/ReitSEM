# RetiSEM: Generalising Causal Models for Fragmented Biomedical Data

This folder is the main GitHub-facing RetiSEM release.

Some scripts and artifacts still use the older internal label `OUR_SEM`; those names are kept for compatibility.

Start here:
- `workflow/RETISEM_STEP_BY_STEP_WORKFLOW.md`
- `docs/DATA.md`
- `workflow/REPRODUCIBILITY_ONE_PAGE.md`

## Legal Notice
Read first:
- `docs/COPYRIGHT_NOTICE.md`

## Summary
RetiSEM is a structured analysis workflow for mixed biomedical data. It is designed for settings where the information does not come from one clean table, but from several linked sources.

In plain language, the workflow asks:
- which systemic variables come first,
- whether retinal vessel features sit in the middle of the pathway,
- and how much of the exposure-outcome relationship may pass through the retina.

It combines:
- biologically ordered variable blocks
- forbidden-edge masking for graph recovery
- synthetic benchmark validation across ten scenarios
- real-world NHANES plus retinal-feature mediation analysis
- interpretable `TE`, `NDE`, and `NIE` pathway decomposition

## Core Formulation
RetiSEM uses ordered domain blocks:
- `(G, Z) < L < R < V`

Where:
- `G` = genetic or ancestry-related variables
- `Z` = covariates
- `L` = molecular or systemic variables
- `R` = retinal microvascular phenotype variables
- `V` = vascular outcomes

Non-technical reading:
- `G` and `Z` describe background differences between participants
- `L` is the body-level risk or exposure layer
- `R` is the retinal measurement layer
- `V` is the final vascular or hemodynamic outcome layer

Code-level split:
- `L -> Lt` and `Lm`
- `Z -> Zfix` and `Znoise`

Operational role rule:
- if true PRS, SNP, or genotype-like variables exist, `G` can remain an upstream block
- if real data only contain proxy-genetic variables such as `GREF_*`, those variables are used as covariates for adjustment
- `Lt` and `Lm` are both kept because some lipid or systemic variables may be used as upstream drivers in one setting and intermediate molecular components in another
- `R` is the retinal hypothesis-testing block used to examine whether retinal features look passive, biomarker-like, mediator-like, or only weakly associated

This point matters for public use:
- the repository does not force the retina to be causal
- it tests whether the retinal variables behave as meaningful pathway variables under the chosen model
- results should therefore be read as structured mediation evidence, not as automatic proof of biology

SEM block structure:
- `L = f_L(G, Z) + e_L`
- `R = f_R(L, G, Z) + e_R`
- `V = f_V(R, L, G, Z) + e_V`

These block equations define the structured regime used for real data and the same ordered interpretation used when moving from synthetic validation to NHANES.

Linear mediation operationalization:
- single mediator: `NIE = alpha * beta`, `NDE = c'`, `TE = c' + alpha * beta`
- multiple retinal mediators: `NIE = sum_j alpha_j * beta_j`, `TE = c' + sum_j alpha_j * beta_j`

Synthetic benchmark equations used for the controlled generative regime:
- `X = B^T X + e`
- `X = (I - B^T)^(-1) e`
- `TE = (I - B)^(-1) - I`

Together, these equations connect the synthetic and real-data regimes in one workflow: the synthetic regime tests graph recovery and effect structure, and the real-data regime applies the same ordered causal logic to the NHANES-linked setting.

Important distinction:
- synthetic validation includes both linear and nonlinear regimes
- the real NHANES-linked workflow is different and is fit with a linear SEM and linear mediation approximation for interpretability, even though the underlying real system may contain nonlinear structure

Simple interpretation:
- the synthetic data are used to stress-test the method under known conditions
- the real NHANES analysis uses a cleaner and more interpretable linear version of the model

## Real-Data Inputs
The main real-data workflow connects three components:
- NHANES clinical and physiological tables
- retinal features extracted from fundus images
- ancestry-sensitive proxy-genetic covariates

You can think of these as three layers of information about the same participant:
- body and clinical measurements
- eye-derived vessel measurements
- background adjustment variables

Retinal feature source used in the locked workflow:
- `data/retinal_traits/macular_zone_b_imputed_with_seq.csv`

Retinal extraction narrative:
- APTOS fundus images were processed with AutoMorph
- quantitative vessel traits were exported
- the resulting retinal trait table was linked to NHANES using `SEQN`

Proxy-genetic source:
- `data/proxy_genetics/NHANES_1000G_proxy_only.csv`

These proxy variables are not participant-level genotype calls. They are used for adjustment when true genetics are unavailable.

This means:
- if a future user has real genotype, SNP, or PRS data, those variables can be placed in the upstream `G` block
- if a future user only has proxy variables, those should remain adjustment covariates

## Main Workflow
1. Clean NHANES, retinal, and proxy-genetic tables separately.
2. Merge them by `SEQN`.
3. Apply post-merge missingness filtering.
4. Run retinal quality control.
5. Prune global multicollinearity with Spearman `|rho| <= 0.70`.
6. Complete hemodynamic outcome checks.
7. Build transformed analysis datasets.
8. Run mediation to estimate `TE`, `NDE`, and `NIE`.
9. Render final figures.

This sequence is intentional:
- first build a clean participant table
- then control feature quality and redundancy
- then estimate retinal mediation pathways on the final locked dataset

Full step-by-step details are in:
- `workflow/RETISEM_STEP_BY_STEP_WORKFLOW.md`

## Main Scripts
- `scripts/run_our_sem_on_nhanes_realdata.py`
- `scripts/run_mediation_te_nde_nie_realdata.py`
- `scripts/make_sem_paper_png_results.py`
- `scripts/build_external_prior_knowledge.py`
- `scripts/run_our_sem_standalone_prioraware.py`
- `scripts/real_data_pipeline/`

## Main Locked NHANES Run
Locked run root:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000`

Main dataset:
- `NHANES_stage6_corr70_r4_z_standard`

Locked summary values:
- `n_pathways = 96`
- `nie_significant_count = 3`
- `nie_significant_rate = 0.03125`
- `mean_abs_nie = 0.0008293552683992055`
- `max_abs_nie = 0.0030195530065822603`

Representative detectable indirect-effect pathways:
- `URXUMA -> Artery_Distance_tortuosity -> BPXPULS`
- `URXUMA -> Vein_Squared_curvature_tortuosity -> BPXPULS`
- `LBXSBU -> Vein_Squared_curvature_tortuosity -> BPXPULS`

## Main Outputs
- `platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/summary_all_datasets.csv`
- `platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/mediation_table_all_combos.csv`
- `platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie.png`
- `platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie_top30.png`
- `platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_summary_te_nde_nie.png`
