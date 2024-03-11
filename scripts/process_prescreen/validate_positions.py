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
import requests
import math

def download_fasta(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return ''.join(response.text.split('\n')[1:])
        else:
            print(f"Error: Unable to download .fasta file. Status Code: {response.status_code}")
            return 'None'

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def validate_start_and_stop_positions():
    ChavezCIRSPRa_root_dir = Path(__file__).resolve().parent.parent.parent
    
    df = pd.read_excel(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'input_data',
            'Supplementary Table 1. Domain origins and sequences.xlsx'),index_col='Domain ID'
        )
    for i in df.index:
        if df.at[i,'Designed or found']=='Found':
            print(i+"...",end="")
            uniprot_name = df.at[i,'UniProt']
            if not isinstance(uniprot_name,str):continue #Checks for NANs
            seq = download_fasta(uniprot_name)
            if i not in ['BAHV1_ICP4','BPV1_NS1','EC_MBPMUT','EC_MBPWT','EF_D920_01889','HS_ATF7','HS_P65']:
                start_aa = seq.find(df.at[i,'AA sequence'])
                re_calculated_start=(start_aa)/len(seq)
                re_calculated_end=((start_aa)+len(df.at[i,'AA sequence']))/len(seq)
            
            #A few activators have slight differences from uniprot that we handle manually
            if i=='BAHV1_ICP4': 
                #Our is missing 1aa compared to uniprot
                our_sequence = df.at[i,'AA sequence']
                original_sequence  = our_sequence[:59]+'R'+our_sequence[59:]
                start_aa = seq.find(original_sequence)
                re_calculated_start=(start_aa)/len(seq)
                re_calculated_end=((start_aa)+len(original_sequence))/len(seq)
            
            if i=='HS_P65':
                #Our version of P65 came from a construct with one extra Serine in the GS-linker
                our_sequence = df.at[i,'AA sequence']
                original_sequence = our_sequence[1:]#skip first AA
                start_aa = seq.find(original_sequence)
                re_calculated_start=(start_aa)/len(seq)
                re_calculated_end=((start_aa)+len(original_sequence))/len(seq)

            if i=='BPV1_NS1':
                #Our version has a 1aa substitution compared to uniprot, R742G
                our_sequence = df.at[i,'AA sequence']
                original_sequence = our_sequence[:116]+'R'+our_sequence[117:]
                start_aa = seq.find(original_sequence)
                re_calculated_start=(start_aa)/len(seq)
                re_calculated_end=((start_aa)+len(original_sequence))/len(seq)

            assert math.isclose(re_calculated_start, df.at[i,'Origin protein start position'],abs_tol=0.0001)
            assert math.isclose(re_calculated_end, df.at[i,'Origin protein end position'],abs_tol=0.0001)
            print("True")

if __name__=="__main__":
    validate_start_and_stop_positions()