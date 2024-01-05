# -*- coding: utf-8 -*-

"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
Provides an interface with the PADDLE_noSS (PADDLE no secondary structure) 
pretrained model published by
 Adrian L Sanborn, Benjamin T Yeh, Jordan T Feigerle, Cynthia V Hao,
 Raphael JL Townshend, Erez Lieberman Aiden, Ron O Dror, Roger D Kornberg (2021)
 Simple biochemical features underlie transcriptional activation domain 
 diversity and dynamic, fuzzy binding to Mediator 
 https://doi.org/10.7554/eLife.68068

In addition to wrappers around their prediction functions, this provides a
processing function, "process_predictions", implementing the following rules,
which were outlined by Sanborn et al

Input:
    Predictions on 53-aa tiles with 1-aa resolution 

Processing steps:
If the input is at least 5 tiles long: 
    1) Smooth predictions with 9-aa moving average
    
    2) Define high strength ADs as at least 5 consecutive 53 AA tiles with 
    smoothed score over 6

    3) ADs which overlap by more than 26 AAs are combined

    4) Define medium strength ADs as at least 5 consecutive 53 AA tiles with
    smoothed score over 4, which do not overlap with a strong AD by more than
    26 AAs

If the input is less than 5 windows, then instead, perform the following steps:
    1) If average score across its windows is greater than 6, define the entire
    length as a high strength AD

    2) If average score across its windows is greater than 4 and less than 6, 
    define the entire length as a medium strength AD

Returns: 
    A dictionary with the following values
    ["Is short"], bool: A true or false value describing if the tiles passed
        the "at least 5 tiles" cutoff
    
    ["Has strong hit"], bool: True if the tiles passed in have at least one 
        strong hit

    ["Has medium hit"], bool: True if the tiles passed in have at least one 
        medium hit

    ["Score"], int: A value that quantifies the confidence of PADDLE 
        that this sequence is a hit. If ["Is short"], it is the average
        of the score for the tiles. Otherwise, it is the maximum score 
        that is true for 5 consecuitive tiles. If this is over 6, then 
        ["Has strong hit"] should be True.
"""

from pathlib import Path
import os
import sys
import contextlib
import numpy as np
import random

bundled_code_path = os.path.join(
    Path(__file__).resolve().parent.parent,
    "bundled_code"
)
root_dir = Path(__file__).resolve().parent.parent

os.chdir(
    os.path.join(
        bundled_code_path,
        "paddle",
    )
)

sys.path.insert(0,os.getcwd())
import paddle
with contextlib.redirect_stdout(None):
    paddle_noSS_model = paddle.PADDLE_noSS()

os.chdir(root_dir)

def get_prediction(seq:str,accept_short=False,SHORT_SAMPLES=100,verbose = False)->np.ndarray:
    if len(seq)<53 and not accept_short:
        raise ValueError('If you are passing a sequence of length less than 53 you must call this with "accept_short=True"\n-See src/paddle_interface.py for explanation-')
        """
        Paddle works natively on sequences of length exactly 53.
        For sequences shorter than this, they recommend embedding the sequence 
        in a random sequence composed of "AGSTNQV" to pad out to 53 amino acids. 
        If you call this function with predict_seq
        Since this introduces some randomness, they recommend doing this sampling many times. 
        We default to SHORT_SAMPLES=100, but this can be modified. 
        """

    if verbose:
            output = sys.stdout
    else:
        output = open(os.devnull,'w')

    short = len(seq)<53
    if short:
        neutral_amino_acids = "AGSTNQV"
        random.seed(42)#reproducibility
        neutral_peptides = list(map(lambda _:"".join(random.choices(neutral_amino_acids,k=53)),range(0,SHORT_SAMPLES)))
        with contextlib.redirect_stdout(output):
            average_score = np.array(paddle_noSS_model.predict_subsequences(seq,neutral_peptides)).reshape(1)
        if verbose:output.close()
        return(average_score)
    
    else:
        seqs = [seq[x:x+53] for x in range(len(seq) - 53 + 1)]
        with contextlib.redirect_stdout(output):
            scores = np.array(paddle_noSS_model.predict(seqs))
            if len(seq)==53:
                scores=scores.reshape(1)
        if verbose:output.close()
        return(scores)

from typing import List
def process_prediction(pred:np.ndarray)->dict:
    if len(pred)<5:
        score = pred.mean()
        if score>6:
            strong=True
            medium = False
        
        elif score>4:
            strong = False
            medium = True

        else:
            strong = False
            medium = False

        strong_windows=[]
        
        results = {}
        results["Is short"]=True

        results["Has strong hit"]=strong

        results["Has medium hit"]=medium

        results["Score"] = float(score)

        return results
    
    ###### - end of "Is short" section - #####
    smoothed_prediction = np.array(
        [np.mean(
            pred[
                max(0, int(n-(9-1)/2)):
                int(n+(9+1)/2)])
            for n in range(len(pred))]
    )
    
    #Find the highest 
    score = max(
        map(lambda x:min(x),
            [smoothed_prediction[i:i+5] for i in range(0,len(smoothed_prediction)-4)]
            )
        )
    
    if score>6:
        strong=True
        medium = False
        
    elif score>4:
        strong = False
        medium = True

    else:
        strong = False
        medium = False
    
    results = {}
    results["Is short"]=True

    results["Has strong hit"]=strong

    results["Has medium hit"]=medium

    results["Score"] = float(score)

    results["Score"] = float(score)

    return results

def process_sequences(sequences:List[str],accept_short=False)->List[dict]:
    results = []
    if isinstance(sequences,str):
        sequences=[sequences]
    for seq in sequences:
        result = process_prediction(get_prediction(seq,accept_short=accept_short))        
        results.append(result)
    return results

