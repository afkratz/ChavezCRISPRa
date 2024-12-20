
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
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent.parent))
from src import biochem_charachterize as bc
from progress.bar import Bar

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
    
    single_domain_tox_df['Construct']=single_domain_tox_df['BC1']
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

    single_domain_sequence_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'input_data',
            'screen_sequences',
            'p1_sequences.csv'
        )
    )
    single_domain_sequence_df['Construct'] = single_domain_sequence_df['BC1']


    bipartite_sequence_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'input_data',
            'screen_sequences',
            'p2_sequences.csv'
        )
    )
    bipartite_sequence_df['Construct'] = bipartite_sequence_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)


    tripartite_sequence_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'input_data',
            'screen_sequences',
            'p3_sequences.csv'
        )
    )
    tripartite_sequence_df['Construct'] = tripartite_sequence_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    
    assert(single_domain_sequence_df['Construct']==single_domain_tox_df['Construct']).all()
    assert(bipartite_sequence_df['Construct']==bipartite_tox_df['Construct']).all()
    assert(tripartite_sequence_df['Construct']==tripartite_tox_df['Construct']).all()
    
    bar = Bar("Biochem charachterizing screen sequences...",max=len(tripartite_sequence_df)+len(bipartite_sequence_df)+len(single_domain_sequence_df),suffix='%(index)i / %(max)i - %(eta)ds')
    for i in single_domain_sequence_df.index: 
        bar.next()
        single_domain_sequence_df.at[i,'Hydrophobicity'] = bc.getHydropathy(single_domain_sequence_df.at[i,'AA sequence'])
        single_domain_sequence_df.at[i,'Disorder promoting fraction'] = bc.getDisorderFraction(single_domain_sequence_df.at[i,'AA sequence'])
    
    for i in bipartite_sequence_df.index: 
        bar.next()
        bipartite_sequence_df.at[i,'Hydrophobicity'] = bc.getHydropathy(bipartite_sequence_df.at[i,'AA sequence'])
        bipartite_sequence_df.at[i,'Disorder promoting fraction'] = bc.getDisorderFraction(bipartite_sequence_df.at[i,'AA sequence'])

    for i in tripartite_sequence_df.index: 
        bar.next()
        tripartite_sequence_df.at[i,'Hydrophobicity'] = bc.getHydropathy(tripartite_sequence_df.at[i,'AA sequence'])
        tripartite_sequence_df.at[i,'Disorder promoting fraction'] = bc.getDisorderFraction(tripartite_sequence_df.at[i,'AA sequence'])
    bar.finish()



    res =pd.concat((
        pd.DataFrame({
        "Activator":single_domain_tox_df['Construct'],
        "Type":"Single-domain",
        "Toxicity":single_domain_tox_df['Average_Tox'],
        "Hydrophobicity":single_domain_sequence_df['Hydrophobicity'],
        "Disorder promoting fraction":single_domain_sequence_df['Disorder promoting fraction']
    }),
    pd.DataFrame({
        "Activator":bipartite_tox_df['Construct'],
        "Type":"Bipartite",
        "Toxicity":bipartite_tox_df['Average_Tox'],
        "Hydrophobicity":bipartite_sequence_df['Hydrophobicity'],
        "Disorder promoting fraction":bipartite_sequence_df['Disorder promoting fraction']
    }),
    pd.DataFrame({
        "Activator":tripartite_tox_df['Construct'],
        "Type":"Tripartite",
        "Toxicity":tripartite_tox_df['Average_Tox'],
        "Hydrophobicity":tripartite_sequence_df['Hydrophobicity'],
        "Disorder promoting fraction":tripartite_sequence_df['Disorder promoting fraction']
    })),
    ignore_index=True)
    return res

 

if __name__=="__main__":
    main()