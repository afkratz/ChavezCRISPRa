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

ChavezCRISPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from src import screen_scoring_tools as sst

barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

tripartite_no_control_classes = {
        "experimental":{
            "BC1":barcodes,
            "BC2":barcodes,
            "BC3":barcodes,
        },
    }


def minilib_toxicity():
    spinner = sp.PieSpinner("Processing minilib toxicity... %(elapsed)ds")

    classes = tripartite_no_control_classes

    dfs={}
    targets=["minilib"]
    replicates=['1']
    bins = ["plasmid_library_rep_1","plasmid_library_rep_2",
            "HEK293T_rep_1","HEK293T_rep_2",
            "HeLa_rep_1","HeLa_rep_2",
            "N2A_rep_1","N2A_rep_2",
            ]
    
    for t in targets:
        dfs[t]={}
        dfs[t]['1']={}
    for t in targets:
        for r in replicates:
            for b in bins:
                dfs[t][r][b]=pd.read_csv(
                        os.path.join(
                            ChavezCRISPRa_root_dir,
                            "screen_output",
                            "screen_results",
                            "processed_reads",
                            "tripartite_minilib",
                            "{}.csv".format(b)
                        )
                    )
    spinner.next()

    sst.discard_errors(dfs,targets,replicates,bins)
    spinner.next()
    
    


    sst.assign_classes(dfs,targets,replicates,bins,classes,spinner=spinner)
    spinner.next()
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

            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["HEK293T_rep_1"],"HEK_1_tox")
            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["HEK293T_rep_2"],"HEK_2_tox")
            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["HEK293T_rep_1","HEK293T_rep_2"],"HEK_av_tox")

            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["HeLa_rep_1"],"HeLa_1_tox")
            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["HeLa_rep_2"],"HeLa_2_tox")
            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["HeLa_rep_1","HeLa_rep_2"],"HeLa_av_tox")

            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["N2A_rep_1"],"N2A_1_tox")
            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["N2A_rep_2"],"N2A_2_tox")
            sst.add_ToxicityScore(dfs[t][r],["plasmid_library_rep_1","plasmid_library_rep_2"],["N2A_rep_1","N2A_rep_2"],"N2A_av_tox")

            """
            Since we are only interested in a subset of them, add a tag
            """
            construct = dfs[t][r].apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
            dfs[t][r]['In_Minilib'] = construct.isin(of_interest)
            dfs[t][r].sort_values(by='In_Minilib',inplace=True,ascending=False)

            dfs[t][r].to_csv(
                os.path.join(
                    ChavezCRISPRa_root_dir,
                    "screen_output",
                    "screen_results",
                    "screen_toxicity", 
                    "minilib_toxicity.csv"        
                     ),index=False)
            
    spinner.finish()

of_interest =[
'A23_A20_A01','A24_A16_A25','A22_A04_A06','A22_A04_A10',
'A25_A19_A12','A25_A19_A19','A25_A19_A01','A16_A06_A06',
'A16_A06_A02','A08_A12_A05','A08_A12_A15','A08_A11_A11',
'A08_A11_A07','A08_A11_A03','A22_A01_A11','A22_A01_A07',
'A04_A24_A06','A04_A24_A23','A04_A24_A16','A10_A16_A12',
'A10_A16_A08','A10_A16_A04','A22_A13_A07','A22_A13_A23',
'A22_A13_A17','A21_A16_A08','A13_A10_A09','A13_A10_A04',
'A08_A20_A09','A08_A20_A04','A04_A18_A18','A06_A06_A16',
'A10_A10_A07','A10_A10_A25','A10_A14_A14','A13_A01_A01',
'A14_A14_A02','A16_A14_A12','A16_A20_A12','A18_A08_A12',
'A18_A18_A03','A18_A23_A24','A18_A25_A22','A22_A20_A12',
'A23_A10_A14','A23_A12_A18','A23_A23_A01','A25_A16_A10',
'A25_A18_A12','A25_A18_A16','A25_A18_A22','A08_A08_A18',
'A08_A25_A08','A10_A18_A04','A10_A18_A17','A22_A16_A12',
]

if __name__=="__main__":minilib_toxicity()