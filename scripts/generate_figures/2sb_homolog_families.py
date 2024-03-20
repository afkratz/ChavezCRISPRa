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
        "02_manually_tested_hits_and_clusters_assigned.csv"),
        index_col="Domain ID"
    )

if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","prescreen_figs")):
    os.mkdir(os.path.join("output","figures","prescreen_figs"))

bel1_variants = df[df['BEL1 variant']==1]
bel1_variants.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2sb - bel1 variants.csv"
    )
)

hsf1_variants = df[df['HSF1 variant']==1]
hsf1_variants.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2sb - hsf1 variants.csv"
    )
)

e1a_variants = df[df['E1A variant']==1]
e1a_variants.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2sb - e1a variants.csv"
    )
)



vp16_variants = df[df['VP16 variant']==1]
vp16_variants = vp16_variants[vp16_variants['Designed or found']=='Found']
vp16_variants.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2sb - vp16 variants.csv"
    )
)