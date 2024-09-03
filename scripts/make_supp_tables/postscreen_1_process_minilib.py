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

import pandas as pd

ChavezCIRSPRa_root_dir = str(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,ChavezCIRSPRa_root_dir)

from src import fastq_process_default as fqp
from src import screen_reads_config


def main():
    reads_dir = screen_reads_config.get_screen_reads_dir()

    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'ScreenData',
            'traits',
            'tripartite_plasmid_traits.csv'#Reuse this for the post screen tox
        )
    )

    tripartite_rules = fqp.df_to_rules(df)

    tripartite_condition = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'ScreenData',
            'conditions',
            'tripartite_minilib.csv'
        )
    )

    for i in range(len(tripartite_condition)):
        fw_reads = tripartite_condition.at[i,"fw reads"]
        rv_reads = tripartite_condition.at[i,"rv reads"]

        if not(isinstance(fw_reads,str)):
            fw_reads=None
        if not(isinstance(rv_reads,str)):
            rv_reads=None

        read_handle = fqp.ScreenReads(reads_dir=reads_dir,fw_read_file=fw_reads,rv_read_file=rv_reads)

        results = fqp.analyze_reads(read_handle,tripartite_rules,tripartite_condition.at[i,"condition"])

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output"))

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results"))

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads"))

        if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads","tripartite_minilib")):
            os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads","tripartite_minilib"))
        
        fqp.save_results(results,
                         tripartite_rules,
                         os.path.join(
                            ChavezCIRSPRa_root_dir,"output","screen_results","processed_reads","tripartite_minilib",
                            tripartite_condition.at[i,"condition"])
        )


if __name__=="__main__":
    main()