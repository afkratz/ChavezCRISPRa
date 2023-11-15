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
os.chdir(Path(__file__).resolve().parent.parent.parent)
print(os.getcwd())
import pandas as pd
import numpy as np
import glob
from Bio import SeqIO

#Load input dataframe
df = pd.read_csv(
    os.path.join(
        "input_data",
        "prescreen",
        "figure_1_manual_testing_results_FC.csv"),
    index_col="Unnamed: 0")

#Drop protein folding domains
df = df[df["PFD or AD"]=="AD"].reset_index(drop=True) 

index_to_shortID = dict(df["ShortID"])
shortID_to_index = dict([(value, key) for key, value in index_to_shortID.items()])

df["Hit on EPCAM"]=df["EPCAM FC_average"]>=2
df["Hit on CXCR4"]=df["CXCR4 FC_average"]>=2
df["Hit on tdTomato"]=df["tdTomato FC_average"]>=2

df['Hit on any']=df[["Hit on EPCAM","Hit on CXCR4","Hit on tdTomato"]].any(axis=1)



Num_clusters = len(glob.glob(os.path.join("output","prescreen_results","clusters","*")))
df['Cluster']=np.nan
df['Is centroid']=False
for file in glob.glob(os.path.join("output","prescreen_results","clusters","*")):
    cluster = os.path.split(file)[-1]
    for cluster_member_number,record in enumerate(SeqIO.parse(file,"fasta")):
        shortID = record.id
        index=shortID_to_index[shortID]
        df.at[index,"Cluster"]=int(cluster)
        df.at[index,"Is centroid"] = cluster_member_number==0
df.to_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "02_manually_tested_hits_and_clusters_assigned.csv")
    )