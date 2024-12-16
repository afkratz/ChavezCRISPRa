
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
    ad_bcs = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,23)))

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

    res = pd.DataFrame()
    for i,bc in enumerate(ad_bcs):
        res.at[i,'AD']=bc
        res.at[i,'Single-domain toxicity'] = construct_to_tox[bc]
        
        res.at[i,'Bipartite AD + PF toxicity']=np.median((
            construct_to_tox["{}_{}".format("A23",bc)],
            construct_to_tox["{}_{}".format("A25",bc)],
            construct_to_tox["{}_{}".format(bc,"A23")],
            construct_to_tox["{}_{}".format(bc,"A25")],
        ))

        res.at[i,'Tripartite AD + 2 PFs toxicity']=np.median((
            construct_to_tox["{}_{}_{}".format("A23","A23",bc)],
            construct_to_tox["{}_{}_{}".format("A23","A25",bc)],
            construct_to_tox["{}_{}_{}".format("A25","A23",bc)],
            construct_to_tox["{}_{}_{}".format("A25","A25",bc)],
            construct_to_tox["{}_{}_{}".format("A23",bc,"A23")],
            construct_to_tox["{}_{}_{}".format("A23",bc,"A25")],
            construct_to_tox["{}_{}_{}".format("A25",bc,"A23")],
            construct_to_tox["{}_{}_{}".format("A25",bc,"A25")],
            construct_to_tox["{}_{}_{}".format(bc,"A23","A23")],
            construct_to_tox["{}_{}_{}".format(bc,"A23","A25")],
            construct_to_tox["{}_{}_{}".format(bc,"A25","A23")],
            construct_to_tox["{}_{}_{}".format(bc,"A25","A25")],
        ))        
        
    res.sort_values(by='Single-domain toxicity',inplace=True)
    return res

 

if __name__=="__main__":
    main()