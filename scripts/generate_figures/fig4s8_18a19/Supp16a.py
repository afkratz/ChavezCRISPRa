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

    single_domain_tox_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'screen_output',
            'screen_results',
            'screen_toxicity',
            'single_domain_toxicity.csv'
        )
    )
    single_domain_tox_df['Construct'] = single_domain_tox_df['BC1']
    single_domain_tox_df['Average_Tox']=single_domain_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)
    
    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'screen_output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    bipartite_tox_df['Average_Tox']=bipartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)

    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'screen_output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    tripartite_tox_df['Average_Tox']=tripartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)

    construct_to_tox = dict()
    for i in single_domain_tox_df.index:
        construct = single_domain_tox_df.at[i,'Construct']
        tox = single_domain_tox_df.at[i,'Average_Tox']
        construct_to_tox[construct]=tox

    for i in bipartite_tox_df.index:
        construct = bipartite_tox_df.at[i,'Construct']
        tox = bipartite_tox_df.at[i,'Average_Tox']
        construct_to_tox[construct]=tox

    for i in tripartite_tox_df.index:
        construct = tripartite_tox_df.at[i,'Construct']
        tox = tripartite_tox_df.at[i,'Average_Tox']
        construct_to_tox[construct]=tox

    res = pd.concat((
        pd.DataFrame({
            "Construct":bipartite_tox_df['Construct'],
            'Type':"Bipartite",
            "P1":bipartite_tox_df['BC1'],
            "P2":bipartite_tox_df['BC2'],
            "P3":"NA",
            
        }),
        pd.DataFrame({
            "Construct":tripartite_tox_df['Construct'],
            'Type':"Tripartite",
            "P1":tripartite_tox_df['BC1'],
            "P2":tripartite_tox_df['BC2'],
            "P3":tripartite_tox_df['BC3'],
        })),
        ignore_index=True
    )

    res['P1 single-domain toxicity'] = res.apply(lambda row: construct_to_tox.get(row['P1'],np.nan), axis=1)
    res['P2 single-domain toxicity'] = res.apply(lambda row: construct_to_tox.get(row['P2'],np.nan), axis=1)
    res['P3 single-domain toxicity'] = res.apply(lambda row: construct_to_tox.get(row['P3'],0), axis=1)
    res['Sum of parts single-domain toxicity'] = res[['P1 single-domain toxicity','P2 single-domain toxicity','P3 single-domain toxicity']].values.sum(axis=1)
    res['Multi-partite toxicity'] = res.apply(lambda row:construct_to_tox.get(row['Construct'],np.nan),axis=1)
    
    return res

 

if __name__=="__main__":
    main()