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
    single_domain_sequences = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "input_data",
            "screen_sequences",
            "p1_sequences.csv"
        )
    )
    single_domain_sequences['Construct'] = single_domain_sequences['BC1']
    single_domain_sequences['AA Len'] = single_domain_sequences.apply(lambda row: len(row['AA sequence']), axis=1)

    bipartite_sequences = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "input_data",
            "screen_sequences",
            "p2_sequences.csv"
        )
    )
    bipartite_sequences['Construct'] = bipartite_sequences.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    bipartite_sequences['AA Len'] = bipartite_sequences.apply(lambda row: len(row['AA sequence']), axis=1)
    


    tripartite_sequences = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "input_data",
            "screen_sequences",
            "p3_sequences.csv"
        )
    )
    tripartite_sequences['Construct'] = tripartite_sequences.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'], row['BC3']), axis=1)
    tripartite_sequences['AA Len'] = tripartite_sequences.apply(lambda row: len(row['AA sequence']), axis=1)

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

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)


    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    assert (single_domain_sequences['Construct']==single_domain_tox_df['Construct']).all()
    assert (bipartite_sequences['Construct']==bipartite_tox_df['Construct']).all()
    assert (tripartite_sequences['Construct']==tripartite_tox_df['Construct']).all()
    
    res = pd.concat((
        pd.DataFrame({
             "Construct":single_domain_sequences['Construct'],
             "Activator type":"Single-domain",
             "Total AD length":single_domain_sequences['AA Len'],
             "Toxicity":single_domain_tox_df['CX&EP Average Tox']
        }),
        pd.DataFrame({
             "Construct":bipartite_sequences['Construct'],
             "Activator type":"Bipartite",
             "Total AD length":bipartite_sequences['AA Len'],
             "Toxicity":bipartite_tox_df['CX&EP Average Tox']
        }),
        pd.DataFrame({
             "Construct":tripartite_sequences['Construct'],
             "Activator type":"Tripartite",
             "Total AD length":tripartite_sequences['AA Len'],
             "Toxicity":tripartite_tox_df['CX&EP Average Tox']
        }),
    ),ignore_index=True)

    return res

 

if __name__=="__main__":
    main()