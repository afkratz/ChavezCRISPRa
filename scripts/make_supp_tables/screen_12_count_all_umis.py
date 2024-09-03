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
        os.path.join(ChavezCRISPRa_root_dir,"output","screen_results","processed_reads","single_domain_sorted"),
        targets,replicates,bins)
    
    spinner.next()
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    sst.drop_item(dfs,'class',targets,replicates)

    spinner.next()

    for t in targets:
        for r in replicates:
            dfs[t][r].to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "output",
                    "screen_results",
                    "screen_bin_counts",
                    "single_domain",
                    t+"_"+r+"_all_umi_counts.csv"
                ),
                index=False
            )
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
        os.path.join(ChavezCRISPRa_root_dir,"output","screen_results","processed_reads","bipartite_sorted"),
        targets,replicates,bins)
    spinner.next()
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    sst.drop_item(dfs,'class',targets,replicates)
    spinner.next()
   
    for t in targets:
        for r in replicates:
            dfs[t][r].to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "output",
                    "screen_results",
                    "screen_bin_counts",
                    "bipartite_screen",
                    t+"_"+r+"_all_umi_counts.csv"
                ),
                index=False
            )
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
        os.path.join(ChavezCRISPRa_root_dir,"output","screen_results","processed_reads","tripartite_sorted"),
        targets,replicates,bins)
    spinner.next()
    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()

    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()

    dfs=sst.combine_bins(dfs,targets,replicates,bins)
    sst.drop_item(dfs,'class',targets,replicates)
    spinner.next()

    
    for t in targets:
        for r in replicates:
            dfs[t][r].to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "output",
                    "screen_results",
                    "screen_bin_counts",
                    "tripartite_screen",
                    t+"_"+r+"_all_umi_counts.csv"
                ),
                index=False
            )
    spinner.finish()


def main():
    
    INCLUDE_NEGATIVE_CONTROLS=False
    single_domain_read_counts(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    bipartite_read_counts(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)
    tripartite_read_counts(include_negative_controls=INCLUDE_NEGATIVE_CONTROLS)

    
if __name__=="__main__":
    main()
