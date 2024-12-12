
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

    single_domain_tox_df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            'output',
            'screen_results',
            'screen_toxicity',
            'single_domain_toxicity.csv'
        )
    )
    single_domain_tox_df['Construct'] = single_domain_tox_df['BC1']
    single_domain_tox_df['Average_Tox']=single_domain_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    bipartite_tox_df['Average_Tox']=bipartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)


    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    tripartite_tox_df['Average_Tox']=tripartite_tox_df[['EPCAM_average_Tox','CXCR4_average_Tox']].values.mean(axis=1)


    
    left_part = pd.concat((
        pd.DataFrame(
            {
                "Construct":bipartite_tox_df['Construct'],
                "Type":"Bipartite",
                "P1":bipartite_tox_df['BC1'],
                "P2":bipartite_tox_df['BC2'],
                "P3":np.nan,
                "Toxicity":bipartite_tox_df['Average_Tox'],
                "":""#Buffer
             }
        ),
        pd.DataFrame(
            {
                "Construct":tripartite_tox_df['Construct'],
                "Type":"Tripartite",
                "P1":tripartite_tox_df['BC1'],
                "P2":tripartite_tox_df['BC2'],
                "P3":tripartite_tox_df['BC3'],
                "Toxicity":tripartite_tox_df['Average_Tox'],
                "":""#Buffer
             }
        )),ignore_index=True
        )
    

    biparte_median_tox_by_position = pd.DataFrame()
    triparte_median_tox_by_position = pd.DataFrame()
    
    for i,bc in enumerate(all_bcs):
        biparte_median_tox_by_position.at[i,'Bipartite AD']=bc
        triparte_median_tox_by_position.at[i,'Tripartite AD']=bc
        
        biparte_median_tox_by_position.at[i,'P1 median toxicity']=np.median(
            bipartite_tox_df[bipartite_tox_df['BC1']==bc]['Average_Tox'].values
        )
        triparte_median_tox_by_position.at[i,'P1 median toxicity']=np.median(
            tripartite_tox_df[tripartite_tox_df['BC1']==bc]['Average_Tox'].values
        )
        

        biparte_median_tox_by_position.at[i,'P2 median toxicity']=np.median(
            bipartite_tox_df[bipartite_tox_df['BC2']==bc]['Average_Tox'].values
        )
        triparte_median_tox_by_position.at[i,'P2 median toxicity']=np.median(
            tripartite_tox_df[tripartite_tox_df['BC2']==bc]['Average_Tox'].values
        )
        
        biparte_median_tox_by_position.at[i,""]=""#Buffer column
        triparte_median_tox_by_position.at[i,'P3 median toxicity']=np.median(
            tripartite_tox_df[tripartite_tox_df['BC3']==bc]['Average_Tox'].values
        )
    

    res = pd.concat((
        left_part,
        biparte_median_tox_by_position,
        triparte_median_tox_by_position,
    ),axis=1)

    return res

 

if __name__=="__main__":
    main()