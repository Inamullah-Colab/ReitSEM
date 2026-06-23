# RetiSEM Step-by-Step Workflow

This is the canonical public workflow note for the current RetiSEM release in this workspace.

Its purpose is to show clearly:
- how the data were created,
- how the three data sources are connected,
- how the synthetic benchmarks were generated and evaluated,
- how the final NHANES validation was performed,
- which exact files should be treated as the main locked result.

This note is written to be readable by users outside the immediate field.
If you only want the main idea, read Sections `1` to `4` first.

## 1. What RetiSEM Is
RetiSEM is a domain-constrained structural equation modelling workflow for fragmented biomedical data.

Simple description:
- it links body-level variables, retinal vessel measurements, and vascular outcomes in one ordered model
- it then tests whether some of the exposure-outcome signal appears to pass through the retinal layer

The causal ordering used throughout the paper and code is:
- `(G, Z) < L < R < V`

Where:
- `G` = genetic or ancestry-proxy variables
- `Z` = covariates
- `L` = molecular or systemic exposure variables
- `R` = retinal microvascular phenotype variables
- `V` = vascular outcomes

The code-level naming keeps a slightly more granular split:
- `G`
- `Zfix` and `Znoise`
- `Lt` and `Lm`
- `R`
- `V`

Interpretation rule used in this release:
- if true participant-level genetic variables are available, `G` can remain an upstream exposure-side block
- if only proxy-genetic variables are available, `G` is treated as covariate adjustment rather than as a main exposure block
- `Lt` and `Lm` are both kept because some lipid or systemic variables may be modeled either as upstream exposures or as intermediate molecular components
- `R` is kept as the retinal mediator block used for hypothesis testing

This is intentional because the project is not making a strong irreversible claim that the retina is always an active causal mediator. The retinal block is used to test whether retinal features behave more like:
- passive indicators,
- reflective biomarkers,
- mediator-like statistical components,
- or weakly associated downstream correlates.

Practical interpretation:
- the retina is treated as a hypothesis-testing layer
- users should not read every indirect effect as proof of direct biological mechanism

## 2. Main Data Sources
RetiSEM connects three real-world data components.

In simple terms, the repository joins:
1. standard NHANES participant tables
2. retinal vessel features measured from eye images
3. proxy background variables used when real genetics are unavailable

### 2.1 NHANES clinical and physiological tables
These are the main systemic-variable source tables used to build the real-data cohort.

Core merge backbone in the staged rebuild:
- `DEMO_D`
- `BMX_D`
- `BPX_D`
- `HDL_D`
- `LEXABPI`
- `SLQ_D`
- `SMQ_D`
- `TCHOL_D`
- `TRIGLY_D`

Extended NHANES provenance used across the broader workflow includes:
- `ALB_CR_D`
- `BIOPRO_D`
- `BPQ_D`
- `CRP_D`
- `DIQ_D`
- `GHB_D`
- `GLU_D`
- `MCQ_D`

Main local rebuild root:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/00_raw_sources/nhanes_xpt/`

### 2.2 Retinal feature source
The retinal feature table used in the main locked workflow is:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/00_raw_sources/retinal_traits/macular_zone_b_imputed_with_seq.csv`

How the retinal features were extracted:
1. fundus images were processed through AutoMorph
2. vessel morphology traits were extracted from the processed images
3. the exported retinal feature table was cleaned and retained as a row-level phenotype file
4. that retinal phenotype file was linked to NHANES using participant identifier `SEQN`

Why this matters:
- the retinal features were not typed by hand
- they were generated from image-processing outputs and then linked back to participant records

The retinal traits include features such as:
- fractal-dimension measurements
- vessel-density measurements
- artery and vein tortuosity measurements
- AVR-style calibre relationships

Reported counts in the local supplementary notes:
- `5,290` AutoMorph-processed retinal images
- `4,050` final graded images in the manuscript narrative
- `4,055` retinal rows in the locked repository merge table

### 2.3 Genetic proxy source
The proxy-genetics table used in the locked workflow is:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/00_raw_sources/proxy_genetics/NHANES_1000G_proxy_only.csv`

These are not participant-level genotype calls.

They are ancestry-sensitive proxy covariates derived from NHANES ethnicity coding and mapped to soft 1000 Genomes-style superpopulation mixture variables:
- `GREF_AFR`
- `GREF_AMR`
- `GREF_EAS`
- `GREF_EUR`
- `GREF_SAS`
- `GREF_entropy`

The local construction script is:
- `NAHES_Dataset/build_1000g_reference_proxy_features.py`

The local assumptions note is:
- `NAHES_Dataset/REFERENCE_1000G_PROXY_ASSUMPTIONS.txt`

Practical rule for reuse:
- with real genetics or PRS data, users can keep `G` as an upstream block
- without real genetics, the proxy variables should stay in adjustment rather than being interpreted as primary exposures

## 3. How The Three Data Sources Are Connected
The real-data workflow joins NHANES, retinal features, and proxy-genetics by participant identifier:
- `SEQN`

This is the key integration idea of the repository:
- each participant row is built by joining systemic measurements, retinal measurements, and background adjustment variables into one analysis table

The connection logic is:
1. Clean each NHANES `.xpt` table separately.
2. Clean the retinal feature table separately.
3. Clean the proxy-genetics table separately.
4. Merge NHANES tables into one participant-level table.
5. Join retinal features onto that table using `SEQN`.
6. Join proxy-genetics covariates onto that table using `SEQN`.

The main merge script is:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/02_harmonize_merge/stage2_harmonize_merge_from_preclean.py`

Stage 2 writes:
- `NHANES_cleaned_stage2_merged.csv`
- `NHANES_stage2_merged_with_retinal_proxy_from_premerge_clean.csv`

## 4. Step-by-Step Real-Data Pipeline
This is the exact staged order used in the locked rebuild.

Short version:
1. clean each source separately
2. merge them into one participant table
3. reduce missingness and unstable variables
4. run the retinal mediation analysis

### Step 1. Pre-merge missingness filtering
Script:
- `01_missingness_premerge/stage1_premerge_missingness.py`

What it does:
- reads each NHANES table, the retinal table, and the proxy table separately
- removes columns with more than `30%` missingness
- protects key model variables from being dropped when needed

Key outputs:
- `01_missingness_premerge/outputs/stage1_premerge_missingness_summary.csv`
- cleaned NHANES tables in `01_missingness_premerge/outputs/nhanes_xpt_clean/`
- cleaned retinal table in `01_missingness_premerge/outputs/retinal_clean/`
- cleaned proxy table in `01_missingness_premerge/outputs/proxy_clean/`

### Step 2. Harmonize and merge
Script:
- `02_harmonize_merge/stage2_harmonize_merge_from_preclean.py`

What it does:
- uses `DEMO_D` as the merge backbone
- left-joins the selected NHANES tables on `SEQN`
- then merges retinal features and proxy-genetics covariates onto the same participant rows

Key outputs:
- `02_harmonize_merge/outputs/NHANES_cleaned_stage2_merged.csv`
- `02_harmonize_merge/outputs/NHANES_stage2_merged_with_retinal_proxy_from_premerge_clean.csv`

### Step 3. Post-merge missingness filtering
Script:
- `03_missingness_postmerge/stage3_postmerge_missingness.py`

What it does:
- applies the `30%` missingness threshold again after the full merge
- explicitly protects retinal columns from being removed

Key output:
- `03_missingness_postmerge/outputs/NHANES_stage3_postmerge_missingness_filtered.csv`

### Step 4. Retinal quality control
Script:
- `04_retinal_qc/stage4_retinal_qc_penalize_then_fix.py`

What it does:
- detects negative values in numeric retinal features
- replaces them using local neighbor means or robust fallback values

Key output:
- `04_retinal_qc/outputs/NHANES_stage4_retinal_qc_fixed.csv`

### Step 5. Global multicollinearity pruning
Script:
- `05_multicollinearity/stage5_corr70_final.py`

What it does:
- computes absolute Spearman correlations on numeric features
- repeatedly drops one feature from the worst-correlated pair until all retained pairs satisfy `|rho| <= 0.70`

Key output:
- `05_multicollinearity/final/pruned_corr70.csv`

### Step 6. Hemodynamics completion and role check
Script:
- `06_hemodynamics_completion/stage6_hemodynamics_check_corr70.py`

What it does:
- restores required hemodynamic outcomes if needed
- checks whether the retained columns are compatible with exposure, mediator, outcome, covariate, and proxy-genetic roles

Key output:
- `06_hemodynamics_completion/corr70_outputs/NHANES_stage6_hemodynamics_checked_corr70.csv`

### Step 7. Transformation benchmark
Script:
- `07_transform_benchmark/build_r4_transforms.py`

What it does:
- creates alternative transformed versions of the selected exposure, outcome, and mediator variables
- compares candidate transforms
- produces the main locked `z_standard` dataset used for the final workflow

Key outputs:
- `07_transform_benchmark/outputs/NHANES_stage6_corr70_r4_z_standard.csv`
- `07_transform_benchmark/outputs/NHANES_stage6_corr70_r4_yeojohnson_winsor.csv`
- `07_transform_benchmark/outputs/r4_transform_summary.json`

### Step 8. Final mediation run
Script:
- `08_model_runs/run_mediation_te_nde_nie_realdata.py`

What it does:
- evaluates exposure-outcome-retina pathways
- estimates `TE`, `NDE`, and `NIE`
- uses bootstrap confidence intervals
- marks `NIE_Significant = True` when the indirect-effect confidence interval excludes zero

### Step 9. Final figure generation
Script:
- `08_model_runs/make_sem_paper_png_results.py`

What it does:
- reads the final mediation tables
- renders the full forest plot
- renders the top-30 `|NIE|` forest plot
- renders the exposure-outcome summary plot

## 5. Which NHANES Dataset Is The Main Locked Dataset
The main locked real-data dataset is:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/07_transform_benchmark/outputs/NHANES_stage6_corr70_r4_z_standard.csv`

This is the main locked mediation input.

Final selected variable blocks:
- Exposures:
  - `URXUMA`
  - `URXCRS`
  - `LBXSBU`
  - `LBDSTRSI`
  - `LBDHDDSI`
  - `LBDTCSI`
- Mediators:
  - `Fractal_dimension`
  - `Artery_Distance_tortuosity`
  - `Vein_Squared_curvature_tortuosity`
  - `AVR_Hubbard`
- Outcomes:
  - `BPXSY1`
  - `BPXDI1`
  - `BPXPLS`
  - `BPXPULS`
- Covariates:
  - `DMDHRAGE`
  - `RIAGENDR`
  - `RIDRETH1`
  - `DMDEDUC3`
  - `GREF_EUR`
  - `GREF_entropy`

## 6. Exact Mediation Formulation Used In Code
RetiSEM uses a linear mediation operationalization for pathway decomposition.

Non-technical interpretation:
- `TE` is the overall association from exposure to outcome in the model
- `NDE` is the part that does not pass through the retinal mediator block
- `NIE` is the part that does pass through the retinal mediator block

Common block equations used for the structured regime:
- `L = f_L(G, Z) + e_L`
- `R = f_R(L, G, Z) + e_R`
- `V = f_V(R, L, G, Z) + e_V`

These block equations define the main structured model used in the real-data regime and the same ordered interpretation that is carried over from the synthetic regime.

Role logic used in this release:
- when true PRS, SNP, or genotype-like variables are available, `G` may remain in the upstream exposure-side block
- when those variables are missing and only `GREF_*` proxy variables are present, `G` is folded into covariate adjustment
- `L` is the broader exposure-side molecular/systemic layer
- `Lt` and `Lm` are kept separately in code because some lipid variables may act as exposure-side drivers in one analysis and mediator-side molecular components in another
- `R` remains the retinal mediator block for hypothesis generation and pathway testing

Single retinal mediator:
- `NIE = alpha * beta`
- `NDE = c'`
- `TE = c' + alpha * beta`

Multiple retinal mediators:
- `NIE = sum_j alpha_j * beta_j`
- `TE = c' + sum_j alpha_j * beta_j`

These mediation equations are used in both regimes:
- synthetic regime: to test whether the recovered pathways match the designed effect structure
- real-data regime: to test whether retinal variables behave as passive, biomarker-like, mediator-like, or weakly associated pathway components

In the code:
- `alpha` is estimated from exposure-to-mediator regressions
- `beta` is estimated from mediator-to-outcome coefficients in the outcome model
- `c'` is the direct exposure coefficient in the outcome model

Main implementation:
- `NAHES_Dataset/final_task/scripts/run_mediation_te_nde_nie_realdata.py`

## 7. How The Synthetic Benchmarks Were Generated
The synthetic benchmark suite is the controlled validation stage before real-data transfer.

Why synthetic data are included:
- they let users check whether the method behaves sensibly when the underlying structure is known
- this makes the later NHANES analysis easier to trust and easier to audit

It contains ten scenarios:
- `D1 = LowDim-L`
- `D2 = LowDim-N`
- `D3 = LowDim-P`
- `D4 = LowDim-D`
- `D5 = MidDim-C`
- `D6 = MidDim-P`
- `D7 = MidDim-D`
- `D8 = MidDim-S`
- `D9 = HigDim-S`
- `D10 = HigDim-D`

The benchmark varies:
- dimensionality `p`
- sample size `n`
- nonlinearity `rho`
- parallel path count `kappa`
- causal depth `ell`

Important distinction:
- the synthetic benchmark explicitly contains both linear and nonlinear data-generating regimes
- the real NHANES-linked setting is different: the underlying biology may be nonlinear, but the released RetiSEM real-data workflow uses a linear SEM and linear mediation approximation for interpretability and stability

Scenario design used in the paper:

| ID | Scenario | p | n | rho | kappa | ell | Meaning |
|---|---|---:|---:|---:|---:|---:|---|
| D1 | LowDim-L | 20 | 6000 | 0.0 | 1 | 3 | linear baseline |
| D2 | LowDim-N | 20 | 6000 | 0.5 | 1 | 3 | nonlinear baseline |
| D3 | LowDim-P | 20 | 6000 | 0.5 | 2 | 2 | parallel paths |
| D4 | LowDim-D | 20 | 6000 | 0.5 | 1 | 6 | deep nonlinear chain |
| D5 | MidDim-C | 50 | 6000 | 0.5 | 1 | 6 | confounded regime |
| D6 | MidDim-P | 100 | 6000 | 0.5 | 2 | 2 | parallel nonlinear |
| D7 | MidDim-D | 100 | 6000 | 0.5 | 1 | 6 | deep causal chain |
| D8 | MidDim-S | 100 | 6000 | 0.5 | 1 | 3 | shallow nonlinear |
| D9 | HigDim-S | 200 | 6000 | 0.5 | 1 | 6 | high-dimensional deep |
| D10 | HigDim-D | 200 | 6000 | 0.5 | 1 | 3 | high-dimensional shallow |

The synthetic equations summarized in the local supplementary material are:
- structural form: `X = B^T X + e`
- reduced form: `X = (I - B^T)^(-1) e`
- total effect matrix: `TE = (I - B)^(-1) - I`
- direct effect: `DE_{x->y} = B_{x,y}`
- indirect effect: `IE_{x->y} = TE_{x->y} - DE_{x->y}`

These synthetic equations are the controlled generative regime used to test graph recovery and effect decomposition before transferring the same structured RetiSEM logic to the real NHANES-linked regime.

This does not mean the real-data regime is assumed to be truly linear in biology. It means the released real-data workflow uses a linear approximation on top of a real system that may contain nonlinear and interaction-driven structure.

Documented benchmark defaults in the local notes:
- methods compared: `PC`, `LINGAM`, `DAGMA`, `NOTEARS`, `DECI`, `OUR_SEM_MODEL`
- graph binarization threshold: quantile `q = 0.35`
- default transform for OUR_SEM benchmark runs: `log1p_signed`
- default benchmark imputation: `knn`

## 8. How Synthetic Validation Was Done
The synthetic benchmarks test whether the domain constraints improve graph recovery before RetiSEM is applied to fragmented NHANES data.

Main validation metrics:
- `SHD`
- `Adjacency_F1`
- `Orientation_F1`
- `Causal_Accuracy`

The local supplementary summary reports that the constrained model achieved the highest causal accuracy across all ten listed scenarios.

Local synthetic figure assets used in the current workspace:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/LowDim-L_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/LowDim-N_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/LowDim-P_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/LowDim-D_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/MidDim-C_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/MidDim-P_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/MidDim-D_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/MidDim-S_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/HigDim-S_mediation_figure.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/figures/HigDim-D_mediation_figure.png`

## 9. How The Synthetic Validation Connects To NHANES
The project sequence is:
1. define the domain ordering on synthetic benchmarks
2. generate data under the structural form `X = B^T X + e`
3. test graph recovery under controlled dimensionality, nonlinearity, depth, and confounding
4. verify that the constrained model is stable enough to recover interpretable pathways and total-effect structure
5. transfer the same ordered block logic to fragmented real data, while using a linear approximation for estimation and interpretation
6. connect NHANES systemic variables, retinal phenotypes, and proxy-genetic covariates
7. test whether retinal features behave mainly as biomarkers or show limited mediator-like indirect effects

This is why the synthetic stage is not separate from the NHANES stage. It is the validation step that justifies using the same structured causal hypothesis in the fragmented real-data setting.

For a new user cloning this repository, this means:
- the synthetic pipeline is the safe place to learn the method
- the NHANES pipeline is the real-data application
- both use the same ordered modelling logic, so users can adapt the setup to their own datasets and compare regimes

## 10. Main Locked Outputs
The main locked result is anchored to:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/summary_all_datasets.csv`

Expected locked values:
- `n_pathways = 96`
- `nie_significant_count = 3`
- `nie_significant_rate = 0.03125`
- `mean_abs_nie = 0.0008293552683992055`
- `max_abs_nie = 0.0030195530065822603`

Main output files:
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/mediation_table_all_combos.csv`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_forest_te_nde_nie_top30.png`
- `NAHES_Dataset/platform_from_scratch_master_2026-02-24/08_model_runs/final_z2000/NHANES_stage6_corr70_r4_z_standard/sem_paper_summary_te_nde_nie.png`

Representative significant retina-hub pathways from the locked run:
- `URXUMA -> Artery_Distance_tortuosity -> BPXPULS`
- `URXUMA -> Vein_Squared_curvature_tortuosity -> BPXPULS`
- `LBXSBU -> Vein_Squared_curvature_tortuosity -> BPXPULS`

## 11. Recommended Reading Order
1. `NAHES_Dataset/final_task/README.md`
2. `NAHES_Dataset/final_task/README_GITHUB.md`
3. `NAHES_Dataset/final_task/RETISEM_STEP_BY_STEP_WORKFLOW.md`
4. `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/README_START_HERE.md`
5. `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/REPRODUCIBILITY_ONE_PAGE.md`
6. `NAHES_Dataset/platform_from_scratch_master_2026-02-24/10_docs/SUPPLEMENTARY_REVIEWER_ONE_PAGE.md`
