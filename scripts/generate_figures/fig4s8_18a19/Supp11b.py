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
            'SuppTables',
            'Supplementary Table 3.csv'
        ),index_col='A-ID'
    )['Domain name'].to_dict()


    gfp_competition_results = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "InputData",
            "GFP_competition_results.csv"
        ),index_col='Construct'
    )

    gfp_competition_results['GFP+ P0_average_GFP_normalized'] = gfp_competition_results['GFP+ P0_average'] * 100 / gfp_competition_results.at['GFP only','GFP+ P0_average']
    gfp_competition_results['GFP+ P1_average_GFP_normalized'] = gfp_competition_results['GFP+ P1_average'] * 100 / gfp_competition_results.at['GFP only','GFP+ P1_average']
    gfp_competition_results['GFP+ P2_average_GFP_normalized'] = gfp_competition_results['GFP+ P2_average'] * 100 / gfp_competition_results.at['GFP only','GFP+ P2_average']
    
    gfp_competition_results['GFP- P0_average_GFP_normalized'] = 100 - gfp_competition_results['GFP+ P0_average_GFP_normalized']
    gfp_competition_results['GFP- P1_average_GFP_normalized'] = 100 - gfp_competition_results['GFP+ P1_average_GFP_normalized']
    gfp_competition_results['GFP- P2_average_GFP_normalized'] = 100 - gfp_competition_results['GFP+ P2_average_GFP_normalized']
    
    gfp_competition_results['GFP- P0 / P0'] = gfp_competition_results['GFP- P0_average_GFP_normalized'] / gfp_competition_results['GFP- P0_average_GFP_normalized']
    gfp_competition_results['GFP- P1 / P0'] = gfp_competition_results['GFP- P1_average_GFP_normalized'] / gfp_competition_results['GFP- P0_average_GFP_normalized']
    gfp_competition_results['GFP- P2 / P0'] = gfp_competition_results['GFP- P2_average_GFP_normalized'] / gfp_competition_results['GFP- P0_average_GFP_normalized']
    
    gfp_competition_results['Decrease in activator population_P1'] = 1-gfp_competition_results['GFP- P1 / P0']
    gfp_competition_results['Decrease in activator population_P2'] = 1-gfp_competition_results['GFP- P2 / P0']
    
    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )
    
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    tripartite_tox_df['Domain Name'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(AID_to_name[row['BC1']], AID_to_name[row['BC2']],AID_to_name[row['BC3']]), axis=1)
    
    tripartite_tox_df['Average_Tox']=tripartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)

    tripartite_construct_to_tox = dict()
    for i in tripartite_tox_df.index:
        construct = tripartite_tox_df.at[i,'Construct']
        tox = tripartite_tox_df.at[i,'Average_Tox']
        assert construct not in tripartite_construct_to_tox
        tripartite_construct_to_tox[construct]=tox


    construct_to_name = dict()
    for i in tripartite_tox_df.index:
        construct_to_name[tripartite_tox_df.at[i,'Construct']]=tripartite_tox_df.at[i,'Domain Name']

    for i in gfp_competition_results.index:
        if i in tripartite_construct_to_tox:
            gfp_competition_results.at[i,'Screen toxicity'] = tripartite_construct_to_tox[i]
            gfp_competition_results.at[i,'Name']=construct_to_name[i]
        else:
            gfp_competition_results.at[i,'Name']=i

    gfp_competition_results.reset_index(inplace=True)

    print(gfp_competition_results)

    return gfp_competition_results

 
if __name__=="__main__":
    main()