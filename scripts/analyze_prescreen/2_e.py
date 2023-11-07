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

import pandas as pd
df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "04_manually_tested_paddle_charachterized.csv"),
        index_col="Unnamed: 0"
    )

x = df["Score"].to_list()
y = df["Hit on any"]
fpr,tpr = auroc_utils.get_FPR_TPR(x,y)
df=auroc_utils.to_df(fpr,tpr)
df.to_csv(
    os.path.join(
        "output",        
        "figures",
        "fig2",
        "2e - PADDLE vs hit-any AUROC.csv"
    )
)
