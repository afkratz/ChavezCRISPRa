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
    
    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    bipartite_tox_df['Average_Tox']=bipartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)
    pfds = ['A23','A25']
    bipartite_tox_df['PFD count'] = bipartite_tox_df.apply(
        lambda row: pfds.count(row['BC1'])+pfds.count(row['BC2']),
        axis=1
    )
    bipartite_tox_df['Has A24'] = bipartite_tox_df.apply(
        lambda row: row['BC1']=='A24' or row['BC2']=='A24',
        axis=1
    )


    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )

    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    tripartite_tox_df['Average_Tox']=tripartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)
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
    for index in bipartite_tox_df.index:
        construct = bipartite_tox_df.at[index,'Construct']
        tox = bipartite_tox_df.at[index,'Average_Tox']
        construct_to_tox[construct]=tox

    for index in tripartite_tox_df.index:
        construct = tripartite_tox_df.at[index,'Construct']
        tox = tripartite_tox_df.at[index,'Average_Tox']
        construct_to_tox[construct]=tox

    res = pd.DataFrame()

    seen = set()
    for index in bipartite_tox_df.index:
        construct = bipartite_tox_df.at[index,'Construct']
        reverse = reverse_construct(construct)
        if construct==reverse:
            continue
        if construct not in seen and reverse not in seen:
            seen.add(construct)
            seen.add(reverse)
            res.at[construct,'Construct']=construct
            res.at[construct,'Activator type']='Bipartite'
            res.at[construct,'P1']=bipartite_tox_df.at[index,'BC1']
            res.at[construct,'P2']=bipartite_tox_df.at[index,'BC2']
            res.at[construct,'P3']=np.nan
            res.at[construct,'Reverse_construct']=reverse
            res.at[construct,'Forward toxicity']=construct_to_tox[construct]
            res.at[construct,'Reverse toxicity']=construct_to_tox[reverse]
            res.at[construct,'ADs only?']=bipartite_tox_df.at[index,'PFD count']==0 and not bipartite_tox_df.at[index,'Has A24']
            res.at[construct,'Tripartite_1 PF only']=False

    for index in tripartite_tox_df.index:
        if tripartite_tox_df.at[index,'Has A24']:continue
        if tripartite_tox_df.at[index,'PFD count']==1:
            construct = tripartite_tox_df.at[index,'Construct']
            reverse = reverse_construct(construct)
            if construct==reverse:
                continue
            
            if construct not in seen and reverse not in seen:
                seen.add(construct)
                seen.add(reverse)
                res.at[construct,'Construct']=construct
                res.at[construct,'Activator type']='Tripartite'
                res.at[construct,'P1']=tripartite_tox_df.at[index,'BC1']
                res.at[construct,'P2']=tripartite_tox_df.at[index,'BC2']
                res.at[construct,'P3']=tripartite_tox_df.at[index,'BC3']
                res.at[construct,'Reverse_construct']=reverse
                res.at[construct,'Forward toxicity']=construct_to_tox[construct]
                res.at[construct,'Reverse toxicity']=construct_to_tox[reverse]
                res.at[construct,'ADs only?']=False
                res.at[construct,'Tripartite_1 PF only']=True
    
    return res

if __name__=="__main__":
    main()