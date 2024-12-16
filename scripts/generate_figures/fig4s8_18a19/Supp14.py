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


    single_domain_scores = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "single_domain_screen_scored.csv"
        )
    )
    single_domain_scores['Construct'] = single_domain_scores['BC1']
    for target in ['EPCAM','CXCR4','Reporter']:
        single_domain_scores['{}_average_score'.format(target)] = single_domain_scores[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)


    bipartite_scores = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "bipartite_screen_scored.csv"
        )
    )
    bipartite_scores['Construct'] = bipartite_scores.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    for target in ['EPCAM','CXCR4','Reporter']:
        bipartite_scores['{}_average_score'.format(target)] = bipartite_scores[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)

    tripartite_scores = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "tripartite_screen_scored.csv"
        )
    )
    tripartite_scores['Construct'] = tripartite_scores.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'], row['BC3']), axis=1)
    for target in ['EPCAM','CXCR4','Reporter']:
        tripartite_scores['{}_average_score'.format(target)] = tripartite_scores[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
    tripartite_scores.replace(np.nan,'NA',inplace=True)

    assert (single_domain_scores['Construct']==single_domain_tox_df['Construct']).all()
    assert (bipartite_scores['Construct']==bipartite_tox_df['Construct']).all()
    assert (tripartite_scores['Construct']==tripartite_tox_df['Construct']).all()
    
    res = pd.concat((
        pd.DataFrame({
             "Construct":single_domain_scores['Construct'],
             "Activator type":"Single-domain",
             "Toxicity":single_domain_tox_df['Average_Tox'],
             "EPCAM average":single_domain_scores['EPCAM_average_score'],
             "CXCR4 average":single_domain_scores['CXCR4_average_score'],
             "Reporter average":single_domain_scores['Reporter_average_score'],
        }),

        pd.DataFrame({
             "Construct":bipartite_tox_df['Construct'],
             "Activator type":"Bipartite",
             "Toxicity":bipartite_tox_df['Average_Tox'],
             "EPCAM average":bipartite_scores['EPCAM_average_score'],
             "CXCR4 average":bipartite_scores['CXCR4_average_score'],
             "Reporter average":bipartite_scores['Reporter_average_score'],
        }),

        pd.DataFrame({
             "Construct":tripartite_tox_df['Construct'],
             "Activator type":"Tripartite",
             "Toxicity":tripartite_tox_df['Average_Tox'],
             "EPCAM average":tripartite_scores['EPCAM_average_score'],
             "CXCR4 average":tripartite_scores['CXCR4_average_score'],
             "Reporter average":tripartite_scores['Reporter_average_score'],
        }),
    ),ignore_index=True)

    return res

if __name__=="__main__":
    main()