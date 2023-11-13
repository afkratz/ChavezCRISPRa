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

bipartite_tox_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "bipartite_screen_toxicity.csv"
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


all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

odf = pd.DataFrame()

for i,bc in enumerate(all_barcodes):
    average_tox_in_p1 = bipartite_tox_df[bipartite_tox_df['BC1']==bc]['CX&EP Average Tox'].values.mean()
    average_tox_in_p2 = bipartite_tox_df[bipartite_tox_df['BC2']==bc]['CX&EP Average Tox'].values.mean()
    odf.at[i,'BC']=bc
    odf.at[i,'Tox in p1']=average_tox_in_p1
    odf.at[i,'Tox in p2']=average_tox_in_p2

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4e - bipartite p1 v p2 v p3 toxicity.csv"
    ),index=False
)
    
odf = pd.DataFrame()

for i,bc in enumerate(all_barcodes):
    average_tox_in_p1 = tripartite_tox_df[tripartite_tox_df['BC1']==bc]['CX&EP Average Tox'].values.mean()
    average_tox_in_p2 = tripartite_tox_df[tripartite_tox_df['BC2']==bc]['CX&EP Average Tox'].values.mean()
    average_tox_in_p3 = tripartite_tox_df[tripartite_tox_df['BC3']==bc]['CX&EP Average Tox'].values.mean()
    
    odf.at[i,'BC']=bc
    odf.at[i,'Tox in p1']=average_tox_in_p1
    odf.at[i,'Tox in p2']=average_tox_in_p2
    odf.at[i,'Tox in p3']=average_tox_in_p3
    

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4e - tripartite p1 v p2 toxicity.csv"
    ),index=False
)

