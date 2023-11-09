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

df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "03_manually_tested_biochem_charachterized.csv"),
        index_col="Unnamed: 0"
    )

if not os.path.exists(os.path.join("output","prescreen_results","adpred_results")):
    os.mkdir(os.path.join("output","prescreen_results","adpred_results"))

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
