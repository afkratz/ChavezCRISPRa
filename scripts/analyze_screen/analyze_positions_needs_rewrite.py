# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 12:15:39 2023

@author: Chavez
"""

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/Chavez/Documents/GitHub/ChavezCRISPRa/input_data/screen_sequences/p1_with_prescreen_info.csv')


locs = dict()
for i in df.index:
    bc = df.at[i,'Unnamed: 0']
    start = df.at[i,'Start']
    end = df.at[i,'End']
    if np.isnan(start):
        continue
    locs[bc]=(start,end)

df1 = pd.read_csv('single_domain_screen_biochem_charachterized.csv',index_col='Unnamed: 0')
df2 = pd.read_csv('bipartite_screen_biochem_charachterized.csv',index_col='Unnamed: 0')
df3 = pd.read_csv('tripartite_screen_biochem_charachterized.csv',index_col='Unnamed: 0')

drop = list()
for i in df2.index:
    bcs = (df2.at[i,'BC1'],df2.at[i,'BC2'])
    if bcs[0] in locs and bcs[1] in locs:
        df2.at[i,'1start']=locs[bcs[0]][0]
        df2.at[i,'1end']=  locs[bcs[0]][1]
        df2.at[i,'2start']=locs[bcs[1]][0]
        df2.at[i,'2end']=  locs[bcs[1]][1]
    else:
        drop.append(i)
df2.drop(drop,inplace=True)
    


drop = list()
for i in df3.index:
    bcs = (df3.at[i,'BC1'],df3.at[i,'BC2'],df3.at[i,'BC3'])
    if bcs[0] in locs and bcs[1] in locs and bcs[2] in locs:
        df3.at[i,'1start']=locs[bcs[0]][0]
        df3.at[i,'1end']=  locs[bcs[0]][1]
        df3.at[i,'2start']=locs[bcs[1]][0]
        df3.at[i,'2end']=  locs[bcs[1]][1]
        df3.at[i,'3start']=locs[bcs[2]][0]
        df3.at[i,'3end']=  locs[bcs[2]][1]
    else:
        drop.append(i)
df3.drop(drop,inplace=True)