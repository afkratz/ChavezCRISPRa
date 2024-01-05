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

import pandas as pd
import numpy as np
import glob
from Bio import SeqIO

#Load input dataframe
df = pd.read_excel(
    os.path.join("input_data","Supplementary Table 1.xlsx"),
    index_col = "Domain ID"
    )

#Load score data
score_df = pd.read_excel(
    os.path.join("input_data","Figure 1 and Supplementary Figures 1-2.xlsx"),
    index_col = "Domain ID"
)

df = df.join(score_df)
df.to_csv('test.csv')

#Drop protein folding domains
df = df[df["Role"]=="Activator"]

#Assign clusters and centroid status
df['Cluster']=np.nan
df['Is centroid']=False
for file in glob.glob(os.path.join("output","prescreen_results","clusters","*")):
    cluster = os.path.split(file)[-1]
    for cluster_member_number,record in enumerate(SeqIO.parse(file,"fasta")):
        domainID = record.id
        df.at[domainID,"Cluster"]=int(cluster)
        df.at[domainID,"Is centroid"] = cluster_member_number==0
        
df.to_csv(
        os.path.join(
        "output",
        "prescreen_results",
        "02_manually_tested_hits_and_clusters_assigned.csv")
    )