# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import numpy as np
import pandas as pd
import os
from pathlib import Path

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    all_bcs = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    res = pd.DataFrame()

    single_domain_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'single_domain_toxicity.csv')
    )#Columns = [BC1,P1 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]
    
    ad_to_tox = dict()
    for i in single_domain_tox_df.index:
        tox = single_domain_tox_df.at[i,'CX&EP Average Tox']

        bc1 = single_domain_tox_df.at[i,'BC1']    
        if bc1 not in ad_to_tox:
            ad_to_tox[bc1]=list()
        ad_to_tox[bc1].append(tox)

    for i,bc in enumerate(all_bcs):
        res.at[i,'AD']=bc
        res.at[i,'Single-domain']=np.median(ad_to_tox[bc])

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,P2 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]
    
    ad_to_tox = dict()
    for i in bipartite_tox_df.index:
        tox = bipartite_tox_df.at[i,'CX&EP Average Tox']

        bc1 = bipartite_tox_df.at[i,'BC1']    
        if bc1 not in ad_to_tox:
            ad_to_tox[bc1]=list()
        ad_to_tox[bc1].append(tox)

        bc2 = bipartite_tox_df.at[i,'BC2']
        if bc2 not in ad_to_tox:
            ad_to_tox[bc2]=list()
        ad_to_tox[bc2].append(tox)
    
    for i,bc in enumerate(all_bcs):
        res.at[i,'Bipartite']=np.median(ad_to_tox[bc])


    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,BC3,P3 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]

    ad_to_tox = dict()
    for i in tripartite_tox_df.index:
        tox = tripartite_tox_df.at[i,'CX&EP Average Tox']

        bc1 = tripartite_tox_df.at[i,'BC1']    
        if bc1 not in ad_to_tox:
            ad_to_tox[bc1]=list()
        ad_to_tox[bc1].append(tox)

        bc2 = tripartite_tox_df.at[i,'BC2']
        if bc2 not in ad_to_tox:
            ad_to_tox[bc2]=list()
        ad_to_tox[bc2].append(tox)
    
        bc3 = tripartite_tox_df.at[i,'BC3']
        if bc3 not in ad_to_tox:
            ad_to_tox[bc3]=list()
        ad_to_tox[bc3].append(tox)

    for i,bc in enumerate(all_bcs):
        res.at[i,'Tripartite']=np.median(ad_to_tox[bc])        
    
    return res
