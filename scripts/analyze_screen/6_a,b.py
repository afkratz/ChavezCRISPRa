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

def make_rank(arr:np.array)->np.array:
    ranked_indices = np.argsort(np.argsort(-arr))#negative to assign low number to top scores
    ranked_values = ranked_indices + 1
    return ranked_values

if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","fig6")):
    os.mkdir(os.path.join("output","figures","fig6"))


bipartite_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "bipartite_screen_scored_with_means.csv"
    )
).dropna()

tripartite_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "tripartite_screen_scored_with_means.csv"
    )
)

tripartite_score_df=tripartite_score_df[tripartite_score_df["Has all scores"]]


for target in ['EPCAM','CXCR4','Reporter']:
    bipartite_score_df[target+'_rank']=make_rank(bipartite_score_df[target+"_average"])
    tripartite_score_df[target+'_rank']=make_rank(tripartite_score_df[target+"_average"])

bipartite_score_df['Sum of ranks']=bipartite_score_df[['EPCAM_rank','CXCR4_rank','Reporter_rank']].values.sum(axis=1)
tripartite_score_df['Sum of ranks']=tripartite_score_df[['EPCAM_rank','CXCR4_rank','Reporter_rank']].values.sum(axis=1)
bipartite_score_df.sort_values(by='Sum of ranks',inplace=True)
tripartite_score_df.sort_values(by='Sum of ranks',inplace=True)
bipartite_score_df.reset_index(inplace=True)
tripartite_score_df.reset_index(inplace=True)

bipartite_score_df['Is top hit'] = bipartite_score_df.index<25
tripartite_score_df['Is top hit'] = tripartite_score_df.index<25


bipartite_score_df.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig6",
        "6a - Bipartite top hits.csv"
    ),index=False
)

tripartite_score_df.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig6",
        "6b - Tripartite top hits.csv"
    ),index=False
)