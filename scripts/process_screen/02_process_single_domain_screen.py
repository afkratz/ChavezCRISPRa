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

os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
from src import fastq_process_default as fqp

def main():
    df = pd.read_csv(os.path.join(
            "screen_data",
            "traits",
            "single_domain_sorted_traits.csv"
            )
    )
    
    single_domain_rules = fqp.df_to_rules(df)

    single_domain_condition = pd.read_csv(os.path.join(
        "screen_data",
        "conditions",
        "single_domain_sorted.csv"
        )
    )
    
    
    for i in range(len(single_domain_condition)):
        fw_reads = single_domain_condition.at[i,"fw reads"]
        rv_reads = single_domain_condition.at[i,"rv reads"]

        if not(isinstance(fw_reads,str)):
            fw_reads=None
        if not(isinstance(rv_reads,str)):
            rv_reads=None

        read_handle = fqp.ScreenReads(fw_read_file=fw_reads,rv_read_file=rv_reads)

        results = fqp.analyze_reads(read_handle,single_domain_rules,single_domain_condition.at[i,"condition"])

        if not os.path.exists("output"):
            os.mkdir("output")

        if not os.path.exists(os.path.join("output","screen_results")):
            os.mkdir(os.path.join("output","screen_results"))
            
        if not os.path.exists(os.path.join("output","screen_results","processed_reads")):
            os.mkdir(os.path.join("output","screen_results","processed_reads"))

        if not os.path.exists(os.path.join("output","screen_results","processed_reads","single_domain_sorted")):
            os.mkdir(os.path.join("output","screen_results","processed_reads","single_domain_sorted"))
        
        fqp.save_results(results,
                         single_domain_rules,
                         os.path.join(
                            "output","screen_results","processed_reads","single_domain_sorted",
                            single_domain_condition.at[i,"condition"])
        )

if __name__=="__main__":
    main()