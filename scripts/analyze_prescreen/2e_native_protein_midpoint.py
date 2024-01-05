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
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "02_manually_tested_hits_and_clusters_assigned.csv")
    )

if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","prescreen_figs")):
    os.mkdir(os.path.join("output","figures","prescreen_figs"))

only_centroids = df[df['Is centroid']==True]
natural_centroids = only_centroids[only_centroids['Designed or found']=='Found']
natural_centroids=natural_centroids.copy()
natural_centroids['mid_point'] = natural_centroids[['Start','End']].mean(axis=1)


hits = natural_centroids[natural_centroids['Hit on any']==True].reset_index(drop=True)
misses = natural_centroids[natural_centroids['Hit on any']==False].reset_index(drop=True)

odf=pd.DataFrame({
    'Hits':hits['Domain ID'],
    'Hits mid position':hits['mid_point'],
    'Misses':misses['Domain ID'],
    'Misses mid position':misses['mid_point']
    }).replace(np.nan,None)

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2e - native protein midpoint.csv"
    ),
    index=False
    )

