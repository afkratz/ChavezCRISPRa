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

from src import biochem_charachterize as bc

df = pd.read_csv(
    os.path.join(
        "output",
        "prescreen_results",
        "03_manually_tested_biochem_charachterized.csv"
    ),
    index_col="Domain ID"
)

if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","prescreen_figs")):
    os.mkdir(os.path.join("output","figures","prescreen_figs"))

only_centroids = df[df['Is centroid']==True]
miss_df = only_centroids[only_centroids["Hit on any"]==False].reset_index()
hit_df = only_centroids[only_centroids["Hit on any"]==True].reset_index()


odf = pd.DataFrame()
window_size = 10
samples = 1000
odf['Position from C to N']=np.linspace(0,1,samples)
for trait in ("NCPR","Hydropathy","FDP"):
    xs=np.linspace(0,1,samples)
    hit_ys=[]
    for i in range(len(hit_df)):
        hit_ys.append(
            bc.samplePoints(
                bc.rollingAverage(
                    bc.getLinearTrait(
                        hit_df.at[i,"AA sequence"],
                        trait
                        ),
                    window_size),
                samples)
            )
    hit_ys=np.stack(hit_ys).mean(axis=0)
    odf['Hits_'+trait]=hit_ys
    miss_ys=[]
    for i in range(len(miss_df)):
        miss_ys.append(
            bc.samplePoints(
                bc.rollingAverage(
                    bc.getLinearTrait(
                        miss_df.at[i,"AA sequence"],
                        trait
                        ),
                    window_size),
                samples)
            )
    miss_ys=np.stack(miss_ys).mean(axis=0)
    odf['Miss_'+trait]=miss_ys

odf.to_csv(
    os.path.join(
        "output",        
        "figures",
        "prescreen_figs",
        "3sa - NCPR hydropathy FDP NtoC.csv"
    )
)