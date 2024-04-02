# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
Analyzes UCLUST output to assign sequences to clusters of similar activators,
annotate them as either being the centroid of their cluster or not, as well as 
assign them as either being hits or misses on the three targets
"""

import os
from pathlib import Path


import pandas as pd
import numpy as np
import glob
from Bio import SeqIO

def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    #Load input dataframe
    seq_df = pd.read_excel(
        os.path.join(ChavezCIRSPRa_root_dir,"InputData","Supplementary Table 1.xlsx"),
        index_col = "Domain ID"
        )

    #Load score data
    score_df = pd.read_excel(
        os.path.join(ChavezCIRSPRa_root_dir,"InputData","Source Data Figure 1 and Supplementary Figures 1-2.xlsx"),
        usecols=range(29),#Only load the first 29 columns
        index_col = "Domain ID",
    )

    #Check that all sequences in the sequence dataframe have scores
    assert set(seq_df.index)==set(score_df.index)
    

    score_df['Hit on any'] = score_df[['Activated 1 target gene 2-fold?','Activated 2 target genes 2-fold?','Activated 3 target genes 2-fold?']].values.any(axis=1)


    #Combine dataframes
    seq_df = seq_df.join(score_df)

    #Drop protein folding domains
    seq_df = seq_df[seq_df["Role"]=="Activator"]

    #Assign clusters and centroid status
    seq_df['Cluster']=np.nan
    seq_df['Is centroid']=False
    for file in glob.glob(os.path.join(ChavezCIRSPRa_root_dir,"output","prescreen_results","clusters","*")):
        cluster = os.path.split(file)[-1]
        for cluster_member_number,record in enumerate(SeqIO.parse(file,"fasta")):
            domainID = record.id
            seq_df.at[domainID,"Cluster"]=int(cluster)
            seq_df.at[domainID,"Is centroid"] = cluster_member_number==0
    seq_df.to_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "prescreen_results",
            "3_manually_tested_hits_and_clusters_assigned.csv")
        )
    
if __name__=="__main__":
    main()