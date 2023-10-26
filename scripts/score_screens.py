# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------

"""

import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np

os.chdir(Path(__file__).resolve().parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))

from src import screen_scoring_tools as sst

def score_single_domain_screen():
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin 1","bin 2","bin 3","bin 4","NS"]
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

    dfs = sst.load_dfs("output/screen_results/processed_reads/single_domain_sorted",targets,replicates,bins)

    sst.discard_errors(dfs,targets,replicates,bins)

    sst.discard_negative_controls(dfs,["BC1"],barcodes,targets,replicates,bins)

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)

    umi_traits={"UMI1":3}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)

    sst.normalize_read_counts(dfs,targets,replicates,bins)

    dfs=sst.combine_bins(dfs,targets,replicates,bins)


    sst.discard_combined_bin_counts(dfs,4,targets,replicates)

    mfis=sst.load_mfis("screen_Data/bin_mfis/p1_sorted_mfi.csv")
    sst.add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)

    sst.drop_item(dfs,"bin 1",targets,replicates)
    sst.drop_item(dfs,"bin 2",targets,replicates)
    sst.drop_item(dfs,"bin 3",targets,replicates)
    sst.drop_item(dfs,"bin 4",targets,replicates)
    sst.drop_item(dfs,"NS",targets,replicates)

    sst.mean_x_over_y(dfs,"FluorescentProductScore","UMI1",1,targets,replicates,bins)

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1"],barcodes)
    odf.to_csv(
        os.path.join(
            "output",
            "screen_results",
            "screen_scores", 
            "single_domain_screen_scored.csv"        
                     )
        ,index=False)


def score_bipartite_screen():
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin 1","bin 2","bin 3","bin 4","NS"]
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

    dfs = sst.load_dfs("output/screen_results/processed_reads/bipartite_sorted",targets,replicates,bins)
    
    sst.discard_errors(dfs,targets,replicates,bins)

    sst.discard_negative_controls(dfs,['BC1','BC2'],barcodes,targets,replicates,bins)

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)

    umi_traits = {"UMI1":0,"UMI2":2}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)

    sst.normalize_read_counts(dfs,targets,replicates,bins)

    dfs=sst.combine_bins(dfs,targets,replicates,bins)


    sst.discard_combined_bin_counts(dfs,20,targets,replicates)

    mfis=sst.load_mfis("screen_Data/bin_mfis/p2_sorted_mfi.csv")
    sst.add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)

    sst.drop_item(dfs,"bin 1",targets,replicates)
    sst.drop_item(dfs,"bin 2",targets,replicates)
    sst.drop_item(dfs,"bin 3",targets,replicates)
    sst.drop_item(dfs,"bin 4",targets,replicates)
    
    sst.drop_item(dfs,"NS",targets,replicates)

    sst.mean_x_over_y(dfs,"FluorescentProductScore","UMI2",3,targets,replicates,bins)

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1","BC2"],barcodes)
    odf.to_csv(
        os.path.join(
            "output",
            "screen_results",
            "screen_scores", 
            "bipartite_screen_scored.csv"        
                     )
        ,index=False)

def bipartite_screen_binned_counts():
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin 1","bin 2","bin 3","bin 4","NS"]
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

    dfs = sst.load_dfs("output/screen_results/processed_reads/bipartite_sorted",targets,replicates,bins)
    
    sst.discard_errors(dfs,targets,replicates,bins)

    sst.discard_negative_controls(dfs,['BC1','BC2'],barcodes,targets,replicates,bins)

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)

    umi_traits = {"UMI1":0,"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)

    sst.normalize_read_counts(dfs,targets,replicates,bins)

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    for t in targets:
        for r in replicates:
            df = sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2"],barcodes)
            df.to_csv(
                os.path.join(
                    "Bipartite_"+t+"_"+r+"_"+"HUF_0BPBinned_Normalized.csv"
                    ),
                    index=False
                    )

def score_tripartite_screen():
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin 1","bin 2","bin 3","bin 4","NS"]
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

    dfs = sst.load_dfs("output/screen_results/processed_reads/tripartite_sorted",targets,replicates,bins)

    sst.discard_errors(dfs,targets,replicates,bins)
    
    sst.discard_negative_controls(dfs,['BC1','BC2','BC3'],barcodes,targets,replicates,bins)

    sst.discard_high_counts_percentage_of_total(dfs,0.01,targets,replicates,bins)
    
    umi_traits = {"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    
    sst.normalize_read_counts(dfs,targets,replicates,bins)
    
    dfs=sst.combine_bins(dfs,targets,replicates,bins)

    sst.discard_min_bin_counts(dfs,0,targets,replicates)

    sst.discard_combined_bin_counts(dfs,493,targets,replicates)

    mfis=sst.load_mfis("screen_Data/bin_mfis/p3_sorted_mfi.csv")
    sst.add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)
    
    sst.drop_item(dfs,"bin 1",targets,replicates)
    sst.drop_item(dfs,"bin 2",targets,replicates)
    sst.drop_item(dfs,"bin 3",targets,replicates)
    sst.drop_item(dfs,"bin 4",targets,replicates)
    sst.drop_item(dfs,"NS",targets,replicates)

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1","BC2","BC3"],barcodes)
    odf.to_csv(
        os.path.join(
            "output",
            "screen_results",
            "screen_scores", 
            "tripartite_screen_scored.csv"        
                     )
        ,index=False)

def tripartite_screen_binned_counts():
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin 1","bin 2","bin 3","bin 4","NS"]
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

    dfs = sst.load_dfs("output/screen_results/processed_reads/tripartite_sorted",targets,replicates,bins)
    
    sst.discard_errors(dfs,targets,replicates,bins)

    sst.discard_negative_controls(dfs,['BC1','BC2','BC3'],barcodes,targets,replicates,bins)

    sst.discard_high_counts_percentage_of_total(dfs,0.01,targets,replicates,bins)

    umi_traits = {"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)

    sst.normalize_read_counts(dfs,targets,replicates,bins)

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    for t in targets:
        for r in replicates:
            df = sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2","BC3"],barcodes)
            df.to_csv(
                os.path.join(
                    "Tripartite_"+t+"_"+r+"_"+"HUF_0BPBinned_Normalized.csv"
                    ),
                    index=False
                    )

def bipartite_plasmid():
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    dfs={}
    targets=["P2 Plasmid",]
    dfs["P2 Plasmid"]={}
    replicates=["1"]
    dfs["P2 Plasmid"]["1"]={}
    bins=["Plasmid library"]
    dfs["P2 Plasmid"]["1"]["Plasmid library"]=pd.read_csv("output/screen_results/processed_reads/bipartite_plasmid/P2 Plasmid library.csv",index_col="Unnamed: 0")
    sst.discard_errors(dfs,targets,replicates,bins)
    sst.discard_negative_controls(dfs,["BC1","BC2"],barcodes,targets,replicates,bins)
    umi_traits={
            "UMI1":0,
            "UMI2":0,
            }
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    sst.normalize_read_counts(dfs,targets,replicates,bins)
    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2"],barcodes).to_csv("Bipartite_Plasmid_0BPBinned_Normalized.csv",index=False)

def tripartite_plasmid():
    
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    dfs={}
    targets=["P3 Plasmid",]
    dfs["P3 Plasmid"]={}
    replicates=["1"]
    dfs["P3 Plasmid"]["1"]={}
    bins=["Plasmid library"]
    dfs["P3 Plasmid"]["1"]["Plasmid library"]=pd.read_csv("output/screen_results/processed_reads/tripartite_plasmid/P3 Plasmid library.csv",index_col="Unnamed: 0")
    sst.discard_errors(dfs,targets,replicates,bins)
    sst.discard_negative_controls(dfs,["BC1","BC2","BC3"],barcodes,targets,replicates,bins)
    umi_traits={
            "UMI1":0,
            "UMI2":0,
            "UMI3":0,
            }
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    sst.normalize_read_counts(dfs,targets,replicates,bins)
    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2","BC3"],barcodes).to_csv("Tripartite_Plasmid_0BPBinned_Normalized.csv",index=False)



if __name__=="__main__":
    #score_single_domain_screen()
    #score_bipartite_screen()
    #score_tripartite_screen()
    bipartite_plasmid()
    #bipartite_screen_binned_counts()
    tripartite_plasmid()
    #tripartite_screen_binned_counts()
    