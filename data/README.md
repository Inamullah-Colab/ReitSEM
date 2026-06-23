# Data Manifest

This public repo includes the prepared real-data inputs needed to understand the released workflow structure.

## Included In This Repo
- `data/nhanes_xpt/`
  - NHANES `.xpt` source tables used in the staged rebuild
- `data/retinal_traits/macular_zone_b_imputed_with_seq.csv`
  - prepared retinal trait table linked by `SEQN`
- `data/proxy_genetics/NHANES_1000G_proxy_only.csv`
  - proxy-genetic adjustment table linked by `SEQN`

## NHANES Tables Included
- `DEMO_D.xpt`
- `BMX_D.xpt`
- `BPX_D.xpt`
- `HDL_D.xpt`
- `LEXABPI.xpt`
- `SLQ_D.xpt`
- `SMQ_D.xpt`
- `TCHOL_D.xpt`
- `TRIGLY_D.xpt`
- `ALB_CR_D.xpt`
- `BIOPRO_D.xpt`
- `BPQ_D.xpt`
- `CRP_D.xpt`
- `DIQ_D.xpt`
- `GHB_D.xpt`
- `GLU_D.xpt`
- `MCQ_D.xpt`

## Connection Logic
- NHANES participant tables are merged by `SEQN`
- retinal traits are linked onto the participant table by `SEQN`
- proxy-genetic covariates are linked onto the same participant table by `SEQN`

## Official NHANES Archive Pattern
The included NHANES files correspond to the standard CDC NHANES archive layout for cycle `2005-2006`.

Direct file pattern:
- `https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/<FILE>.XPT`

Examples:
- `https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/DEMO_D.XPT`
- `https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/BPX_D.XPT`
- `https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/HDL_D.XPT`
- `https://wwwn.cdc.gov/Nchs/Nhanes/2005-2006/TRIGLY_D.XPT`

## Important Note
- the NHANES tables are public
- the retinal trait table in this repo is the prepared analysis table used in the locked workflow
- the proxy-genetic table in this repo is an adjustment table used when true participant-level genetics are unavailable
