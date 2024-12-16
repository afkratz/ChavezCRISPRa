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

    single_domain_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "single_domain_screen_scored.csv",
        )
    )
    single_domain_activity_df['Construct'] = single_domain_activity_df['BC1']
    
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

    tripartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "tripartite_screen_scored.csv",
        )
    )
    tripartite_activity_df['Construct'] = tripartite_activity_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    for target in ['EPCAM','CXCR4','Reporter']:
        tripartite_activity_df['{}_average'.format(target)] = tripartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
        bipartite_activity_df['{}_average'.format(target)] = bipartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
        single_domain_activity_df['{}_average'.format(target)] = single_domain_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)

    

    left_part = pd.concat((
        pd.DataFrame({
            'Construct':single_domain_activity_df['Construct'],
            'Activator type':'Single-domain',
            'P1':single_domain_activity_df['BC1'],
            'P2':'',
            'P3':'',
            'EPCAM average':single_domain_activity_df['EPCAM_average'],
            'CXCR4 average':single_domain_activity_df['CXCR4_average'],
            'Reporter average':single_domain_activity_df['Reporter_average'],
            "":"",#buffer
        }),
        pd.DataFrame({
            'Construct':bipartite_activity_df['Construct'],
            'Activator type':'Bipartite',
            'P1':bipartite_activity_df['BC1'],
            'P2':bipartite_activity_df['BC2'],
            'P3':'',
            'EPCAM average':bipartite_activity_df['EPCAM_average'],
            'CXCR4 average':bipartite_activity_df['CXCR4_average'],
            'Reporter average':bipartite_activity_df['Reporter_average'],
            "":"",#buffer
        }),
        pd.DataFrame({
            'Construct':tripartite_activity_df['Construct'],
            'Activator type':'Tripartite',
            'P1':tripartite_activity_df['BC1'],
            'P2':tripartite_activity_df['BC2'],
            'P3':tripartite_activity_df['BC3'],
            'EPCAM average':tripartite_activity_df['EPCAM_average'],
            'CXCR4 average':tripartite_activity_df['CXCR4_average'],
            'Reporter average':tripartite_activity_df['Reporter_average'],
            "":"",#buffer
        })
    ),ignore_index=True)


    right_part = pd.DataFrame()
    
        
    for target in ['EPCAM','CXCR4','Reporter']:
        ad_to_score = dict()
        for i in single_domain_activity_df.index:
            score = single_domain_activity_df.at[i,'{}_average'.format(target)]

            bc1 = single_domain_activity_df.at[i,'BC1']    
            if bc1 not in ad_to_score:
                ad_to_score[bc1]=list()
            ad_to_score[bc1].append(score)

        for i,bc in enumerate(all_bcs):
            right_part.at[i,'AD']=bc
            right_part.at[i,'Single-domain median {}'.format(target)]=np.median(ad_to_score[bc])

    for target in ['EPCAM','CXCR4','Reporter']:
        ad_to_score = dict()
        for i in bipartite_activity_df.index:
            score = bipartite_activity_df.at[i,'{}_average'.format(target)]
            bc1 = bipartite_activity_df.at[i,'BC1']    
            if bc1 not in ad_to_score:
                ad_to_score[bc1]=list()
            ad_to_score[bc1].append(score)

            bc2 = bipartite_activity_df.at[i,'BC2']    
            if bc2 not in ad_to_score:
                ad_to_score[bc2]=list()
            ad_to_score[bc2].append(score)

        for i,bc in enumerate(all_bcs):
            right_part.at[i,'Bipartite median {}'.format(target)]=np.median(ad_to_score[bc])
    
    for target in ['EPCAM','CXCR4','Reporter']:
        ad_to_score = dict()
        for i in tripartite_activity_df.index:
            score = tripartite_activity_df.at[i,'{}_average'.format(target)]
            if not np.isnan(score):
                bc1 = tripartite_activity_df.at[i,'BC1']    
                if bc1 not in ad_to_score:
                    ad_to_score[bc1]=list()
                ad_to_score[bc1].append(score)

                bc2 = tripartite_activity_df.at[i,'BC2']    
                if bc2 not in ad_to_score:
                    ad_to_score[bc2]=list()
                
                ad_to_score[bc2].append(score)

                bc3 = tripartite_activity_df.at[i,'BC3']    
                if bc3 not in ad_to_score:
                    ad_to_score[bc3]=list()
                ad_to_score[bc3].append(score)

        for i,bc in enumerate(all_bcs):
            right_part.at[i,'Tripartite median {}'.format(target)]=np.median(ad_to_score[bc])
    
    left_part[['EPCAM average','CXCR4 average','Reporter average']] = left_part[['EPCAM average','CXCR4 average','Reporter average']].replace(np.nan,"NA")


    res = pd.concat((
        left_part,
        right_part
    ),axis=1)
    return res

    

if __name__=="__main__":
    main()