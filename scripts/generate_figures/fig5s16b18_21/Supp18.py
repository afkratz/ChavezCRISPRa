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

    bc_to_single_domain_score=dict()
    for i in single_domain_activity_df.index:
        bc = single_domain_activity_df.at[i,'BC1']
        bc_to_single_domain_score[bc]=dict()
        bc_to_single_domain_score[bc]['EPCAM']=single_domain_activity_df.at[i,'EPCAM_average']
        bc_to_single_domain_score[bc]['CXCR4']=single_domain_activity_df.at[i,'CXCR4_average']
        bc_to_single_domain_score[bc]['Reporter']=single_domain_activity_df.at[i,'Reporter_average']
    for i in bipartite_activity_df.index:
        for target in ['EPCAM','CXCR4','Reporter']:
            bipartite_activity_df.at[i,'Single-domain P1 {}_average'.format(target)] =\
                  bc_to_single_domain_score[bipartite_activity_df.at[i,'BC1']][target]
            
            bipartite_activity_df.at[i,'Single-domain P2 {}_average'.format(target)] =\
                  bc_to_single_domain_score[bipartite_activity_df.at[i,'BC2']][target]
            
            bipartite_activity_df.at[i,'Single-domain P3 {}_average'.format(target)] = ""
    for i in tripartite_activity_df.index:
        for target in ['EPCAM','CXCR4','Reporter']:
            tripartite_activity_df.at[i,'Single-domain P1 {}_average'.format(target)] =\
                  bc_to_single_domain_score[tripartite_activity_df.at[i,'BC1']][target]
            
            tripartite_activity_df.at[i,'Single-domain P2 {}_average'.format(target)] =\
                  bc_to_single_domain_score[tripartite_activity_df.at[i,'BC2']][target]
            
            tripartite_activity_df.at[i,'Single-domain P3 {}_average'.format(target)] =\
                  bc_to_single_domain_score[tripartite_activity_df.at[i,'BC3']][target]
        
    for target in ['EPCAM','CXCR4','Reporter']:
        bipartite_activity_df['Single-domain {}_average sum'.format(target)]=\
        bipartite_activity_df[['Single-domain P1 {}_average'.format(target),
                               'Single-domain P2 {}_average'.format(target)]].values.sum(axis=1)
        
        tripartite_activity_df['Single-domain {}_average sum'.format(target)]=\
        tripartite_activity_df[['Single-domain P1 {}_average'.format(target),
                               'Single-domain P2 {}_average'.format(target),
                               'Single-domain P3 {}_average'.format(target)
                               ]].values.sum(axis=1)
        
    


    res = pd.concat((
        pd.DataFrame({
            "Construct":bipartite_activity_df['Construct'],
            'Activator type':'Bipartite',
            'P1':bipartite_activity_df['BC1'],
            'P2':bipartite_activity_df['BC2'],
            'P3':'',
            'Single-domain P1 EPCAM_average':bipartite_activity_df['Single-domain P1 EPCAM_average'],
            'Single-domain P2 EPCAM_average':bipartite_activity_df['Single-domain P2 EPCAM_average'],
            'Single-domain P3 EPCAM_average':bipartite_activity_df['Single-domain P3 EPCAM_average'],
            'Single-domain EPCAM_average sum':bipartite_activity_df['Single-domain EPCAM_average sum'],

            'Single-domain P1 CXCR4_average':bipartite_activity_df['Single-domain P1 CXCR4_average'],
            'Single-domain P2 CXCR4_average':bipartite_activity_df['Single-domain P2 CXCR4_average'],
            'Single-domain P3 CXCR4_average':bipartite_activity_df['Single-domain P3 CXCR4_average'],
            'Single-domain CXCR4_average sum':bipartite_activity_df['Single-domain CXCR4_average sum'],

            'Single-domain P1 Reporter_average':bipartite_activity_df['Single-domain P1 Reporter_average'],
            'Single-domain P2 Reporter_average':bipartite_activity_df['Single-domain P2 Reporter_average'],
            'Single-domain P3 Reporter_average':bipartite_activity_df['Single-domain P3 Reporter_average'],
            'Single-domain Reporter_average sum':bipartite_activity_df['Single-domain Reporter_average sum'],

            'Multi-partite EPCAM_average':bipartite_activity_df['EPCAM_average'],
            'Multi-partite CXCR4_average':bipartite_activity_df['CXCR4_average'],
            'Multi-partite Reporter_average':bipartite_activity_df['Reporter_average'],
        }),
        pd.DataFrame({
            "Construct":tripartite_activity_df['Construct'],
            'Activator type':'Tripartite',
            'P1':tripartite_activity_df['BC1'],
            'P2':tripartite_activity_df['BC2'],
            'P3':tripartite_activity_df['BC3'],
            'Single-domain P1 EPCAM_average':tripartite_activity_df['Single-domain P1 EPCAM_average'],
            'Single-domain P2 EPCAM_average':tripartite_activity_df['Single-domain P2 EPCAM_average'],
            'Single-domain P3 EPCAM_average':tripartite_activity_df['Single-domain P3 EPCAM_average'],
            'Single-domain EPCAM_average sum':tripartite_activity_df['Single-domain EPCAM_average sum'],

            'Single-domain P1 CXCR4_average':tripartite_activity_df['Single-domain P1 CXCR4_average'],
            'Single-domain P2 CXCR4_average':tripartite_activity_df['Single-domain P2 CXCR4_average'],
            'Single-domain P3 CXCR4_average':tripartite_activity_df['Single-domain P3 CXCR4_average'],
            'Single-domain CXCR4_average sum':tripartite_activity_df['Single-domain CXCR4_average sum'],

            'Single-domain P1 Reporter_average':tripartite_activity_df['Single-domain P1 Reporter_average'],
            'Single-domain P2 Reporter_average':tripartite_activity_df['Single-domain P2 Reporter_average'],
            'Single-domain P3 Reporter_average':tripartite_activity_df['Single-domain P3 Reporter_average'],
            'Single-domain Reporter_average sum':tripartite_activity_df['Single-domain Reporter_average sum'],

            'Multi-partite EPCAM_average':tripartite_activity_df['EPCAM_average'],
            'Multi-partite CXCR4_average':tripartite_activity_df['CXCR4_average'],
            'Multi-partite Reporter_average':tripartite_activity_df['Reporter_average'],
        }),
    )).replace(np.nan,'NA')


    
    return res

    

if __name__=="__main__":
    main()