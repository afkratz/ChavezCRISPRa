# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import pandas as pd

os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from src import screen_scoring_tools as sst

p1_score = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_scores",
        "single_domain_screen_scored.csv"
    )
)

p2_score = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_scores",
        "bipartite_screen_scored.csv"
    )
)

p3_score = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_scores",
        "tripartite_screen_scored.csv"
    )
)
p3_score.replace(np.nan,None,inplace=True)

p3_score = p3_score[(p3_score.values!=None).all(axis=1)].reset_index()

if not os.path.exists(os.path.join("output","screen_analysis")):
    os.mkdir(os.path.join("output","screen_analysis"))

if not os.path.exists(os.path.join("output","screen_analysis","activity_analysis")):
    os.mkdir(os.path.join("output","screen_analysis","activity_analysis"))

for df in p1_score,p2_score,p3_score:
    df['EPCAM_average']=df[["EPCAM_1","EPCAM_2"]].mean(axis=1)
    df['CXCR4_average']=df[["CXCR4_1","CXCR4_2"]].mean(axis=1)
    df['Reporter_average']=df[["Reporter_1","Reporter_2"]].mean(axis=1)
    
    sst.calculate_zscore(df,"EPCAM_average","EPCAM_Zscore")
    sst.calculate_zscore(df,"CXCR4_average","CXCR4_Zscore")
    sst.calculate_zscore(df,"Reporter_average","Reporter_Zscore")
    

p1_score.to_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_single_domain_screen_scored_with_zscore.csv"
    ),
    index=False
)

p2_score.to_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_bipartite_screen_scored_with_zscore.csv"
    ),
    index=False
)

p3_score.to_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_tripartite_screen_scored_with_zscore.csv"
    ),
    index=False
)