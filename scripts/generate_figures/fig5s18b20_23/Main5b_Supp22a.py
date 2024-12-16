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
    pfds = ['A23','A25']
    ads = all_bcs[:22]

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
    
    single_domain_activity_df['1 AD copy']=True
    single_domain_activity_df['2 AD copy']=False
    single_domain_activity_df['3 AD copy']=False

    for i in bipartite_activity_df.index:
        bc1=bipartite_activity_df.at[i,'BC1']
        bc2=bipartite_activity_df.at[i,'BC2']
        if "A24" in (bc1,bc2):
            bipartite_activity_df.at[i,'1 AD copy']=False
            bipartite_activity_df.at[i,'2 AD copy']=False
        else:
            n_pfds = sum([1 if bc in pfds else 0 for bc in (bc1,bc2)])
            bipartite_activity_df.at[i,'1 AD copy']=n_pfds==1
            bipartite_activity_df.at[i,'2 AD copy'] = bc1==bc2 and n_pfds==0
    bipartite_activity_df['3 AD copy']=False

    for i in tripartite_activity_df.index:
        bc1=tripartite_activity_df.at[i,'BC1']
        bc2=tripartite_activity_df.at[i,'BC2']
        bc3=tripartite_activity_df.at[i,'BC3']
        if "A24" in (bc1,bc2,bc3):
            tripartite_activity_df.at[i,'1 AD copy']=False
            tripartite_activity_df.at[i,'2 AD copy']=False
            tripartite_activity_df.at[i,'3 AD copy']=False
        else:
            n_pfds = sum([1 if bc in pfds else 0 for bc in (bc1,bc2,bc3)])
            n_different_ads = len(set((bc1,bc2,bc3))-set(pfds))

            tripartite_activity_df.at[i,'1 AD copy']=n_pfds==2
            tripartite_activity_df.at[i,'2 AD copy']=(n_pfds==1) and (n_different_ads==1)
            tripartite_activity_df.at[i,'3 AD copy']=(bc1==bc2) and (bc2==bc3) and n_pfds==0


        

    left_part =pd.concat((
        pd.DataFrame({
        "Construct":single_domain_activity_df['Construct'],
        'Activator Type':'Single-domain',
        'P1':single_domain_activity_df['BC1'],
        'P2':"",
        'P3':"",
        'EPCAM average':single_domain_activity_df['EPCAM_average'],
        'CXCR4 average':single_domain_activity_df['CXCR4_average'],
        'Reporter average':single_domain_activity_df['Reporter_average'],
        '1 AD copy':single_domain_activity_df['1 AD copy'],
        '2 AD copy':single_domain_activity_df['2 AD copy'],
        '3 AD copy':single_domain_activity_df['3 AD copy'],
    }),
    pd.DataFrame({
        "Construct":bipartite_activity_df['Construct'],
        'Activator Type':'Bipartite',
        'P1':bipartite_activity_df['BC1'],
        'P2':bipartite_activity_df['BC2'],
        'P3':"",
        'EPCAM average':bipartite_activity_df['EPCAM_average'],
        'CXCR4 average':bipartite_activity_df['CXCR4_average'],
        'Reporter average':bipartite_activity_df['Reporter_average'],
        '1 AD copy':bipartite_activity_df['1 AD copy'],
        '2 AD copy':bipartite_activity_df['2 AD copy'],
        '3 AD copy':bipartite_activity_df['3 AD copy'],
    }),
    pd.DataFrame({
        "Construct":tripartite_activity_df['Construct'],
        'Activator Type':'Tripartite',
        'P1':tripartite_activity_df['BC1'],
        'P2':tripartite_activity_df['BC2'],
        'P3':tripartite_activity_df['BC3'],
        'EPCAM average':tripartite_activity_df['EPCAM_average'],
        'CXCR4 average':tripartite_activity_df['CXCR4_average'],
        'Reporter average':tripartite_activity_df['Reporter_average'],
        '1 AD copy':tripartite_activity_df['1 AD copy'],
        '2 AD copy':tripartite_activity_df['2 AD copy'],
        '3 AD copy':tripartite_activity_df['3 AD copy'],
    })),
    ignore_index=True)
    left_part[""]=""


    bipart_right_part = pd.DataFrame()
    for ad in ads:
        bipart_right_part.at[ad,'Bipartite AD']=ad
        
        for target in 'EPCAM','CXCR4','Reporter':
            bipart_right_part.at[ad,'1 copy median {} screen score'.format(target)]=bipartite_activity_df[
                bipartite_activity_df['1 AD copy']& ((bipartite_activity_df['BC1']==ad)|(bipartite_activity_df['BC2']==ad))
                ]['{}_average'.format(target)].median()
        
        for target in 'EPCAM','CXCR4','Reporter':
            bipart_right_part.at[ad,'2 copy median {} screen score'.format(target)]=bipartite_activity_df[
                bipartite_activity_df['2 AD copy']& ((bipartite_activity_df['BC1']==ad)|(bipartite_activity_df['BC2']==ad))
                ]['{}_average'.format(target)].median()
                    
            
    bipart_right_part['']=''#buffer col

    tripart_right_part = pd.DataFrame()
    for ad in ads:
        tripart_right_part.at[ad,'Tripartite AD']=ad
        for target in 'EPCAM','CXCR4','Reporter':
            tripart_right_part.at[ad,'1 copy median {} screen score'.format(target)]=tripartite_activity_df[
                tripartite_activity_df['1 AD copy']& ((tripartite_activity_df['BC1']==ad)|(tripartite_activity_df['BC2']==ad)|(tripartite_activity_df['BC3']==ad))
                ]['{}_average'.format(target)].median()
        
        for target in 'EPCAM','CXCR4','Reporter':
            tripart_right_part.at[ad,'2 copy median {} screen score'.format(target)]=tripartite_activity_df[
                tripartite_activity_df['2 AD copy']& ((tripartite_activity_df['BC1']==ad)|(tripartite_activity_df['BC2']==ad)|(tripartite_activity_df['BC3']==ad))
                ]['{}_average'.format(target)].median()
        
        for target in 'EPCAM','CXCR4','Reporter':
            tripart_right_part.at[ad,'3 copy median {} screen score'.format(target)]=tripartite_activity_df[
                tripartite_activity_df['3 AD copy']& ((tripartite_activity_df['BC1']==ad)|(tripartite_activity_df['BC2']==ad)|(tripartite_activity_df['BC3']==ad))
                ]['{}_average'.format(target)].median()

        
    right_part = pd.concat((
            bipart_right_part,tripart_right_part),
            axis=1
    )
    left_part.reset_index(drop=True,inplace=True)
    left_part[['EPCAM average','CXCR4 average','Reporter average']] =left_part[['EPCAM average','CXCR4 average','Reporter average']].replace(np.nan,'NA')

    right_part.reset_index(drop=True,inplace=True)
    right_part.replace(np.nan,'NA',inplace=True)    

    res = pd.concat(
        (left_part,right_part),
        axis=1
    )
    return res

if __name__=="__main__":
    main()