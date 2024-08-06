# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2024 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------

"""

import os
import sys
from pathlib import Path
from progress import spinner as sp
import pandas as pd

ChavezCRISPRa_root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0,str(ChavezCRISPRa_root_dir))


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

def single_domain_score_no_umis():
    spinner = sp.PieSpinner("Processing single domain screen w/out umis... %(elapsed)ds")
    
    classes = single_domain_no_control_classes
    
    targets = ['EPCAM','CXCR4','Reporter']
    replicates = ['1','2']
    bins = ['bin_1','bin_2','bin_3','bin_4']
    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"output","screen_results","processed_reads","single_domain_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()


    umi_traits={"UMI1":0}#Total UMI binning!
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

    spinner.next()

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1"],barcodes)
    spinner.next()
    
    odf.to_csv(
        os.path.join(
            ChavezCRISPRa_root_dir,
            "output",
            "screen_results",
            "screen_scores", 
            "single_domain_screen_scored_no_umis.csv"        
            ),
        index=False)
    spinner.finish()


def bipartite_score_no_umis():
    spinner = sp.PieSpinner("Processing bipartite score w/out umis... %(elapsed)ds")

    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4"]

    classes = bipartite_no_control_classes    

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"output","screen_results","processed_reads","bipartite_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    umi_traits = {"UMI1":0,"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
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

    spinner.next()

    odf=sst.combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = sst.fill_in_combinatorial_results(odf,["BC1","BC2"],barcodes)
    spinner.next()

    odf.to_csv(
        os.path.join(
            ChavezCRISPRa_root_dir,
            "output",
            "screen_results",
            "screen_scores", 
            "bipartite_screen_scored_no_umis.csv"),
        index=False)
    spinner.finish()



def tripartite_score_no_umi():
    spinner = sp.PieSpinner("Processing tripartite score w/out umis... %(elapsed)ds")

    classes = tripartite_no_control_classes  

    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin_1","bin_2","bin_3","bin_4"]

    dfs = sst.load_dfs(
        os.path.join(ChavezCRISPRa_root_dir,"output","screen_results","processed_reads","tripartite_sorted"),
        targets,replicates,bins)
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    umi_traits = {"UMI2":0}
    sst.bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    spinner.next()

    sst.normalize_read_counts(dfs,targets,replicates,bins)

    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
        
    spinner.next()
    
    sst.discard_min_bin_counts(dfs,0,targets,replicates)
    
    sst.discard_combined_bin_counts(dfs,458,targets,replicates)
    
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
            "output",
            "screen_results",
            "screen_scores", 
            "tripartite_screen_scored_no_umis.csv"        
                     )
        ,index=False)
    spinner.finish()








if __name__=="__main__":
    #single_domain_score_no_umis()
    bipartite_score_no_umis()
    #tripartite_score_no_umi()
