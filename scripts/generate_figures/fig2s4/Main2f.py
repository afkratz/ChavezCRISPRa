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

def overlap(a_start,a_end,b_start,b_end)->bool:
    if a_start <= b_start:
        return a_end >= b_start
        """
        as------ae return true
           bs     
        
        as------ae return false
                    bs 
        """
    else:
        return a_start <= b_end
        """
            as
        bs------be return true
        
                   as
        bs------be return False
        """

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    df = pd.read_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "prescreen_results",
            "2_manually_tested_clusters_assigned.csv")
        )

    only_centroids = df[df['Is centroid']==True]
    has_start_end = only_centroids[only_centroids['Origin protein start position'].notna()]

    hits = has_start_end[has_start_end['Hit on any']==True].reset_index(drop=True)
    misses = has_start_end[has_start_end['Hit on any']==False].reset_index(drop=True)
    
    hits=pd.DataFrame({
        'Hits':hits['Domain ID'],
        'Starting position':hits['Origin protein start position'],
        'Ending position':hits['Origin protein end position'],
        "":""#buffer column
        })
    
    misses=pd.DataFrame({
        'Misses':misses['Domain ID'],
        'Starting position':misses['Origin protein start position'],
        'Ending position':misses['Origin protein end position'],
        "":""#buffer column
        })

    bin_count = pd.DataFrame()
    for i,bin_start in enumerate(np.linspace(0,0.95,20)):
        bin_end = bin_start+0.05
        bin_count.at[i,'Bin start']=bin_start
        bin_count.at[i,'Bin end']=bin_end
        
        hit_overlap = 0
        for index in hits.index:
            if overlap(
                    hits.at[index,'Starting position'],
                    hits.at[index,'Ending position'],
                    bin_start,
                    bin_end
                       ):
                hit_overlap+=1
        bin_count.at[i,'Hits count'] = hit_overlap

        miss_overlap = 0
        for index in misses.index:
            if overlap(
                    misses.at[index,'Starting position'],
                    misses.at[index,'Ending position'],
                    bin_start,
                    bin_end
                       ):
                miss_overlap+=1
        bin_count.at[i,'Miss count'] = miss_overlap
    bin_count['Hits count normalized'] = bin_count['Hits count']/bin_count['Hits count'].sum()
    bin_count['Miss count normalized'] = bin_count['Miss count']/bin_count['Miss count'].sum()
    
    result = pd.concat([hits, misses,bin_count], axis=1)

    return result

if __name__=="__main__":
    main()