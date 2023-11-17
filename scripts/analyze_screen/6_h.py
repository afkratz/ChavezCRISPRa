

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import pandas as pd

os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))


def filter_dataframe(input_df: pd.DataFrame, mask: dict) -> pd.DataFrame:
    """
    Filter DataFrame based on the provided dictionary of column-value pairs.

    Parameters:
    - input_df: pd.DataFrame, the input DataFrame to be filtered
    - mask: dict, dictionary with column-value pairs for filtering

    Returns:
    - pd.DataFrame, a copy of the input DataFrame with the specified conditions
    """
    # Initialize a boolean mask
    mask_series = pd.Series([True] * len(input_df), dtype=bool)

    # Apply filtering based on the dictionary
    for column, value in mask.items():
        mask_series &= (input_df[column] == value)

    # Use the boolean mask to filter the DataFrame and return a copy
    filtered_df = input_df[mask_series].copy()
    
    return filtered_df


hbb_bh1_qpcr_df = pd.read_csv(
    os.path.join(
        "input_data",
        "top_hit_validation",
        "final_2_qpcr_HBB-BH1_N2A.csv"
    )
)


activators = ['MHV','MMH','SAM','MCP-empty']

activator_target_average_ct = pd.DataFrame()

activator_target_average_delta_ct=pd.DataFrame()



for replicate in (1,2):
    for activator in activators:
        activator_target_results = filter_dataframe(
            hbb_bh1_qpcr_df,
            mask={
                "Activator":activator,
                "Transfection replicate":replicate,
                "qPCR target":"HBB-BH1"
            })
        
        #Should have 3 qPCR replicates
        assert(len(activator_target_results)==3)

        average_cq_against_target = activator_target_results['Cq'].values.mean()


        activator_target_results = filter_dataframe(
            hbb_bh1_qpcr_df,
            mask={
                "Activator":activator,
                "Transfection replicate":replicate,
                "qPCR target":'B-actin'
            })
        
        #Should have 3 qPCR replicates
        assert(len(activator_target_results)==3)

        average_cq_against_beta_actin = activator_target_results['Cq'].values.mean()

        delta_ct = average_cq_against_target - average_cq_against_beta_actin

        activator_target_average_ct.at[activator,'HBB-BH1 average cq replicate {}'.format(replicate)]=average_cq_against_target
        activator_target_average_ct.at[activator,'beta actin average cq replicate {}'.format(replicate)]=average_cq_against_beta_actin

        activator_target_average_delta_ct.at[activator,"HBB-BH1 delta Ct replicate {}".format(replicate)] = delta_ct
            


double_delta_ct_df = pd.DataFrame()

for activator in activators:
    for replicate in (1,2):
        activator_delta_ct =  activator_target_average_delta_ct.at[activator,"HBB-BH1 delta Ct replicate {}".format(replicate)]
        mcp_delta_ct = activator_target_average_delta_ct.at['MCP-empty',"HBB-BH1 delta Ct replicate {}".format(replicate)]
        double_delta_ct = activator_delta_ct - mcp_delta_ct
        double_delta_ct_df.at[activator,'HBB-BH1 ddCt replicate {}'.format(replicate)] = double_delta_ct


#intermediate results, commented out unless they're of interest
#activator_target_average_ct.to_csv(os.path.join('output','figures','fig6','6h - average CT.csv'))
#activator_target_average_delta_ct.to_csv(os.path.join('output','figures','fig6','6h - dCT.csv'))
#double_delta_ct_df.to_csv(os.path.join('output','figures','fig6','6h - ddCT.csv'))
rna_fold_change_df = pd.DataFrame()

for activator in activators:
    for replicate in (1,2):
        rna_fold_change_df.at[activator,'HBB-BH1 RNA fold change replicate {} '.format(replicate)] =\
                np.power(2,- double_delta_ct_df.at[activator,'HBB-BH1 ddCt replicate {}'.format(replicate)])
            
rna_fold_change_df.to_csv(os.path.join('output','figures','fig6','6h - Final 2 qPCR RNA fc N2A.csv'))