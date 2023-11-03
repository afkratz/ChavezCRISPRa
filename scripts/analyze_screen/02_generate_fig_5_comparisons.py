# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import pandas as pd

os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from src import screen_scoring_tools as sst

p1_score = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_single_domain_screen_scored_with_zscore.csv"
    )
)

p2_score = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_bipartite_screen_scored_with_zscore.csv"
    )
)

p3_score = pd.read_csv(
    os.path.join(
        "output",
        "screen_analysis",
        "activity_analysis",
        "01_tripartite_screen_scored_with_zscore.csv"
    )
)
all_barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
activator_barcodes = all_barcodes[0:22]
pfd_barcodes = ['A23','A25']

def generate_5c():
    bcs2scores ={}
    for i in p2_score.index:
        bc1 = p2_score.at[i,'BC1']
        bc2 = p2_score.at[i,'BC2']
        epcam_score = p2_score.at[i,"EPCAM_Zscore"]
        cxcr4_score = p2_score.at[i,"CXCR4_Zscore"]
        reporter_score = p2_score.at[i,"Reporter_Zscore"]
        bcs2scores[(bc1,bc2)]={}
        bcs2scores[(bc1,bc2)]['EPCAM']=epcam_score
        bcs2scores[(bc1,bc2)]['CXCR4']=cxcr4_score
        bcs2scores[(bc1,bc2)]['Reporter']=reporter_score

    odf = pd.DataFrame()
    odf['BCA']=""
    odf['BCB']=""
    for bcB in activator_barcodes:
        for bcA in activator_barcodes:
            if bcA==bcB:break
            i=len(odf)
            odf.at[i,"BCA"]=bcA
            odf.at[i,"BCB"]=bcB
            for target in ['EPCAM','CXCR4','Reporter']:
                odf.at[i,"A-B "+target]=bcs2scores[(bcA,bcB)][target]
                odf.at[i,"B-A "+target]=bcs2scores[(bcB,bcA)][target]
    odf.to_csv(
        os.path.join(
            "output",
            "screen_analysis",
            "activity_analysis",
            "5c_left.csv"
        ),
        index=False
    )

    for i in p3_score.index:
        bc1 = p3_score.at[i,'BC1']
        bc2 = p3_score.at[i,'BC2']
        bc3 = p3_score.at[i,'BC3']
        epcam_score = p3_score.at[i,"EPCAM_Zscore"]
        cxcr4_score = p3_score.at[i,"CXCR4_Zscore"]
        reporter_score = p3_score.at[i,"Reporter_Zscore"]
        bcs2scores[(bc1,bc2,bc3)]={}
        bcs2scores[(bc1,bc2,bc3)]['EPCAM']=epcam_score
        bcs2scores[(bc1,bc2,bc3)]['CXCR4']=cxcr4_score
        bcs2scores[(bc1,bc2,bc3)]['Reporter']=reporter_score
    
    odf = pd.DataFrame()
    odf['BCA']=""
    odf['MiddleBC']=""
    odf['BCB']=""

    for bcA in activator_barcodes:
        for middle_bc in all_barcodes:
            for bcB in activator_barcodes:
                if bcB==bcA:
                    break

                if (bcA,middle_bc,bcB) in bcs2scores and (bcB,middle_bc,bcA) in bcs2scores:
                    i=len(odf)
                    odf.at[i,"BCA"]=bcA
                    odf.at[i,"MiddleBC"]=middle_bc
                    odf.at[i,"BCB"]=bcB
                    for target in ['EPCAM','CXCR4','Reporter']:
                        odf.at[i,"BCA-middleBC-BCB "+target]=bcs2scores[(bcA,middle_bc,bcB)][target]
                        odf.at[i,"BCB-middleBC-BCA "+target]=bcs2scores[(bcB,middle_bc,bcA)][target]
    odf.to_csv(
        os.path.join(
            "output",
            "screen_analysis",
            "activity_analysis",
            "5c_middle.csv"
        ),
        index=False
    )
    odf=pd.DataFrame()
    odf['Activator']=""
    odf['MiddleBC']=""
    odf['PFD']=""
    for ad in activator_barcodes:
        for middle_barcode in all_barcodes:
            for pfd_partner in pfd_barcodes:
                if (ad,middle_barcode,pfd_partner) in bcs2scores and (pfd_partner,middle_barcode,ad) in bcs2scores:
                    i=len(odf)
                    odf.at[i,'Activator']=ad
                    odf.at[i,'MiddleBC'] = middle_barcode
                    odf.at[i,'PFD'] = pfd_partner
                    for target in ['EPCAM','CXCR4','Reporter']:
                        odf.at[i,'AD-middle-PFD '+target]=bcs2scores[(ad,middle_barcode,pfd_partner)][target]
                        odf.at[i,'PFD-middle-AD '+target]=bcs2scores[(pfd_partner,middle_barcode,ad)][target]
    odf.to_csv(
        os.path.join(
            "output",
            "screen_analysis",
            "activity_analysis",
            "5c_right.csv"
        ),
        index=False
    )                

def generate_5d():
    bcs2scores ={}
    for i in p2_score.index:
        bc1 = p2_score.at[i,'BC1']
        bc2 = p2_score.at[i,'BC2']
        epcam_score = p2_score.at[i,"EPCAM_Zscore"]
        cxcr4_score = p2_score.at[i,"CXCR4_Zscore"]
        reporter_score = p2_score.at[i,"Reporter_Zscore"]
        bcs2scores[(bc1,bc2)]={}
        bcs2scores[(bc1,bc2)]['EPCAM']=epcam_score
        bcs2scores[(bc1,bc2)]['CXCR4']=cxcr4_score
        bcs2scores[(bc1,bc2)]['Reporter']=reporter_score

    for i in p3_score.index:
        bc1 = p3_score.at[i,'BC1']
        bc2 = p3_score.at[i,'BC2']
        bc3 = p3_score.at[i,'BC3']
        epcam_score = p3_score.at[i,"EPCAM_Zscore"]
        cxcr4_score = p3_score.at[i,"CXCR4_Zscore"]
        reporter_score = p3_score.at[i,"Reporter_Zscore"]
        bcs2scores[(bc1,bc2,bc3)]={}
        bcs2scores[(bc1,bc2,bc3)]['EPCAM']=epcam_score
        bcs2scores[(bc1,bc2,bc3)]['CXCR4']=cxcr4_score
        bcs2scores[(bc1,bc2,bc3)]['Reporter']=reporter_score

    odf = pd.DataFrame()
    odf['Activator']=""
    for ad in activator_barcodes:
        i=len(odf)
        odf.at[i,'Activator']=ad
        for target in ['EPCAM','CXCR4','Reporter']:
            odf.at[i,"AD-AD "+target]=bcs2scores[(ad,ad)][target]
            for pfd in pfd_barcodes:
                odf.at[i,"AD-"+pfd+" "+target]=bcs2scores[(ad,pfd)][target]
                odf.at[i,pfd+"-AD "+target]=bcs2scores[(pfd,ad)][target]
            odf.at[i,'PFD & AD '+target]=np.mean((
                bcs2scores[('A23',ad)][target],
                bcs2scores[('A25',ad)][target],
                bcs2scores[(ad,'A23')][target],
                bcs2scores[(ad,'A25')][target],
            ))
    odf.to_csv(
        os.path.join(
            "output",
            "screen_analysis",
            "activity_analysis",
            "5d_left.csv"
        ),
        index=False
    )

    tripartite_copy_number_results={}
    for key in bcs2scores:
        if len(key)==2:continue
        if 'A24' in key:continue
        pfd_count = key.count('A23')+key.count('A25')
        present_activators = set(key).intersection(set(activator_barcodes))
        if len(present_activators)==1:
            activator = present_activators.pop()
            activator_copy_number = key.count(activator)
            assert (activator_copy_number+pfd_count)==3
            copy_number_key= (activator,activator_copy_number)
            if copy_number_key not in tripartite_copy_number_results:
                tripartite_copy_number_results[copy_number_key]={}
                tripartite_copy_number_results[copy_number_key]['EPCAM']=[]
                tripartite_copy_number_results[copy_number_key]['CXCR4']=[]
                tripartite_copy_number_results[copy_number_key]['Reporter']=[]
            for target in ['EPCAM','CXCR4','Reporter']:
                tripartite_copy_number_results[copy_number_key][target].append(bcs2scores[key][target])
    
    odf = pd.DataFrame()
    odf['Activator']=""
    for ad in activator_barcodes:
        i = len(odf)
        odf.at[i,'Activator']=ad
        for copy_number in [1,2,3]:
            if (ad,copy_number) not in tripartite_copy_number_results:
                n_observations = 0
            else:
                n_observations = len(tripartite_copy_number_results[(ad,copy_number)]['EPCAM'])
            odf.at[i,'N observations with '+str(copy_number)+' copies'] = n_observations
    for i in odf.index:
        ad = odf.at[i,'Activator']
        for copy_number in [1,2,3]:
            if odf.at[i,'N observations with '+str(copy_number)+' copies']>0:
                for target in ['EPCAM','CXCR4','Reporter']:
                    odf.at[i,str(copy_number)+" "+target]=np.mean(tripartite_copy_number_results[(ad,copy_number)][target])
    odf.to_csv(
        os.path.join(
            "output",
            "screen_analysis",
            "activity_analysis",
            "5d_center.csv"
        ),
        index=False
    )

    


if __name__=="__main__":
    generate_5c()
    generate_5d()