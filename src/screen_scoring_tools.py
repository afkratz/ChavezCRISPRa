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
def load_dfs(path,targets,replicates,bins):
    dfs={}
    for t in targets:
        dfs[t]={}
        for r in replicates:
            dfs[t][r]={}
            for b in bins:
                df=pd.read_csv(os.path.join(path,t+"_"+r+"_"+b+".csv"),index_col="Unnamed: 0")
                dfs[t][r][b]=df
    return dfs

def discard_errors(dfs,targets,replicates,bins):
    for t in targets:
        for r in replicates:
            for b in bins:
                dfs[t][r][b]=dfs[t][r][b][dfs[t][r][b]["Errors"]==0]
                dfs[t][r][b].drop("Errors",axis=1,inplace=True)
                dfs[t][r][b]=dfs[t][r][b].reset_index(drop=True)

def discard_negative_controls(dfs,columns,keep,targets,replicates,bins):
    for t in targets:
        for r in replicates:
            for b in bins:
                for column in columns:
                    for bc in set(dfs[t][r][b][column]):
                        if bc in keep:continue
                        dfs[t][r][b]=dfs[t][r][b][dfs[t][r][b][column]!=bc]
                    dfs[t][r][b]=dfs[t][r][b].reset_index(drop=True)
        

def discard_high_counts_percentage_of_total(dfs,percentage,targets,replicates,bins):
    for t in targets:
        for r in replicates:
            for b in bins:
                limit= int(sum(dfs[t][r][b]["count"])*percentage)
                dfs[t][r][b]=dfs[t][r][b][dfs[t][r][b]["count"]<limit].reset_index(drop=True)

def normalize_read_counts(dfs,targets,replicates,bins):
    for t in targets:
        for r in replicates:
            for b in bins:
                df=dfs[t][r][b]
                df['count']=df['count'].astype(float)
                total_reads=sum(df["count"])
                for i in range(0,len(df)):
                    df.at[i,"count"]=float((df.at[i,"count"]*100*len(df))/total_reads)

def bin_on_traits(dfs,traits,targets,replicates,bins):
    for t in targets:
        for r in replicates:
            for b in bins:
                df=dfs[t][r][b]
                dics={}
                for col in df.columns:
                    if col in traits:
                        if(traits[col]>0):
                            dics[col]={}
                    else:
                        dics[col]={}

                for i in range(len(df)):
                    label=""
                    for col in df.columns:
                        if col=="count":
                            pass
                        elif col in traits:
                            if(traits[col]>0):
                                label=label+df.at[i,col][:traits[col]]
                        else:
                            label=label+df.at[i,col]

                    for col in df.columns:
                        if col=="count":
                            continue
                        if col in traits:
                            if(traits[col]>0):
                                dics[col][label]=df.at[i,col][:traits[col]]
                        else:
                            dics[col][label]=df.at[i,col]
                            
                    if label not in dics["count"].keys():
                        dics["count"][label]=0
                    dics["count"][label]+=df.at[i,"count"]
                dfs[t][r][b]=pd.DataFrame(dics).reset_index(drop=True)

def combine_bins(dfs,targets,replicates,bins):
    condensed_dfs={}
    for t in targets:
        condensed_dfs[t]={}
        for r in replicates:
            dics={}
            for col in dfs[t][r][bins[0]]:
                if col=="count":
                    continue
                else:
                    dics[col]={}
            for b in bins:
                dics[b]={}
            for b in bins:
                df=dfs[t][r][b]
                for i in range(0,len(df)):
                    label=""
                    for col in df.columns:
                        if col=="count":
                            continue
                        else:
                            label=label+df.at[i,col]
                    if label not in dics[b].keys():
                        for col in df.columns:
                            if(col=="count"):
                                continue
                            else:
                                dics[col][label]=df.at[i,col]
                        for b2 in bins:
                            dics[b2][label]=0
                    dics[b][label]+=df.at[i,"count"]
            condensed_dfs[t][r]=pd.DataFrame(dics).reset_index(drop=True)
    return(condensed_dfs)


def discard_combined_bin_counts(dfs,mincount,targets,replicates):
    for t in targets:
        for r in replicates:
            df=dfs[t][r]
            keep_indexes=[]
            for i in range(0,len(dfs[t][r])):
                if df.at[i,"bin 1"]+df.at[i,"bin 2"]+df.at[i,"bin 3"]+df.at[i,"bin 4"]>mincount:
                    keep_indexes.append(i)
            dfs[t][r]=dfs[t][r].iloc[keep_indexes].reset_index(drop=True)

def discard_min_bin_counts(dfs,mincount,targets,replicates):
    for t in targets:
        for r in replicates:
            df=dfs[t][r]
            keep_indexes=[]
            for i in range(0,len(dfs[t][r])):
                if df.at[i,"bin 1"]>mincount:
                    if df.at[i,"bin 2"]>mincount:
                        if df.at[i,"bin 3"]>mincount:
                            if df.at[i,"bin 4"]>mincount:
                                keep_indexes.append(i)
            dfs[t][r]=dfs[t][r].iloc[keep_indexes].reset_index(drop=True)

def load_mfis(filename):
    return pd.read_csv(filename,index_col="Condition")

def add_FluorescentProductScore(dfs,mfis,targets,replicates,bins):
    for t in targets:
        for r in replicates:
            dfs[t][r]["FluorescentProductScore"]=np.nan

            for i in range(len(dfs[t][r])):
                score=0
                for b in bins:
                    if b=="NS":continue
                    score+=mfis.at[t+"_"+r,b]*dfs[t][r].at[i,b]
                if(sum(dfs[t][r].iloc[i][["bin 1","bin 2","bin 3","bin 4"]])>0):
                    score=score/sum(dfs[t][r].iloc[i][["bin 1","bin 2","bin 3","bin 4"]])
                    dfs[t][r].at[i,"FluorescentProductScore"]=score

def drop_item(dfs,trait,targets,replicates):
    for t in targets:
        for r in replicates:
            dfs[t][r].drop(trait,axis=1,inplace=True)
            
def mean_x_over_y(dfs,x,y,min_count,targets,replicates,bins):
    for t in targets:
        for r in replicates:
            df=dfs[t][r]
            dics={}
            for col in df.columns:
                if col==x:#the column we're going to be averaging
                    dics[col]={}
                elif col==y:#the the column we're going to be averaging OVER
                    pass
                else:
                    dics[col]={}
            for i in range(0,len(df)):
                label=""
                for col in df.columns:
                    if col==x:
                        pass
                    elif col==y:
                        pass
                    elif col in bins:
                        pass
                    else:
                        label=label+df.at[i,col]
                
                for col in df.columns:
                    if col==y:
                        pass
                    elif col==x:
                        pass
                    else:
                        dics[col][label]=df.at[i,col]
                if label not in dics[x].keys():
                    dics[x][label]=[]
                if(df.at[i,x]!=""):dics[x][label].append(df.at[i,x])
            for label in dics[x].keys():
                if len(dics[x][label])>3:
                    dics[x][label]=np.mean(dics[x][label])
                else:
                    dics[x][label]=None
            dfs[t][r]=pd.DataFrame(dics).reset_index(drop=True)

def combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore'):
    odf=pd.DataFrame()
    columns = []
    for col in dfs[targets[0]][replicates[0]].columns:
        if col==keep:continue
        columns.append(col)
        odf[col]=""
    assert(len(columns)+1==len(dfs[targets[0]][replicates[0]].columns))
    
    for t in targets:
        for r in replicates:
            name = t+"_"+r
            df=dfs[t][r]
            for i in range(len(df)):
                label = ""
                for col in columns:
                    label+=df.at[i,col]
                for col in columns:
                    odf.at[label,col]=df.at[i,col]
                    odf.at[label,name]=df.at[i,keep]
    return odf

def fill_in_combinatorial_results(df,columns,entries):
    full_df = pd.DataFrame()
    labels = [[]]
    for key in columns:
        new_labels = []
        for label in labels:
            for value in entries:
                if len(label)>0:new_labels.append(label+[value])
                else: new_labels.append(label+[value])
        labels=new_labels
    for label in labels:
        for i in range(len(columns)):
            full_df.at["_".join(label),columns[i]]=label[i]
    for index in df.index:
        label = []
        for c in columns:
            label.append(df.at[index,c])
        for c in df.columns:
            full_df.at["_".join(label),c]=df.at[index,c]
    return full_df


def test_2():
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin 1","bin 2","bin 3","bin 4","NS"]
    dfs = load_dfs("output/screen_results/processed_reads/bipartite_sorted",targets,replicates,bins)
    print('loaded')
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    discard_errors(dfs,targets,replicates,bins)
    print('errors discarded')
    discard_negative_controls(dfs,['BC1','BC2'],barcodes,targets,replicates,bins)
    discard_high_counts_percentage_of_total(dfs,0.0005,targets,replicates,bins)
    print('negatives discarded')
    umi_traits = {"UMI1":0,"UMI2":2}
    bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    print('binned on umis')
    normalize_read_counts(dfs,targets,replicates,bins)
    print('normalized')
    dfs=combine_bins(dfs,targets,replicates,bins)
    discard_combined_bin_counts(dfs,20,targets,replicates)
    mfis=load_mfis("screen_Data/bin_mfis/p2_sorted_mfi.csv")
    add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)
    print('scored')
    drop_item(dfs,"bin 1",targets,replicates)
    drop_item(dfs,"bin 2",targets,replicates)
    drop_item(dfs,"bin 3",targets,replicates)
    drop_item(dfs,"bin 4",targets,replicates)
    drop_item(dfs,"NS",targets,replicates)
    mean_x_over_y(dfs,"FluorescentProductScore","UMI2",3,targets,replicates,bins)

    odf=combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = fill_in_combinatorial_results(odf,["BC1","BC2"],barcodes)
    odf.to_csv("P2_sorted_scored.csv",index=False)

def test_3():
    targets=["EPCAM","CXCR4","Reporter"]
    replicates=["1","2"]
    bins=["bin 1","bin 2","bin 3","bin 4","NS"]
    dfs = load_dfs("output/screen_results/processed_reads/tripartite_sorted",targets,replicates,bins)
    print('loaded')
    barcodes = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    discard_errors(dfs,targets,replicates,bins)
    print('errors discarded')
    discard_negative_controls(dfs,['BC1','BC2','BC3'],barcodes,targets,replicates,bins)
    discard_high_counts_percentage_of_total(dfs,0.01,targets,replicates,bins)
    print('negatives discarded')
    umi_traits = {"UMI2":0}
    bin_on_traits(dfs,umi_traits,targets,replicates,bins)
    print('binned on umis')
    normalize_read_counts(dfs,targets,replicates,bins)
    print('normalized')
    dfs=combine_bins(dfs,targets,replicates,bins)
    discard_min_bin_counts(dfs,0,targets,replicates)
    discard_combined_bin_counts(dfs,493,targets,replicates)
    mfis=load_mfis("screen_Data/bin_mfis/p3_sorted_mfi.csv")
    add_FluorescentProductScore(dfs,mfis,targets,replicates,bins)
    print('scored')
    drop_item(dfs,"bin 1",targets,replicates)
    drop_item(dfs,"bin 2",targets,replicates)
    drop_item(dfs,"bin 3",targets,replicates)
    drop_item(dfs,"bin 4",targets,replicates)
    drop_item(dfs,"NS",targets,replicates)
    odf=combine_replicates(dfs,targets,replicates,keep='FluorescentProductScore')
    odf = fill_in_combinatorial_results(odf,["BC1","BC2","BC3"],barcodes)
    odf.to_csv("P3_sorted_scored.csv",index=False)
