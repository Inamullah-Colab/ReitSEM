# Real-Data Pipeline Scripts

These are the staged preprocessing scripts used to build the locked NHANES-linked analysis dataset before the final mediation and SEM runs.

Run order:
1. `stage1_premerge_missingness.py`
2. `stage2_harmonize_merge_from_preclean.py`
3. `stage3_postmerge_missingness.py`
4. `stage4_retinal_qc_penalize_then_fix.py`
5. `stage5_corr70_final.py`
6. `stage6_hemodynamics_check.py`
7. `stage6_hemodynamics_check_corr70.py`
8. `build_r4_transforms.py`

What they do:
- clean NHANES, retinal, and proxy tables separately
- merge all sources by `SEQN`
- protect key retinal and outcome variables during filtering
- repair retinal numeric quality issues
- prune multicollinearity
- check hemodynamic outcome completeness and role compatibility
- generate the transformed dataset used in the locked release
