## Code supporting "Combinatorial protein engineering to identify improved CRISPR activators"

### Summary

This repository contains code and configuration files required to reproduce the findings of the manuscript "Combinatorial protein engineering to identify improved CRISPR activators" by M. Giddins*, A. Kratz*, L. Wei‡, and A. Chavez‡ (*: Contributed equally, ‡: Jointly supervised)

### Overview

Pipeline overall can be divided into two high-level steps:

1) Generating the Supp tables, bin counts, activation scores, and toxicity scores

2) Generating the Figure Source Data tables

The first step covers the raw steps to process the input data, including NGS reads, to produce processed output files.

The code for this step is found in `scripts/make_supp_tables`, and can be run in the following steps:

1) prescreen scripts, ordered from prescreen_1 to prescreen_4. These process the data relating to our manual screen of 230 domains fused to dCas9.

2) screen scripts, ordered from screen_1 to screen_9. These download the NGS reads from SRA, extract barcodes from them, and score screen members. 

The second section, contained in `scripts/generate_figures`, converts the outputs from the first step into the source data tables for figures 2-5, formatted as submitted. There is one script in generate_figures for each Source Data Figure excel sheet.

### Requirements

This code was written on Linux with occasional testing in Windows. It requires a python environment, as well as the git CLI.

The environmental dependencies that python requires are:

```
Conda installable packages:
 python=3.9
 biopython=1.83
 pandas=2.2.2
 tensorflow=2.10
 openpyxl=3.1.2
 xlsxwriter=3.1.9
Pip installable packages:
 localcider==0.1.21
 progress==1.6
```

### Installation

We recommend running this code in a Conda environment. We provide two files, conda_packages.txt and pip_packages.txt which specify the external software needed to run all scripts to reproduce our results.

##### Step 1: Install Conda

If you haven't already installed Conda, you can download and install Miniconda or Anaconda by following the instructions on their [official website.](https://conda.io/projects/conda/en/latest/index.html)

##### Step 2: Set up environment

Example installation instructions:

```
conda config --set channel_priority flexible
conda env create --name chavezcrispra --file conda_packages.txt
conda activate chavezcrispra
pip install -r pip_packages.txt
```

Estimated install time fifteen minutes

##### Step 3: Running scripts:

Before running any code, ensure that you are in the chavezcrispra environment by running `conda activate chavezcrispra`, then run any script by navigating to the directory containing it and then running the command `python -script-name-.py`

### Detailed summary and run times

#### make_supp_tables

- **prescreen_1_run_uclust.py**
  - Description - Guides the user to download and run uclust executable to cluster prescreen sequences at 50% identity. Assigns status as either a centroid or non-centroid and cluster membership to the prescreen sequences.
  
  - Input files 
    
    - input_data/Supplementary Table 1.xlsx`
  
  - Output files 
    
    - cluster fastas in `screen_output/prescreen_results/clusters/`
    
    - `screen_output/prescreen_results/centroids.fasta`
    
    - `screen_output/prescreen_results/2_manually_tested_clusters_assigned.csv`
  
  - Estimated run time - 1 minute
- **prescreen_2_characterize_domains.py**
  - Description - Uses package [localCIDER](https://pappulab.github.io/localCIDER/) to calculate biochemical traits of prescreen sequences.
  
  - Input files
    
    - `screen_output/prescreen_results/1_manually_tested_clusters_assigned.csv`
  
  - Output files
    
    - `screen_output/prescreen_results/2_manually_tested_biochem_charachterized.csv`
  
  - Estimated run time - 1 minute
- **prescreen_3_run_PADDLE_make_supp3.py**
  - Description - Guides the user to clone the [PADDLE github repository](https://github.com/asanborn/PADDLE) which it then runs to predict if our prescreen sequences are strong or medium transactivation domains. Calculates precision and recall for PADDLE.
  
  - Input files
    
    - `screen_output/prescreen_results/1_manually_tested_clusters_assigned.csv`
  
  - Output files
    
    - `screen_output/prescreen_results/3_PADDLE_precision_recall_data.csv`
    
    - `Supplementary Files/Supplementary Data 3.xlsx`
  
  - Estimated run time - 10 minutes without GPU acceleration, 4 minutes on GPU
- **screen_1_download_ngs.py** 
  
  - Description - Guides the user to designate a directory to receive the NGS reads from the screen. This is done to allow users to specify external large-storage devices. Guides the user to download the sra_toolkit. Downloads NGS reads from SRA and converts them to .fastq.gz files.
  
  - Input files
    
    - `screen_data/screen_download_files.tsv`
  
  - Output files
    
    - 140 fastq.gz files, total size 57 gb
  
  - Estimated run time - 36 hours (Dependent on internet speed)
- **screen_2_process_single_domain_plasmid.py**
  
  - Description - Processes NGS reads to produce barcode counts for the single domain plasmid library.
  
  - Input files
    
    - .fastq.gz files
    
    - `screen_data/traits/single_domain_plasmid_traits.csv`
    
    - `screen_data/conditions/single_domain_plasmid_conditions.csv`
  
  - Output files
    
    - `screen_output/screen_results/processed_reads/single_domain_plasmid/single_domain_plasmid.csv`
  
  - Estimated run time - 1 minute
- **screen_3_process_single_domain_screen.py**
  
  - Description - Processes NGS reads to produce barcode counts for the single domain screen results.
  
  - Input files
    
    - .fastq.gz files
    
    - `screen_data/traits/single_domain_screen_traits.csv`
    
    - `screen_data/conditions/single_domain_screen_conditions.csv`
  
  - Output files
    
    - barcode counts located at `screen_output/screen_results/processed_reads/single_domain_sorted/`
  
  - Estimated run time - 1 minute
- **screen_4_process_bipartite_plasmid.py**
  
  - Description - Processes NGS reads to produce barcode counts for the bipartite plasmid library.
  
  - Input files
    
    - .fastq.gz files
    
    - screen_data/traits/bipartite_plasmid_traits.csv`
    
    - `screen_data/conditions/bipartite_plasmid_conditions.csv`
  
  - Output files
    
    - `screen_output/screen_results/processed_reads/bipartite_plasmid/bipartite_plasmid.csv`
  
  - Estimated run time - 1 minute
- **screen_5_process_bipartite_screen.py**
  
  - Description - Processes NGS reads to produce barcode counts for the bipartite screen results.
  
  - Input files
    
    - .fastq.gz files
    
    - `screen_data/traits/bipartite_screen_traits.csv`
    
    - `screen_data/conditions/bipartite_screen_conditions.csv`
  
  - Output files
    
    - barcode counts located at `output/screen_results/processed_reads/bipartite_sorted/`
  
  - Estimated run time - 5 minutes
- **screen_6_process_tripartite_plasmid.py**
  
  - Description - Processes NGS reads to produce barcode counts for the tripartite plasmid library.
  
  - Input files
    
    - .fastq.gz files
    
    - screen_data/traits/tripartite_plasmid_traits.csv`
    
    - `screen_data/conditions/tripartite_plasmid_conditions.csv`
  
  - Output files
    
    - `screen_output/screen_results/processed_reads/tripartite_plasmid/tripartite_plasmid.csv`
  
  - Estimated run time - 1 minute
- **screen_7_process_tripartite_screen.py**
  
  - Description - Processes NGS reads to produce barcode counts for the tripartite screen results.
  
  - Input files
    
    - .fastq.gz files
    
    - `screen_data/traits/tripartite_screen_traits.csv`
    
    - `screen_data/conditions/tripartite_screen_conditions.csv`
  
  - Output files
    
    - barcode counts located at screen_output/screen_results/processed_reads/tripartite_sorted/`
  
  - Estimated run time - 6 hours
- **screen_8_score_screens.py**
  
  - Description - Processes the barcode counts from the previous steps to calculate normalized bin-counts, activation scores, and toxicity scores for all 3 screens.
  
  - Input files
    
    - The 6 output files from screen_2 to screen_7 (above)
  
  - Output files
    
    - Screen bin counts, stored in `screen_output/screen_results/screen_bin_counts/`
    
    - Screen activation scores, stored in `screen_output/screen_results/screen_scores/`
    
    - Screen tox scores, stored in `screen_output/screen_results/screen_toxicity/`
  
  - Estimated run time - 30 minutes
- **screen_9_make_supp4_5.py**
  
  - Description - Generates supp table 4 and 5 from the outputs of screen_8_score_screens.py.
  - Input files
    
    - Screen activation score csv's
    
    - Screen toxicity score csv's
  - Output files
    
    - `Supplementary Files/Supplementary Data 4.xlsx`
    
    - `Supplementary Files/Supplementary Data 5.xlsx`
  - Estimated run time - 1 minute
- **postscreen_1_process_minilib.py**
  - Description - Processes NGS reads to produce barcode counts for the tripartite mini-screen which we performed after the main screen to validate toxicity.
  - Input files
    - .fastq.gz files
    - `screen_data/traits/tripartite_plasmid_traits.csv`
    - `screen_data/conditions/tripartite_minilib.csv`
  - Output files
    - barcode counts located at `screen_output/screen_results/processed_reads/tripartite_minilib/`
  - Estimated run time - 1 minute
- **postscreen_2_calc_tox_minilib.py**
  - Description - Calculates toxicity scores for the minilibrary constructs in multiple cell lines.
  - Input files
    - output files from postscreen_1_process_minilib.py
  - Output files
    - minilib tox scores, stored in `screen_output/screen_results/screen_toxicity/`
  - Estimated run time - 1 minute

#### generate_figures

- **generate_figure_2_and_supp4
  - Description - Generates `Source Data Figure 2 and Supplementary Figure 4.xlsx` which contains analysis of various elements of the prescreen results, specifically biochemical traits and native protein location.
  
  - Input files
    
    - `screen_output/prescreen_results/2_manually_tested_clusters_asssigned.csv`
    
    - `screen_output/prescreen_results/3_manually_tested_biochem_charachterized.csv`
  
  - Output files
    
    - `Figure Source Data/Source Data Figure 2 and Supplementary Figure 4.xlsx`
  
  - Estimated run time - 1 minute
  
- **generate_figure3_and_supp567.py**
  - Description - Generates `Source Data Figure 3 and Supplementary Figures 5-7.xlsx` which contains high level analysis of screen results, including the rep-rep correlations, correlation to manual validation, and distribution of activator reads in the plasmid library.
  
  - Input files
    
    - Screen bin counts, stored in `screen_output/screen_results/screen_bin_counts/`
    
    - Screen activation scores, stored in `screen_output/screen_results/screen_scores/`
    
    - Manual screen validation `input_data/Manual_validation_random_clones.csv`
  
  - Output files
    
    - `Figure Source Data/Source Data Figure 3 and Supplementary Figures 5-7.xlsx`
  
  - Estimated run time - 1 minute
  
- **generate_figure_4_and_supp_8_18a19.py**
  - Description - Generates `Source Data Figure 4 and Supplementary Figures 8-18a and 19.xlsx` which contains analysis of toxicity within the screen, including consistency between biological replicates, correlation of toxicity when targeting different genes, toxicity as as function of copy number, as a function of target, as a function of length, as a function of activation, as a function of biochemical traits, and manual validation of toxicity.
  
  - Input files
    
    - Screen toxicity scores, `screen_output/screen_results/screen_toxicity/`
    
    - Manual toxicity validation `input_data/GFP_competition_results.csv`
  
  - Output files
    
    - `Figure Source Data/Source Data Figure 4 and Supplementary Figures 8-18a and 19.xlsx`
  
  - Estimated run time - 2 minutes
  
- **generate_figure5_and_supp18b20_23.py**
  - Description - Generates `Source Data Figure 5 and Supplementary Figures 18b and 20-23.xlsx` which contains analysis of activation within the screen, including consistency between biological replicates, correlations of activity when targeting different genes, activation as a function of copy number, as a function of activator position, activation as a synergistic or anti-synergistic phenomenon.
  
  - Input files
    
    - Screen activation scores
  
  - Output files
    
    - `Figure Source Data/Source Data Figure 5 and Supplementary Figures 18b and 20-23.xlsx`
  
  - Estimated run time - 1 minute

### Contact and inquiries

For questions relating to this code, please contact Alexander Kratz at afk2133@cumc.columbia.edu or kratzalexander1313@gmail.com
