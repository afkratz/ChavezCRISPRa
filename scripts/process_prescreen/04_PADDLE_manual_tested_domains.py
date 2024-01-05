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
        index_col="Domain ID"
    )

from progress.bar import Bar
bar = Bar("PADDLE predicting...",max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
for i in df.index:
    bar.next()
    results = pi.process_sequences(df.at[i,"AA sequence"],accept_short=True)[0]
    for key in results:
        if 'Paddle:'+key not in df.columns:df['Paddle:'+key]=''
        df.at[i,'Paddle:'+key]=str(results[key])

df.to_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "04_manually_tested_Paddle.csv")
    )
