# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
This script analyzes a set of 
This script will run the main function from the following files:
    01_process_single_domain_plasmid.py
    02_process_single_domain_screen.py 
    03_process_bipartite_plasmid.py       
    04_process_bipartite_screen.py
    05_process_tripartite_plasmid.py
    06_process_tripartite_screen.py
These files each process a set of NGS reads in a .fastq.gz, all of which can be
downloaded with the download_ngs.py script. It outputs a file which consists of 
counts of barcodes and UMIs for each condition. Because different screens had
different structures (number of barcodes etc), they are processed one at a time.

Finally, it calls 07_score_screens.py, which converts the read-counts into 
activation scores, toxicity scores, read-bin counts, etc.

"""
import importlib
for file in "01_process_single_domain_plasmid","02_process_single_domain_screen","03_process_bipartite_plasmid",\
            "04_process_bipartite_screen","05_process_tripartite_plasmid","06_process_tripartite_screen",\
            "07_score_screens":
    print("Running {}.py".format(file))
    importlib.import_module(file).main()
    print("File {}.py completed".format(file))

