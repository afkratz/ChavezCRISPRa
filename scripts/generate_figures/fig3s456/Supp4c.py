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
            'single_domain_toxicity.csv')
    )#Columns = [BC1,P1 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox]
    
    single_domain_plasmid_count = pd.DataFrame(
        {
            'Single-domain activator':single_domain_tox_df['BC1'],
            'Plasmid library reads':single_domain_tox_df['P1 Plasmid'],
            "":""#Buffer column
        }
    )
    
    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,P2 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox]
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    bipartite_plasmid_count = pd.DataFrame(
        {
            'Bipartite activator':bipartite_tox_df['Construct'],
            'Plasmid library reads':bipartite_tox_df['P2 Plasmid'],
            "":""#Buffer column
        }
    ).sort_values(by='Plasmid library reads',ascending=False).reset_index(drop=True)

    bipartite_bin_count = pd.DataFrame()
    for i,lower_bound in enumerate(range(35,205,5)):
        upper_bound = lower_bound+5
        bipartite_bin_count.at[i,'Bin'] = lower_bound
        bipartite_bin_count.at[i,'Bipartite frequency'] = ((bipartite_plasmid_count['Plasmid library reads'] > lower_bound) & (bipartite_plasmid_count['Plasmid library reads'] < upper_bound)).to_list().count(True)
    bipartite_bin_count.at[i+1,'Bin']="More than {}".format(upper_bound)
    bipartite_bin_count.at[i+1,'Bipartite frequency'] = (bipartite_plasmid_count['Plasmid library reads'] > upper_bound).to_list().count(True)
    bipartite_bin_count[""]=""#Buffer column

    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,BC3,P3 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox]
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)


    tripartite_plasmid_count = pd.DataFrame(
        {
            'Bipartite activator':tripartite_tox_df['Construct'],
            'Plasmid library reads':tripartite_tox_df['P3 Plasmid'],
            "":""#Buffer column
        }
    ).sort_values(by='Plasmid library reads',ascending=False).reset_index(drop=True)


    tripartite_bin_count = pd.DataFrame()
    for i,lower_bound in enumerate(range(0,270,10)):
        upper_bound = lower_bound+10
        tripartite_bin_count.at[i,'Bin'] = lower_bound
        tripartite_bin_count.at[i,'Tripartite frequency'] = ((tripartite_plasmid_count['Plasmid library reads'] > lower_bound) & (tripartite_plasmid_count['Plasmid library reads'] < upper_bound)).to_list().count(True)
    tripartite_bin_count.at[i+1,'Bin']="More than {}".format(upper_bound)
    tripartite_bin_count.at[i+1,'Tripartite frequency'] = (tripartite_plasmid_count['Plasmid library reads'] > upper_bound).to_list().count(True)


    result = pd.concat([single_domain_plasmid_count,
                        bipartite_plasmid_count,
                        tripartite_plasmid_count,
                        bipartite_bin_count,
                        tripartite_bin_count
                        ], axis=1)
    return result


