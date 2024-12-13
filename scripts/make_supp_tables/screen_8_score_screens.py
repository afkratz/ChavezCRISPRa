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

ChavezCRISPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from src import screen_scoring_tools as sst

barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
single_domain_neg_control_classes = {
        "experimental":{
            "BC1":barcodes,
        },
        "mcpmut_neg_control":{
            "BC1":["MCP_MUTATION1"],
        },
        "puro_neg_control":{
            "BC1":["PuroR1"],
        },
        "supernatant_neg_control":{
            "BC1":["SUPERNATANT1"],
        },
    }

single_domain_no_control_classes = {
        "experimental":{
            "BC1":barcodes,
        },
    }

bipartite_neg_control_classes = {
        "experimental":{
            "BC1":barcodes,
            "BC2":barcodes,
        },
        "mcpmut_neg_control":{
            "BC1":["MCP_MUTATION1"],
            "BC2":["MCP_MUTATION2"],
        },
        "puro_neg_control":{
            "BC1":["PuroR1"],
            "BC2":["PuroR2"],
        },
        "supernatant_neg_control":{
            "BC1":["SUPERNATANT1"],
            "BC2":["SUPERNATANT2"],
        },
    }

bipartite_no_control_classes = {
        "experimental":{
            "BC1":barcodes,
            "BC2":barcodes,
        },
    }

tripartite_neg_control_classes = {
        "experimental":{
            "BC1":barcodes,
            "BC2":barcodes,
            "BC3":barcodes,
        },
        "mcpmut_neg_control":{
            "BC1":["MCP_MUTATION1"],
            "BC2":["MCP_MUTATION2"],
            "BC3":["MCP_MUTATION3"],
        },
        "puro_neg_control":{
            "BC1":["PuroR1"],
            "BC2":["PuroR2"],
            "BC3":["PuroR3"],
        },
        "supernatant_neg_control":{
            "BC1":["SUPERNATANT1"],
            "BC2":["SUPERNATANT2"],
            "BC3":["SUPERNATANT3"],
        },
    }

tripartite_no_control_classes = {
        "experimental":{
            "BC1":barcodes,
            "BC2":barcodes,
            "BC3":barcodes,
        },
    }


def single_domain_score(include_negative_controls = False):
    spinner = sp.PieSpinner("Processing single domain screen... %(elapsed)ds")
    
    if include_negative_controls:
        classes = single_domain_neg_control_classes
    else:
        classes = single_domain_no_control_classes    

    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4"]

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","processed_reads","single_domain_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
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
            ChavezCRISPRa_root_dir,
            "ScreenData",
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
    sst.drop_item(dfs,'class',targets,replicates)

    sst.mean_x_over_y(dfs,"FluorescentProductScore","UMI1",targets,replicates,bins)
    spinner.next()

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1"],barcodes)
    spinner.next()
    
    odf.to_csv(
        os.path.join(
            ChavezCRISPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores", 
            "single_domain_screen_scored.csv"        
            ),
        index=False)
    spinner.finish()

def single_domain_toxicity(include_negative_controls = False):
    spinner = sp.PieSpinner("Processing single domain toxicity... %(elapsed)ds")
    if include_negative_controls:
        classes = single_domain_neg_control_classes
    else:
        classes = single_domain_no_control_classes    

    dfs={}
    targets=["Plasmid"]
    replicates=["1"]
    for t in targets:
        dfs[t]={}
        for r in replicates:
            dfs[t][r]={}
    bins=["P1 Plasmid","EPCAM_1_NS","EPCAM_2_NS","CXCR4_1_NS","CXCR4_2_NS","Reporter_1_NS","Reporter_2_NS"]

    for t in targets:
        for r in replicates:
            dfs[t][r]["P1 Plasmid"]=pd.read_csv(
                    os.path.join(
                        ChavezCRISPRa_root_dir,
                        "screen_output",
                        "screen_results",
                        "processed_reads",
                        "single_domain_plasmid",
                        "single_domain_plasmid.csv"
                    ))
            
            for b in bins[1:]:
                dfs[t][r][b] = pd.read_csv(
                    os.path.join(
                        ChavezCRISPRa_root_dir,
                        "screen_output",
                        "screen_results",
                        "processed_reads",
                        "single_domain_sorted",
                        b+".csv"
                    )
                )
    spinner.next()
    
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins[1:])
    spinner.next()

    umi_traits={"UMI1":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()
    
    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    sst.drop_item(dfs,'class',targets,replicates)


    spinner.next()
    for t in targets:
        for r in replicates:
            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["EPCAM_1_NS"],"EPCAM_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["EPCAM_2_NS"],"EPCAM_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["EPCAM_1_NS","EPCAM_2_NS"],"EPCAM_average_Tox")

            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["CXCR4_1_NS"],"CXCR4_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["CXCR4_2_NS"],"CXCR4_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["CXCR4_1_NS","CXCR4_2_NS"],"CXCR4_average_Tox")

            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["Reporter_1_NS"],"Reporter_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["Reporter_2_NS"],"Reporter_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P1 Plasmid",["Reporter_1_NS","Reporter_2_NS"],"Reporter_average_Tox")




            sst.fill_in_combinatorial_results(dfs[t][r],["BC1"],barcodes).to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "screen_output",
                    "screen_results",
                    "screen_toxicity", 
                    "single_domain_toxicity.csv"        
                     ),index=False)
            
    spinner.finish()

def single_domain_read_counts(include_negative_controls = False):
    spinner = sp.PieSpinner("Generating single domain read counts... %(elapsed)ds")
    if include_negative_controls:
        classes = single_domain_neg_control_classes
    else:
        classes = single_domain_no_control_classes

    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4","NS"]

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","processed_reads","single_domain_sorted"),
        targets,replicates,bins)
    
    spinner.next()
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)
    spinner.next()

    umi_traits={"UMI1":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    normalized_dfs=sst.combine_bins(dfs,targets,replicates,bins)
    sst.drop_item(normalized_dfs,'class',targets,replicates)

    spinner.next()

    if not os.path.exists(os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts","single_domain")):
        os.mkdir(
            os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts","single_domain"))
    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(normalized_dfs[t][r],["BC1"],barcodes).fillna(0).to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "screen_output",
                    "screen_results",
                    "screen_bin_counts",
                    "single_domain",
                    t+"_"+r+"_normalized_counts.csv"
                ),
                index=False
            )
    spinner.finish()

def bipartite_score(include_negative_controls = False):
    spinner = sp.PieSpinner("Processing bipartite score... %(elapsed)ds")

    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4"]

    if include_negative_controls:
        classes = bipartite_neg_control_classes
    else:
        classes = bipartite_no_control_classes    

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","processed_reads","bipartite_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
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
            ChavezCRISPRa_root_dir,
            "ScreenData",
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
    sst.drop_item(dfs,'class',targets,replicates)

    sst.mean_x_over_y(dfs,"FluorescentProductScore","UMI2",targets,replicates,bins)
    spinner.next()

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1","BC2"],barcodes)
    spinner.next()

    odf.to_csv(
        os.path.join(
            ChavezCRISPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores", 
            "bipartite_screen_scored.csv"),
        index=False)
    spinner.finish()

def bipartite_toxicity(include_negative_controls=False):
    spinner = sp.PieSpinner("Processing bipartite toxicity... %(elapsed)ds")

    if include_negative_controls:
        classes = bipartite_neg_control_classes
    else:
        classes = bipartite_no_control_classes  
    

    dfs={}
    targets=["Plasmid"]
    replicates=["1"]
    for t in targets:
        dfs[t]={}
        for r in replicates:
            dfs[t][r]={}
            
    bins=["P2 Plasmid","EPCAM_1_NS","EPCAM_2_NS","CXCR4_1_NS","CXCR4_2_NS","Reporter_1_NS","Reporter_2_NS"]
    for t in targets:
            for r in replicates:
                dfs[t][r]["P2 Plasmid"]=pd.read_csv(
                        os.path.join(
                            ChavezCRISPRa_root_dir,
                            "screen_output",
                            "screen_results",
                            "processed_reads",
                            "bipartite_plasmid",
                            "bipartite_plasmid.csv"
                        )
                    )
                
                for b in bins[1:]:
                    dfs[t][r][b] = pd.read_csv(
                        os.path.join(
                            ChavezCRISPRa_root_dir,
                            "screen_output",
                            "screen_results",
                            "processed_reads",
                            "bipartite_sorted",
                            b+".csv"
                        )
                    )
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
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
    sst.drop_item(dfs,'class',targets,replicates)

    spinner.next()

    for t in targets:
        for r in replicates:
            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["EPCAM_1_NS"],"EPCAM_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["EPCAM_2_NS"],"EPCAM_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["EPCAM_1_NS","EPCAM_2_NS"],"EPCAM_average_Tox")

            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["CXCR4_1_NS"],"CXCR4_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["CXCR4_2_NS"],"CXCR4_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["CXCR4_1_NS","CXCR4_2_NS"],"CXCR4_average_Tox")

            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["Reporter_1_NS"],"Reporter_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["Reporter_2_NS"],"Reporter_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P2 Plasmid",["Reporter_1_NS","Reporter_2_NS"],"Reporter_average_Tox")
            sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2"],barcodes).to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "screen_output",
                    "screen_results",
                    "screen_toxicity", 
                    "bipartite_screen_toxicity.csv"        
                     ),index=False)
    spinner.finish()

def bipartite_read_counts(include_negative_controls = False):
    spinner = sp.PieSpinner("Generating bipartite read counts... %(elapsed)ds")
    
    if include_negative_controls:
        classes = bipartite_neg_control_classes
    else:
        classes = bipartite_no_control_classes  


    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4","NS"]

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","processed_reads","bipartite_sorted"),
        targets,replicates,bins)
    spinner.next()
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)
    spinner.next()

    umi_traits={"UMI1":0,"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    normalized_dfs=sst.combine_bins(dfs,targets,replicates,bins)
    sst.drop_item(normalized_dfs,'class',targets,replicates)
    spinner.next()

    if not os.path.exists(os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts","bipartite_screen")):
        os.mkdir(os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts","bipartite_screen"))
    
    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(normalized_dfs[t][r],["BC1","BC2"],barcodes).fillna(0).to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "screen_output",
                    "screen_results",
                    "screen_bin_counts",
                    "bipartite_screen",
                    t+"_"+r+"_normalized_counts.csv"
                ),
                index=False
            )
    spinner.finish()

def tripartite_score(include_negative_controls=False):
    spinner = sp.PieSpinner("Processing tripartite score... %(elapsed)ds")

    if include_negative_controls:
        classes = tripartite_neg_control_classes
    else:
        classes = tripartite_no_control_classes  

    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4"]

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","processed_reads","tripartite_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
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
    if include_negative_controls:
        sst.discard_combined_bin_counts(dfs,200,targets,replicates)
    else:
        sst.discard_combined_bin_counts(dfs,493,targets,replicates)
    spinner.next()

    mfis=sst.load_mfis(
        os.path.join(
            ChavezCRISPRa_root_dir,
            "ScreenData",
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
    sst.drop_item(dfs,'class',targets,replicates)


    odf = sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1","BC2","BC3"],barcodes)
    spinner.next()
    
    odf.to_csv(
        os.path.join(
            ChavezCRISPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores", 
            "tripartite_screen_scored.csv"        
                     )
        ,index=False)
    spinner.finish()


def tripartite_toxicity(include_negative_controls=False):
    spinner = sp.PieSpinner("Processing tripartite toxicity... %(elapsed)ds")

    if include_negative_controls:
        classes = tripartite_neg_control_classes
    else:
        classes = tripartite_no_control_classes

    dfs={}
    targets=["Plasmid"]
    replicates=["1"]
    for t in targets:
        dfs[t]={}
        for r in replicates:
            dfs[t][r]={}
    bins=["P3 Plasmid","EPCAM_1_NS","EPCAM_2_NS","CXCR4_1_NS","CXCR4_2_NS","Reporter_1_NS","Reporter_2_NS"]
    for t in targets:
            for r in replicates:
                dfs[t][r]["P3 Plasmid"]=pd.read_csv(
                        os.path.join(
                            ChavezCRISPRa_root_dir,
                            "screen_output",
                            "screen_results",
                            "processed_reads",
                            "tripartite_plasmid",
                            "tripartite_plasmid.csv"
                        )
                    )
                
                for b in bins[1:]:
                    dfs[t][r][b] = pd.read_csv(
                        os.path.join(
                            ChavezCRISPRa_root_dir,
                            "screen_output",
                            "screen_results",
                            "processed_reads",
                            "tripartite_sorted",
                            b+".csv"
                        )
                    )
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
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
    sst.drop_item(dfs,'class',targets,replicates)

    spinner.next()
    for t in targets:
        for r in replicates:

            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["EPCAM_1_NS"],"EPCAM_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["EPCAM_2_NS"],"EPCAM_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["EPCAM_1_NS","EPCAM_2_NS"],"EPCAM_average_Tox")

            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["CXCR4_1_NS"],"CXCR4_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["CXCR4_2_NS"],"CXCR4_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["CXCR4_1_NS","CXCR4_2_NS"],"CXCR4_average_Tox")

            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["Reporter_1_NS"],"Reporter_1_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["Reporter_2_NS"],"Reporter_2_Tox")
            sst.add_ToxicityScore(dfs[t][r],"P3 Plasmid",["Reporter_1_NS","Reporter_2_NS"],"Reporter_average_Tox")

            sst.fill_in_combinatorial_results(dfs[t][r],["BC1","BC2","BC3"],barcodes).to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "screen_output",
                    "screen_results",
                    "screen_toxicity", 
                    "tripartite_screen_toxicity.csv"        
                     ),index=False)
            
    spinner.finish()

def tripartite_read_counts(include_negative_controls=False):
    spinner = sp.PieSpinner("Generating tripartite read counts... %(elapsed)ds")
    if include_negative_controls:
        classes = tripartite_neg_control_classes
    else:
        classes = tripartite_no_control_classes

    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4","NS"]

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","processed_reads","tripartite_sorted"),
        targets,replicates,bins)
    spinner.next()
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    sst.discard_high_counts_percentage_of_total(dfs,0.01,targets,replicates,bins)
    spinner.next()

    umi_traits={"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    normalized_dfs=sst.combine_bins(dfs,targets,replicates,bins)
    sst.drop_item(normalized_dfs,'class',targets,replicates)
    spinner.next()

    if not os.path.exists(os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts","tripartite_screen")):
        os.mkdir(
            os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts","tripartite_screen"))
    for t in targets:
        for r in replicates:
            sst.fill_in_combinatorial_results(normalized_dfs[t][r],["BC1","BC2","BC3"],barcodes).fillna(0).to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "screen_output",
                    "screen_results",
                    "screen_bin_counts",
                    "tripartite_screen",
                    t+"_"+r+"_normalized_counts.csv"
                ),
                index=False
            )
    spinner.finish()


def main():
    if not os.path.exists(
            os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_scores")
                ):
            os.mkdir(os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_scores"))
    if not os.path.exists(
        os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_toxicity")
            ):
        os.mkdir(os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_toxicity"))
    if not os.path.exists(os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts")):
        os.mkdir(
            os.path.join(ChavezCRISPRa_root_dir,"screen_output","screen_results","screen_bin_counts"))
    
    INCLUDE_NEGATIVE_CONTROLS=False

    single_domain_score(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    single_domain_toxicity(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    single_domain_read_counts(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    bipartite_score(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    bipartite_toxicity(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    bipartite_read_counts(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    tripartite_score(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    tripartite_toxicity(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    tripartite_read_counts(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)

    
if __name__=="__main__":
    main()
