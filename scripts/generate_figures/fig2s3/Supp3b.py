# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import numpy as np
import pandas as pd
import os
from pathlib import Path

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent

    df = pd.read_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "prescreen_results",
            "02_manually_tested_hits_and_clusters_assigned.csv")
        )

    only_centroids = df[df['Is centroid']==True]
    has_start_end = only_centroids[only_centroids['Origin protein start position'].notna()]
    has_start_end=has_start_end.copy()
    has_start_end['mid_point'] = has_start_end[['Origin protein start position','Origin protein end position']].mean(axis=1)


    hits = has_start_end[has_start_end['Hit on any']==True].reset_index(drop=True)
    misses = has_start_end[has_start_end['Hit on any']==False].reset_index(drop=True)

    hit_df=pd.DataFrame({
        'Hits':hits['Domain ID'],
        'Hits mid position':hits['mid_point'],
        '':''#buffer column
    })

    miss_df = pd.DataFrame({
        'Misses':misses['Domain ID'],
        'Misses mid position':misses['mid_point'],
        })
    
    result = pd.concat([hit_df, miss_df], axis=1)
    return result