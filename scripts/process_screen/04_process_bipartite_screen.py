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
    df = pd.read_csv(
        os.path.join(
            "screen_data",
            "traits",
            "bipartite_sorted_traits.csv"
        )
    )

    bipartite_rules = fqp.df_to_rules(df)

    bipartite_condition = pd.read_csv(
        os.path.join(
            "screen_data",
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
        
        read_handle = fqp.ScreenReads(fw_read_file=fw_reads,rv_read_file=rv_reads)

        results = fqp.analyze_reads(read_handle,bipartite_rules,bipartite_condition.at[i,"condition"])

        if not os.path.exists("output"):
            os.mkdir("output")

        if not os.path.exists(os.path.join("output","screen_results")):
            os.mkdir(os.path.join("output","screen_results"))
            
        if not os.path.exists(os.path.join("output","screen_results","processed_reads")):
            os.mkdir(os.path.join("output","screen_results","processed_reads"))

        if not os.path.exists(os.path.join("output","screen_results","processed_reads","bipartite_sorted")):
            os.mkdir(os.path.join("output","screen_results","processed_reads","bipartite_sorted"))
        
        fqp.save_results(results,
                         bipartite_rules,
                         os.path.join(
                            "output","screen_results","processed_reads","bipartite_sorted",
                            bipartite_condition.at[i,"condition"])
        )

if __name__=="__main__":
    main()