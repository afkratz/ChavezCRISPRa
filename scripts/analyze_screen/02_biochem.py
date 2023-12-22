# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import pandas as pd
import os
from pathlib import Path
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))


import os
from pathlib import Path
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
from src import biochem_charachterize as bc

import pandas as pd

df_1 = pd.read_csv(
        os.path.join(
        "input_data",
        "screen_sequences",
        "p1_sequences.csv"),
    )
df_2 = pd.read_csv(
        os.path.join(
        "input_data",
        "screen_sequences",
        "p2_sequences.csv")
    )
df_3 = pd.read_csv(
        os.path.join(
        "input_data",
        "screen_sequences",
        "p3_sequences.csv")
    )

scores_1 = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "single_domain_screen_scored_with_means.csv"
    )
)
scores_2 = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "bipartite_screen_scored_with_means.csv"
    )
)
scores_3 = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "tripartite_screen_scored_with_means.csv"
    )
)

tox_1 = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "single_domain_toxicity.csv"
    )
)

tox_2 = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "bipartite_screen_toxicity.csv"
    )
)

tox_3 = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "tripartite_screen_toxicity.csv"
    )
)


if not os.path.exists(os.path.join("output","screen_analysis","biochem_analysis")):
    os.mkdir(os.path.join("output","screen_analysis","biochem_analysis"))


from progress.bar import Bar
bar = Bar("Charachterizing...",max=len(df_1)+len(df_2)+len(df_3),suffix='%(index)i / %(max)i - %(eta)ds')

for i in range(len(df_1)):
    for col in ['EPCAM_average','CXCR4_average','Reporter_average']:
        df_1.at[i,col]=scores_1.at[i,col]
    sequence = df_1.at[i,"AA sequence"]
    df_1.at[i,'CX&EP Average Tox'] = tox_1.at[i,'CX&EP Average Tox']
    df_1.at[i,"NCPR"]=bc.getNCPR(sequence)
    df_1.at[i,"Hydropathy"]=bc.getHydropathy(sequence)
    df_1.at[i,"Disorder promoting fraction"]=bc.getDisorderFraction(sequence)
    df_1.at[i,"Kappa"]=bc.getKappa(sequence)
    df_1.at[i,"Omega"]=bc.getOmega(sequence)
    bar.next()

df_1.to_csv(
        os.path.join(
        "output",
        "screen_analysis",
        "biochem_analysis",
        "single_domain_screen_biochem_charachterized.csv")
    )


for i in range(len(df_2)):
    for col in ['EPCAM_average','CXCR4_average','Reporter_average']:
        df_2.at[i,col]=scores_2.at[i,col]
    sequence = df_2.at[i,"AA sequence"]
    df_2.at[i,'CX&EP Average Tox'] = tox_2.at[i,'CX&EP Average Tox']
    df_2.at[i,"NCPR"]=bc.getNCPR(sequence)
    df_2.at[i,"Hydropathy"]=bc.getHydropathy(sequence)
    df_2.at[i,"Disorder promoting fraction"]=bc.getDisorderFraction(sequence)
    df_2.at[i,"Kappa"]=bc.getKappa(sequence)
    df_2.at[i,"Omega"]=bc.getOmega(sequence)
    bar.next()

df_2.to_csv(
        os.path.join(
        "output",
        "screen_analysis",
        "biochem_analysis",
        "bipartite_screen_biochem_charachterized.csv")
    )


for i in range(len(df_3)):
    for col in ['EPCAM_average','CXCR4_average','Reporter_average','Has EPCAM score', 'Has CXCR4 score', 'Has Reporter score', 'Has all scores']:
        df_3.at[i,col]=scores_3.at[i,col]
    sequence = df_3.at[i,"AA sequence"]
    df_3.at[i,'CX&EP Average Tox'] = tox_3.at[i,'CX&EP Average Tox']

    df_3.at[i,"NCPR"]=bc.getNCPR(sequence)
    df_3.at[i,"Hydropathy"]=bc.getHydropathy(sequence)
    df_3.at[i,"Disorder promoting fraction"]=bc.getDisorderFraction(sequence)
    df_3.at[i,"Kappa"]=bc.getKappa(sequence)
    df_3.at[i,"Omega"]=bc.getOmega(sequence)
    bar.next()

df_3.to_csv(
        os.path.join(
        "output",
        "screen_analysis",
        "biochem_analysis",
        "tripartite_screen_biochem_charachterized.csv")
    )