# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
from src import biochem_charachterize as bc

import pandas as pd

def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    df = pd.read_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "prescreen_results",
            "1_manually_tested_clusters_assigned.csv"),
            index_col="Domain ID"
        )

    from progress.bar import Bar
    bar = Bar("Charachterizing...",max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
    for i in df.index:
        sequence = df.at[i,"AA sequence"]
        df.at[i,"NCPR"]=bc.getNCPR(sequence)
        df.at[i,"Hydropathy"]=bc.getHydropathy(sequence)
        df.at[i,"Disorder promoting fraction"]=bc.getDisorderFraction(sequence)
        df.at[i,"Kappa"]=bc.getKappa(sequence)
        df.at[i,"Omega"]=bc.getOmega(sequence)
        bar.next()
    bar.finish()
    df.to_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "prescreen_results",
            "2_manually_tested_biochem_charachterized.csv")
        )


if __name__ == "__main__":
    main()