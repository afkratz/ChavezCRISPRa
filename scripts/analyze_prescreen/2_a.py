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
df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "02_manually_tested_hits_and_clusters_assigned.csv"),
        index_col="Unnamed: 0"
    )

VP16_Derived = [
    'SaHV1_VP64',
    'CercAHV2_VP64_1',
    'LAHV4_VP64',
    'HHV2_VP16',
    'ChHV1_VP16',
    'SaHV1_VP16',
    'CercAHV2_VP16',
    'FBAHV1_VP16',
    'FBAHV1_VP64',
    'CercAHV2_VP64_2',
    'LAHV4_VP16',
    'SaHV1_VP16x2',
    'FBAHV1_VP16x2',
    'HHV2_VP16x2',
    'LAHV4_VP16x2',
    'HHV1_VP16',
    'CercAHV2_VP16x2',
    'HHV1_VP16x2',
    'HHV1_VP64',
    'ChHV_VP16x2',
]

df['Is VP16 derived']=False
for i in df.index:
    full_name = df.at[i,'Full name']
    if full_name in VP16_Derived:
        df.at[i,'Is VP16 derived'] = True

if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","fig2")):
    os.mkdir(os.path.join("output","figures","fig2"))

odf = pd.DataFrame()
odf['Full name']=df['Full name']
odf['EPCAM FC']=df['EPCAM FC_average']
odf['CXCR4 FC']=df['CXCR4 FC_average']
odf['Reporter FC']=df['tdTomato FC_average']

odf['EPCAM_Rank']=df['EPCAM FC_average'].rank()
odf['CXCR4_Rank']=df['CXCR4 FC_average'].rank()
odf['Reporter_Rank']=df['tdTomato FC_average'].rank()
odf['Hit on any']=df['Hit on any']
odf['Is VP16 derived']=df['Is VP16 derived']
odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2a - Ranked prescreen scatter plot.csv"
    )
)