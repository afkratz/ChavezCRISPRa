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
has_start_end = only_centroids[only_centroids['Origin protein start position'].notna()]

hits = has_start_end[has_start_end['Hit on any']==True].reset_index(drop=True)
misses = has_start_end[has_start_end['Hit on any']==False].reset_index(drop=True)

odf=pd.DataFrame({
    'Hits':hits['Domain ID'],
    'Hits starting position':hits['Origin protein start position'],
    'Hits ending position':hits['Origin protein end position'],
    
    'Misses':misses['Domain ID'],
    'Misses starting position':misses['Origin protein start position'],
    'Misses ending position':misses['Origin protein end position']
    }).replace(np.nan,None)

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2d - native protein start and end.csv"
    ),
    index=False
    )