import pandas as pd
import os
from pathlib import Path
import subprocess
import gzip
import shutil
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
from src import screen_reads_config


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

    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,'screen_data','screen_download_files.tsv'
        ),
        sep = '\t')

    if os.name == 'nt':
        prefetch_path = os.path.expanduser("~/Documents/GitHub/sratoolkit.3.1.0-win64/bin/prefetch.exe")
        fasterq_dump_path = os.path.expanduser("~/Documents/GitHub/sratoolkit.3.1.0-win64/bin/fasterq-dump.EXE")
    elif os.name == 'posix':
        prefetch_path = os.path.expanduser("~/sratoolkit.3.1.0-ubuntu64/bin/prefetch")
        fasterq_dump_path = os.path.expanduser("~/sratoolkit.3.1.0-ubuntu64/bin/fasterq-dump")
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
                
                subprocess.run([fasterq_dump_path,download_path,'--split-files','-O',screen_reads_dir])
                
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
                subprocess.run([fasterq_dump_path,download_path,'--split-files','-O',screen_reads_dir])
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