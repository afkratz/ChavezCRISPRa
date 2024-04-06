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

    single_domain_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "screen_results",
            "screen_scores",
            "single_domain_screen_scored.csv",
        ))
    single_domain_activity_df['Construct'] = single_domain_activity_df['BC1']
    
    bipartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "screen_results",
            "screen_scores",
            "bipartite_screen_scored.csv",
        ))
    bipartite_activity_df['Construct'] = bipartite_activity_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    tripartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "screen_results",
            "screen_scores",
            "tripartite_screen_scored.csv",
        ))
    tripartite_activity_df['Construct'] = tripartite_activity_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    for target in ['EPCAM','CXCR4','Reporter']:
        tripartite_activity_df['{}_average'.format(target)] = tripartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
        bipartite_activity_df['{}_average'.format(target)] = bipartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
        single_domain_activity_df['{}_average'.format(target)] = single_domain_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)

    left_part = pd.concat((
        pd.DataFrame({
            "Construct":single_domain_activity_df['Construct'],
            'Activator type':'Single-domain',
            'P1':single_domain_activity_df['BC1'],
            'P2':'',
            'P3':'',
            'EPCAM_average':single_domain_activity_df['EPCAM_average'],
            'CXCR4_average':single_domain_activity_df['CXCR4_average'],
            'Reporter_average':single_domain_activity_df['Reporter_average'],
        }),
        pd.DataFrame({
            "Construct":bipartite_activity_df['Construct'],
            'Activator type':'Bipartite',
            'P1':bipartite_activity_df['BC1'],
            'P2':bipartite_activity_df['BC2'],
            'P3':'',
            'EPCAM_average':bipartite_activity_df['EPCAM_average'],
            'CXCR4_average':bipartite_activity_df['CXCR4_average'],
            'Reporter_average':bipartite_activity_df['Reporter_average'],
        }),
        pd.DataFrame({
            "Construct":tripartite_activity_df['Construct'],
            'Activator type':'Tripartite',
            'P1':tripartite_activity_df['BC1'],
            'P2':tripartite_activity_df['BC2'],
            'P3':tripartite_activity_df['BC3'],
            'EPCAM_average':tripartite_activity_df['EPCAM_average'],
            'CXCR4_average':tripartite_activity_df['CXCR4_average'],
            'Reporter_average':tripartite_activity_df['Reporter_average'],
        })
    )).reset_index(drop=True)
    left_part['']=''#buffer col

    bipartite_medians = pd.DataFrame()
    for ad in ads:
        subdf = bipartite_activity_df[bipartite_activity_df['BC1']==ad]
        bipartite_medians.at[ad,'Median EPCAM P1']=np.median(subdf['EPCAM_average'])
        bipartite_medians.at[ad,'Median CXCR4 P1']=np.median(subdf['CXCR4_average'])
        bipartite_medians.at[ad,'Median Reporter P1']=np.median(subdf['Reporter_average'])

        subdf = bipartite_activity_df[bipartite_activity_df['BC2']==ad]
        bipartite_medians.at[ad,'Median EPCAM P2']=np.median(subdf['EPCAM_average'])
        bipartite_medians.at[ad,'Median CXCR4 P2']=np.median(subdf['CXCR4_average'])
        bipartite_medians.at[ad,'Median Reporter P2']=np.median(subdf['Reporter_average'])
        
    tripartite_medians = pd.DataFrame()
    for ad in ads:
        subdf = tripartite_activity_df[tripartite_activity_df['BC1']==ad]
        tripartite_medians.at[ad,'Median EPCAM P1']=subdf['EPCAM_average'].median()
        tripartite_medians.at[ad,'Median CXCR4 P1']=subdf['CXCR4_average'].median()
        tripartite_medians.at[ad,'Median Reporter P1']=subdf['Reporter_average'].median()
        
        subdf = tripartite_activity_df[tripartite_activity_df['BC2']==ad]
        tripartite_medians.at[ad,'Median EPCAM P2']=subdf['EPCAM_average'].median()
        tripartite_medians.at[ad,'Median CXCR4 P2']=subdf['CXCR4_average'].median()
        tripartite_medians.at[ad,'Median Reporter P2']=subdf['Reporter_average'].median()
        
        subdf = tripartite_activity_df[tripartite_activity_df['BC3']==ad]
        tripartite_medians.at[ad,'Median EPCAM P3']=subdf['EPCAM_average'].median()
        tripartite_medians.at[ad,'Median CXCR4 P3']=subdf['CXCR4_average'].median()
        tripartite_medians.at[ad,'Median Reporter P3']=subdf['Reporter_average'].median()

    bipartite_medians.reset_index(inplace=True)
    bipartite_medians.rename(columns={'index':'Bipartite AD'},inplace=True)

    bipartite_medians['']=''#buffer col    

    tripartite_medians.reset_index(inplace=True)
    tripartite_medians.rename(columns={'index':'Tripartite AD'},inplace=True)

    res = pd.concat((
        left_part,
        bipartite_medians,
        tripartite_medians.replace(np.nan,'NA'),

    ),axis=1)
    
    return res

    

if __name__=="__main__":
    main()