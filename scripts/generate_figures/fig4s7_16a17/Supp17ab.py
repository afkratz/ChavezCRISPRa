
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
    
    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,BC3,P3 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    tripartite_sequence_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'input_data',
            'screen_sequences',
            'p3_sequences.csv'
        )
    )
    tripartite_sequence_df['Construct'] = tripartite_sequence_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    
    assert(tripartite_sequence_df['Construct']==tripartite_tox_df['Construct']).all()
    
    bar = Bar("Biochem charachterizing tripartite sequences...",max=len(tripartite_sequence_df),suffix='%(index)i / %(max)i - %(eta)ds')
    for i in tripartite_sequence_df.index: 
        bar.next()
        tripartite_sequence_df.at[i,'Hydrophobicity'] = bc.getHydropathy(tripartite_sequence_df.at[i,'AA sequence'])
        tripartite_sequence_df.at[i,'Disorder promoting fraction'] = bc.getDisorderFraction(tripartite_sequence_df.at[i,'AA sequence'])
    res = pd.DataFrame({
        "Activator":tripartite_tox_df['Construct'],
        "Type":"Tripartite",
        "Toxicity":tripartite_tox_df['CX&EP Average Tox'],
        "Hydrophobicity":tripartite_sequence_df['Hydrophobicity'],
        "Disorder promoting fraction":tripartite_sequence_df['Disorder promoting fraction']
    })
    return res

 

if __name__=="__main__":
    main()