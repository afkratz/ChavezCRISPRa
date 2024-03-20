# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
This script runs some preliminary processing on our single-domain pre screen, in
which we fused 225 domains to dCas9 and transfected them into HEK cells, 
staining and flowing them to measure the effect of these tools on expression of 
those proteins. This process is broken up into four steps, which this script
will execute all of. 
This script will run the main function from the following files:

    01_run_uclust:
        Downloads and runs UCLUST 
        https://drive5.com/usearch/manual/uclust_algo.html
        to cluster our screen sequences at an identity of 0.5

    02_assign_hits_and_clusters:
        Analyzes UCLUST output to assign sequences to clusters of similar 
        activators, annotate them as either being the centroid of their cluster
        or not, as well as assign them as either being hits or misses on the 
        three targets


    03_charachterize_manual_tested_domains:
        This script uses the LocalCIDER library
        https://pappulab.wustl.edu/localCIDER.html
        to analyze the sequences of the domains we tested, assigning the
        following traits:
            NCPR - net charge per residue, a measure of acidity
            Hydropathy - Kyte-Doolittle hydropathy aka hydrophobicity
            Disorder promoting fraction - Fraction of protein consisting of TAGRDHQKSEP
            Kappa - Measure of mixture between positive and negative charge (low = well mixed)
            Omega - Measure of mixture between (WFYL) and (DE) (low = well mixed)
            

    04_PADDLE_manual_tested_domains:
        This script runs the activation domain prediction algorithm PADDLE
        https://paddle.stanford.edu/
        In brief, this algorithm divides a sequence into 53 amino acid windows
        and assigns a score to each window that correlates with the strength
        of the domain as an activator. 
        For precise details on the algorithm, see src/paddle_interface.py

"""
import importlib
for file in "01_run_uclust","02_assign_hits_and_clusters","03_charachterize_manual_tested_domains","04_PADDLE_manual_tested_domains":
    print("Running {}.py".format(file))
    importlib.import_module(file).main()
    print("File {}.py completed".format(file))

