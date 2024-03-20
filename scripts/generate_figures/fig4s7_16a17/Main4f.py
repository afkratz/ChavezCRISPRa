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
    ad_bcs = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,23)))

    bipartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'bipartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,P2 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]
    bipartite_tox_df['Construct'] = bipartite_tox_df.apply(lambda row: "{}_{}".format(row['BC1'], row['BC2']), axis=1)
    bipartite_construct_to_tox = dict()
    for i in bipartite_tox_df.index:
        construct = bipartite_tox_df.at[i,'Construct']
        tox = bipartite_tox_df.at[i,'CX&EP Average Tox']
        assert construct not in bipartite_construct_to_tox
        bipartite_construct_to_tox[construct]=tox
    
    bipartite_copy_number_tox = pd.DataFrame()
    for i,bc in enumerate(ad_bcs):
        bipartite_copy_number_tox.at[i,'Bipartite AD']=bc
        bipartite_copy_number_tox.at[i,'1 copy median toxicity']=np.median((
            bipartite_construct_to_tox["{}_{}".format("A23",bc)],
            bipartite_construct_to_tox["{}_{}".format("A25",bc)],
            bipartite_construct_to_tox["{}_{}".format(bc,"A23")],
            bipartite_construct_to_tox["{}_{}".format(bc,"A25")],
        ))
        
        bipartite_copy_number_tox.at[i,'2 copy median toxicity']=bipartite_construct_to_tox["{}_{}".format(bc,bc)]

        


    tripartite_tox_df = pd.read_csv(
        os.path.join(
                ChavezCIRSPRa_root_dir,
                'output',
                'screen_results',
                'screen_toxicity',
                'tripartite_screen_toxicity.csv')
    )#Columns = [BC1,BC2,BC3,P3 Plasmid,EPCAM_1_NS,EPCAM_2_NS,CXCR4_1_NS,CXCR4_2_NS,Reporter_1_NS,Reporter_2_NS,EPCAM_Tox,CXCR4_Tox,Reporter_Tox,CX&EP Average Tox]
    tripartite_tox_df['Construct'] = tripartite_tox_df.apply(lambda row: "{}_{}_{}".format(row['BC1'], row['BC2'],row['BC3']), axis=1)
    tripartite_construct_to_tox = dict()
    for i in tripartite_tox_df.index:
        construct = tripartite_tox_df.at[i,'Construct']
        tox = tripartite_tox_df.at[i,'CX&EP Average Tox']
        assert construct not in tripartite_construct_to_tox
        tripartite_construct_to_tox[construct]=tox
    
    tripartite_copy_number_tox = pd.DataFrame()
    for i,bc in enumerate(ad_bcs):
        tripartite_copy_number_tox.at[i,'Tripartite AD']=bc

        tripartite_copy_number_tox.at[i,'1 copy median toxicity']=np.median((
            tripartite_construct_to_tox["{}_{}_{}".format("A23","A23",bc)],
            tripartite_construct_to_tox["{}_{}_{}".format("A23","A25",bc)],
            tripartite_construct_to_tox["{}_{}_{}".format("A25","A23",bc)],
            tripartite_construct_to_tox["{}_{}_{}".format("A25","A25",bc)],
            tripartite_construct_to_tox["{}_{}_{}".format("A23",bc,"A23")],
            tripartite_construct_to_tox["{}_{}_{}".format("A23",bc,"A25")],
            tripartite_construct_to_tox["{}_{}_{}".format("A25",bc,"A23")],
            tripartite_construct_to_tox["{}_{}_{}".format("A25",bc,"A25")],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,"A23","A23")],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,"A23","A25")],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,"A25","A23")],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,"A25","A25")],
        ))


        tripartite_copy_number_tox.at[i,'2 copy median toxicity']=np.median((
            tripartite_construct_to_tox["{}_{}_{}".format("A23",bc,bc)],
            tripartite_construct_to_tox["{}_{}_{}".format("A25",bc,bc)],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,"A23",bc)],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,"A25",bc)],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,bc,"A23")],
            tripartite_construct_to_tox["{}_{}_{}".format(bc,bc,"A25")],
        ))
        
        tripartite_copy_number_tox.at[i,'3 copy median toxicity']=tripartite_construct_to_tox["{}_{}_{}".format(bc,bc,bc)]
    

    bipartite_copy_number_tox[""]=""
    res = pd.concat(
        [bipartite_copy_number_tox,tripartite_copy_number_tox],
        axis=1)
    return res

if __name__=="__main__":
    main()