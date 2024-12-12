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

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    minilib_tox_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_toxicity',
            'minilib_toxicity.csv'
        )
    )
    minilib_tox_df['Construct'] = minilib_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'], row['BC3']), axis=1)
    minilib_tox_df = minilib_tox_df[minilib_tox_df['In_Minilib']]
    
    res = pd.DataFrame(
        {
            'Mini–library member':minilib_tox_df['Construct'],
            'HEK293T toxicity':minilib_tox_df['HEK_av_tox'],
            'HeLa toxicity':minilib_tox_df['HeLa_av_tox'],
            'N2A toxicity':minilib_tox_df['N2A_av_tox'],

        }
    )

    return res

if __name__=="__main__":
    main()