# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

df = pd.read_csv(
    os.path.join(
        "output",
        "prescreen_results",
        "04_manually_tested_paddle_charachterized.csv"
    ),
    index_col='Unnamed: 0'
)
df['len aa']=list( map(lambda x:len(x),df['AA sequence']))
df['fraction strong']=df['AA in strong hits']/df['len aa']
#only_centroids = df[df['Is centroid']==True].reset_index(drop=True)

hits = df[df['Hit on any']==True].reset_index(drop=True)
misses = df[df['Hit on any']==False].reset_index(drop=True)

odf=pd.DataFrame({
    'Hits':hits['Full name'],
    'Hits fraction strong':hits['fraction strong'],
    'Misses':misses['Full name'],
    'Misses fraction strong':misses['fraction strong']
    }).replace(np.nan,None)

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2f - PADDLE fraction.csv"
    ),
    index=False
    )