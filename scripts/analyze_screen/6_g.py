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

hela_flow_results = pd.read_csv(
    os.path.join(
        "input_data",
        "top_hit_validation",
        "final_2_4_target_flow_hela.csv"
    ),index_col='Activator'
)

odf = pd.DataFrame()
for target in ['CD2','CD45','EPCAM','EGFR']:
    for activator in ['MHV','MMH','SAM','MCP-empty']:
        for replicate in (1,2):
            activator_median_fi = hela_flow_results.at[activator,'Median {} of BFP+ rep {}'.format(target,replicate)]
            mcp_median_fi = hela_flow_results.at['MCP-empty','Median {} of BFP+ rep {}'.format(target,replicate)]
            
            odf.at[activator,"{} fc replicate {}".format(target,replicate)] =activator_median_fi/mcp_median_fi

odf.to_csv(
    os.path.join(
        'output',
        'figures',
        'fig6','6g - Final 2 4target panel HELA.csv'
    )
)