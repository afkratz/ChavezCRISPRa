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


if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","fig3")):
    os.mkdir(os.path.join("output","figures","fig3"))

p1_scores = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_single_domain_screen_scored.csv"
    )
)

p2_scores = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_bipartite_screen_scored.csv"
    )
)

p3_scores = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_tripartite_screen_scored.csv"
    )
)


p1_scores.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig3",
        "3d - Single domain all replicates.csv"
    )
)

p2_scores.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig3",
        "3d - Bipartite all replicates.csv"
    )
)

for target in ['EPCAM','CXCR4','Reporter']:
    p3_scored = p3_scores[p3_scores['Has '+target+' score']].copy()
    p3_scored.drop('Has EPCAM score',axis=1,inplace=True)
    p3_scored.drop('Has CXCR4 score',axis=1,inplace=True)
    p3_scored.drop('Has Reporter score',axis=1,inplace=True)
    p3_scored.drop('Has all scores',axis=1,inplace=True)
    
    for drop_target in ['EPCAM','CXCR4','Reporter']:
        if target==drop_target:
            continue
        p3_scored.drop(drop_target+"_1",axis=1,inplace=True)
        p3_scored.drop(drop_target+"_2",axis=1,inplace=True)
        p3_scored.drop(drop_target+"_average",axis=1,inplace=True)
    

    
    p3_scored.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig3",
            "3d - Tripartite "+target+" replicates.csv"
    ),index=False
    )