from pathlib import Path
import os
import json
def load_config_storage_dir()->str:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent
    config_file = os.path.join(ChavezCIRSPRa_root_dir,'config.json')
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config.get("ngs_storage_directory", None)

def set_up_config():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent
    config_file = os.path.join(ChavezCIRSPRa_root_dir,'config.json')
    if os.path.exists(config_file):
        storage_dir = load_config_storage_dir()
        if not os.path.exists(storage_dir):
            raise FileNotFoundError("Dir {} from config.json does not exist".format(storage_dir))
    else:
        print("Enter path to an existing directory to download NGS reads to")
        print("Download size is 60.5 gb")
        print("Will create a subdir within the directory to hold the reads")
        print("Current path (for reference):")
        print(os.getcwd())
        while True:
            print("Enter path to an existing directory to download NGS reads to: ",end="")
            storage_dir = input()
            if os.path.exists(storage_dir):
                print("Saving config data {} to ChavezCRISPRa/config.json".format(storage_dir))
                break
            else:
                print("Directory {} not found".format(storage_dir))
        config = {"ngs_storage_directory" : storage_dir}
        with open(
            os.path.join(ChavezCIRSPRa_root_dir,'config.json'),'w') as f:
            json.dump(config,f,indent=4)

def get_screen_reads_dir():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent
    config_file = os.path.join(ChavezCIRSPRa_root_dir,'config.json')
    if os.path.exists(config_file):
        storage_dir = load_config_storage_dir()
        reads_dir = os.path.join(storage_dir,'CRISPRa_screen_reads')
        return reads_dir
    else:
        print("No existing file config.json specifying where NGS reads are")
        print("We recommend running download_ngs.py to set up config.json")
        print("Otherwise, see src/screen_reads_config.py for guidance on manually downloading NGS reads")
        """
        config.json should look like this:
            {
                "ngs_storage_directory": "/SOME_DIR/"
            }
            Where within SOME_DIR there is a subdirectory named CRISPRa_screen_reads that contains the .fastq.gz's that will be processed
            Example:
            
            $ ls CRISPRa_screen_reads/
            bi_CXCR4_1_bin_1.fastq.gz bi_Reporter_1_NS.fastq.gz sd_EPCAM_2_NS.fastq.gz tri_CXCR4_2_bin_2_fw.fastq.gz tri_EPCAM_2_bin_4_rv.fastq.gz
            ...
            tri_Reporter_2_bin_4_fw.fastq.gz tri_Reporter_2_bin_4_rv.fastq.gz tri_Reporter_2_NS_fw.fastq.gz tri_Reporter_2_NS_rv.fastq.gz
        """
        raise FileNotFoundError()