## Code supporting "Combinatorial protein engineering to identify improved CRISPR activators"

### Summary

This repository contains code and configuration files required to reproduce the findings of the Manuscript "Combinatorial protein engineering to identify improved CRISPR activators" by M. Giddins*, A Kratz*, L Wei‡, and A Chavez‡ (*: Contributed equally, ‡: Jointly supervised)

### Overview

Pipeline overall can be divided into two high-level steps:

1) Generating the Supp tables

2) Generating the Figure Source Data tables

The first step covers the raw steps to process the input data, including NGS reads, to produce processed output files.

The code for this step is found in `scripts/make_supp_tables`, and can be run in the following steps:

1) prescreen scripts, ordered from prescreen_1 to prescreen_4. These process the data relating to our manual screen of 231 domains fused to dCas9.

2) screen scripts, ordered from screen_1 to screen_9. These download the NGS reads from SRA, extract barcodes from them, and score screen members. 

The second section, contained in `scripts/generate_figures`, converts the outputs from the first step into the source data tables for figures 2-5, formatted as submitted. For each of these files, there is one script in generate_figures which generates each Source Data Figure excel sheet.

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

Before running any code, ensure that you are in the chavezcrispra environment by running

```
conda activate chavezcrispra
```

Then run any script with the command

```
python -script-name-.py  
```

### Detailed summary and run times

#### make_supp_tables

- **prescreen_1_validate_sequences_sources.py**
  
  - Description - Confirms that prescreen sequences are found within the uniprot sequence listed in Supp 1, throws an error if it fails to locate a sequence
  
  - Input files 
    
    - `InputData/Supplementary Table 1.xlsx`
  
  - Output files - None
  
  - Estimated run time - 10 minutes

- **prescreen_2_run_uclust.py**
  
  - Description - Guides the user to download and run uclust executable to cluster prescreen sequences at 50% identity. Assigns status as either a centroid or non-centroid and cluster membership to the prescreen sequences.
  
  - Input files 
    
    - `InputData/Supplementary Table 1.xlsx`
  
  - Output files 
    
    - cluster fastas in `outputs/prescreen_results/clusters/`
    
    - `outputs/prescreen_results/centroids.fasta`
    
    - `output/prescreen_results/2_manually_tested_clusters_assigned.csv`
  
  - Estimated run time - 1 minute

- **prescreen_3_charachterize_domains.py**
  
  - Description - Uses package [localCIDER](https://pappulab.github.io/localCIDER/) to calculate biochemical traits of prescreen sequences
  
  - Input files
    
    - `output/prescreen_results/2_manually_tested_clusters_assigned.csv`
  
  - Output files
    
    - `output/prescreen_results/3_manually_tested_biochem_charachterized.csv`
  
  - Estimated run time - 1 minute

- **prescreen_4_run_PADDLE_make_supp2.py**
  
  - Description - Guides the user to clone the [PADDLE github repository](https://github.com/asanborn/PADDLE) which it then runs to predict if our prescreen sequences are strong or medium transactivation domains. Calculates precision and recall for PADDLE.
  
  - Input files
    
    - `output/prescreen_results/3_manually_tested_hits_and_clusters_assigned.csv`
  
  - Output files
    
    - `output/prescreen_results/4_PADDLE_precision_recall_data.csv`
    
    - `SuppTables/Supplementary Table 2.csv`
  
  - Estimated run time - 10 minutes without GPU acceleration, 4 minutes on GPU

- **screen_1_download_ngs.py** 
  
  - Description - Guides the user to designate a directory to recieve the NGS reads from the screen. This is done to allow users to specify external large-storage devices. Guides the user to download the sra_toolkit. Downloads NGS reads from SRA and converts them to .fastq.gz files. Skips over existing files.
  
  - Input files
    
    - `ScreenData/screen_download_files.tsv`
  
  - Output files
    
    - 124 fastq.gz files, total size 55.8 gb
  
  - Estimated run time - 36 hours (Dependent on internet speed)

- **screen_2_process_single_domain_plasmid.py**
  
  - Description - Processes NGS reads to produce barcode counts for the single domain pre-selection plasmid library
  
  - Input files
    
    - .fastq.gz files
    
    - `ScreenData/traits/single_domain_plasmid_traits.csv`
    
    - `ScreenData/conditions/single_domain_plasmid_conditions.csv`
  
  - Output files
    
    - `output/screen_results/processed_reads/single_domain_plasmid/single_domain_plasmid.csv`
  
  - Estimated run time - 1 minute

- **screen_3_process_single_domain_screen.py**
  
  - Description - Processes NGS reads to produce barcode counts for the single domain screen results
  
  - Input files
    
    - .fastq.gz files
    
    - `ScreenData/traits/single_domain_screen_traits.csv`
    
    - `ScreenData/conditions/single_domain_screen_conditions.csv`
  
  - Output files
    
    - barcode counts located at `output/screen_results/processed_reads/single_domain_sorted/`
  
  - Estimated run time - 1 minute

- **screen_4_process_bipartite_plasmid.py**
  
  - Description - Processes NGS reads to produce barcode counts for the bipartite pre-selection plasmid library
  
  - Input files
    
    - .fastq.gz files
    
    - `ScreenData/traits/bipartite_plasmid_traits.csv`
    
    - `ScreenData/conditions/bipartite_plasmid_conditions.csv`
  
  - Output files
    
    - `output/screen_results/processed_reads/bipartite_plasmid/bipartite_plasmid.csv`
  
  - Estimated run time - 1 minute

- **screen_5_process_bipartite_screen.py**
  
  - Description - Processes NGS reads to produce barcode counts for the bipartite screen results
  
  - Input files
    
    - .fastq.gz files
    
    - `ScreenData/traits/bipartite_screen_traits.csv`
    
    - `ScreenData/conditions/bipartite_screen_conditions.csv`
  
  - Output files
    
    - barcode counts located at `output/screen_results/processed_reads/bipartite_sorted/`
  
  - Estimated run time - 5 minutes

- **screen_6_process_tripartite_plasmid.py**
  
  - Description - Processes NGS reads to produce barcode counts for the tripartite pre-selection plasmid library
  
  - Input files
    
    - .fastq.gz files
    
    - `ScreenData/traits/tripartite_plasmid_traits.csv`
    
    - `ScreenData/conditions/tripartite_plasmid_conditions.csv`
  
  - Output files
    
    - `output/screen_results/processed_reads/tripartite_plasmid/tripartite_plasmid.csv`
  
  - Estimated run time - 1 minute

- **screen_7_process_tripartite_screen.py**
  
  - Description - Processes NGS reads to produce barcode counts for the tripartite screen results
  
  - Input files
    
    - .fastq.gz files
    
    - `ScreenData/traits/tripartite_screen_traits.csv`
    
    - `ScreenData/conditions/tripartite_screen_conditions.csv`
  
  - Output files
    
    - barcode counts located at `output/screen_results/processed_reads/tripartite_sorted/`
  
  - Estimated run time - 6 hours

- **screen_8_score_screens.py**
  
  - Description - Processes the barcode counts from the previous steps to calculate normalized bin-counts, activity scores, and toxicity scores for all 3 screens
  
  - Input files
    
    - The 6 output files from screen_2 to screen_7 (above)
  
  - Output files
    
    - Screen bin counts, stored in `output/screen_results/screen_bin_counts/`
    
    - Screen activity scores, stored in `output/screen_results/screen_scores/`
    
    - Screen tox scores, stored in `output/screen_results/screen_toxicity/`
  
  - Estimated run time - 30 minutes

- **screen_9_make_supp4_5.py**
  
  - Description - Generates supp table 4 and 5 from the outputs of screen_8_score_screens.py
  
  - Input files
    
    - Screen activity score csv's
    
    - Screen toxicity score csv's
  
  - Output files
    
    - `SuppTables/Supplementary Table 4.csv`
    
    - `SuppTables/Supplementary Table 5.csv`
  
  - Estimated run time - 1 minute

- **combine_supps.py**
  
  - Description - Combines the supp table .csvs into one .xslx for easier transmission
  
  - Input files
    
    - Supp tables 1-9, located at `SuppTables/Supplementary table X.csv`
  
  - Output files
    
    - `SuppTables/Supplementary Tables 1-9.xlsx`
  
  - Estimated run time - 1 minute

#### generate_figures

- **generate_figure_2_and_supp3**
  
  - Description - Generates `Figure 2 and Supplementary Figure 3.xlsx` which contains analysis of various elements of the prescreen results, specifically biochemical traits and native protein location
  
  - Input files
    
    - `output/prescreen_results/2_manually_tested_clusters_asssigned.csv`
    
    - `output/prescreen_results/3_manually_tested_biochem_charachterized.csv`
  
  - Ouput files
    
    - `FigureSourceData/Figure 2 and Supplementary Figure 3.xlsx`
  
  - Estimated run time - 1 minute

- **generate_figure3_and_supp465.py**
  
  - Description - Generates `Figure 3 and Supplementary Figures 4-6.xlsx` which contains high level analysis of screen results, including the rep-rep correlations, correlation to manual validation, and distribution of activator reads in the pre-selection plasmid library.
  
  - Input files
    
    - Screen bin counts, stored in `output/screen_results/screen_bin_counts/`
    
    - Screen activity scores, stored in `output/screen_results/screen_scores/`
    
    - Manual screen validation `InputData/Manual_validation_random_clones.csv`
  
  - Output files
    
    - `FigureSourceData/Figure 3 and Supplementary Figure 4-6.xlsx`
  
  - Estimated run time - 1 minute

- **generate_figure_4_and_supp_7_16a17.py**
  
  - Description - Generates `Figure 4 and Supplementary Figures 7-16a and 17.xlsx` which contains analysis of toxicity within the screen, including correlations between replicates, correlations between screens, toxicity as as function of copy number, as a function of target, as a function of length, as a function of activity, as a function of biochemical traits, and manual validation of toxicity.
  
  - Input files
    
    - Screen toxicity scores, `output/screen_results/screen_toxicity/`
    
    - Manual toxicity validation `InputData/GFP_competition_results.csv`
  
  - Output files
    
    - `FigureSourceData/Figure 4 and Supplementary Figures 7-16a and 17.xlsx`
  
  - Estimated run time - 2 minutes

- **generate_figure5_and_supp16b18_21.py**
  
  - Description - Generates FigureSourceData/Figure 5 and Supplementary Figures 16b and 18-21.xlsx which contains analysis of activity within the screen, including correlations between replicates, correlations between screens, activity as a function of copy number, as a function of activator position, activity as a synergistic or anti-synergistic phenomenon.
  
  - Input files
    
    - Screen activity scores
  
  - Output files
    
    - `Figure 5 and Supplementary Figures 16b and 18-21.xlsx`
  
  - Estimated run time - 1 minute

### Contact and inquiries

For questions relating to this code, please contact Alexander Kratz at afk2133@cumc.columbia.edu
