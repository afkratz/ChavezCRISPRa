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
    
    single_domain_plasmid_NS = pd.DataFrame(
        {
            'Activator':single_domain_tox_df['BC1'],
            'Type':'Single-domain',
            'Plasmid library':single_domain_tox_df['P1 Plasmid'],

            'EPCAM 1 NS':single_domain_tox_df['EPCAM_1_NS'],
            'EPCAM 2 NS':single_domain_tox_df['EPCAM_2_NS'],
            'EPCAM NS average':single_domain_tox_df[['EPCAM_1_NS','EPCAM_2_NS']].values.mean(axis=1),

            'CXCR4 1 NS':single_domain_tox_df['CXCR4_1_NS'],
            'CXCR4 2 NS':single_domain_tox_df['CXCR4_2_NS'],
            'CXCR4 NS average':single_domain_tox_df[['CXCR4_1_NS','CXCR4_2_NS']].values.mean(axis=1),

            'Reporter 1 NS':single_domain_tox_df['Reporter_1_NS'],
            'Reporter 2 NS':single_domain_tox_df['Reporter_2_NS'],
            'Reporter NS average':single_domain_tox_df[['Reporter_1_NS','Reporter_2_NS']].values.mean(axis=1),
            
            'EPCAM ranked?':True,
            'CXCR4 ranked?':True,
            'Reporter ranked?':True,           
        }
    )

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'screen_output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    bipartite_plasmid_NS = pd.DataFrame(
        {
            'Activator':bipartite_tox_df['Construct'],
            'Type':'Bipartite',
            'Plasmid library':bipartite_tox_df['P2 Plasmid'],

            'EPCAM 1 NS':bipartite_tox_df['EPCAM_1_NS'],
            'EPCAM 2 NS':bipartite_tox_df['EPCAM_2_NS'],
            'EPCAM NS average':bipartite_tox_df[['EPCAM_1_NS','EPCAM_2_NS']].values.mean(axis=1),

            'CXCR4 1 NS':bipartite_tox_df['CXCR4_1_NS'],
            'CXCR4 2 NS':bipartite_tox_df['CXCR4_2_NS'],
            'CXCR4 NS average':bipartite_tox_df[['CXCR4_1_NS','CXCR4_2_NS']].values.mean(axis=1),

            'Reporter 1 NS':bipartite_tox_df['Reporter_1_NS'],
            'Reporter 2 NS':bipartite_tox_df['Reporter_2_NS'],
            'Reporter NS average':bipartite_tox_df[['Reporter_1_NS','Reporter_2_NS']].values.mean(axis=1),
            
            'EPCAM ranked?':True,
            'CXCR4 ranked?':True,
            'Reporter ranked?':True,           
        }
    )

    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'screen_output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    tripartite_score_df = pd.read_csv(
        os.path.join(
           ChavezCIRSPRa_root_dir,
           'screen_output',
           'screen_results',
           'screen_scores',
           'tripartite_screen_scored.csv'
        )
    ).replace(np.nan,None)
    

    tripartite_plasmid_NS = pd.DataFrame(
        {
            'Activator':tripartite_tox_df['Construct'],
            'Type':'Tripartite',
            'Plasmid library':tripartite_tox_df['P3 Plasmid'],

            'EPCAM 1 NS':tripartite_tox_df['EPCAM_1_NS'],
            'EPCAM 2 NS':tripartite_tox_df['EPCAM_2_NS'],
            'EPCAM NS average':tripartite_tox_df[['EPCAM_1_NS','EPCAM_2_NS']].values.mean(axis=1),

            'CXCR4 1 NS':tripartite_tox_df['CXCR4_1_NS'],
            'CXCR4 2 NS':tripartite_tox_df['CXCR4_2_NS'],
            'CXCR4 NS average':tripartite_tox_df[['CXCR4_1_NS','CXCR4_2_NS']].values.mean(axis=1),

            'Reporter 1 NS':tripartite_tox_df['Reporter_1_NS'],
            'Reporter 2 NS':tripartite_tox_df['Reporter_2_NS'],
            'Reporter NS average':tripartite_tox_df[['Reporter_1_NS','Reporter_2_NS']].values.mean(axis=1),
            
            'EPCAM ranked?':(tripartite_score_df[["EPCAM_1","EPCAM_2"]].values!=None).all(axis=1),
            'CXCR4 ranked?':(tripartite_score_df[["CXCR4_1","CXCR4_2"]].values!=None).all(axis=1),
            'Reporter ranked?':(tripartite_score_df[["Reporter_1","Reporter_2"]].values!=None).all(axis=1),      
        }
    )


    res = pd.concat([
        single_domain_plasmid_NS,
        bipartite_plasmid_NS,
        tripartite_plasmid_NS
        ],ignore_index=True)
    return res

if __name__=="__main__":
    main()