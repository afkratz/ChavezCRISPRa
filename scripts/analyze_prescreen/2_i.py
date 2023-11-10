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
        index_col="Full name"#use this to fish out our entries of interest
    )
df.drop('Unnamed: 0',axis=1,inplace=True)
bel1_variants = df.loc[[
    "JMSFV1_BEL1",
    "SFV3_BEL1",
    "SFV1_BEL1",
    "HSV1_BEL1",
    ]]
bel1_variants.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2i - bel1 variants.csv"
    )
)

hsf1_variants = df.loc[[
    "CA_HSF1",
    "SH_HSF1",
    "HS_HSF1",
    ]]
hsf1_variants.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2i - hsf1 variants.csv"
    )
)

vp16_variants = df.loc[[
    "CercAHV2_VP16",
    "LAHV4_VP16",
    "FBAHV1_VP16",
    "SaHV1_VP16",
    "ChHV1_VP16",
    "HHV1_VP16",
    "HHV2_VP16",
    ]]
vp16_variants.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2i - vp16 variants.csv"
    )
)