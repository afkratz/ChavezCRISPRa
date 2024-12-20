# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
Uses UCLUST (https://drive5.com/usearch/manual/uclust_algo.html) to cluster our 
screen sequences at an identity of 0.5
"""

import os
from pathlib import Path
import hashlib
import gzip
import requests
import pandas as pd
import numpy as np
import shutil
import glob
from Bio import SeqIO



def download_file(url,filename):
    response = requests.get(url,stream=True)
    with open(filename,'wb') as f:
        shutil.copyfileobj(response.raw, f)

def decompress_gzip(filename):
    with gzip.open(filename,'rb') as f_in:
        with open(filename[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(filename)

def calculate_md5(filename):
    with open(filename, 'rb') as f:
        md5_hash = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
        return md5_hash.hexdigest()
uclust_path = ""

def download_uclust():
    permission = input('This script will download uclust for windows or linux and place the executable in the external_code directory. Please type "okay" to give permission:')
    if permission != "okay":
        print("Quitting")
        quit()
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    external_code_dir = os.path.join(ChavezCIRSPRa_root_dir,'external_code')
    if not os.path.exists(external_code_dir):os.mkdir(external_code_dir)
    if os.name =='nt':#We are in windows
        uclust_path = os.path.join(external_code_dir,'uclust.exe')
        if not os.path.exists(uclust_path):
            download_file(
                'https://drive5.com/downloads/usearch11.0.667_win32.exe.gz',
                uclust_path+'.gz'
                )
            expected_md5='fd5e149d0977a570cdaa10652a994d45'
            downloaded_file_md5 = calculate_md5(uclust_path+'.gz')
            if downloaded_file_md5 != expected_md5:
                print("MD5 for uclust does not match expected value...")
                r='x'
                while r not in 'qcQC':
                    r = input("Quit or continue? Q/C:")
                if r in 'Qq':
                    print("Quitting")
                    exit()
                else:
                    print("Continuing with un-verified uclust.exe")
            decompress_gzip(uclust_path+'.gz')
            return 
    elif os.name == 'posix':#We are in linux
        uclust_path = os.path.join(external_code_dir,'uclust')
        if not os.path.exists(uclust_path):
            download_file(
                'https://drive5.com/downloads/usearch11.0.667_i86linux32.gz',
                uclust_path+'.gz'
                )
            expected_md5='27cc6b779b899daa5d17a95fd0eeb69c'
            downloaded_file_md5 = calculate_md5(uclust_path+'.gz')
            if downloaded_file_md5 != expected_md5:
                print("MD5 for uclust does not match expected value...")
                r='x'
                while r not in 'qcQC':
                    r = input("Quit or continue? Q/C:")
                if r in 'Qq':
                    print("Quitting")
                    exit()
                else:
                    print("Continuing with un-verified uclust.exe")
            decompress_gzip(uclust_path+'.gz')
            os.chmod(uclust_path, os.stat(uclust_path).st_mode | 0o111)
            return 
    else:
        print("Sorry, we only natively support windows or linux")
        quit()

def call_uclust():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    external_code_dir = os.path.join(ChavezCIRSPRa_root_dir,'external_code')

    if os.name =='nt':#We are in windows
        uclust_path = os.path.join(external_code_dir,'uclust.exe')

    elif os.name =='posix':#We are in windows
        uclust_path = os.path.join(external_code_dir,'uclust')

    else:
        print("Sorry, I only wrote the code to support windows or linux")
        """
        Feel free to edit this file to point the varial uclust_path to where ever you have uclust installed
        """
        raise NotImplementedError()
    
    if not os.path.exists(uclust_path):
        download_uclust()

    #Make paths for output if they don't exist
    if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"screen_output")):
        os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"screen_output"))

    if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","prescreen_results")):
        os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","prescreen_results"))

    if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","prescreen_results","clusters")):
        os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","prescreen_results","clusters"))

    #Load input dataframe
    df = pd.read_excel(
        os.path.join(ChavezCIRSPRa_root_dir,'Supplementary Files','Supplementary Data 1.xlsx'),
        index_col='Domain ID'
    )

    #Drop protein folding domains
    df = df[df["Role"]=="Activator"]


    #Write sequences to a .fasta for clustering
    with open(
            os.path.join(ChavezCIRSPRa_root_dir,"sequences_to_cluster.fasta"),
            'w') as fh:
        for i in df.index:
            fh.write(">{}\n".format(i))
            fh.write(df.at[i,"AA sequence"]+"\n")

    #Run uclust
    uclust_command = uclust_path +" -cluster_fast {} -id 0.5 -centroids {} -clusters {}".format(
        os.path.join(ChavezCIRSPRa_root_dir,"sequences_to_cluster.fasta"),
        os.path.join(ChavezCIRSPRa_root_dir,"screen_output","prescreen_results","centroids.fasta"),
        os.path.join(ChavezCIRSPRa_root_dir,"screen_output","prescreen_results","clusters/"),
    )

    os.system(uclust_command)

    #Clean up after ourselves
    os.remove(os.path.join(ChavezCIRSPRa_root_dir,"sequences_to_cluster.fasta"))

def assign_clusters():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    #Load input dataframe

    seq_df = pd.read_excel(
        os.path.join(ChavezCIRSPRa_root_dir,'Supplementary Files','Supplementary Data 1.xlsx'),
        index_col='Domain ID'
    )

    #Load score data
    score_df = pd.read_excel(
        os.path.join(ChavezCIRSPRa_root_dir,"Supplementary Files","Supplementary Data 2.xlsx"),
        index_col="Domain ID"
    )
    for target in "EPCAM","CXCR4","Reporter":
        score_df['Hit on {}'.format(target)]=score_df['{} FC_average'.format(target)]>2
    score_df['Hit on any']=score_df['Hit on EPCAM']|score_df['Hit on CXCR4']|score_df['Hit on Reporter']


    #Check that all sequences in the sequence dataframe have scores

    assert set(seq_df.index)==set(score_df.index)
    


    #Combine dataframes
    seq_df = seq_df.join(score_df)

    #Drop protein folding domains
    seq_df = seq_df[seq_df["Role"]=="Activator"]

    #Assign clusters and centroid status
    seq_df['Cluster']=np.nan
    seq_df['Is centroid']=False
    for file in glob.glob(os.path.join(ChavezCIRSPRa_root_dir,"screen_output","prescreen_results","clusters","*")):
        cluster = os.path.split(file)[-1]
        for cluster_member_number,record in enumerate(SeqIO.parse(file,"fasta")):
            domainID = record.id
            seq_df.at[domainID,"Cluster"]=int(cluster)
            seq_df.at[domainID,"Is centroid"] = cluster_member_number==0
    seq_df.to_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "prescreen_results",
            "1_manually_tested_clusters_assigned.csv")
        )

def main():
    call_uclust()
    assign_clusters()

if __name__=="__main__":
    main()
