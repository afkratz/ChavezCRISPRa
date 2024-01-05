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
        index_col="Domain ID"
    )


if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","prescreen_figs")):
    os.mkdir(os.path.join("output","figures","prescreen_figs"))

odf = pd.DataFrame()
odf['EPCAM L2FC']=df['EPCAM log2FC_average']
odf['CXCR4 L2FC']=df['CXCR4 log2FC_average']
odf['Reporter L2FC']=df['Reporter log2FC_average']

odf['EPCAM FC']=df['EPCAM FC_average']
odf['CXCR4 FC']=df['CXCR4 FC_average']
odf['Reporter FC']=df['Reporter FC_average']


odf['EPCAM_Rank']=df['EPCAM FC_average'].rank()
odf['CXCR4_Rank']=df['CXCR4 FC_average'].rank()
odf['Reporter_Rank']=df['Reporter FC_average'].rank()
odf['Hit on any']=df['Hit on any']
odf['VP16 variant']=df['VP16 variant']

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "prescreen_figs",
        "2sa - prescreen scatter plot.csv"
    )
)


