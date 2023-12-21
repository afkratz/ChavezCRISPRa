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


#from src import paddle_interface as pi
from src import biochem_charachterize as bc

import json
class StringCache:
    def __init__(self, cache_directory):
        self.cache_directory = cache_directory
        if not os.path.exists(cache_directory):
            os.makedirs(cache_directory)

    def add_item(self, key, value):
            file_path = os.path.join(self.cache_directory, f"{key}.json")
            with open(file_path, 'w') as file:
                json.dump(value, file)

    def has_item(self, key):
        file_path = os.path.join(self.cache_directory, f"{key}.json")
        return os.path.exists(file_path)

    def retrieve_item(self, key):
        if not self.has_item(key):
            raise KeyError(f"Key '{key}' not found in the cache")

        file_path = os.path.join(self.cache_directory, f"{key}.json")
        with open(file_path, 'r') as file:
            return json.load(file)

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
    run_paddle()

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
        df.to_csv("{}_bc_output.csv".format(screen),index=False)


def run_paddle():
    dfs = load_data_sets()
    dfs['hanh'] = sub_process_hanh_dataset(dfs['hanh'])
    dfs['hanh'].to_csv("50k_hanh.csv",index=False)
    for screen in dfs:
        df = dfs[screen]
        bar = Bar("Charachterizing...{}".format(screen),max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
        cache = StringCache(os.path.join(
                "output",
                "extrascreen_analysis",
                "{}_paddle_cache".format(screen)))
        
        for i in range(0,len(df)):
            bar.next(1)
            seq = df.iloc[i]['sequence']
            try:
                result = cache.retrieve_item(seq)
            except:
                assert False
                result=pi.process_sequences(seq,accept_short=True)[0]
                cache.add_item(seq,result)

            if i==0:
                for key in result:
                    df['Paddle:'+key]=''
            for key in result:
                df.at[i,'Paddle:'+key]=str(result[key])
        bar.finish()
        df.to_csv("{}_paddle_output.csv".format(screen),index=False)

if __name__=='__main__':
    main()

    