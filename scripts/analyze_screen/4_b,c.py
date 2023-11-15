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

if not os.path.exists(os.path.join("output","figures","fig4")):
    os.mkdir(os.path.join("output","figures","fig4"))


tripartite_tox_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "tripartite_screen_toxicity.csv"
    )
)


b_df = tripartite_tox_df[['BC1','BC2','BC3','P3 Plasmid']].copy()
b_df['EPCAM_Average_NS']=tripartite_tox_df[["EPCAM_1_NS","EPCAM_2_NS"]].values.mean(axis=1)
b_df['CXCR4_Average_NS']=tripartite_tox_df[["CXCR4_1_NS","CXCR4_2_NS"]].values.mean(axis=1)
b_df['Reporter_Average_NS']=tripartite_tox_df[["Reporter_1_NS","Reporter_2_NS"]].values.mean(axis=1)

b_df.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4b - P3 Plasmid vs Average_NS.csv"
    ),index=False
)

c_df = tripartite_tox_df[['BC1','BC2','BC3','EPCAM_1_NS','EPCAM_2_NS','CXCR4_1_NS','CXCR4_2_NS','Reporter_1_NS','Reporter_2_NS']].copy()
c_df.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4c - NS replicate vs replicate.csv"
    ),index=False
)