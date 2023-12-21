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
        "figures",
        "fig2",
        "2c - lr preds.csv"
        ),
        index_col="Unnamed: 0"
    )
lr_x = df['Logistic regression predictions'].to_list()
lr_y = df["Hit on any"].to_list()
lr_fpr,lr_tpr = auroc_utils.get_FPR_TPR(lr_x,lr_y)

area = auroc_utils.calculate_auc(lr_fpr,lr_tpr)
print(area)
odf=auroc_utils.to_df(lr_fpr,lr_tpr)
odf.to_csv(
    os.path.join(
        "output",        
        "figures",
        "fig2",
        "2c - LR AUROC.csv"
    )
)