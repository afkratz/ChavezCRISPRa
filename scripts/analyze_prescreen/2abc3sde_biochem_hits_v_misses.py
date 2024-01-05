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
import numpy as np


df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "03_manually_tested_biochem_charachterized.csv")
    )


if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","prescreen_figs")):
    os.mkdir(os.path.join("output","figures","prescreen_figs"))

only_centroids = df[df['Is centroid']==True]

hit_df = df[df['Hit on any']==True].reset_index(drop=True)
miss_df = df[df['Hit on any']==False].reset_index(drop=True)

odf=pd.DataFrame({
    'Hits':hit_df['Domain ID'],
    'Hits NCPR':hit_df['NCPR'],
    'Hits Hydropathy':hit_df['Hydropathy'],
    'Hits Disorder promoting fraction':hit_df['Disorder promoting fraction'],
    'Hits Kappa':hit_df['Kappa'],
    'Hits Omega':hit_df['Omega'],
    
    'Misses':miss_df['Domain ID'],
    'Misses NCPR':miss_df['NCPR'],
    'Misses Hydropathy':miss_df['Hydropathy'],
    'Misses Disorder promoting fraction':miss_df['Disorder promoting fraction'],
    'Misses Kappa':miss_df['Kappa'],
    'Misses Omega':miss_df['Omega'],

    }).replace(np.nan,None)

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2abc3sde - biochem traits between hits and misses.csv"
    ),
    index=False
    )