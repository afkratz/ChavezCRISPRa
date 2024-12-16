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
            "screen_output",
            "screen_results",
            "screen_scores",
            "single_domain_screen_scored.csv",
        ))
    single_domain_activity_df['Construct'] = single_domain_activity_df['BC1']
    
    bipartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "bipartite_screen_scored.csv",
        ))
    bipartite_activity_df['Construct'] = bipartite_activity_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    tripartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "tripartite_screen_scored.csv",
        ))
    tripartite_activity_df['Construct'] = tripartite_activity_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)

    for target in ['EPCAM','CXCR4','Reporter']:
        tripartite_activity_df['{}_average'.format(target)] = tripartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
        bipartite_activity_df['{}_average'.format(target)] = bipartite_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
        single_domain_activity_df['{}_average'.format(target)] = single_domain_activity_df[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)

    for i in single_domain_activity_df.index:
        single_domain_activity_df.at[i,'1 AD copy']=True
        single_domain_activity_df.at[i,'2 AD copy']=False
        single_domain_activity_df.at[i,'3 AD copy']=False
    for i in bipartite_activity_df.index:
        bc1 = bipartite_activity_df.at[i,'BC1']
        bc2 = bipartite_activity_df.at[i,'BC2']
        bipartite_activity_df.at[i,'1 AD copy'] = (bc1 in pfds and bc2 in ads) or (bc2 in pfds and bc1 in ads)
        bipartite_activity_df.at[i,'2 AD copy'] = (bc1==bc2 and bc1 in ads)
        bipartite_activity_df.at[i,'3 AD copy'] = False
    for i in tripartite_activity_df.index:
        bc1 = tripartite_activity_df.at[i,'BC1']
        bc2 = tripartite_activity_df.at[i,'BC2']
        bc3 = tripartite_activity_df.at[i,'BC3']
        pfd_count = int(bc1 in pfds) + int(bc2 in pfds) + int(bc3 in pfds)
        ad_count = int(bc1 in ads) + int(bc2 in ads) + int(bc3 in ads)
        tripartite_activity_df.at[i,'1 AD copy'] = (ad_count==1 and pfd_count==2)
        tripartite_activity_df.at[i,'2 AD copy'] = (ad_count==2 and pfd_count==1 and len(set((bc1,bc2,bc3)))==2)
        tripartite_activity_df.at[i,'3 AD copy'] = (bc1==bc2 and bc2==bc3 and bc1 in ads)


    
    
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
            '1 AD copy':single_domain_activity_df['1 AD copy'],
            '2 AD copy':single_domain_activity_df['2 AD copy'],
            '3 AD copy':single_domain_activity_df['3 AD copy'],
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
            '1 AD copy':bipartite_activity_df['1 AD copy'],
            '2 AD copy':bipartite_activity_df['2 AD copy'],
            '3 AD copy':bipartite_activity_df['3 AD copy'],
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
            '1 AD copy':tripartite_activity_df['1 AD copy'],
            '2 AD copy':tripartite_activity_df['2 AD copy'],
            '3 AD copy':tripartite_activity_df['3 AD copy'],
            "":"",#buffer
        })
    ),ignore_index=True)

    bipartite_medians = pd.DataFrame()
    for target in ['EPCAM','CXCR4','Reporter']:
        single_copy_scores = dict()
        two_copy_scores = dict()
        for i in bipartite_activity_df.index:
            bc1 = bipartite_activity_df.at[i,'BC1']
            bc2 = bipartite_activity_df.at[i,'BC2']
            score = bipartite_activity_df.at[i,'{}_average'.format(target)]
            if bipartite_activity_df.at[i,'1 AD copy']:
                if bc1 in ads:
                    if bc1 not in single_copy_scores:
                        single_copy_scores[bc1]=[]
                    single_copy_scores[bc1].append(score)
                if bc2 in ads:
                    if bc2 not in single_copy_scores:
                        single_copy_scores[bc2]=[]
                    single_copy_scores[bc2].append(score)
            if bipartite_activity_df.at[i,'2 AD copy']:
                assert bc1==bc2
                two_copy_scores[bc1]=score

        for i,ad in enumerate(ads):
            scores = single_copy_scores[ad]
            assert len(scores)==4 #Axx_A23, Axx_A25, A23_Axx, A25_Axx
            bipartite_medians.at[i,'Bipartite AD'] = ad
            bipartite_medians.at[i,'1 copy median {} screen score'.format(target)] = np.median(scores)

        for i,ad in enumerate(ads):
            score = two_copy_scores[ad]
            bipartite_medians.at[i,'2 copies median {} screen score'.format(target)] = score
    bipartite_medians['']=''#buffer

    tripartite_medians = pd.DataFrame()
    for target in ['EPCAM','CXCR4','Reporter']:
        single_copy_scores = dict()
        two_copy_scores = dict()
        three_copy_scores = dict()
        for i in tripartite_activity_df.index:
            bc1 = tripartite_activity_df.at[i,'BC1']
            bc2 = tripartite_activity_df.at[i,'BC2']
            bc3 = tripartite_activity_df.at[i,'BC3']
            score = tripartite_activity_df.at[i,'{}_average'.format(target)]
            if np.isnan(score):continue
            if tripartite_activity_df.at[i,'1 AD copy']:
                if bc1 in ads:
                    if bc1 not in single_copy_scores:
                        single_copy_scores[bc1]=[]
                    single_copy_scores[bc1].append(score)
                if bc2 in ads:
                    if bc2 not in single_copy_scores:
                        single_copy_scores[bc2]=[]
                    single_copy_scores[bc2].append(score)
                if bc3 in ads:
                    if bc3 not in single_copy_scores:
                        single_copy_scores[bc3]=[]
                    single_copy_scores[bc3].append(score)
            
            if tripartite_activity_df.at[i,'2 AD copy']:
                if bc1 in ads:
                    if bc1 not in two_copy_scores:
                        two_copy_scores[bc1]=[]
                    two_copy_scores[bc1].append(score)
                if bc2 in ads:
                    if bc2 not in two_copy_scores:
                        two_copy_scores[bc2]=[]
                    two_copy_scores[bc2].append(score)
                if bc3 in ads:
                    if bc3 not in two_copy_scores:
                        two_copy_scores[bc3]=[]
                    two_copy_scores[bc3].append(score)

            if tripartite_activity_df.at[i,'3 AD copy']:
                if bc1 in ads:
                    if bc1 not in three_copy_scores:
                        three_copy_scores[bc1]=[]
                    three_copy_scores[bc1].append(score)
                if bc2 in ads:
                    if bc2 not in three_copy_scores:
                        three_copy_scores[bc2]=[]
                    three_copy_scores[bc2].append(score)
                if bc3 in ads:
                    if bc3 not in three_copy_scores:
                        three_copy_scores[bc3]=[]
                    three_copy_scores[bc3].append(score)
                
        for i,ad in enumerate(ads):
            if ad in single_copy_scores:
                scores = single_copy_scores[ad]
                tripartite_medians.at[i,'Tripartite AD'] = ad
                tripartite_medians.at[i,'1 copy median {} screen score'.format(target)] = np.median(scores)
            else:
                tripartite_medians.at[i,'Tripartite AD'] = ad
                tripartite_medians.at[i,'1 copy median {} screen score'.format(target)] = "NA"

        for i,ad in enumerate(ads):
            if ad in two_copy_scores:
                scores = two_copy_scores[ad]
                tripartite_medians.at[i,'2 copy median {} screen score'.format(target)] = np.median(scores)
            else:
                tripartite_medians.at[i,'2 copy median {} screen score'.format(target)] = "NA"

        for i,ad in enumerate(ads):
            if ad in three_copy_scores:
                scores = three_copy_scores[ad]
                tripartite_medians.at[i,'3 copy median {} screen score'.format(target)] = np.median(scores)
            else:
                tripartite_medians.at[i,'3 copy median {} screen score'.format(target)] = "NA"


    res = pd.concat((
        left_part,
        bipartite_medians,
        tripartite_medians
    ),axis=1)
    return res

    

if __name__=="__main__":
    main()