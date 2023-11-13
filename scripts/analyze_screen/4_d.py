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


construct_to_tox = dict()
for i in bipartite_tox_df.index:
    bc1 = bipartite_tox_df.at[i,'BC1']
    bc2 = bipartite_tox_df.at[i,'BC2']
    construct = bc1+"_"+bc2
    toxicity = bipartite_tox_df.at[i,'CX&EP Average Tox']
    construct_to_tox[construct] = toxicity

for i in tripartite_tox_df.index:
    bc1 = tripartite_tox_df.at[i,'BC1']
    bc2 = tripartite_tox_df.at[i,'BC2']
    bc3 = tripartite_tox_df.at[i,'BC3']

    construct = bc1+"_"+bc2+"_"+bc3
    toxicity = tripartite_tox_df.at[i,'CX&EP Average Tox']
    construct_to_tox[construct] = toxicity

all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))


odf = pd.DataFrame()
for i in range(0,len(all_barcodes)-1):
    for middle_bc in all_barcodes:
        for j in range(1,len(all_barcodes)):
            index = len(odf)
            bc_a = all_barcodes[i]
            bc_b = all_barcodes[j]
            odf.at[index,'BC A']=bc_a
            odf.at[index,'Middle BC']=middle_bc
            odf.at[index,'BC B']=bc_b
            a_mid_b_tox = construct_to_tox[bc_a+"_"+middle_bc+"_"+bc_b]

            b_mid_a_tox = construct_to_tox[bc_b+"_"+middle_bc+"_"+bc_a]
            odf.at[index,'A-X-B toxicity']=a_mid_b_tox
            odf.at[index,'B-X-A toxicity']=b_mid_a_tox

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4d - tripartite fw rv toxicity.csv"
    ),index=False
)

