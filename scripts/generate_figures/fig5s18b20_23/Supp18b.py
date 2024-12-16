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

    res = pd.DataFrame()
    for i,ad in enumerate(ads):
        res.at[i,'AD']=ad
    for target in ['EPCAM','CXCR4','Reporter']:
        single_domain_scores = dict()
        for i in single_domain_activity_df.index:
            bc1 = single_domain_activity_df.at[i,'BC1']
            score = single_domain_activity_df.at[i,'{}_average'.format(target)]
            single_domain_scores[bc1]=score
        for i,ad in enumerate(ads):
            res.at[i,'Single-domain {}_average'.format(target)]=single_domain_scores[ad]


    for target in ['EPCAM','CXCR4','Reporter']:
        single_copy_scores = dict()
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

        for i,ad in enumerate(ads):
            scores = single_copy_scores[ad]
            assert len(scores)==4 #Axx_A23, Axx_A25, A23_Axx, A25_Axx
            res.at[i,'Bipartite {}_median with PFs'.format(target)] = np.median(scores)


    for target in ['EPCAM','CXCR4','Reporter']:
        single_copy_scores = dict()
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

        for i,ad in enumerate(ads):
            if ad in single_copy_scores:
                scores = single_copy_scores[ad]
                res.at[i,'Tripartite {} with PFs'.format(target)] = np.median(scores)
            else:
                res.at[i,'Tripartite {} with PFs'.format(target)] = "NA"


    return res

    

if __name__=="__main__":
    main()