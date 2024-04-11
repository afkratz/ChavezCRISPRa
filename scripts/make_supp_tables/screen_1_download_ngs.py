# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
Downloads NGS reads from SRA using the file 
ChavezCRISPRa/screen_data/screen_download_files.tsv as a guide for which SRR 
numbers to download
The steps are:

1) Locate the SRA tools, and if they are not present, download them

2) Use a file at screen_data/screen_download_files.tsv to identify which SRR 
files to download

3) For each file, if the output .fastq.gz is not already present:
    a) Use prefetch to download the .sra file
    b) For Use fasterq-dump to unpaack the .sra to a .fastq file
    c) Recompress the .fastq to a .fastq.gz file

The final disk size is ~60 gb, and this script takes ~36 hours on my machine
If you would like to, you may be able to get the reads faster by manually 
downloading them, but that may lead to you having to manually edit files such 
as config.json to ensure that all scripts can find their targets

"""
import pandas as pd
import os
from pathlib import Path
import subprocess
import gzip
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
from src import screen_reads_config
import requests

def download_file(url,filename):
    response = requests.get(url,stream=True)
    with open(filename,'wb') as f:
        shutil.copyfileobj(response.raw, f)

def download_sra_tools():
    print("Did not find the sratoolkit in the default path this script expects them to be in")
    print("You can either download them manually and edit this scripts prefetch_path and fasterq_dump_path to point to them, or let us try to download and run them")
    permission = input("Please type \"okay\" if you give this script permission to download the sra-toolkit to chavezCRISPR/external_code/sratookit.3.1.0/:")
    if permission != "okay":
        print("Quitting")
        quit()
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    external_code_dir = os.path.join(ChavezCIRSPRa_root_dir,'external_code')
    
    if not os.path.exists(external_code_dir):os.mkdir(external_code_dir)

    if os.name =='nt':
        download_file(
            "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.1.0/sratoolkit.3.1.0-win64.zip",
            os.path.join(ChavezCIRSPRa_root_dir,'sratoolkit.3.1.0-win64.zip')
        )
        shutil.unpack_archive(os.path.join(ChavezCIRSPRa_root_dir,'sratoolkit.3.1.0-win64.zip'),external_code_dir)
        os.remove(os.path.join(ChavezCIRSPRa_root_dir,'sratoolkit.3.1.0-win64.zip'))
    elif os.name == 'posix':
        download_file(
            "https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/3.1.0/sratoolkit.3.1.0-ubuntu64.tar.gz",
            os.path.join(ChavezCIRSPRa_root_dir,'sratoolkit.3.1.0-ubuntu64.tar.gz')
        )
        shutil.unpack_archive(os.path.join(ChavezCIRSPRa_root_dir,'sratoolkit.3.1.0-ubuntu64.tar.gz'),external_code_dir)
        os.remove(os.path.join(ChavezCIRSPRa_root_dir,'sratoolkit.3.1.0-ubuntu64.tar.gz'))
    else:
        raise(NotImplementedError("We only support windows and linux, and your os seems to be neither"))
    print("Downloaded!")

def gzip_file(infile,outfile):
    with open(infile, 'rb') as f_in:
        with gzip.open(outfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(infile)

def main():
    screen_reads_config.set_up_config()
    storage_dir = screen_reads_config.load_config_storage_dir()

    print("Downloading reads to {}".format(os.path.join(storage_dir,'CRISPRa_screen_reads')))
    screen_reads_dir = os.path.join(storage_dir,"CRISPRa_screen_reads")
    if not os.path.exists(screen_reads_dir):
        os.mkdir(screen_reads_dir)


    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    external_code_dir = os.path.join(ChavezCIRSPRa_root_dir,'external_code')


    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,'screen_data','screen_download_files.tsv'
        ),
        sep = '\t')

    if os.name == 'nt':
        prefetch_path = os.path.join(external_code_dir,'sratoolkit.3.1.0-win64','bin','prefetch.exe')
        fasterq_dump_path = os.path.join(external_code_dir,'sratoolkit.3.1.0-win64','bin','fasterq-dump.exe')
        if not os.path.exists(prefetch_path):
            download_sra_tools()
    elif os.name == 'posix':
        prefetch_path = os.path.join(external_code_dir,'sratoolkit.3.1.0-ubuntu64','bin','prefetch')
        fasterq_dump_path = os.path.join(external_code_dir,'sratoolkit.3.1.0-ubuntu64','bin','fasterq-dump')
        if not os.path.exists(prefetch_path):
            download_sra_tools()

    if not os.path.exists(prefetch_path):
        print("Cant find prefect executable at {}, Quitting".format(prefetch_path))
        quit()
    if not os.path.exists(fasterq_dump_path):
        print("Cant find fasterq_dump_path executable at {}, Quitting".format(fasterq_dump_path))
        quit()
    
    for i in df.index:

        srr = df.at[i,'Accession']
        download_path = os.path.join(screen_reads_dir,srr,'{}.sra'.format(srr))
        condition_name = df.at[i,'SRA.filename']
        
        paired_reads = "," in condition_name

        if not paired_reads:
            final_fastq_gz_location = os.path.join(screen_reads_dir,condition_name)
            print(final_fastq_gz_location)
            if os.path.exists(final_fastq_gz_location):
                print("{} Already present".format(final_fastq_gz_location))
                continue
            else:
                subprocess.run([prefetch_path,srr,'-O',screen_reads_dir ,'-p'])
                
                subprocess.run([fasterq_dump_path,download_path,'--split-files','-O',screen_reads_dir,'--size-check','off','-p'])
                
                print("Compressing reads...")
                gzip_file(
                    infile = os.path.join(screen_reads_dir,'{}.fastq'.format(srr)),
                    outfile = os.path.join(screen_reads_dir,final_fastq_gz_location)
                    )
                shutil.rmtree(os.path.join(screen_reads_dir,srr))

        else:
            final_fastq_location_1,final_fastq_location_2 = condition_name.split(",")
            final_fastq_location_1=final_fastq_location_1.strip()
            final_fastq_location_2=final_fastq_location_2.strip()
            print(final_fastq_location_1,final_fastq_location_2)
            if os.path.exists(os.path.join(screen_reads_dir,final_fastq_location_1)) and os.path.exists(os.path.join(screen_reads_dir,final_fastq_location_2)):
                print("{},{} Already present".format(final_fastq_location_1,final_fastq_location_2))
                continue
            else:
                subprocess.run([prefetch_path,srr,'-O',screen_reads_dir ,'-p'])
                subprocess.run([fasterq_dump_path,download_path,'--split-files','-O',screen_reads_dir,'--size-check','off','-p'])
                print("Compressing fw reads...")
                gzip_file(
                    infile = os.path.join(screen_reads_dir,'{}_1.fastq'.format(srr)),
                    outfile = os.path.join(screen_reads_dir,final_fastq_location_1)
                    )
                print("Compressing rv reads...")
                gzip_file(
                    infile = os.path.join(screen_reads_dir,'{}_2.fastq'.format(srr)),
                    outfile = os.path.join(screen_reads_dir,final_fastq_location_2)
                    )
                shutil.rmtree(os.path.join(screen_reads_dir,srr))
        print()

if __name__ == "__main__":
    main()