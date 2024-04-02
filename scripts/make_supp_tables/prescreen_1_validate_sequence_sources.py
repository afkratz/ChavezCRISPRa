# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
This script compares our sequences from Supp table 1 to uniprot to confirm
that the domains which are annotated as "found" rather than designed match
the listed uniprot at the location that they say.
Two sequences, EF_D920_01889 and HS_ATF7 are annoated as found but do not match
any published UniProt sequence. EF_D920 was derived from a hypothetical protein
with homology to activators, and HS_ATF7 has a 10 amino acid deletion compared
to its published sequence. For this reason, we do not assign them N-C locations
Additionally, five sequences, BAHV1_ICP4, HS_P65, BPV1_NS1, EC_MBP & EC_MBPTRUNC
had slight differences compared to the uniprot versions. We address these 
sequences explicitly by finding the location of the wild-type sequence, which
differs by one amino acid in all cases.

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


def validate_sources():
    ChavezCIRSPRa_root_dir = Path(__file__).resolve().parent.parent.parent
    
    df = pd.read_excel(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'InputData',
            'Supplementary Table 1.xlsx'),index_col='Domain ID'
        )
    for i in df.index:
        if df.at[i,'Designed or found']=='Found':
            print(i+"...",end="")
            uniprot_name = df.at[i,'UniProt ID']

            if i=='EF_D920_01889':
                #This is a hypothetical protein from Enterococcus Facalis that had homology to activators
                #It is not present in UniProt, so we do not assign it an N-C location
                print("Skipped")
                continue
        
            if i=='HS_ATF7':
                #Our version of this protein has a 10 amino acid deletion compared to the UniProt sequence
                #This is sufficiently large that we do not assign it an N-C location
                print("Skipped")
                continue


            #Other than EF_D920 and HS_ATF7, all found-not-designed activators have a UniProt Location
            if not isinstance(uniprot_name,str):raise ValueError 

            #Download the fasta and calculate where our sequence appears in the fasta
            #Four activators are present in UniProt but with slight differences that we handle manually below
            seq = download_fasta(uniprot_name)
            if i not in ['BAHV1_ICP4','HS_P65','BPV1_NS1','EC_MBP','EC_MBPTRUNC']:
                start_aa = seq.find(df.at[i,'AA sequence'])
                re_calculated_start=(start_aa)/len(seq)
                re_calculated_end=((start_aa)+len(df.at[i,'AA sequence']))/len(seq)
            
            
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

            if i=='EC_MBP' or i=='EC_MBPTRUNC':
                #Our version has an extra M as the first base
                our_sequence = df.at[i,'AA sequence']
                original_sequence = our_sequence[1:]#skip first AA
                start_aa = seq.find(original_sequence)
                re_calculated_start=(start_aa)/len(seq)
                re_calculated_end=((start_aa)+len(original_sequence))/len(seq)

            assert math.isclose(re_calculated_start, df.at[i,'Origin protein start position'],abs_tol=0.0001)
            assert math.isclose(re_calculated_end, df.at[i,'Origin protein end position'],abs_tol=0.0001)
            print("Validated")

if __name__=="__main__":
    validate_sources()