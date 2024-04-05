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
            'output',
            'screen_results',
            'screen_toxicity',
            'single_domain_toxicity.csv'
        )
    )
    single_domain_tox_df['Construct'] = single_domain_tox_df['BC1']
    single_domain_tox_df['Average_Tox']=single_domain_tox_df[['EPCAM_Tox','CXCR4_Tox']].values.mean(axis=1)

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    bipartite_tox_df['Average_Tox']=bipartite_tox_df[['EPCAM_Tox','CXCR4_Tox']].values.mean(axis=1)

    construct_to_tox = dict()
    for i in single_domain_tox_df.index:
        construct = single_domain_tox_df.at[i,'Construct']
        tox = single_domain_tox_df.at[i,'Average_Tox']
        construct_to_tox[construct]=tox

    for i in bipartite_tox_df.index:
        construct = bipartite_tox_df.at[i,'Construct']
        tox = bipartite_tox_df.at[i,'Average_Tox']
        construct_to_tox[construct]=tox

    ordered_tox = single_domain_tox_df.sort_values(by='Average_Tox',ascending=False)['Construct'].to_list()
    top_right = pd.DataFrame()
    bottom_right = pd.DataFrame()

    for col in ordered_tox[::-1]:
        bottom_right.at["",col]=col
        for row in ordered_tox:
            top_right.at[row,col]="{}_{}".format(row,col)
            bottom_right.at[row,col]=construct_to_tox['{}_{}'.format(row,col)]
    
    top_right.reset_index(inplace=True)
    bottom_right.reset_index(inplace=True)

    
    left_part = pd.DataFrame(
        {
            "Bipartite construct" : bipartite_tox_df['Construct'],
            "Toxicity":bipartite_tox_df['Average_Tox'],
            "":""#Buffer
        }
    )

    right_part = pd.concat((
        top_right,
        pd.DataFrame({
            "A18":["",""]#This is a very ugly way to add a buffer line between 
        }),
        bottom_right,)
    ).reset_index(drop=True)

    res = pd.concat((
        left_part,
        right_part
    ),axis=1)

    return res

 

if __name__=="__main__":
    main()