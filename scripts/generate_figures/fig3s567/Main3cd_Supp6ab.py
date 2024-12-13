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
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    
    all_bcs = list(map(lambda x: 'A'+('0'*(2-len(str(x))))+str(x),range(1,26)))
    constructs = list()
    for bc in all_bcs:
        constructs.append(bc)
    single_domain = pd.DataFrame(
        {
            "Construct":constructs,
            "Activator type":"Single-domain"
        }
    )
    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "single_domain_screen_scored.csv",
        )
    )
    for target in ['EPCAM','CXCR4','Reporter']:
        for replicate in ['1','2']:
            single_domain["{}_{}".format(target,replicate)]=df["{}_{}".format(target,replicate)]

    for target in ['EPCAM','CXCR4','Reporter']:
        single_domain['{}_average'.format(target)] = single_domain[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)

    #END OF SINGLE DOMAIN
    
    constructs = list()
    for bc1 in all_bcs:
        for bc2 in all_bcs:
            constructs.append("{}_{}".format(bc1,bc2))
    bipartite = pd.DataFrame(
        {
            "Construct":constructs,
            "Activator type":"Bipartite"
        }
    )
    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "bipartite_screen_scored.csv",
        )
    )
    for target in ['EPCAM','CXCR4','Reporter']:
        for replicate in ['1','2']:
            bipartite["{}_{}".format(target,replicate)]=df["{}_{}".format(target,replicate)]

    for target in ['EPCAM','CXCR4','Reporter']:
        bipartite['{}_average'.format(target)] = bipartite[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
    
    #END OF BIPARTITE
    
    constructs = list()
    for bc1 in all_bcs:
        for bc2 in all_bcs:
            for bc3 in all_bcs:
                constructs.append("{}_{}_{}".format(bc1,bc2,bc3))
    tripartite = pd.DataFrame(
        {
            "Construct":constructs,
            "Activator type":"Tripartite"
        }
    )
    df = pd.read_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "screen_results",
            "screen_scores",
            "tripartite_screen_scored.csv",
        )
    )
    for target in ['EPCAM','CXCR4','Reporter']:
        for replicate in ['1','2']:
            tripartite["{}_{}".format(target,replicate)]=df["{}_{}".format(target,replicate)]

    for target in ['EPCAM','CXCR4','Reporter']:
        tripartite['{}_average'.format(target)] = tripartite[["{}_1".format(target),"{}_2".format(target)]].values.mean(axis=1)
    
    single_domain.replace(np.nan,'NA',inplace=True)
    bipartite.replace(np.nan,'NA',inplace=True)
    tripartite.replace(np.nan,'NA',inplace=True)

    res = pd.concat([single_domain,bipartite,tripartite],ignore_index=True)
    return res


if __name__=="__main__":
    main()