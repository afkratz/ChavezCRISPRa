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

biochem_traits = {}
biochem_traits['NCPR']=(-only_centroids['NCPR']).to_list()
biochem_traits['Hydropathy']=only_centroids['Hydropathy'].to_list()
biochem_traits['Omega']=(-only_centroids['Omega']).to_list()
biochem_traits['Kappa']=(-only_centroids['Kappa']).to_list()
biochem_traits['Disorder promoting fraction']=only_centroids['Disorder promoting fraction'].to_list()

is_hit = only_centroids['Hit on any'].to_list()

odf = pd.DataFrame()
auroc_df = pd.DataFrame()
for trait_name in biochem_traits:
    fpr,tpr = au.get_FPR_TPR(biochem_traits[trait_name],is_hit)
    odf['fpr '+trait_name+' predicting hit on any']= fpr
    odf['tpr '+trait_name+' predicting hit on any']= tpr
    auroc_df.at[trait_name,'AUROC']=au.calculate_auc(fpr,tpr)
odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2b - Biochem traits vs hit-any fpr vs tpr.csv"
    )
)
auroc_df.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2b - Biochem traits vs hit-any AUROC.csv"
    )
)


odf = pd.DataFrame()
auroc_df = pd.DataFrame()

for target in ['EPCAM','CXCR4','tdTomato']:
    is_hit = only_centroids['Hit on '+target].to_list()
    for trait_name in biochem_traits:
        fpr,tpr = au.get_FPR_TPR(biochem_traits[trait_name],is_hit)
        odf['fpr '+trait_name+' predicting hit on '+target]= fpr
        odf['tpr '+trait_name+' predicting hit on '+target]= tpr
        auroc_df.at[trait_name,'predicting hit on '+target]=au.calculate_auc(fpr,tpr)
    
odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "S2b - Biochem traits vs all targets fpr vs tpr.csv"
    )
)

auroc_df.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "S2b - Biochem traits vs all targets AUROC.csv"
    )
)