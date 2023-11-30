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
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
import pandas as pd

from progress.bar import Bar


from src import paddle_interface as pi
from src import biochem_charachterize as bc

def load_data_sets()->dict[pd.DataFrame]:
    hanh_df = pd.read_csv(
        os.path.join(
            'input_data',
            'extrascreen',
            'hanh',
            'mmc2.csv'
        )
    )
    kornberg_df = pd.read_csv(
        os.path.join(
            'input_data',
            'extrascreen',
            'kornberg',
            'kornberg.csv'
        )
    )
    
    taipale_df = pd.read_csv(
        os.path.join(
            'input_data',
            'extrascreen',
            'taipale',
            'tadseq.csv'
        )
    )
    
    return {'hanh':hanh_df,'kornberg':kornberg_df,'taipale':taipale_df}


def sub_process_hanh_dataset(df:pd.DataFrame)->pd.DataFrame:
    hits_subsamples = df[df['AD_set'] == 'AD_positive'].sample(n=25000, replace=False, random_state=42)
    
    # Filter rows where the string column is 'B'
    miss_subsamples = df[df['AD_set'] == 'AD_negative'].sample(n=25000, replace=False, random_state=42)
    sampled_df = pd.concat([hits_subsamples, miss_subsamples], ignore_index=True)
    
    return sampled_df

def main():
    #biochem()
    paddle()

def biochem():
    dfs = load_data_sets()
    dfs['hanh'] = sub_process_hanh_dataset(dfs['hanh'])
    dfs['hanh'].to_csv("50k_hanh.csv",index=False)

    for screen in dfs:
        df = dfs[screen]


        bar = Bar("Charachterizing...{}".format(screen),max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
    
        for i in range(len(df)):
            sequence = df.at[i,"sequence"]
            df.at[i,"NCPR"]=bc.getNCPR(sequence)
            df.at[i,"Hydropathy"]=bc.getHydropathy(sequence)
            df.at[i,"Disorder promoting fraction"]=bc.getDisorderFraction(sequence)
            df.at[i,"Kappa"]=bc.getKappa(sequence)
            df.at[i,"Omega"]=bc.getOmega(sequence)
            bar.next()

        bar.finish()
        df.to_csv("{}__bc_output.csv".format(screen),index=False)

def paddle():
    PARRALEL_SEQS = 5

    dfs = load_data_sets()
    dfs['hanh'] = sub_process_hanh_dataset(dfs['hanh'])
    dfs['hanh'].to_csv("50k_hanh.csv",index=False)
    for screen in dfs:
        df = dfs[screen]
        bar = Bar("Charachterizing...{}".format(screen),max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')

        for i in range(0,len(df),PARRALEL_SEQS):
            bar.next(PARRALEL_SEQS)
            seqs = df.iloc[i:i+PARRALEL_SEQS]['sequence'].to_list()
            results=pi.process_sequences(seqs,accept_short=True)

            if i==0:
                for key in results[0]:
                    df['Paddle:'+key]=''

            for j in range(len(results)):
                index = i+j
                for key in results[j]:
                    df.at[index,'Paddle:'+key]=str(results[j][key])

        df.to_csv("{}_paddle_output.csv".format(screen),index=False)

if __name__=='__main__':
    main()

    