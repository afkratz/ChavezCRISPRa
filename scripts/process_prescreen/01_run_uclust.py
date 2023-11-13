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

#Find path to useach
#The license is ambiguous on if it'd be ok to redistribute the binary
#Regardless, for compatibility with whatever OS you are using, 
# we allow/require you to supply the usearch executable  

path_to_uclust = "../uclust/usearch.exe" #Personally where I placed it

while not os.path.exists(path_to_uclust):
    path_to_uclust = input("Please enter path to usearch executable ")
path_to_uclust = os.path.abspath(path_to_uclust)

#Make paths for output if they don't exist
if not os.path.exists(os.path.join("output","prescreen_results")):
    os.mkdir(os.path.join("output","prescreen_results"))

if not os.path.exists(os.path.join("output","prescreen_results","clusters")):
    os.mkdir(os.path.join("output","prescreen_results","clusters"))

#Load input dataframe
df = pd.read_csv(
    os.path.join("input_data","prescreen","figure_1_manual_testing_results_FC.csv"))

#Drop protein folding domains
df = df[df["PFD or AD"]=="AD"].reset_index(drop=True) 


#Write sequences to a .fasta for clustering
with open("sequences_to_cluster.fasta",'w') as fh:
    for i in range(len(df)):
        fh.write(">"+df.at[i,"ShortID"]+"\n")
        fh.write(df.at[i,"AA sequence"]+"\n")

#Run uclust
uclust_command = path_to_uclust +" -cluster_fast sequences_to_cluster.fasta -id 0.5 -centroids output/prescreen_results/centroids.fasta -clusters output/prescreen_results/clusters/"

os.system(uclust_command)

#Clean up after ourselves
os.remove("sequences_to_cluster.fasta")
