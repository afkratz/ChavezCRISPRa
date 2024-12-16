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
                'single_domain_toxicity.csv')
    )
    
    single_domain_tox_df['Construct']=single_domain_tox_df['BC1']
    single_domain_tox_df['Average Tox']=single_domain_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)
    single_domain_tox_df.sort_values(by='Average Tox',inplace=True)

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'screen_output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    bipartite_tox_df['Average Tox']=bipartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)
    bipartite_tox_df.sort_values(by='Average Tox',inplace=True)

    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'screen_output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )
    
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    tripartite_tox_df['Average Tox']=tripartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)
    tripartite_tox_df.sort_values(by='Average Tox',inplace=True)

    res =pd.concat((
        pd.DataFrame({
        "Construct":single_domain_tox_df['Construct'],
        'Type':'Single-domain',
        'EPCAM':single_domain_tox_df['EPCAM_average_Tox'],
        'CXCR4':single_domain_tox_df['CXCR4_average_Tox'],
        'Reporter':single_domain_tox_df['Reporter_average_Tox'],
        'EPCAM and CXCR4 average':single_domain_tox_df['Average Tox'],
    }),
    pd.DataFrame({
        "Construct":bipartite_tox_df['Construct'],
        'Type':'Bipartite',
        'EPCAM':bipartite_tox_df['EPCAM_average_Tox'],
        'CXCR4':bipartite_tox_df['CXCR4_average_Tox'],
        'Reporter':bipartite_tox_df['Reporter_average_Tox'],
        'EPCAM and CXCR4 average':bipartite_tox_df['Average Tox'],
    }),
    pd.DataFrame({
        "Construct":tripartite_tox_df['Construct'],
        'Type':'Tripartite',
        'EPCAM':tripartite_tox_df['EPCAM_average_Tox'],
        'CXCR4':tripartite_tox_df['CXCR4_average_Tox'],
        'Reporter':tripartite_tox_df['Reporter_average_Tox'],
        'EPCAM and CXCR4 average':tripartite_tox_df['Average Tox'],
    })),
    ignore_index=True)

    return res

        

if __name__=="__main__":
    main()