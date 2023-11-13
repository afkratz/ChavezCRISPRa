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


if not os.path.exists(os.path.join("output","figures")):
    os.mkdir(os.path.join("output","figures"))

if not os.path.exists(os.path.join("output","figures","fig3")):
    os.mkdir(os.path.join("output","figures","fig3"))

p1_screen_scores = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_single_domain_screen_scored.csv"
    )
)

p2_screen_scores = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_bipartite_screen_scored.csv"
    )
)

p3_screen_scores = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_tripartite_screen_scored.csv"
    )
)


p1_manual_scores = pd.read_csv(
    os.path.join(
        "input_data",
        "screen_validation",
        "single_domain_manual_validation.csv"
    )
)

p2_manual_scores = pd.read_csv(
    os.path.join(
        "input_data",
        "screen_validation",
        "bipartite_manual_validation.csv"
    )
)

p3_manual_scores = pd.read_csv(
    os.path.join(
        "input_data",
        "screen_validation",
        "tripartite_manual_validation.csv"
    )
)

#Combine screen and manual validation results
odf = pd.DataFrame()
odf['Construct']=""
for i in p1_manual_scores.index:
    construct = p1_manual_scores.at[i,'Construct']
    odf.at[construct,'Construct']=construct
    for column in ['Mean EPCAM_1','Mean CXCR4_1']:
        odf.at[construct,'Manual validation '+column]=p1_manual_scores.at[i,column]

for i in p1_screen_scores.index:
    bc1 = p1_screen_scores.at[i,'BC1']
    construct = bc1
    for column in ['EPCAM_1', 'EPCAM_2', 'CXCR4_1', 'CXCR4_2', 'Reporter_1','Reporter_2', 'EPCAM_average', 'CXCR4_average', 'Reporter_average']:
        odf.at[construct,"Screen "+column] = p1_screen_scores.at[i,column]


odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig3",
        "3e - Single domain screen vs manual validation.csv"
    ),index=False
)

#Combine bipartite screen and manual validation results
odf = pd.DataFrame()
odf['Construct']=""
for i in p2_manual_scores.index:
    construct = p2_manual_scores.at[i,'Construct']
    odf.at[construct,'Construct']=construct
    for column in [
        'Mean EPCAM_1','Mean EPCAM_2','Mean EPCAM_average',
        'Mean CXCR4_1','Mean CXCR4_2','Mean CXCR4_average',
        'Mean Reporter of iRFP+_1','Mean Reporter of iRFP+_2','Mean Reporter of iRFP+_average']:
        odf.at[construct,'Manual validation '+column]=p2_manual_scores.at[i,column]
for i in p2_screen_scores.index:
    bc1 = p2_screen_scores.at[i,'BC1']
    bc2 = p2_screen_scores.at[i,'BC2']
    
    construct = bc1+"_"+bc2
    if construct not in odf.index:
        continue

    for column in ['EPCAM_1', 'EPCAM_2', 'CXCR4_1', 'CXCR4_2', 'Reporter_1','Reporter_2', 'EPCAM_average', 'CXCR4_average', 'Reporter_average']:
        odf.at[construct,"Screen "+column] = p2_screen_scores.at[i,column]

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig3",
        "3e - Bipartite screen vs manual validation.csv"
    ),index=False
)


#Combine tripartite screen and manual validation results
odf = pd.DataFrame()
odf['Construct']=""
for i in p3_manual_scores.index:
    construct = p3_manual_scores.at[i,'Construct']
    odf.at[construct,'Construct']=construct
    for column in [
        'Mean EPCAM_1','Mean EPCAM_2','Mean EPCAM_average',
        'Mean CXCR4_1','Mean CXCR4_2','Mean CXCR4_average',
        'Mean Reporter of iRFP+_1','Mean Reporter of iRFP+_2','Mean Reporter of iRFP+_average']:
        odf.at[construct,'Manual validation '+column]=p3_manual_scores.at[i,column]
        
for i in p3_screen_scores.index:
    bc1 = p3_screen_scores.at[i,'BC1']
    bc2 = p3_screen_scores.at[i,'BC2']
    bc3 = p3_screen_scores.at[i,'BC3']
    
    construct = bc1+"_"+bc2+"_"+bc3
    if construct not in odf.index:
        continue

    for column in ['EPCAM_1', 'EPCAM_2', 'CXCR4_1', 'CXCR4_2', 'Reporter_1','Reporter_2', 'EPCAM_average', 'CXCR4_average', 'Reporter_average']:
        odf.at[construct,"Screen "+column] = p3_screen_scores.at[i,column]

odf.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig3",
        "3e - Tripartite screen vs manual validation.csv"
    ),index=False
)
