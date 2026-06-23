# RetiSEM

![Model](https://img.shields.io/badge/model-RetiSEM-1f6feb)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![SEM](https://img.shields.io/badge/method-SEM%20%2B%20TE%2FNDE%2FNIE-0A7E8C)
![Retina](https://img.shields.io/badge/domain-retinal%20features-2E8B57)
![Heart](https://img.shields.io/badge/focus-retina%20to%20vascular%20pathways-C0392B)
![Synthetic](https://img.shields.io/badge/benchmark-linear%20%2B%20nonlinear-F39C12)
![NHANES](https://img.shields.io/badge/data-NHANES%20linked-34495E)
![GitHub](https://img.shields.io/badge/release-public%20workflow-black?logo=github)

First public release of RetiSEM, a retina-domain-constrained structural equation modelling workflow for fragmented biomedical data.

In plain language, this repository asks one central question:
- can retinal vessel features help explain how systemic risk markers relate to vascular and hemodynamic outcomes?

It is designed for hypothesis generation in settings where the retina may behave as:
- an active mediator,
- a passive indicator,
- a dominant pathway variable,
- or a weakly associated biomarker-like signal.

## What This Repository Contains
- a structured SEM workflow with ordered biomedical variable blocks
- real-data pathway analysis using NHANES-linked retinal and systemic variables
- synthetic benchmark evidence across linear and nonlinear regimes
- locked summary tables and publication-style figures
- reusable scripts for users who want to test the same setup on another regime

## Core Model
RetiSEM uses the ordered formulation:
- `(G, Z) < L < R < V`

Where:
- `G` = genetic or ancestry-related variables
- `Z` = covariates
- `L` = molecular or systemic exposure-side variables
- `R` = retinal microvascular phenotype variables
- `V` = vascular or hemodynamic outcomes

Main block equations:
- `L = f_L(G, Z) + e_L`
- `R = f_R(L, G, Z) + e_R`
- `V = f_V(R, L, G, Z) + e_V`

Mediation equations:
- single mediator: `NIE = alpha * beta`, `NDE = c'`, `TE = c' + alpha * beta`
- multiple mediators: `NIE = sum_j alpha_j * beta_j`, `TE = c' + sum_j alpha_j * beta_j`

Synthetic benchmark equations:
- `X = B^T X + e`
- `X = (I - B^T)^(-1) e`
- `TE = (I - B)^(-1) - I`

## Role Logic Used In This Release
- if true PRS, SNP, or genotype-like variables exist, `G` can remain an upstream block
- if only proxy variables such as `GREF_*` are available, they are used as covariates for adjustment
- `Lt` and `Lm` are both kept in code because lipid or systemic variables can act as upstream drivers in one setting and intermediate components in another
- `R` is the retinal hypothesis-testing block rather than a forced causal claim

This means the repository does not assume the retina is always causal. It tests whether retinal features behave more like mediator-like variables, passive indicators, or biomarker-like signals under the structured model.

## Real-Data Picture
The main real-data workflow connects three sources:
- NHANES clinical and physiological tables
- retinal features extracted from fundus images
- proxy-genetic adjustment variables when true participant-level genetics are unavailable

Retinal features were extracted from fundus images with AutoMorph-derived vessel measurements and linked back to participant-level NHANES records using `SEQN`.

## Start Here
1. `docs/PROJECT_OVERVIEW.md`
2. `workflow/RETISEM_STEP_BY_STEP_WORKFLOW.md`
3. `workflow/REPRODUCIBILITY_ONE_PAGE.md`
4. `results/main_locked/summary_all_datasets.csv`

## Main Public Structure
- `README.md`
- `docs/`
- `scripts/`
- `data/`
- `results/`
- `figures/`
- `workflow/`

## Main Scripts
- `scripts/run_our_sem_on_nhanes_realdata.py`
- `scripts/run_mediation_te_nde_nie_realdata.py`
- `scripts/make_sem_paper_png_results.py`
- `scripts/build_external_prior_knowledge.py`
- `scripts/run_our_sem_standalone_prioraware.py`

## Main Locked Outputs
- `results/main_locked/summary_all_datasets.csv`
- `results/main_locked/mediation_table_all_combos.csv`
- `figures/main/sem_paper_forest_te_nde_nie.png`
- `figures/main/sem_paper_forest_te_nde_nie_top30.png`
- `figures/main/sem_paper_summary_te_nde_nie.png`

## Main vs Legacy
Use these as the main public release paths:
- `docs/`
- `scripts/`
- `results/main_locked/`
- `figures/main/`
- `figures/synthetic/`
- `workflow/`

Treat these as reference or archival material:
- `results/` subfolders other than `main_locked/`
- `reports/`
- `other_models_run_2026-02-22/`

Some scripts still use the older internal name `OUR_SEM`. That naming is kept for compatibility only.
