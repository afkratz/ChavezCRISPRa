# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
This script runs the activation domain prediction algorithm PADDLE
https://paddle.stanford.edu/
In brief, this algorithm divides a sequence into 53 amino acid windows and
assigns a score to each window that correlates with the strength of the domain
as an activator. 
For precise details on the algorithm, see src/paddle_interface.py
"""
import os
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))
import pandas as pd

print("Loading PADDLE model...")
from src import paddle_interface as pi
def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    df = pd.read_csv(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "prescreen_results",
            "1_manually_tested_clusters_assigned.csv"),
        )

    from progress.bar import Bar
    bar = Bar("PADDLE predicting...",max=len(df),suffix='%(index)i / %(max)i - %(eta)ds')
    for i in df.index:
        bar.next()
        results = pi.process_sequences(df.at[i,"AA sequence"],accept_short=True)[0]
        for key in results:
            if 'Paddle:'+key not in df.columns:df['Paddle:'+key]=''
            df.at[i,'Paddle:'+key]=results[key]
    bar.finish()

    df['True medium positive'] = df['Paddle:Has medium hit'] & df['Hit on any']
    df['False medium positive'] = df['Paddle:Has medium hit'] & ~df['Hit on any']
    df['True medium negative'] = ~df['Paddle:Has medium hit'] & ~df['Hit on any']
    df['False medium negative'] = ~df['Paddle:Has medium hit'] & df['Hit on any']

    df['True strong positive'] = df['Paddle:Has strong hit'] & df['Hit on any']
    df['False strong positive'] = df['Paddle:Has strong hit'] & ~df['Hit on any']
    df['True strong negative'] = ~df['Paddle:Has strong hit'] & ~df['Hit on any']
    df['False strong negative'] = ~df['Paddle:Has strong hit'] & df['Hit on any']
    
    df.to_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "prescreen_results",
            "3_PADDLE_predictions.csv"
        )
    )
    
    only_centroids = df[df['Is centroid']]

    odf = pd.DataFrame()

    odf.at["Strong","True positives"] = only_centroids['True strong positive'].to_list().count(True)
    odf.at["Strong","False positives"] = only_centroids['False strong positive'].to_list().count(True)
    odf.at["Strong","True negatives"] = only_centroids['True strong negative'].to_list().count(True)
    odf.at["Strong","False negatives"] = only_centroids['False strong negative'].to_list().count(True)

    odf.at["Medium","True positives"] = only_centroids['True medium positive'].to_list().count(True)
    odf.at["Medium","False positives"] = only_centroids['False medium positive'].to_list().count(True)
    odf.at["Medium","True negatives"] = only_centroids['True medium negative'].to_list().count(True)
    odf.at["Medium","False negatives"] = only_centroids['False medium negative'].to_list().count(True)

    odf.at["Strong","Precision"] = only_centroids['True strong positive'].to_list().count(True)/only_centroids['Paddle:Has strong hit'].to_list().count(True)
    odf.at["Strong","Recall"] = only_centroids['True strong positive'].to_list().count(True)/only_centroids['Hit on any'].to_list().count(True)
    odf.at["Medium","Precision"] = only_centroids['True medium positive'].to_list().count(True)/only_centroids['Paddle:Has medium hit'].to_list().count(True)
    odf.at["Medium","Recall"] = only_centroids['True medium positive'].to_list().count(True)/only_centroids['Hit on any'].to_list().count(True)

    output_sup_table = pd.DataFrame({
        'Domain':only_centroids['Domain ID'],
        'Hit on EPCAM':only_centroids['Hit on EPCAM'],
        'Hit on CXCR4':only_centroids['Hit on CXCR4'],
        'Hit on tdTomato':only_centroids['Hit on Reporter'],
        'Hit on any':only_centroids['Hit on any'],
        'Paddle has strong hit':only_centroids['Paddle:Has strong hit'],
        'Paddle has medium hit':only_centroids['Paddle:Has medium hit'],
        'Strong hit true positive':only_centroids['True strong positive'],
        'Strong hit false positive':only_centroids['False strong positive'],
        'Strong hit true negative':only_centroids['True strong negative'],
        'Strong hit false negative':only_centroids['False strong negative'],
        'Medium hit true positive':only_centroids['True medium positive'],
        'Medium hit false positive':only_centroids['False medium positive'],
        'Medium hit true negative':only_centroids['True medium negative'],
        'Medium hit false negative':only_centroids['False medium negative'],
    })


    output_sup_table.to_excel(
            os.path.join(
            ChavezCIRSPRa_root_dir,
            "Supplementary Files",
            "Supplementary Data 3.xlsx"
            ),
        index=False
    )

    odf.to_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "screen_output",
            "prescreen_results",
            "3_PADDLE_precision_recall_data.csv"
        )
    )

if __name__=="__main__":
    main()