# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
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
            "output",
            "prescreen_results",
            "02_manually_tested_hits_and_clusters_assigned.csv"),
            index_col="Domain ID"
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
            "output",
            "prescreen_results",
            "04_manually_tested_Paddle.csv"
            )
        )



    odf = pd.DataFrame()

    odf.at["Strong","True positives"] = df['True strong positive'].to_list().count(True)
    odf.at["Strong","False positives"] = df['False strong positive'].to_list().count(True)
    odf.at["Strong","True negatives"] = df['True strong negative'].to_list().count(True)
    odf.at["Strong","False negatives"] = df['False strong negative'].to_list().count(True)

    odf.at["Medium","True positives"] = df['True medium positive'].to_list().count(True)
    odf.at["Medium","False positives"] = df['False medium positive'].to_list().count(True)
    odf.at["Medium","True negatives"] = df['True medium negative'].to_list().count(True)
    odf.at["Medium","False negatives"] = df['False medium negative'].to_list().count(True)

    odf.at["Strong","Precision"] = df['True strong positive'].to_list().count(True)/df['Paddle:Has strong hit'].to_list().count(True)
    odf.at["Strong","Recall"] = df['True strong positive'].to_list().count(True)/df['Hit on any'].to_list().count(True)
    odf.at["Medium","Precision"] = df['True medium positive'].to_list().count(True)/df['Paddle:Has medium hit'].to_list().count(True)
    odf.at["Medium","Recall"] = df['True medium positive'].to_list().count(True)/df['Hit on any'].to_list().count(True)

    odf.to_csv(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "prescreen_results",
            "04_Paddle_precision_recall.csv"
        )
        )

if __name__=="__main__":
    main()