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

growth_results = pd.read_csv(
    os.path.join(
        "input_data",
        "competitive_growth_toxicity",
        "GFP_competitive_growth_toxicity_results.csv"
    )
)

tripartite_tox_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "tripartite_screen_toxicity.csv"
    )
)

tripartite_tox_dict = dict()
for i in tripartite_tox_df.index:
    bc1 = tripartite_tox_df.at[i,'BC1']
    bc2 = tripartite_tox_df.at[i,'BC2']
    bc3 = tripartite_tox_df.at[i,'BC3']
    construct ="_".join((bc1,bc2,bc3))
    toxicity = tripartite_tox_df.at[i,'CX&EP Average Tox']
    tripartite_tox_dict[construct]=toxicity

growth_results['Screen toxicity']=np.nan
for i in growth_results.index:
    construct = growth_results.at[i,'Construct']
    if construct in ("MCP-mutant","GFP only"):
        continue
    growth_results.at[i,'Screen toxicity']=tripartite_tox_dict[construct]

growth_results.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4h,i - GFP competition plus screen tox.csv"
    ),index=False
)
    
