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

    single_domain_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "single_domain_screen_scored.csv",
        )
    )
    single_domain_activity_df['Construct'] = single_domain_activity_df['BC1']
    
    bipartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "bipartite_screen_scored.csv",
        )
    )
    bipartite_activity_df['Construct'] = bipartite_activity_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    for target in ['EPCAM','CXCR4','Reporter']:
        bipartite_activity_df['{}_average'.format(target)] = bipartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
        single_domain_activity_df['{}_average'.format(target)] = single_domain_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)

    construct_to_score=dict()

    for i in bipartite_activity_df.index:
        construct = bipartite_activity_df.at[i,'Construct']
        score = bipartite_activity_df.at[i,'Reporter_average']
        construct_to_score[construct]=score

    ordered_activity= single_domain_activity_df.sort_values(by='Reporter_average',ascending=False)['Construct'].to_list()

    right_part = pd.DataFrame()
    for col in ordered_activity[::-1]:
        for row in ordered_activity:
            right_part.at[row,col]=construct_to_score['{}_{}'.format(row,col)]
    right_part.reset_index(inplace=True)
    
    left_part = pd.DataFrame(
        {
            "Cconstruct" : bipartite_activity_df['Construct'],
            "Activator type":"Bipartite",
            "P1":bipartite_activity_df['BC1'],
            "P2":bipartite_activity_df['BC2'],
            "EPCAM1 ":bipartite_activity_df["EPCAM_1"],
            "EPCAM 2":bipartite_activity_df["EPCAM_2"],
            "CXCR4 1":bipartite_activity_df["CXCR4_1"],
            "CXCR4 2":bipartite_activity_df["CXCR4_2"],
            "Reporter 1":bipartite_activity_df["Reporter_1"],
            "Reporter 2":bipartite_activity_df["Reporter_2"],
            "EPCAM average":bipartite_activity_df["EPCAM_average"],
            "CXCR4 average":bipartite_activity_df["CXCR4_average"],
            "Reporter average":bipartite_activity_df["Reporter_average"],           
            
            "":""#Buffer
        }
    )

    res = pd.concat((
        left_part,
        right_part
    ),axis=1)
    return res

    

if __name__=="__main__":
    main()