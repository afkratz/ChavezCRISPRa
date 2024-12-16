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
    all_bcs = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    ads = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,23)))
    pfds = ['A23','A25']

   
    bipartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "bipartite_screen_scored.csv",
        )
    )
    bipartite_activity_df['Construct'] = bipartite_activity_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    for target in ['EPCAM','CXCR4','Reporter']:
        bipartite_activity_df['{}_average'.format(target)] = bipartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)

    with_ad = pd.DataFrame()
    with_pfd = pd.DataFrame()

    for i in bipartite_activity_df.index:
        bc1 = bipartite_activity_df.at[i,'BC1']
        bc2 = bipartite_activity_df.at[i,'BC2']
        score = bipartite_activity_df.at[i,'EPCAM_average']
        if bc1 in ads and bc2 in ads:
            with_ad.at['{}_in_p1'.format(bc1),bc2]=score
            with_ad.at['{}_in_p2'.format(bc2),bc1]=score
        
        if bc1 in ads and bc2 in pfds:
             with_pfd.at['{}_in_p2'.format(bc2),bc1]=score
        
        if bc2 in ads and bc1 in pfds:
            with_pfd.at['{}_in_p1'.format(bc1),bc2]=score
        

    ad_col_to_median = dict()
    for c in with_ad.columns:
        ad_col_to_median[c]=np.median(with_ad[c].values)
    with_ad.loc['Median']=ad_col_to_median

    pfd_col_to_median = dict()
    for c in with_pfd.columns:
        pfd_col_to_median[c]=np.median(with_pfd[c].values)
    with_pfd.loc['Median']=pfd_col_to_median
    
    
    with_ad.reset_index(inplace=True)
    with_ad.rename(columns={'index':'With ADs'},inplace=True)
    with_pfd.reset_index(inplace=True)
    with_pfd.rename(columns={'index':'With PFDs'},inplace=True)
    
    with_ad['']=''#buffer col
    with_pfd['']=''#buffer col

    median_df = pd.DataFrame()
    transposed = pd.DataFrame()


    for bc in ads:
        median_df.at['Median with PF',bc]=pfd_col_to_median[bc]
        median_df.at['Median with AD',bc]=ad_col_to_median[bc]
        median_df.at['Median gain from PF to AD',bc] = ad_col_to_median[bc]/pfd_col_to_median[bc]

        transposed.at[bc,'Median with PF'] = median_df.at['Median with PF',bc]
        transposed.at[bc,'Median gain from PF to AD'] = median_df.at['Median gain from PF to AD',bc]
    
    median_df.reset_index(inplace=True)
    median_df['']=''
    transposed.reset_index(inplace=True)


    res = pd.concat((
        with_ad,
        with_pfd,
        median_df,
        transposed

    ),axis=1)
    return res

    

if __name__=="__main__":
    main()