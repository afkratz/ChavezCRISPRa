# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import os
from pathlib import Path
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
from src import auroc_utils as au

import pandas as pd
df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "03_manually_tested_biochem_charachterized.csv"),
        index_col="Unnamed: 0"
    )
only_centroids = df[df['Is centroid']==True]
ncpr = (-only_centroids['NCPR']).to_list()
disorder = only_centroids['Disorder promoting fraction']
is_hit = only_centroids['Hit on any'].to_list()
fpr_ncpr_any,tpr_ncpr_any = au.get_FPR_TPR(ncpr,is_hit)
print('NCPR:',au.calculate_auc(fpr_ncpr_any,tpr_ncpr_any))
fpr_disorder_any,tpr_disorder_any = au.get_FPR_TPR(disorder,is_hit)
print('NCPR:',au.calculate_auc(fpr_disorder_any,tpr_disorder_any))

odf = pd.DataFrame({
    'fpr NCPR predicting hit on any':fpr_ncpr_any,
    'tpr NCPR predicting hit on any':tpr_ncpr_any,
    'fpr Disorder promoting fraction predicting hit on any':fpr_disorder_any,
    'tpr Disorder promoting fraction predicting hit on any':tpr_disorder_any,

})
odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2b - NCPR and disorder vs hit-any AUROC.csv"
    )
)

ncpr = (-df['NCPR']).to_list()
disorder = df['Disorder promoting fraction']
odf = pd.DataFrame()
for target in ['EPCAM','CXCR4','tdTomato']:
    
    is_hit = df['Hit on '+target].to_list()
    fpr_ncpr_any,tpr_ncpr_any = au.get_FPR_TPR(ncpr,is_hit)
    fpr_disorder_any,tpr_disorder_any = au.get_FPR_TPR(disorder,is_hit)

    odf['fpr NCPR predicting hit on '+target]=fpr_ncpr_any
    odf['tpr NCPR predicting hit on '+target]=tpr_ncpr_any
    odf['fpr Disorder promoting fraction predicting hit on '+target]=fpr_disorder_any
    odf['tpr Disorder promoting fraction predicting hit on '+target]=tpr_disorder_any
    
odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "S2b - NCPR and disorder vs all targets AUROC.csv"
    )
)