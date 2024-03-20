# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import numpy as np
import pandas as pd
import os
from pathlib import Path


def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    ad_bcs = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,23)))

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,P2 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    res = pd.DataFrame({
        "Construct":bipartite_tox_df['Construct'],
        'Type':'Bipartite',
        'EPCAM':bipartite_tox_df['EPCAM_Tox'],
        'CXCR4':bipartite_tox_df['CXCR4_Tox'],
        'Reporter':bipartite_tox_df['Reporter_Tox'],
        'EPCAM and CXCR4 average':bipartite_tox_df['CX&EP Average Tox'],
    }).sort_values(by='EPCAM and CXCR4 average',ascending=False)

    return res

        


    

if __name__=="__main__":
    main()