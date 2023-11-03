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
        "prescreen",
        "03_manually_tested_biochem_charachterized.csv"),
        index_col="Unnamed: 0"
    )

from progress.bar import Bar
bar = Bar("PADDLE predicting...",max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
for i in range(len(df)):
    bar.next()
    res = pi.process_sequences(df.at[i,"AA sequence"],accept_short=True)[0]
    if i==0:
        for k in res:
            df[k]=''
    for k in res:
        df.at[i,k]=str(res[k])
df.to_csv(
        os.path.join(
        "output",
        "prescreen",
        "04_manually_tested_paddle_charachterized.csv")
    )
