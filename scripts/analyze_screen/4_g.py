# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import pandas as pd

os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

single_domain_tox_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "single_domain_toxicity.csv"
    )
)

bipartite_tox_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "bipartite_screen_toxicity.csv"
    )
)

tripartite_tox_df = pd.read_csv(
    os.path.join(
        "output",
        "screen_results",
        "screen_toxicity",
        "tripartite_screen_toxicity.csv"
    )
)

all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

#Assemble Single domain toxicities into a dictionary of toxicities
single_domain_to_tox = dict()
for i in single_domain_tox_df.index:
    activator = single_domain_tox_df.at[i,'BC1']
    toxicity = single_domain_tox_df.at[i,'CX&EP Average Tox']
    single_domain_to_tox[activator]=toxicity

#Assemble Bipartite toxicities into a dictionary of lists of toxicities
bc_to_bipartite_toxicities = dict()
for bc in all_barcodes:
    bc_to_bipartite_toxicities[bc]=[]#List to store toxicities

for i in bipartite_tox_df.index:
    bc1 = bipartite_tox_df.at[i,'BC1']
    bc2 = bipartite_tox_df.at[i,'BC2']
    toxicity = bipartite_tox_df.at[i,'CX&EP Average Tox']
    for bc in (bc1,bc2):
        bc_to_bipartite_toxicities[bc].append(toxicity)

#Assemble Tripartite toxicities into a dictionary of lists of toxicities
bc_to_tripartite_toxicities = dict()
for bc in all_barcodes:
    bc_to_tripartite_toxicities[bc]=[]#List to store toxicities

for i in tripartite_tox_df.index:
    bc1 = tripartite_tox_df.at[i,'BC1']
    bc2 = tripartite_tox_df.at[i,'BC2']
    bc3 = tripartite_tox_df.at[i,'BC3']
    toxicity = tripartite_tox_df.at[i,'CX&EP Average Tox']
    for bc in (bc1,bc2,bc3):
        bc_to_tripartite_toxicities[bc].append(toxicity)

odf = pd.DataFrame()
odf['Activator']=""
odf['Single domain toxicity']=0
odf['Bipartite median toxicity']=0
odf['Tripartite median toxicity']=0

for i,bc in enumerate(all_barcodes):
    odf.at[i,'Activator']=bc
    odf.at[i,'Single domain toxicity']=single_domain_to_tox[bc]
    odf.at[i,'Bipartite median toxicity']=np.median(bc_to_bipartite_toxicities[bc])    
    odf.at[i,'Tripartite median toxicity']=np.median(bc_to_tripartite_toxicities[bc])

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4g - single domain vs multidomain median toxicity.csv"
    ),index=False
)