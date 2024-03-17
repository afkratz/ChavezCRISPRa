# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
Provides functions used to process the tripartite screen.
Due to differences in the read structure of the (single&bipartite) vs tripartite
screens, we broke the pipeline up into slightly different forms for the tripartite
screen. 
"""
from pathlib import Path
import os
import gzip
from typing import List,Tuple

import pandas as pd
import numpy as np
from Bio import SeqIO

from progress import spinner as sp
from progress.bar import Bar

def revcom(ori):
    trans=str.maketrans('ATGC', 'TACG')
    return ori.upper().translate(trans)[::-1]

class ScreenReads:
    def __init__(self,reads_dir,fw_read_file=None,rv_read_file=None):
        if fw_read_file==None and rv_read_file==None:
            raise ValueError("Need to pass in at least one of fw_read_file or rv_read_file")
        
        self._has_fw=False
        if fw_read_file!=None:
            self._has_fw=True
            path_to_fw = os.path.join(reads_dir,fw_read_file)
            if not os.path.exists(path_to_fw):
                raise FileNotFoundError("Could not find file {}".format(path_to_fw))
            if path_to_fw[-3:]=='.gz':
                self._fwfh=gzip.open(path_to_fw,mode='rt')
            elif path_to_rv[-6:]=='.fastq':
                self._fwfh=open(path_to_fw,mode='rt')
            else:
                raise TypeError("Filepath should be a .fastq or a .gz, recieved {}".format(path_to_fw))
            self._fw_records = SeqIO.parse(self._fwfh,'fastq')

        self._has_rv=False
        if rv_read_file!=None:
            self._has_rv=True
            path_to_rv = os.path.join(reads_dir,rv_read_file)
            if not os.path.exists(path_to_rv):
                raise FileNotFoundError("Could not find file {}".format(rv_read_file))
            if path_to_rv[-3:]=='.gz':
                self._rvfh=gzip.open(path_to_rv,mode='rt')
            elif path_to_rv[-6:]=='.fastq':
                self._rvfh=open(path_to_rv,mode='rt')
            else:
                raise TypeError("Filepath should be a .fastq or a .gz, recieved {}".format(path_to_rv))
            self._rv_records = SeqIO.parse(self._rvfh,'fastq')
        
    def __iter__(self):
        self.n_read=0
        return self
    
    def __next__(self):
        self.n_read+=1
        if self._has_fw:
            fw = str(self._fw_records.__next__().seq)
        else:
            fw = ""
        if self._has_rv:
            rv = revcom(str(self._rv_records.__next__().seq))
        else:
            rv = ""
        return (fw,rv)

class Rule:
    def __init__(self,name,in_read,header,tail,length,window,rename,rename_dict):
        self.name=name
        self.in_read=in_read
        self.header=header
        self.tail=tail
        self.length=length
        self.rename=rename
        self.window=window
        self.rename_dict=rename_dict

    def __repr__(self):
        return(self.header+"_"+self.name+"_"+self.tail+"{}".format(self.length))

def analyze_read(read_pair:Tuple[str,str],rules:List[Rule])->Tuple[str]:
    key = []
    for rule in rules:
        if rule.in_read=='f':
            read = read_pair[0]
        else:
            assert rule.in_read=='r'
            read = read_pair[1]
        substring = read[rule.window[0]:rule.window[1]]
        if rule.rename == 1:
            found=[]
            for dict_key in rule.rename_dict:
                if dict_key in substring:
                    found.append(rule.rename_dict[dict_key])
            if len(found)==0:
                key.append("No BCs in window")
                continue
            if len(found)==1:
                key.append(found[0])
                continue
            if len(found)>1:
                key.append("Multiple BC")
                continue
        else:
            header = rule.header
            if header not in substring:
                key.append("Missing header")
                continue
            removed_header = substring.split(header)[1]
        
            tail = rule.tail
            if tail not in removed_header:
                key.append("Missing tail")
                continue
            removed_tail = tail.join(removed_header.split(tail)[:-1])

            if len(removed_tail) not in rule.length:
                key.append("Length failed")
                continue        

            key.append(removed_tail)

    assert len(key)==len(rules)
    return tuple(key)

def analyze_reads(read_handle:ScreenReads,rules,condition_name = None):
    if condition_name!=None:
        spinner = sp.PieSpinner("Processing {}...%(index)d k reads ... %(elapsed)ds".format(condition_name))
    results = {}
    for read_pair in read_handle:
        if condition_name!=None and read_handle.n_read%25_000==0:
            spinner.next(25)
        key = analyze_read(read_pair,rules)
        if key not in results:
            results[key]=0
        results[key]+=1

    if condition_name!=None:spinner.finish()
    return results

def save_results(res:dict,rules:List[Rule],condition_name:str):
    from src import fastq_process_default 
    fastq_process_default.save_results(res,rules,condition_name)


def df_to_rules(df:pd.DataFrame)->List[Rule]:
    ChavezCIRSPRa_root_dir = Path(__file__).resolve().parent.parent
    rules = []
    for i in range(len(df)):
        length = df.at[i,"length"]
        if "," not in length:
            length = [int(df.at[i,"length"])]
        else:
            length = list(map(lambda x:int(x),length.split(",")))

        if df.at[i,"rename?"]==1:
            rename_dict ={}
            rename_file = df.at[i,"rename dict"]
            rename_df=pd.read_csv(os.path.join(ChavezCIRSPRa_root_dir,rename_file))
            for j in range(0,len(rename_df)):
                From = rename_df.at[j,"from"]
                To = rename_df.at[j,"to"]
                assert From not in rename_dict
                rename_dict[From]=To
        else:
            rename_dict = {}

        rules.append(
            Rule(
                name=df.at[i,"trait name"],
                in_read=df.at[i,"in read"],
                header=df.at[i,"header"],
                tail=df.at[i,"tail"],
                length=length,
                window=[int(df.at[i,"window start"]),int(df.at[i,"window end"])],
                rename = df.at[i,"rename?"],
                rename_dict=rename_dict,
            )
        )
    return rules
