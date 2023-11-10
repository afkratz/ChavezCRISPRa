# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import pandas as pd
import os
from pathlib import Path
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from src import auroc_utils

df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "05_manually_tested_PaddleAndAdpred.csv"),
        index_col="Unnamed: 0"
    )
only_centroids = df[df['Is centroid']==True]
paddle_x = only_centroids["Paddle:Score"].to_list()
paddle_y = only_centroids["Hit on any"].to_list()

has_adpred = only_centroids[only_centroids['Adpred:Is short']==False]
adpred_x = has_adpred["Adpred:Score"].to_list()
adpred_y = has_adpred["Hit on any"].to_list()


paddle_fpr,paddle_tpr = auroc_utils.get_FPR_TPR(paddle_x,paddle_y)
adpred_fpr,adpred_tpr = auroc_utils.get_FPR_TPR(adpred_x,adpred_y)

odf=auroc_utils.to_df(paddle_fpr,paddle_tpr)
odf.to_csv(
    os.path.join(
        "output",        
        "figures",
        "fig2",
        "2e - Paddle AUROC.csv"
    )
)

odf=auroc_utils.to_df(adpred_fpr,adpred_tpr)
odf.to_csv(
    os.path.join(
        "output",        
        "figures",
        "fig2",
        "2e - Adpred AUROC.csv"
    )
)
