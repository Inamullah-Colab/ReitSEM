# RetiSEM

Public release folder for the RetiSEM workflow.

In simple terms, this repository asks one main question:
- can retinal vessel features help explain how systemic risk markers relate to vascular outcomes?

The repository is organised so that a new user can:
- understand the method,
- see how the data sources are connected,
- run the main analysis scripts,
- and inspect the locked results and figures.

## Structure
- `README.md`
  - main landing page
- `docs/`
  - overview, data note, copyright note
- `scripts/`
  - main runnable code
- `data/`
  - demo or user-prepared inputs
- `results/`
  - main locked summary tables
- `figures/`
  - main real-data figures and synthetic benchmark figures
- `workflow/`
  - step-by-step pipeline and reproducibility notes

## Start Here
1. `docs/PROJECT_OVERVIEW.md`
2. `workflow/RETISEM_STEP_BY_STEP_WORKFLOW.md`
3. `workflow/REPRODUCIBILITY_ONE_PAGE.md`
4. `results/main_locked/summary_all_datasets.csv`

If you are new to this topic:
- read `docs/PROJECT_OVERVIEW.md` first for the big picture
- read `workflow/RETISEM_STEP_BY_STEP_WORKFLOW.md` second for the exact pipeline
- then open `results/main_locked/` and `figures/main/` to see the final outputs

## Main Scripts
- `scripts/run_our_sem_on_nhanes_realdata.py`
- `scripts/run_mediation_te_nde_nie_realdata.py`
- `scripts/make_sem_paper_png_results.py`
- `scripts/build_external_prior_knowledge.py`
- `scripts/run_our_sem_standalone_prioraware.py`

What these scripts do:
- build the structured SEM view of the variables
- estimate direct and indirect pathways through retinal features
- render the summary figures used for interpretation

## Main Locked Outputs
- `results/main_locked/summary_all_datasets.csv`
- `results/main_locked/mediation_table_all_combos.csv`
- `figures/main/sem_paper_forest_te_nde_nie.png`
- `figures/main/sem_paper_forest_te_nde_nie_top30.png`
- `figures/main/sem_paper_summary_te_nde_nie.png`

Some scripts still use the older internal name `OUR_SEM`. Those names are kept for compatibility.

## Main vs Legacy
Use these as the main public release paths:
- `docs/`
- `scripts/`
- `data/`
- `results/main_locked/`
- `figures/main/`
- `figures/synthetic/`
- `workflow/`

Treat these as legacy or archival material:
- `results/` subfolders other than `main_locked/`
- `reports/`
- `other_models_run_2026-02-22/`

Those legacy folders are retained for traceability, small demo-style reference material, and historical reruns, but they are not the main release entry points.
