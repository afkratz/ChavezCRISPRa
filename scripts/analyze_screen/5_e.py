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

single_domain_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_single_domain_screen_scored.csv",
        
    )
)

bipartite_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_bipartite_screen_scored.csv"
    )
)

tripartite_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_tripartite_screen_scored.csv"
    )
)





all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

for target in 'EPCAM','CXCR4','Reporter':
    ad_to_single_domain_score_list=dict()
    ad_to_bipartite_score_list=dict()
    ad_to_tripartite_score_list=dict()

    for ad in all_barcodes:
        ad_to_single_domain_score_list[ad]=list()
        ad_to_bipartite_score_list[ad]=list()
        ad_to_tripartite_score_list[ad]=list()
    
    for i in single_domain_score_df.index:
        bc1 = single_domain_score_df.at[i,'BC1']
        score = single_domain_score_df.at[i,target+"_average"]
        ad_to_single_domain_score_list[bc1].append(score)

    for i in bipartite_score_df.index:
        bc1 = bipartite_score_df.at[i,'BC1']
        bc2 = bipartite_score_df.at[i,'BC2']
        score = bipartite_score_df.at[i,target+"_average"]
        ad_to_bipartite_score_list[bc1].append(score)    
        ad_to_bipartite_score_list[bc2].append(score)    
        
    for i in tripartite_score_df.index:
        if tripartite_score_df.at[i,'Has '+target+' score']:
            bc1 = tripartite_score_df.at[i,'BC1']
            bc2 = tripartite_score_df.at[i,'BC2']
            bc3 = tripartite_score_df.at[i,'BC3']
            score = tripartite_score_df.at[i,target+"_average"]
            ad_to_tripartite_score_list[bc1].append(score)     
            ad_to_tripartite_score_list[bc2].append(score)
            ad_to_tripartite_score_list[bc3].append(score)   
    
    odf = pd.DataFrame()
    odf['Activator']=""
    odf['Single domain median score on {}'.format(target)]=np.nan
    odf['Bipartite median score on {}'.format(target)]=np.nan
    odf['Tripartite median score on {}'.format(target)]=np.nan

    for i,ad in enumerate(all_barcodes):
        odf.at[i,'Activator']=ad
        odf.at[i,'Single domain median score on {}'.format(target)] = np.median(ad_to_single_domain_score_list[ad])
        odf.at[i,'Bipartite median score on {}'.format(target)] = np.median(ad_to_bipartite_score_list[ad])
        odf.at[i,'Tripartite median score on {}'.format(target)] = np.median(ad_to_tripartite_score_list[ad])
    
    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig5",
            "5e - AD median {} activity.csv".format(target)
        ),index=False
    )