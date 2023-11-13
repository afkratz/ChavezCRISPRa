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
print("Loading PADDLE model...")
from src import paddle_interface as pi
import pandas as pd
df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "02_manually_tested_hits_and_clusters_assigned.csv"),
        index_col="Unnamed: 0"
    )

from progress.bar import Bar
bar = Bar("PADDLE predicting...",max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
for i in range(len(df)):
    bar.next()
    results = pi.process_sequences(df.at[i,"AA sequence"],accept_short=True)[0]
    
    #if this is the first item in the dataframe, initialize all values of the result as
    #new columns as empty strings
    if i==0:
        for key in results:
            df['Paddle:'+key]=''
    
    for key in results:
        df.at[i,'Paddle:'+key]=str(results[key])
df.to_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "04_manually_tested_Paddle.csv")
    )
