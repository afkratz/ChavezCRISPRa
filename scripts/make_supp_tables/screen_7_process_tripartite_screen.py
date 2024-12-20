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
from src import fastq_process_p3_sorted as fqp
from src import screen_reads_config

def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    reads_dir = screen_reads_config.get_screen_reads_dir()

    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_data",
            "traits",
            "tripartite_sorted_traits.csv"
        )
    )

    tripartite_screen_rules = fqp.df_to_rules(df)

    tripartite_screen_conditions = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_data",
            "conditions",
            "tripartite_sorted.csv"
        )
        )
    
    for i in range(len(tripartite_screen_conditions)):
        fw_reads = tripartite_screen_conditions.at[i,"fw reads"]
        rv_reads = tripartite_screen_conditions.at[i,"rv reads"]

        if not(isinstance(fw_reads,str)):
            fw_reads=None
        if not(isinstance(rv_reads,str)):
            rv_reads=None

        read_handle = fqp.ScreenReads(reads_dir=reads_dir,fw_read_file=fw_reads,rv_read_file=rv_reads)

        results = fqp.analyze_reads(read_handle,tripartite_screen_rules,tripartite_screen_conditions.at[i,"condition"])

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"screen_output")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"screen_output"))

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","screen_results")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","screen_results"))
            
        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","screen_results","processed_reads")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","screen_results","processed_reads"))

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","screen_results","processed_reads","tripartite_sorted")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","screen_results","processed_reads","tripartite_sorted"))
        
        fqp.save_results(results,
                         tripartite_screen_rules,
                         os.path.join(
                            ChavezCIRSPRa_root_dir,"screen_output","screen_results","processed_reads","tripartite_sorted",
                            tripartite_screen_conditions.at[i,"condition"])
        )

if __name__=="__main__":
    main()