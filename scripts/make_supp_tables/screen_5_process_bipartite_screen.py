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

sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
from src import fastq_process_default as fqp
from src import screen_reads_config

def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    reads_dir = screen_reads_config.get_screen_reads_dir()

    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "ScreenData",
            "traits",
            "bipartite_sorted_traits.csv"
        )
    )

    bipartite_rules = fqp.df_to_rules(df)

    bipartite_condition = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "ScreenData",
            "conditions",
            "bipartite_sorted.csv"
        )
    )

    for i in range(len(bipartite_condition)):
        fw_reads = bipartite_condition.at[i,"fw reads"]
        rv_reads = bipartite_condition.at[i,"rv reads"]

        if not(isinstance(fw_reads,str)):
            fw_reads=None
        if not(isinstance(rv_reads,str)):
            rv_reads=None
        
        read_handle = fqp.ScreenReads(reads_dir=reads_dir,fw_read_file=fw_reads,rv_read_file=rv_reads)

        results = fqp.analyze_reads(read_handle,bipartite_rules,bipartite_condition.at[i,"condition"])

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output"))

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results"))
            
        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads"))

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads","bipartite_sorted")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads","bipartite_sorted"))
        
        fqp.save_results(
            results,
            bipartite_rules,
            os.path.join(
                ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads","bipartite_sorted",
                bipartite_condition.at[i,"condition"])
        )

if __name__=="__main__":
    main()