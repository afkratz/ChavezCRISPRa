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

tripartite_score_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_tripartite_screen_scored.csv"
    )
)

for i in tripartite_score_df.index:
    bc1 = tripartite_score_df.at[i,'BC1']
    bc2 = tripartite_score_df.at[i,'BC2']
    bc3 = tripartite_score_df.at[i,'BC3']
    
    bcs_to_scores[(bc1,bc2,bc3)]=dict()
    for target in ['EPCAM','CXCR4','Reporter']:
        if tripartite_score_df.at[i,'Has '+target+' score']:
            score = tripartite_score_df.at[i,target+"_average"]
        else:
            score = None
        bcs_to_scores[(bc1,bc2,bc3)][target]=score

#all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
activator_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,23)))

for target in ['EPCAM','CXCR4','Reporter']:
    odf = pd.DataFrame()
    odf['Activator']=""
    for i,ad in enumerate(activator_barcodes):
        odf.at[i,'Activator']=ad
        odf.at[i,'AD-AD score']=bcs_to_scores[(ad,ad)][target]
        odf.at[i,'Median score with PFD'] = np.median((
            bcs_to_scores[(ad,'A23')][target],
            bcs_to_scores[('A23',ad)][target],
            bcs_to_scores[(ad,'A25')][target],
            bcs_to_scores[('A25',ad)][target],
        ))
        odf.at[i,'AD-A23 score']=bcs_to_scores[(ad,'A23')][target]
        odf.at[i,'A23-AD score']=bcs_to_scores[('A23',ad)][target]
        odf.at[i,'AD-A25 score']=bcs_to_scores[(ad,'A25')][target]
        odf.at[i,'A25-AD score']=bcs_to_scores[('A23',ad)][target]
        
    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig5",
            "5d - bipartite two copy vs with pfd {} activity.csv".format(target)
        ),index=False
    )

for target in ['EPCAM','CXCR4','Reporter']:
    
    

    tripartite_copy_number_results={}

    for key in bcs_to_scores:
        if len(key)==2:continue #Ignore the bipartites
        if 'A24' in key:continue #Ignore the non-normal PFD
        if bcs_to_scores[key][target]==None:continue #Ignore activators we don't have scores for

        pfd_count = key.count('A23')+key.count('A25')
        present_activators = set(key).intersection(set(activator_barcodes))
        if len(present_activators)==1:
            activator = present_activators.pop()
            activator_copy_number = key.count(activator)
            assert (activator_copy_number+pfd_count)==3
            copy_number_key= (activator,activator_copy_number)
            if copy_number_key not in tripartite_copy_number_results:
                tripartite_copy_number_results[copy_number_key]=[]
            tripartite_copy_number_results[copy_number_key].append(bcs_to_scores[key][target])
    
    odf = pd.DataFrame()
    odf['Activator']=""
    odf['1 copy + 2 pfd Median']=np.nan
    odf['1 copy + 2 pfd N']=0
    odf['2 copy + 1 pfd Median']=np.nan
    odf['2 copy + 1 pfd N']=0
    odf['3 copy + 0 pfd Median']=np.nan
    odf['3 copy + 0 pfd N']=0
    for i,ad in enumerate(activator_barcodes):
        odf.at[i,'Activator']=ad
        if (ad,1) in tripartite_copy_number_results:
            odf.at[i,'1 copy + 2 pfd Median']=np.median(
                tripartite_copy_number_results[(ad,1)]
            )
            odf.at[i,'1 copy + 2 pfd N']=len(tripartite_copy_number_results[(ad,1)])

        if (ad,2) in tripartite_copy_number_results:
            odf.at[i,'2 copy + 1 pfd Median']=np.median(
                tripartite_copy_number_results[(ad,2)]
            )
            odf.at[i,'2 copy + 1 pfd N']=len(tripartite_copy_number_results[(ad,2)])

        if (ad,3) in tripartite_copy_number_results:
            odf.at[i,'3 copy + 0 pfd Median']=np.median(
                tripartite_copy_number_results[(ad,3)]
            )
            odf.at[i,'3 copy + 0 pfd N']=len(tripartite_copy_number_results[(ad,3)])
        
        

    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig5",
            "5d - tripartite N copy number {} activity.csv".format(target)
        ),index=False
    )