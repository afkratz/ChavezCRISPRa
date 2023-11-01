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
os.chdir(Path(__file__).resolve().parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from src import biochem_charachterize as bc

import pandas as pd

df = pd.read_csv(
        os.path.join(
        "output",
        "prescreen",
        "02_manually_tested_hits_and_clusters_assigned.csv"),
        index_col="Unnamed: 0"
    )

from progress.bar import Bar
bar = Bar("Charachterizing...",max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
for i in range(len(df)):
    sequence = df.at[i,"AA sequence"]
    df.at[i,"NCPR"]=bc.getNCPR(sequence)
    df.at[i,"Hydropathy"]=bc.getHydropathy(sequence)
    df.at[i,"Disorder promoting fraction"]=bc.getDisorderFraction(sequence)
    df.at[i,"Kappa"]=bc.getKappa(sequence)
    df.at[i,"Omega"]=bc.getOmega(sequence)
    bar.next()

df.to_csv(
        os.path.join(
        "output",
        "prescreen",
        "03_manually_tested_biochem_charachterized.csv")
    )
