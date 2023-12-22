# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 14:06:01 2023

@author: Chavez
"""

import pandas as pd
df1 = pd.read_csv('single_domain_screen_biochem_charachterized.csv',index_col='Unnamed: 0')
df2 = pd.read_csv('bipartite_screen_biochem_charachterized.csv',index_col='Unnamed: 0')
df3 = pd.read_csv('tripartite_screen_biochem_charachterized.csv',index_col='Unnamed: 0')
pfds = ['A23','A24','A25']

for i in df1.index:
    bcs = (df1.at[i,'BC1'],)
    df1.at[i,'pfd_count']=0
    for bc in bcs:
        if bc in pfds:
            df1.at[i,'pfd_count']+=1

for i in df2.index:
    bcs = (df2.at[i,'BC1'],df2.at[i,'BC2'])
    df2.at[i,'pfd_count']=0
    for bc in bcs:
        if bc in pfds:
            df2.at[i,'pfd_count']+=1

for i in df3.index:
    bcs = (df3.at[i,'BC1'],df3.at[i,'BC2'],df3.at[i,'BC3'])
    df3.at[i,'pfd_count']=0
    for bc in bcs:
        if bc in pfds:
            df3.at[i,'pfd_count']+=1

def find_correls(dfs):
    odf = pd.DataFrame()
    for target in ['EPCAM_average','CXCR4_average','Reporter_average','CX&EP Average Tox']:
        for trait in ['NCPR', 'Hydropathy', 'Disorder promoting fraction','Kappa','Omega']:
            for n,df in enumerate(dfs):
                correl = df.corr().at[target,trait]
                odf.at["Screen_"+str(n+1)"_"+target,trait]=correl
    return odf

dfs = [df1,df2,df3]
odf = find_correls(dfs)
odf.to_csv('correls.csv')


df1=df1[df1['pfd_count']!=1]
df1.to_csv('single_domain_screen_bc_no_all_pfds.csv')
df2=df2[df2['pfd_count']!=2]
df2.to_csv('bipartite_screen_bc_no_all_pfds.csv')
df3=df3[df3['pfd_count']!=3]
df3.to_csv('tripartite_screen_bc_no_all_pfds.csv')

dfs = [df1,df2,df3]
odf = find_correls(dfs)
odf.to_csv('correls_no_all_pfds.csv')

import numpy as np
pfds = ['A23','A24','A25']
df3 = pd.read_csv('tripartite_screen_biochem_charachterized.csv',index_col='Unnamed: 0')
for i in df3.index:
    bcs = (df3.at[i,'BC1'],df3.at[i,'BC2'],df3.at[i,'BC3'])
    df3.at[i,'pfd_count']=0
    for bc in bcs:
        if bc in pfds:
            df3.at[i,'pfd_count']+=1
df3_nap=df3[df3['pfd_count']!=3]

data = dict()

for trait in ['NCPR', 'Hydropathy', 'Disorder promoting fraction','Kappa','Omega','CX&EP Average Tox']:
    scored_all = df3[df3['Has all scores']][trait].to_list()
    nscored_all = df3[~df3['Has all scores']][trait].to_list()
    scored_nap = df3_nap[df3_nap['Has all scores']][trait].to_list()
    nscored_nap = df3_nap[~df3_nap['Has all scores']][trait].to_list()
    
    max_length = max(len(scored_all),len(nscored_all),len(nscored_nap),len(scored_nap))
    
    data['{} all_library_lowtox'.format(trait)] = scored_all + [np.nan] * (max_length - len(scored_all))
    data['{} all_library_hightox'.format(trait)] = nscored_all + [np.nan] * (max_length - len(nscored_all))
    
    data['{} no_NAP_lowtox'.format(trait)] = scored_nap + [np.nan] * (max_length - len(scored_nap))
    data['{} no_NAP_hightox'.format(trait)] = nscored_nap + [np.nan] * (max_length - len(nscored_nap))
    
odf = pd.DataFrame(data)
    