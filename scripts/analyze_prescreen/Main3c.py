# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import numpy as np
import pandas as pd
import os
from pathlib import Path


def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    all_bcs = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))

    
    contents = list()
    for bc in all_bcs:
        contents.append(bc)
    single_domain = pd.DataFrame(
        {
            "Construct":contents,
            "Activator type":"Single-domain"
        }
    )

    for target in ['EPCAM','CXCR4','Reporter']:
        for replicate in ['1','2']:
            df = pd.read_csv(
                os.path.join(
                    ChavezCIRSPRa_root_dir,
                    "output",
                    "screen_results",
                    "screen_bin_counts",
                    "single_domain",
                    "{}_{}_normalized_counts.csv".format(target,replicate)
                )
            )
            for bin in ['bin_1','bin_2','bin_3','bin_4','NS']:
                single_domain["{}_{}_{}".format(target,replicate,bin)]=df[bin]

    for target in ['EPCAM','CXCR4','Reporter']:
        for bin in ['bin_1','bin_2','bin_3','bin_4','NS']:
            single_domain['{}_average_{}'.format(target,bin)] = single_domain[["{}_1_{}".format(target,bin),"{}_2_{}".format(target,bin)]].values.mean(axis=1)

    #END OF SINGLE DOMAIN
    
    contents = list()
    for bc1 in all_bcs:
        for bc2 in all_bcs:
            contents.append("{}_{}".format(bc1,bc2))
    bipartite = pd.DataFrame(
        {
            "Construct":contents,
            "Activator type":"Bipartite"
        }
    )

    for target in ['EPCAM','CXCR4','Reporter']:
        for replicate in ['1','2']:
            df = pd.read_csv(
                os.path.join(
                    ChavezCIRSPRa_root_dir,
                    "output",
                    "screen_results",
                    "screen_bin_counts",
                    "bipartite_screen",
                    "{}_{}_normalized_counts.csv".format(target,replicate)
                )
            )
            for bin in ['bin_1','bin_2','bin_3','bin_4','NS']:
                bipartite["{}_{}_{}".format(target,replicate,bin)]=df[bin]

    for target in ['EPCAM','CXCR4','Reporter']:
        for bin in ['bin_1','bin_2','bin_3','bin_4','NS']:
            bipartite['{}_average_{}'.format(target,bin)] = bipartite[["{}_1_{}".format(target,bin),"{}_2_{}".format(target,bin)]].values.mean(axis=1)
    
    #END OF BIPARTITE
    
    contents = list()
    for bc1 in all_bcs:
        for bc2 in all_bcs:
            for bc3 in all_bcs:
                contents.append("{}_{}_{}".format(bc1,bc2,bc3))
    tripartite = pd.DataFrame(
        {
            "Construct":contents,
            "Activator type":"tripartite"
        }
    )

    for target in ['EPCAM','CXCR4','Reporter']:
        for replicate in ['1','2']:
            df = pd.read_csv(
                os.path.join(
                    ChavezCIRSPRa_root_dir,
                    "output",
                    "screen_results",
                    "screen_bin_counts",
                    "tripartite_screen",
                    "{}_{}_normalized_counts.csv".format(target,replicate)
                )
            )
            for bin in ['bin_1','bin_2','bin_3','bin_4','NS']:
                tripartite["{}_{}_{}".format(target,replicate,bin)]=df[bin]

    for target in ['EPCAM','CXCR4','Reporter']:
        for bin in ['bin_1','bin_2','bin_3','bin_4','NS']:
            tripartite['{}_average_{}'.format(target,bin)] = tripartite[["{}_1_{}".format(target,bin),"{}_2_{}".format(target,bin)]].values.mean(axis=1)
    
    res = pd.concat([single_domain,bipartite,tripartite],ignore_index=True)
    return res

if __name__=="__main__":
    main()
