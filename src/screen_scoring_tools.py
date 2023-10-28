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
                df=pd.read_csv(os.path.join(path,t+"_"+r+"_"+b+".csv"))
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
                        if bc in keep:
                            continue
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

def bin_on_traits(dfs,binning_rules:dict,targets,replicates,bins):
    """
    This function combines entries within a dataframe 
    Takes in a dictionary, binning_rules, of the form
    {
    'key1':n1,
    'key2':n2
    ...
    'keyx':nx
    } 
    Where each key is the name of a column and each value
    corresponds to an integer that governs how we will bin
    on that column. If the integer is 0, then we will
    completely eliminate that column, summing the "count" 
    column for entries which are identical other than that
    column.
    Example:
        input:
            BC1     umi1       count
            A01     AAAAAA     12
            A01     ATAGTA     13
            A02     CGTAGT     1
            A02     GTACAT     9
    Run with traits = {'umi1':0}
        output:
            BC1     count
            A01     25 
            A02     10

    For non-zero values, we will bin based on that many
    charachters of the column, discarding the rest
    Example:
        input:
            BC1     umi1       count
            A01     AAAAAA     12
            A01     AAAGTA     13
            A01     TATAGT     7
            A02     CGTAGT     1
            A02     GTACAT     9
            A02     CGGGAG     14
    Run with traits = {'umi1':2}
        output:
            BC1     umi1       count
            A01     AA     25
            A01     TA     7
            A02     CG     15
            A02     GT     9
    """
    for t in targets:
        for r in replicates:
            for b in bins:
                df=dfs[t][r][b]
                
                """
                First, we make a dictionary to hold each column,
                excluding those columns that we will be dropping
                """
                condensed_columns = {}
                for column in df.columns:
                    if column in binning_rules and binning_rules[column]==0:
                        continue #Skip because we're completely binning on this
                    else:
                        condensed_columns[column]={}#Add a dictionary to be of the form [index]->value
                
                """
                Then, for each index of the dataframe, we construct an index of the form
                [('column_name1','column_value1')...('column_nameN','column_valueN')]
                Where we are applying the following rules:
                if the column is count, then skip it, because that value gets summed
                else, if the column is in our traits, then:
                    if the number of chars we're binning on is >0, shorten it and add it to the index
                    However, if it's 0, then skip it
                otherwise, it's a normal column, like the barcodes, so just append it
                """

                for i in df.index:
                    label=[]
                    for column in df.columns:
                        if column=="count":
                            pass
                        elif column in binning_rules:
                            if(binning_rules[column]>0):
                                number_of_charachters = binning_rules[column]
                                label.append((column,df.at[i,column][0:number_of_charachters]))
                        else:
                            label.append((column,df.at[i,column]))
                    """
                    label now looks something like:
                    [('BC1':'Axx'),('UMI1':'xxx'),('BC2',:'Axx')]
                    Once we've generated this new label, we string-ify it, and use it as an index
                    to assign identities to the condensed_columns dictionaries for each column
                    """

                    str_label = str(label)
                    for column in df.columns:
                        if column=="count":
                            if str_label not in condensed_columns['count']:
                                condensed_columns['count'][str_label]=0
                            condensed_columns['count'][str_label]+=df.at[i,'count']
                        else:
                            if column in binning_rules:
                                number_of_charachters = binning_rules[column]
                                if number_of_charachters>0:
                                    condensed_columns[column][str_label]=df.at[i,column][0:number_of_charachters]
                            else:
                                condensed_columns[column][str_label]=df.at[i,column]

                #Finally, we convert this dictionary of dictionaries back to a dataframe and drop our stringy labels
                dfs[t][r][b]=pd.DataFrame(condensed_columns).reset_index(drop=True)



def combine_bins(dfs,targets,replicates,bins):
    columns = dfs[targets[0]][replicates[0]][bins[0]].columns
    for t in targets:
        for r in replicates:
            for b in bins:
                assert set(dfs[t][r][b].columns.values)==set(columns.values)
                

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
                    for col in dfs[t][r][bins[0]].columns:
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
                if df.at[i,"bin_1"]+df.at[i,"bin_2"]+df.at[i,"bin_3"]+df.at[i,"bin_4"]>mincount:
                    keep_indexes.append(i)
            dfs[t][r]=dfs[t][r].iloc[keep_indexes].reset_index(drop=True)

def discard_min_bin_counts(dfs,mincount,targets,replicates):
    for t in targets:
        for r in replicates:
            df=dfs[t][r]
            keep_indexes=[]
            for i in range(0,len(dfs[t][r])):
                if df.at[i,"bin_1"]>mincount:
                    if df.at[i,"bin_2"]>mincount:
                        if df.at[i,"bin_3"]>mincount:
                            if df.at[i,"bin_4"]>mincount:
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
                if(sum(dfs[t][r].iloc[i][["bin_1","bin_2","bin_3","bin_4"]])>0):
                    score=score/sum(dfs[t][r].iloc[i][["bin_1","bin_2","bin_3","bin_4"]])
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
                if len(dics[x][label])>min_count:
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

def _generate_combinations(columns, options, current_combo=[]):
    if not columns:
        return [[]]
    current_column = columns[0]
    sub_combinations = _generate_combinations(columns[1:], options)
    combinations = []
    for option in options:
        for sub_combo in sub_combinations:
            combinations.append([(current_column,option)] + sub_combo)
    return combinations

def fill_in_combinatorial_results(df,key_columns,entries):
    
    """
    This function takes in a dataframe with a series of columns,
    and "completes" some of them with combinatorial results. 
    For instance:

    DF: BC1     BC2     Score
        A01     A01     100
        A01     A03     120
        A01     A04     90
        ...
        A25     A25     130

    In this df, we have scores for A01-A01, but A01-A02 is missing
    We'd like to fill in all the values for all possible 
    combinations of barcodes to produce the following DF:

    DF: 
        BC1     BC2     Score
        A01     A01     100
        A01     A02     None
        A01     A03     120
        A01     A04     90
        ...
        A25     A25     130

    In this example, you would call this function as:
    df  = fill_in_combinatorial_results(
            df,
            key_columns =['BC1','BC2'],
            entries=['A01','A02',...,'A25']
            )
        
    First, we generate a list of lists of tuples, where
    each tuple is of the form ('BC1':'A01'). Next, these 
    are organized into lists, so a list of the form:
    [
    ('BC1':'A01'),
    ('BC2':'A01'),
    ('BC3':'A01'),
    ]
    Where each tuple's left value is a key_column entry. 
    The outermost list is a list of all possible permutations
    of these values for each item in entries.
    In effect, if you call with
    columns = ['BC1','BC2'], options=['A01' ... 'A25'],
    you will get a list of all possible combinations of A values
    in each of BC1 and BC2.
    """
    for column in key_columns:
        assert column in df.columns

    all_possible_labels = _generate_combinations(key_columns,entries)

    full_df = pd.DataFrame()

    for label in all_possible_labels:
        str_label = str(label)#using this an index
        for (key_column,value) in label:
            full_df.at[str_label,key_column] = value
    """
    full_df now has all key_columns filled in with indexes
    constructed from the labels in all combinations
    full_df:
        indexes                             BC1     BC2     
        '[('BC1','A01'),('BC2','A01')]'     A01     A01 
        '[('BC1','A01'),('BC2','A02')]'     A01     A02 
        '[('BC1','A01'),('BC2','A03')]'     A01     A03 
        '[('BC1','A01'),('BC2','A04')]'     A01     A04
        ...
        '[('BC1','A25'),('BC2','A25')]'     A25     A25 

    Finally, we loop through the input dataframe,
    reconstructing the label from the key_columns, and
    setting all columns for that row equal to the values
    from the input dataframe
    """
    
    for index in df.index:
        label = []
        for key in key_columns:
            label.append(
                (key, df.at[index,key])
            )
        str_label = str(label)
        for col in df.columns:
            full_df.at[str_label,col]=df.at[index,col]
    return full_df

