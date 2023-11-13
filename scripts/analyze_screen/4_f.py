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


construct_to_tox = dict()
for i in bipartite_tox_df.index:
    bc1 = bipartite_tox_df.at[i,'BC1']
    bc2 = bipartite_tox_df.at[i,'BC2']
    construct = bc1+"_"+bc2
    toxicity = bipartite_tox_df.at[i,'CX&EP Average Tox']
    construct_to_tox[construct] = toxicity

for i in tripartite_tox_df.index:
    bc1 = tripartite_tox_df.at[i,'BC1']
    bc2 = tripartite_tox_df.at[i,'BC2']
    bc3 = tripartite_tox_df.at[i,'BC3']

    construct = bc1+"_"+bc2+"_"+bc3
    toxicity = tripartite_tox_df.at[i,'CX&EP Average Tox']
    construct_to_tox[construct] = toxicity


all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
activator_barcodes = all_barcodes[:22]
pfd_barcodes = ['A23','A25']
odf = pd.DataFrame()
odf['AD']=""
for i,activator_barcode in enumerate(activator_barcodes):
    odf.at[i,'AD']=activator_barcode
    odf.at[i,'AD - PFD tox']=np.median((
        construct_to_tox[activator_barcode+"_A23"],
        construct_to_tox[activator_barcode+"_A25"],
        construct_to_tox["A23_"+activator_barcode],
        construct_to_tox["A25_"+activator_barcode],
    ))
    odf.at[i,'AD-AD tox']=construct_to_tox[activator_barcode+"_"+activator_barcode]
odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4f - bipartite two copy vs median with pfd.csv"
    ),index=False
)

odf = pd.DataFrame()
activator_copy_number_to_tox = dict()
for i in tripartite_tox_df.index:
    bc1 = tripartite_tox_df.at[i,'BC1']
    bc2 = tripartite_tox_df.at[i,'BC2']
    bc3 = tripartite_tox_df.at[i,'BC3']
    barcodes = tuple((bc1,bc2,bc3))
    if 'A24' in barcodes:continue
    pfd_count = barcodes.count('A23')+barcodes.count('A25')

    #This set will contain the activators that are present, other than the protein folding domains
    present_activators = set(barcodes) - set(('A23','A25'))
    if (len(present_activators))==1:
        activator = present_activators.pop()#get the activator out
        activator_copy_number = barcodes.count(activator)#count how many occurances
        
        #sanity check
        assert (activator_copy_number + pfd_count )==3

        copy_number_key = (activator,activator_copy_number)

        if copy_number_key not in activator_copy_number_to_tox:
            activator_copy_number_to_tox[copy_number_key]=[]
        activator_copy_number_to_tox[copy_number_key].append(tripartite_tox_df.at[i,'CX&EP Average Tox'])

for ad in activator_barcodes:
    for copy_number in (1,2,3):
        odf.at[ad,str(copy_number)+" copy tox"] = np.median(activator_copy_number_to_tox[(ad,copy_number)])
    
odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig4",
        "4f - tripartite activator copy number toxicity.csv"
    )
)