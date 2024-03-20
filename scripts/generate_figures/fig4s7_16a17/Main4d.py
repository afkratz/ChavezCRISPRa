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

def reverse_construct(construct:str)->str:
    return "_".join(construct.split("_")[::-1])

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    
    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,BC3,P3 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    pfds = ['A23','A25']
    tripartite_tox_df['PFD count'] = tripartite_tox_df.apply(
        lambda row: pfds.count(row['BC1'])+pfds.count(row['BC2'])+pfds.count(row['BC3']),
        axis=1
    )
    tripartite_tox_df['Has A24'] = tripartite_tox_df.apply(
        lambda row: row['BC1']=='A24' or row['BC2']=='A24' or row['BC3']=='A24',
        axis=1
    )
    construct_to_tox = dict()
    for i in tripartite_tox_df.index:
        construct = tripartite_tox_df.at[i,'Construct']
        tox = tripartite_tox_df.at[i,'CX&EP Average Tox']
        construct_to_tox[construct]=tox

    res = pd.DataFrame()

    seen = set()
    for i in tripartite_tox_df.index:
        if tripartite_tox_df.at[i,'Has A24']:continue
        if tripartite_tox_df.at[i,'PFD count']==1:
            construct = tripartite_tox_df.at[i,'Construct']
            reverse = reverse_construct(construct)
            if construct==reverse:
                continue
            
            if construct not in seen and reverse not in seen:
                seen.add(construct)
                seen.add(reverse)
                res.at[i,'Construct']=construct
                res.at[i,'Activator type']='Tripartite'
                res.at[i,'P1']=tripartite_tox_df.at[i,'BC1']
                res.at[i,'P2']=tripartite_tox_df.at[i,'BC2']
                res.at[i,'P3']=tripartite_tox_df.at[i,'BC3']
                res.at[i,'Reverse_construct']=reverse
                res.at[i,'Forward toxicity']=construct_to_tox[construct]
                res.at[i,'Reverse toxicity']=construct_to_tox[reverse]
                res.at[i,'ADs only?']=False
                res.at[i,'Tripartite_1 PF only']=True
    
    return res

