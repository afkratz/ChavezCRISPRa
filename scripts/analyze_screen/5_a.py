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

if not os.path.exists(os.path.join("output","figures","fig5")):
    os.mkdir(os.path.join("output","figures","fig5"))

bipartite_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_bipartite_screen_scored.csv"
    )
)


all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

construct_to_scores = dict()
for i in bipartite_score_df.index:
    bc1 = bipartite_score_df.at[i,'BC1']
    bc2 = bipartite_score_df.at[i,'BC2']
    for target in ['EPCAM','CXCR4','Reporter']:
        construct_to_scores[((bc1,bc2),target)]=bipartite_score_df.at[i,target+"_average"]


bc_to_all_scores = dict()
for bc in all_barcodes:
    bc_to_all_scores[bc]=dict()
    bc_to_all_scores[bc]['EPCAM']=[] 
    bc_to_all_scores[bc]['CXCR4']=[] 
    bc_to_all_scores[bc]['Reporter']=[] 
    
for i in bipartite_score_df.index:
    bc1 = bipartite_score_df.at[i,'BC1']
    bc2 = bipartite_score_df.at[i,'BC2']
    for bc in (bc1,bc2):
        for target in ['EPCAM','CXCR4','Reporter']:
            bc_to_all_scores[bc][target].append(bipartite_score_df.at[i,target+"_average"])

bc_to_median_scores = dict()
for bc in all_barcodes:
    for target in ['EPCAM','CXCR4','Reporter']:
        bc_to_median_scores[(bc,target)]=np.median(bc_to_all_scores[bc][target])
        
epcam_rankings = sorted(all_barcodes,key = lambda x:bc_to_median_scores[(x,'EPCAM')])


odf = pd.DataFrame()

for bc1 in epcam_rankings:
    for bc2 in epcam_rankings:
        odf.at[bc1,bc2] = construct_to_scores[((bc1,bc2),'EPCAM')]

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig5",
        "5a - EPCAM score square.csv"
    )
)