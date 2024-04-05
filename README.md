## Code supporting "Combinatorial protein engineering to identify improved CRISPR activators"

### Summary

This repository contains code and configuration files required to reproduce the findings of the Manuscript "Combinatorial protein engineering to identify improved CRISPR activators" by M. Giddins*, A Kratz*, L Wei‡, and A Chavez‡ (*: Contributed equally, ‡: Jointly supervised)

### Overview

Pipeline overall can be divided into two high-level steps:

1) Generating the Supp tables

2) Generating the Figure Source Data tables

The first step covers the raw steps to process the input data, including NGS reads, to produce processed output files.

The code for this step is found in scripts/make_supp_tables, and can be run in the following steps:

1) prescreen scripts, ordered from prescreen_1 to prescreen_5. These process the data relating to our manual screen of 231 domains fused to dCas9.

2) screen scripts, ordered from screen_1 to screen_9. These download the NGS reads from SRA, extract barcodes from them, and score screen members. 

The second section, contained in scripts/generate_figures, converts the outputs from the first step into the source data tables for figures 2-5, formatted as submitted. For each of these files, there is one script in generate_figures which generates each Source Data Figure excel sheet.

### Requirements

This code was written on Linux with occasional testing in Windows. Many packages are needed only for a few scripts which not all users may run. For full list, please see package-list.txt

### Contact and inquiries

For questions relating to this code, please contact Alexander Kratz at afk2133@cumc.columbia.edu
