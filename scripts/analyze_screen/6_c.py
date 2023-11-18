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

bipartite_top_hit_testing = pd.read_csv(
    os.path.join(
        "input_data",
        "top_hit_validation",
        "flow",
        "bipartite_top_25_4_target_flow_panel_HEK.csv"
    ),index_col='Construct'
)
for replicate in ['1','2']:
    for target in ['CD45','EPCAM','EGFR','CXCR4']:
        mcp_score = bipartite_top_hit_testing.at['MCP empty','Median '+target+' of BFP+ cells_'+replicate]
        for i in bipartite_top_hit_testing.index:
            bipartite_top_hit_testing.at[i,target+' FC_'+replicate] = bipartite_top_hit_testing.at[i,'Median '+target+' of BFP+ cells_'+replicate]/mcp_score

for target in ['CD45','EPCAM','EGFR','CXCR4']:
    bipartite_top_hit_testing[target+'_average FC'] = bipartite_top_hit_testing[[target+' FC_1',target+' FC_2']].mean(axis=1)

bipartite_top_hit_testing.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig6",
        "6c - Bipartite top 25 hits full panel.csv"
    )
)


for target in ['CD45','EPCAM','EGFR','CXCR4']:
    odf = bipartite_top_hit_testing[[target+' FC_1',target+' FC_2',target+'_average FC']].copy()
    odf.sort_values(by=target+'_average FC',inplace=True,ascending=False)
    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig6",
            "6c - Bipartite top 25 hits {} manual testing.csv".format(target)
        )
    )