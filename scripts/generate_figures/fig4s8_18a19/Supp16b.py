# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import pandas as pd
import os
from pathlib import Path

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent

    AID_to_name = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'input_data',
            'AId_to_name.csv'
        ),index_col='A-ID'
    )['Domain name'].to_dict()
    name_to_AID = {v:k for (k,v) in AID_to_name.items()}


    single_domain_tox_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'screen_output',
            'screen_results',
            'screen_toxicity',
            'single_domain_toxicity.csv'
        )
    )
    for i in single_domain_tox_df.index:
        single_domain_tox_df.at[i,'Construct'] = AID_to_name[single_domain_tox_df.at[i,'BC1']]
    single_domain_tox_df['Average_Tox']=single_domain_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'screen_output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(AID_to_name[row['BC1']], AID_to_name[row['BC2']]), axis=1)
    bipartite_tox_df['Average_Tox']=bipartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)

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
            top_right.at[row,col]="{}_{}".format(name_to_AID[row],name_to_AID[col])
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
            "A18":["",""]#This is a very ugly way to add a buffer line 
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