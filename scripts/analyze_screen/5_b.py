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


bipartite_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_bipartite_screen_scored.csv"
    )
)

bcs_to_scores = dict()
for i in bipartite_score_df.index:
    bc1 = bipartite_score_df.at[i,'BC1']
    bc2 = bipartite_score_df.at[i,'BC2']
    bcs_to_scores[(bc1,bc2)]=dict()
    for target in ['EPCAM','CXCR4','Reporter']:
        score = bipartite_score_df.at[i,target+"_average"]
        bcs_to_scores[(bc1,bc2)][target]=score

activator_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,22)))

pfd_barcodes = ['A23','A25']
for target in ['EPCAM','CXCR4','Reporter']:
    activator_to_result_list = dict()
    for ad in activator_barcodes:
        activator_to_result_list[ad]=dict()
        activator_to_result_list[ad]['PFDs']=[]
        activator_to_result_list[ad]['ADs']=[]
    for i in bipartite_score_df.index:
        bc1 = bipartite_score_df.at[i,'BC1']
        bc2 = bipartite_score_df.at[i,'BC2']
        score = bipartite_score_df.at[i,target+"_average"]
        
        if bc1 in activator_barcodes:
            if bc2 in activator_barcodes:
                activator_to_result_list[bc1]['ADs'].append(score)
            if bc2 in pfd_barcodes:
                activator_to_result_list[bc1]['PFDs'].append(score)
        
        if bc2 in activator_barcodes:
            if bc1 in activator_barcodes:
                activator_to_result_list[bc2]['ADs'].append(score)
            if bc1 in pfd_barcodes:
                activator_to_result_list[bc2]['PFDs'].append(score)
    
    odf = pd.DataFrame()
    odf['Activator']=""
    for i,ad in enumerate(activator_barcodes):
        odf.at[i,'Activator'] = ad
        odf.at[i,'Median performance with PFD partner']= np.median(activator_to_result_list[ad]['PFDs'])
        odf.at[i,'Median performance with AD partner']= np.median(activator_to_result_list[ad]['ADs'])
        for other_ad in activator_barcodes:
            odf.at[i,"X_"+other_ad]=bcs_to_scores[(ad,other_ad)][target]
            odf.at[i,other_ad+"_X"]=bcs_to_scores[(other_ad,ad)][target]
        for pfd in pfd_barcodes:
            odf.at[i,"X_"+pfd]=bcs_to_scores[(ad,pfd)][target]
            odf.at[i,pfd+"_X"]=bcs_to_scores[(pfd,ad)][target]
        
        
            
        
    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig5",
            "5b - {} scores with PFD or AD partner.csv".format(target)
        ),index=False
    )    
    