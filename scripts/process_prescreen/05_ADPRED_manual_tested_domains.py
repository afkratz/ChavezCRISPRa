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

import contextlib

from adpred import ADpred as adp
import pandas as pd
import numpy as np

if not os.path.exists(os.path.join("output","prescreen_results","adpred_results")):
    os.mkdir(os.path.join("output","prescreen_results","adpred_results"))


def run_adpred(df):
    output = open(os.devnull,'w')
    from progress.bar import Bar
    bar = Bar("ADPRED predicting...",max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
    for i in range(len(df)):
        activator_name = df.at[i,'ShortID']
        bar.next()
        if os.path.exists(
            os.path.join("output","prescreen_results","adpred_results",activator_name+'.npy')
        ):
            continue
        
        with contextlib.redirect_stdout(output):
            try:
                result = adp.predict(df.at[i,"AA sequence"])
            except:
                result = 'Sequence too short for ADPRED'
        np.save(os.path.join("output","prescreen_results","adpred_results",activator_name+'.npy'),result)

def has_ADpred_hit(arr,cutoff=0.8)->bool:
    conseq = 0
    for v in arr:
        if v>=cutoff:
            conseq+=1
        else:
            conseq=0
            
        if conseq>=10:
            return True
    return False

def find_hit_cutoff(arr)->float:
    values = sorted(list(arr),reverse=True)
    for v in values:
        if has_ADpred_hit(arr,v):
            return v

def process_adpred_results(df:pd.DataFrame):
    df['Adpred:Is short']=False
    df['Adpred:Has strong hit']=False
    df['Adpred:Score']=np.nan
    for i in df.index:
        activator_name = df.at[i,'ShortID']
        
        result = np.load(os.path.join("output","prescreen_results","adpred_results",activator_name+'.npy'))
        # If the sequence was too short for ADPRED, result will be:
        #           array('Sequence too short for ADPRED', dtype='<U29')
        # If the result's dtype is a float64, then we have an array of ADPRED predictions
        # We check the dtype to determine if the sequence was too short, and only process 
        # the results if the sequence was sufficiently long.
        df.at[i,'Adpred:Is short']=result.dtype != np.dtype("float64")

        if not df.at[i,'Adpred:Is short']:
            df.at[i,'Adpred:Has strong hit']=has_ADpred_hit(result,0.8)#Default cutoff from ADpred paper
            df.at[i,'Adpred:Score']=find_hit_cutoff(result)


def main():
    df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "04_manually_tested_paddle.csv"),
        index_col="Unnamed: 0"
    )
    run_adpred(df)
    process_adpred_results(df)
    df.to_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "05_manually_tested_PaddleAndAdpred.csv")
    )

if __name__=="__main__":
    main()