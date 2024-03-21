# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import pandas as pd
from pathlib import Path
from . import Supp10b

def main()->pd.DataFrame:
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent.parent
    
    gfp_10_b_output=Supp10b.main().iloc[0:27]

    res = pd.DataFrame(
        {
            'Construct':gfp_10_b_output['Construct'],
            'Decrease in activator population_P2':gfp_10_b_output['Decrease in activator population_P2'],
            'Screen toxicity':gfp_10_b_output['Screen toxicity'],
        }
    )

    return res

 

if __name__=="__main__":
    main()