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

def reverse_construct(construct:str)->str:
    return "_".join(construct.split("_")[::-1])

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    
    single_domain_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "screen_results",
            "screen_scores",
            "single_domain_screen_scored.csv",
        )
    )
    single_domain_activity_df['Construct'] = single_domain_activity_df['BC1']
    
    bipartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "screen_results",
            "screen_scores",
            "bipartite_screen_scored.csv",
        )
    )
    bipartite_activity_df['Construct'] = bipartite_activity_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)

    tripartite_activity_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
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


   
    pfds = ['A23','A25']
    bipartite_activity_df['PFD count'] = bipartite_activity_df.apply(
        lambda row: pfds.count(row['BC1'])+pfds.count(row['BC2']),
        axis=1
    )
    bipartite_activity_df['Has A24'] = bipartite_activity_df.apply(
        lambda row: row['BC1']=='A24' or row['BC2']=='A24',
        axis=1
    )

    tripartite_activity_df['PFD count'] = tripartite_activity_df.apply(
        lambda row: pfds.count(row['BC1'])+pfds.count(row['BC2'])+pfds.count(row['BC3']),
        axis=1
    )
    tripartite_activity_df['Has A24'] = tripartite_activity_df.apply(
        lambda row: row['BC1']=='A24' or row['BC2']=='A24' or row['BC3']=='A24',
        axis=1
    )
    
    construct_to_score = dict()
    for index in bipartite_activity_df.index:
        construct = bipartite_activity_df.at[index,'Construct']
        epcam_score = bipartite_activity_df.at[index,'EPCAM_average']
        cxcr4_score = bipartite_activity_df.at[index,'CXCR4_average']
        reporter_score = bipartite_activity_df.at[index,'Reporter_average']
        construct_to_score[construct]={'EPCAM':epcam_score,'CXCR4':cxcr4_score,'Reporter':reporter_score}

    for index in tripartite_activity_df.index:
        construct = tripartite_activity_df.at[index,'Construct']
        epcam_score = tripartite_activity_df.at[index,'EPCAM_average']
        cxcr4_score = tripartite_activity_df.at[index,'CXCR4_average']
        reporter_score = tripartite_activity_df.at[index,'Reporter_average']
        construct_to_score[construct]={'EPCAM':epcam_score,'CXCR4':cxcr4_score,'Reporter':reporter_score}

    res = pd.DataFrame()

    seen = set()
    for index in bipartite_activity_df.index:
        construct = bipartite_activity_df.at[index,'Construct']
        reverse = reverse_construct(construct)
        if construct==reverse:
            continue
        if construct not in seen and reverse not in seen:
            seen.add(construct)
            seen.add(reverse)
            res.at[construct,'Construct']=construct
            res.at[construct,'Activator type']='Bipartite'
            res.at[construct,'P1']=bipartite_activity_df.at[index,'BC1']
            res.at[construct,'P2']=bipartite_activity_df.at[index,'BC2']
            res.at[construct,'P3']=np.nan
            res.at[construct,'Reverse_construct']=reverse

            res.at[construct,'EPCAM_average']=construct_to_score[construct]['EPCAM']
            res.at[construct,'CXCR4_average']=construct_to_score[construct]['CXCR4']
            res.at[construct,'Reporter_average']=construct_to_score[construct]['Reporter']

            res.at[construct,'Reverse_EPCAM_average']=construct_to_score[reverse]['EPCAM']
            res.at[construct,'Reverse_CXCR4_average']=construct_to_score[reverse]['CXCR4']
            res.at[construct,'Reverse_Reporter_average']=construct_to_score[reverse]['Reporter']
            
            res.at[construct,'ADs only?']=bipartite_activity_df.at[index,'PFD count']==0 and not bipartite_activity_df.at[index,'Has A24']
            res.at[construct,'Tripartite_1 PF only']=False

    for index in tripartite_activity_df.index:
        construct = tripartite_activity_df.at[index,'Construct']
        reverse = reverse_construct(construct)
        if construct==reverse:
            continue
        
        if construct not in seen and reverse not in seen:
            seen.add(construct)
            seen.add(reverse)
            res.at[construct,'Construct']=construct
            res.at[construct,'Activator type']='Tripartite'
            res.at[construct,'P1']=tripartite_activity_df.at[index,'BC1']
            res.at[construct,'P2']=tripartite_activity_df.at[index,'BC2']
            res.at[construct,'P3']=tripartite_activity_df.at[index,'BC3']
            res.at[construct,'Reverse_construct']=reverse

            res.at[construct,'EPCAM_average']=construct_to_score[construct]['EPCAM']
            res.at[construct,'CXCR4_average']=construct_to_score[construct]['CXCR4']
            res.at[construct,'Reporter_average']=construct_to_score[construct]['Reporter']

            res.at[construct,'Reverse_EPCAM_average']=construct_to_score[reverse]['EPCAM']
            res.at[construct,'Reverse_CXCR4_average']=construct_to_score[reverse]['CXCR4']
            res.at[construct,'Reverse_Reporter_average']=construct_to_score[reverse]['Reporter']
            res.at[construct,'ADs only?']=False
            res.at[construct,'Tripartite_1 PF only']=True
    res.replace(np.nan,'NA',inplace=True)
    return res

if __name__=="__main__":
    main()