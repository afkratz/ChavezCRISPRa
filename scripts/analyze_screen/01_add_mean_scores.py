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
p3_score['Has EPCAM score']=(p3_score[["EPCAM_1","EPCAM_2"]].values!=None).all(axis=1)
p3_score['Has CXCR4 score']=(p3_score[["CXCR4_1","CXCR4_2"]].values!=None).all(axis=1)
p3_score['Has Reporter score']=(p3_score[["Reporter_1","Reporter_2"]].values!=None).all(axis=1)
p3_score['Has all scores']=p3_score[['Has EPCAM score','Has CXCR4 score','Has Reporter score']].values.all(axis=1)


if not os.path.exists(os.path.join("output","screen_analysis")):
    os.mkdir(os.path.join("output","screen_analysis"))
if not os.path.exists(os.path.join("output","screen_analysis","activity_analysis")):
    os.mkdir(os.path.join("output","screen_analysis","activity_analysis"))

for df in p1_score,p2_score,p3_score:
    df['EPCAM_average']=df[["EPCAM_1","EPCAM_2"]].mean(axis=1)
    df['CXCR4_average']=df[["CXCR4_1","CXCR4_2"]].mean(axis=1)
    df['Reporter_average']=df[["Reporter_1","Reporter_2"]].mean(axis=1)

p3_score.loc[(p3_score['Has EPCAM score']==False),'EPCAM_average']=np.nan
p3_score.loc[(p3_score['Has CXCR4 score']==False),'CXCR4_average']=np.nan
p3_score.loc[(p3_score['Has Reporter score']==False),'Reporter_average']=np.nan
    

p1_score.to_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "single_domain_screen_scored_with_means.csv"
    ),
    index=False
)

p2_score.to_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "bipartite_screen_scored_with_means.csv"
    ),
    index=False
)

p3_score.to_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "tripartite_screen_scored_with_means.csv"
    ),
    index=False
)