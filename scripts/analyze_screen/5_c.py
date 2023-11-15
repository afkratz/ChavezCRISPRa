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

all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))


for target in ['EPCAM','CXCR4','Reporter']:
    odf = pd.DataFrame()
    odf['BC_A']=""
    odf['BC_B']=""

    for i in range(len(all_barcodes)-1):
        bc_A = all_barcodes[i]
        for j in range(i+1,len(all_barcodes)):
            bc_B = all_barcodes[j]
            index = len(odf)
            odf.at[index,'BC_A']=bc_A
            odf.at[index,'BC_B']=bc_B
            odf.at[index,'A-B score']=bcs_to_scores[(bc_A,bc_B)][target]
            odf.at[index,'B-A score']=bcs_to_scores[(bc_B,bc_A)][target]
    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig5",
            "5c - bipartite fw rv {} activity.csv".format(target)
        ),index=False
    )

for target in ['EPCAM','CXCR4','Reporter']:
    odf = pd.DataFrame()
    odf['BC_A']=""
    odf['Middle_BC']=""
    odf['BC_B']=""
    for i in range(len(all_barcodes)-1):
        bc_A = all_barcodes[i]
        for j in range(i+1,len(all_barcodes)):
            bc_B = all_barcodes[j]
            for middle_barcode in all_barcodes:
                A_mid_B_score =  bcs_to_scores[(bc_A,middle_barcode,bc_B)][target]
                B_mid_A_score =  bcs_to_scores[(bc_B,middle_barcode,bc_A)][target]
                if A_mid_B_score!=None and B_mid_A_score!=None:
                    index = len(odf)
                    odf.at[index,'BC_A']=bc_A
                    odf.at[index,'Middle_BC']=middle_barcode
                    odf.at[index,'BC_B']=bc_B
                    odf.at[index,'A-mid-B score']=A_mid_B_score
                    odf.at[index,'B-mid-A score']=B_mid_A_score               
    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig5",
            "5c - tripartite fw rv {} activity.csv".format(target)
        ),index=False
    )

for target in ['EPCAM','CXCR4','Reporter']:
    odf = pd.DataFrame()
    odf['BC_A']=""
    odf['Middle_BC']=""
    odf['BC_B']=""

    for i in range(len(all_barcodes)-1):
        bc_A = all_barcodes[i]
        for j in range(i+1,len(all_barcodes)):
            bc_B = all_barcodes[j]
            for middle_barcode in all_barcodes:

                pfd_count = (bc_A,middle_barcode,bc_B).count('A23')+(bc_A,middle_barcode,bc_B).count('A25')
                if pfd_count==0:
                    continue

                A_mid_B_score =  bcs_to_scores[(bc_A,middle_barcode,bc_B)][target]
                B_mid_A_score =  bcs_to_scores[(bc_B,middle_barcode,bc_A)][target]
                if A_mid_B_score!=None and B_mid_A_score!=None:
                    index = len(odf)
                    odf.at[index,'BC_A']=bc_A
                    odf.at[index,'Middle_BC']=middle_barcode
                    odf.at[index,'BC_B']=bc_B
                    odf.at[index,'A-mid-B score']=A_mid_B_score
                    odf.at[index,'B-mid-A score']=B_mid_A_score               
    odf.to_csv(
        os.path.join(
            "output",
            "figures",
            "fig5",
            "5c - tripartite with pfd fw rv {} activity.csv".format(target)
        ),index=False
    )