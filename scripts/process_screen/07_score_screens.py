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
from progress import spinner as sp
import pandas as pd

os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from src import screen_scoring_tools as sst


def single_domain_score():
    spinner = sp.PieSpinner("Processing single domain screen... %(elapsed)ds")

    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4","NS"]

    dfs = sst.load_dfs(
        os.path.join("output","screen_results","processed_reads","single_domain_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_negative_controls(dfs,["BC1"],barcodes,targets,replicates,bins)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)
    spinner.next()

    umi_traits={"UMI1":3}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    spinner.next()
    
    sst.discard_combined_bin_counts(dfs,4,targets,replicates)
    spinner.next()

    mfis=sst.load_mfis(
        os.path.join(
            "screen_data",
            "bin_mfis",
            "p1_sorted_mfi.csv"
            )
        )
    sst.add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)
    spinner.next()

    sst.drop_item(dfs,"bin_1",targets,replicates)
    sst.drop_item(dfs,"bin_2",targets,replicates)
    sst.drop_item(dfs,"bin_3",targets,replicates)
    sst.drop_item(dfs,"bin_4",targets,replicates)
    sst.drop_item(dfs,"NS",targets,replicates)

    sst.mean_x_over_y(dfs,"FluorescentProductScore","UMI1",3,targets,replicates,bins)
    spinner.next()

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1"],barcodes)
    spinner.next()
    odf.to_csv(
        os.path.join(
            "output",
            "screen_results",
            "screen_scores", 
            "single_domain_screen_scored.csv"        
            ),
        index=False)
    spinner.finish()

def single_domain_toxicity():
    spinner = sp.PieSpinner("Processing single domain toxicity... %(elapsed)ds")

    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    dfs={}
    targets=["Plasmid"]
    replicates=["1"]
    for t in targets:
        dfs[t]={}
        for r in replicates:
            dfs[t][r]={}
    bins=["P1 Plasmid","EPCAM_1_NS","EPCAM_2_NS","CXCR4_1_NS","CXCR4_2_NS"]
    for t in targets:
        for r in replicates:
            dfs[t][r]["P1 Plasmid"]=pd.read_csv(
                    os.path.join(
                        "output",
                        "screen_results",
                        "processed_reads",
                        "single_domain_plasmid",
                        "single_domain_plasmid.csv"
                    )
                )
            
            for b in bins[1:]:
                dfs[t][r][b] = pd.read_csv(
                    os.path.join(
                        "output",
                        "screen_results",
                        "processed_reads",
                        "single_domain_sorted",
                        b+".csv"
                    )
                )
    spinner.next()
    
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_negative_controls(dfs,["BC1"],barcodes,targets,replicates,bins)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins[1:])
    spinner.next()

    umi_traits={
            "UMI1":0,
            }
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()
    
    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    spinner.next()
    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(dfs[t][r],["BC1"],barcodes).to_csv("single_domain_plasmid_and_unsorted_normalized_reads.csv",index=False)
    spinner.finish()

def bipartite_score():
    spinner = sp.PieSpinner("Processing bipartite score... %(elapsed)ds")

    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4","NS"]

    dfs = sst.load_dfs(
        os.path.join("output","screen_results","processed_reads","bipartite_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_negative_controls(dfs,['BC1','BC2'],barcodes,targets,replicates,bins)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)
    spinner.next()

    umi_traits = {"UMI1":0,"UMI2":2}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_combined_bin_counts(dfs,20,targets,replicates)
    spinner.next()

    mfis=sst.load_mfis(
        os.path.join(
            "screen_data",
            "bin_mfis",
            "p2_sorted_mfi.csv"
            )
        )
    sst.add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)
    spinner.next()

    sst.drop_item(dfs,"bin_1",targets,replicates)
    sst.drop_item(dfs,"bin_2",targets,replicates)
    sst.drop_item(dfs,"bin_3",targets,replicates)
    sst.drop_item(dfs,"bin_4",targets,replicates)
    sst.drop_item(dfs,"NS",targets,replicates)

    sst.mean_x_over_y(dfs,"FluorescentProductScore","UMI2",3,targets,replicates,bins)
    spinner.next()

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1","BC2"],barcodes)
    spinner.next()

    odf.to_csv(
        os.path.join(
            "output",
            "screen_results",
            "screen_scores", 
            "bipartite_screen_scored.csv"        
                     )
        ,index=False)
    spinner.finish()

def bipartite_toxicity():
    spinner = sp.PieSpinner("Processing bipartite toxicity... %(elapsed)ds")

    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    dfs={}
    targets=["Plasmid"]
    replicates=["1"]
    for t in targets:
        dfs[t]={}
        for r in replicates:
            dfs[t][r]={}
    bins=["P2 Plasmid","EPCAM_1_NS","EPCAM_2_NS","CXCR4_1_NS","CXCR4_2_NS"]
    for t in targets:
            for r in replicates:
                dfs[t][r]["P2 Plasmid"]=pd.read_csv(
                        os.path.join(
                            "output",
                            "screen_results",
                            "processed_reads",
                            "bipartite_plasmid",
                            "bipartite_plasmid.csv"
                        )
                    )
                
                for b in bins[1:]:
                    dfs[t][r][b] = pd.read_csv(
                        os.path.join(
                            "output",
                            "screen_results",
                            "processed_reads",
                            "bipartite_sorted",
                            b+".csv"
                        )
                    )
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_negative_controls(dfs,["BC1","BC2"],barcodes,targets,replicates,bins)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins[1:])
    spinner.next()

    umi_traits={
            "UMI1":0,
            "UMI2":0,
            }
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    spinner.next()

    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2"],barcodes).to_csv("bipartite_plasmid_and_unsorted_normalized_reads.csv",index=False)
    spinner.finish()

def tripartite_score():
    spinner = sp.PieSpinner("Processing tripartite score... %(elapsed)ds")

    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4","NS"]

    dfs = sst.load_dfs(
        os.path.join("output","screen_results","processed_reads","tripartite_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_negative_controls(dfs,['BC1','BC2','BC3'],barcodes,targets,replicates,bins)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.01,targets,replicates,bins)
    spinner.next()

    umi_traits = {"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_min_bin_counts(dfs,0,targets,replicates)
    sst.discard_combined_bin_counts(dfs,493,targets,replicates)
    spinner.next()

    mfis=sst.load_mfis(
        os.path.join(
            "screen_data",
            "bin_mfis",
            "p3_sorted_mfi.csv"
            )
        )
    sst.add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)
    spinner.next()

    sst.drop_item(dfs,"bin_1",targets,replicates)
    sst.drop_item(dfs,"bin_2",targets,replicates)
    sst.drop_item(dfs,"bin_3",targets,replicates)
    sst.drop_item(dfs,"bin_4",targets,replicates)
    sst.drop_item(dfs,"NS",targets,replicates)

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1","BC2","BC3"],barcodes)
    spinner.next()

    odf.to_csv(
        os.path.join(
            "output",
            "screen_results",
            "screen_scores", 
            "tripartite_screen_scored.csv"        
                     )
        ,index=False)
    spinner.finish()

def tripartite_toxicity():
    spinner = sp.PieSpinner("Processing tripartite toxicity... %(elapsed)ds")

    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    dfs={}
    targets=["Plasmid"]
    replicates=["1"]
    for t in targets:
        dfs[t]={}
        for r in replicates:
            dfs[t][r]={}
    bins=["P3 Plasmid","EPCAM_1_NS","EPCAM_2_NS","CXCR4_1_NS","CXCR4_2_NS"]
    for t in targets:
            for r in replicates:
                dfs[t][r]["P3 Plasmid"]=pd.read_csv(
                        os.path.join(
                            "output",
                            "screen_results",
                            "processed_reads",
                            "tripartite_plasmid",
                            "tripartite_plasmid.csv"
                        )
                    )
                
                for b in bins[1:]:
                    dfs[t][r][b] = pd.read_csv(
                        os.path.join(
                            "output",
                            "screen_results",
                            "processed_reads",
                            "tripartite_sorted",
                            b+".csv"
                        )
                    )
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.discard_negative_controls(dfs,["BC1","BC2","BC3"],barcodes,targets,replicates,bins)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.01,targets,replicates,bins[1:])
    spinner.next()

    for b in bins[1:]:
        dfs[targets[0]][replicates[0]][b]["UMI1"]=""
        dfs[targets[0]][replicates[0]][b]["UMI3"]=""
    all_umi_traits={
            "UMI1":0,
            "UMI2":0,
            "UMI3":0,
            }
    sst.bin_on_traits(dfs,all_umi_traits,targets,replicates,bins)
    spinner.next()
    
    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    spinner.next()
    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2","BC3"],barcodes).to_csv("tripartite_plasmid_and_unsorted_normalized_reads.csv",index=False)
    spinner.finish()


if __name__=="__main__":
    single_domain_score()
    single_domain_toxicity()
    bipartite_score()
    bipartite_toxicity()
    tripartite_score()
    tripartite_toxicity()
    
    
    