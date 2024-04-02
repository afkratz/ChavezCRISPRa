# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------

"""

import os
from pathlib import Path
import pandas as pd

ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent

def make_supptable_4():
    single_domain_scores = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_scores',
            'single_domain_screen_scored.csv'
        )
    )
    single_domain_scores['Construct'] = single_domain_scores['BC1']

    bipartite_scores = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_scores',
            'bipartite_screen_scored.csv'
        )
    )
    bipartite_scores['Construct'] = bipartite_scores.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    tripartite_scores = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_scores',
            'tripartite_screen_scored.csv'
        )
    )
    tripartite_scores['Construct'] = tripartite_scores.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    output = pd.concat((
        pd.DataFrame({
            'Construct':single_domain_scores['Construct'],
            'Activator type':'Single-domain',
            'EPCAM_activation_score_1':single_domain_scores['EPCAM_1'],
            'EPCAM_activation_score_2':single_domain_scores['EPCAM_2'],
            'CXCR4_activation_score_1':single_domain_scores['CXCR4_1'],
            'CXCR4_activation_score_2':single_domain_scores['CXCR4_2'],
            'Reporter_activation_score_1':single_domain_scores['Reporter_1'],
            'Reporter_activation_score_2':single_domain_scores['Reporter_2'],
            'EPCAM_activation_score_average':single_domain_scores[['EPCAM_1','EPCAM_2']].mean(axis=1),
            'CXCR4_activation_score_average':single_domain_scores[['CXCR4_1','CXCR4_2']].mean(axis=1),
            'Reporter_activation_score_average':single_domain_scores[['Reporter_1','Reporter_2']].mean(axis=1),  
        }),
        pd.DataFrame({
            'Construct':bipartite_scores['Construct'],
            'Activator type':'Bipartite',
            'EPCAM_activation_score_1':bipartite_scores['EPCAM_1'],
            'EPCAM_activation_score_2':bipartite_scores['EPCAM_2'],
            'CXCR4_activation_score_1':bipartite_scores['CXCR4_1'],
            'CXCR4_activation_score_2':bipartite_scores['CXCR4_2'],
            'Reporter_activation_score_1':bipartite_scores['Reporter_1'],
            'Reporter_activation_score_2':bipartite_scores['Reporter_2'],
            'EPCAM_activation_score_average':bipartite_scores[['EPCAM_1','EPCAM_2']].mean(axis=1),
            'CXCR4_activation_score_average':bipartite_scores[['CXCR4_1','CXCR4_2']].mean(axis=1),
            'Reporter_activation_score_average':bipartite_scores[['Reporter_1','Reporter_2']].mean(axis=1),  
        }),
        pd.DataFrame({
            'Construct':tripartite_scores['Construct'],
            'Activator type':'Tripartite',
            'EPCAM_activation_score_1':tripartite_scores['EPCAM_1'],
            'EPCAM_activation_score_2':tripartite_scores['EPCAM_2'],
            'CXCR4_activation_score_1':tripartite_scores['CXCR4_1'],
            'CXCR4_activation_score_2':tripartite_scores['CXCR4_2'],
            'Reporter_activation_score_1':tripartite_scores['Reporter_1'],
            'Reporter_activation_score_2':tripartite_scores['Reporter_2'],
            'EPCAM_activation_score_average':tripartite_scores[['EPCAM_1','EPCAM_2']].mean(axis=1),
            'CXCR4_activation_score_average':tripartite_scores[['CXCR4_1','CXCR4_2']].mean(axis=1),
            'Reporter_activation_score_average':tripartite_scores[['Reporter_1','Reporter_2']].mean(axis=1),  
        })
    ),ignore_index=True)
    
    output.to_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "SuppTables",
            "Supplementary Table 4.csv"
            ),
            index=False
    )

def make_supptable_5():
    single_domain_tox = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_toxicity',
            'single_domain_toxicity.csv'
        )
    )
    single_domain_tox['Construct'] = single_domain_tox['BC1']

    bipartite_tox = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_toxicity',
            'bipartite_screen_toxicity.csv'
        )
    )
    bipartite_tox['Construct'] = bipartite_tox.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    tripartite_tox = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_toxicity',
            'tripartite_screen_toxicity.csv'
        )
    )
    tripartite_tox['Construct'] = tripartite_tox.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    output = pd.concat((
        pd.DataFrame({
            'Construct':single_domain_tox['Construct'],
            'Activator type':'Single-domain',
            'EPCAM_toxicity_score':single_domain_tox['EPCAM_Tox'],
            'CXCR4_toxicity_score':single_domain_tox['CXCR4_Tox'],
            'Toxicity_score_average':single_domain_tox[['EPCAM_Tox','CXCR4_Tox']].values.mean(axis=1),
            }),
        pd.DataFrame({
            'Construct':bipartite_tox['Construct'],
            'Activator type':'Bipartite',
            'EPCAM_toxicity_score':bipartite_tox['EPCAM_Tox'],
            'CXCR4_toxicity_score':bipartite_tox['CXCR4_Tox'],
            'Toxicity_score_average':bipartite_tox[['EPCAM_Tox','CXCR4_Tox']].values.mean(axis=1),
            }),
            pd.DataFrame({
            'Construct':tripartite_tox['Construct'],
            'Activator type':'Tripartite',
            'EPCAM_toxicity_score':tripartite_tox['EPCAM_Tox'],
            'CXCR4_toxicity_score':tripartite_tox['CXCR4_Tox'],
            'Toxicity_score_average':tripartite_tox[['EPCAM_Tox','CXCR4_Tox']].values.mean(axis=1),
            })
    ),ignore_index=True)
    
    output.to_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "SuppTables",
            "Supplementary Table 5.csv"
            ),
            index=False
    )

def main():
    make_supptable_4()
    make_supptable_5()
    

if __name__=="__main__":

    main()
    
    