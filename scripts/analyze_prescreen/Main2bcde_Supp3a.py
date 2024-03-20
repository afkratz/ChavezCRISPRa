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
import pandas as pd

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    df = pd.read_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "prescreen_results",
            "03_manually_tested_biochem_charachterized.csv")
        )

    only_centroids = df[df['Is centroid']==True]

    hit_df = only_centroids[only_centroids['Hit on any']==True].reset_index(drop=True)
    miss_df = only_centroids[only_centroids['Hit on any']==False].reset_index(drop=True)
    
    hit_df=pd.DataFrame({
        'Hits':hit_df['Domain ID'],
        'NCPR':hit_df['NCPR'],
        'Hydropathy':hit_df['Hydropathy'],
        'Disorder promoting fraction':hit_df['Disorder promoting fraction'],
        'Kappa':hit_df['Kappa'],
        'Omega':hit_df['Omega'],
        '':''#buffer column
    })

    miss_df = pd.DataFrame({
        'Misses':miss_df['Domain ID'],
        'NCPR':miss_df['NCPR'],
        'Hydropathy':miss_df['Hydropathy'],
        'Disorder promoting fraction':miss_df['Disorder promoting fraction'],
        'Kappa':miss_df['Kappa'],
        'Omega':miss_df['Omega'],
        })
    result = pd.concat([hit_df, miss_df], axis=1)
    return result
