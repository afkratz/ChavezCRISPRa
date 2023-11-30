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

    ["N strong hits"], int: Number of distinct strong activation domains. 
        Remember that domains which are close are combined by the algorithm

    ["N medium hits"], int: Number of distinct medium activation domains. 
        Remember that domains which are close are combined by the algorithm
    
    ["AA in strong hits"], int: Number of AAs within the protein that were
        part of a strong domain
    
    ["AA in medium hits"], int: Number of AAs within the protein that were
        part of a medium domain
    
    ["Strong domain indexes"], list[(int,int)]: List of tuples of ints,
        where each tuple is the (start,end) of a strong domain. 0-indexed
    
    ["Strong medium indexes"], list[(int,int)]: List of tuples of ints,
        where each tuple is the (start,end) of a medium domain. 0-indexed

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

from typing import List,Tuple
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
        if strong:
            strong_windows = [(0,len(pred))]
        medium_windows=[]
        if medium:
            medium_windows = [(0,len(pred))]
        results = {}
        results["Is short"]=True

        results["Has strong hit"]=len(strong_windows)>0
        results["Has medium hit"]=len(medium_windows)>0

        results["N strong hits"]=len(strong_windows)
        results["N medium hits"]=len(medium_windows)

        results["AA in strong hits"]=sum(map(lambda win:-win[0]+win[1]+53,_condense_windows(strong_windows,0)))    
        results["AA in medium hits"]=sum(map(lambda win:-win[0]+win[1]+53,_condense_windows(medium_windows,0)))
        
        results["AA in strong or medium hits"] =max(results["AA in strong hits"],results["AA in medium hits"])

        results["Strong domain indexes"]=list(map(lambda win:(win[0],win[1]+53),strong_windows))
        results["Medium domain indexes"]=list(map(lambda win:(win[0],win[1]+53),medium_windows))

        results["Score"] = score

        return results
    ###### - end of "Is short" section - #####
    smoothed_prediction = np.array(
        [np.mean(
            pred[
                max(0, int(n-(9-1)/2)):
                int(n+(9+1)/2)])
            for n in range(len(pred))]
    )
    
    strong_windows = _consec_trues(smoothed_prediction>=6,min_len=5)
    condensed_strong_windows = _condense_windows(strong_windows,overlap_threshold=26)
    
    medium_windows = _consec_trues(smoothed_prediction>=4,min_len=5)
    condensed_medium_windows = _condense_windows(medium_windows,overlap_threshold=26)

    checked_medium_windows = []
    for medium_window in condensed_medium_windows:
        medium_window_aas = (medium_window[0],medium_window[1]+53)
        overlaps_strong = False
        for strong_window in condensed_strong_windows:
            strong_window_aas = (strong_window[0],strong_window[1]+53)
            aa_overlap = _get_overlap(medium_window_aas,strong_window_aas)
            if aa_overlap > 26:
                overlaps_strong = True
        if not overlaps_strong:
            checked_medium_windows.append(medium_window)

    results = {}
    results["Is short"]=False

    results["Has strong hit"]=len(condensed_strong_windows)>0
    results["Has medium hit"]=len(checked_medium_windows)>0

    results["N strong hits"]=len(condensed_strong_windows)
    results["N medium hits"]=len(checked_medium_windows)

    results["AA in strong hits"]=_count_in_windows(list(map(lambda win:(win[0],win[1]+53),condensed_strong_windows)))
    results["AA in medium hits"]=_count_in_windows(list(map(lambda win:(win[0],win[1]+53),checked_medium_windows)))
    results["AA in strong or medium hits"]=_count_in_windows(list(map(lambda win:(win[0],win[1]+53),condensed_strong_windows+checked_medium_windows)))
    

    results["Strong domain indexes"]=list(map(lambda win:(win[0],win[1]+53),condensed_strong_windows))
    results["Medium domain indexes"]=list(map(lambda win:(win[0],win[1]+53),checked_medium_windows))
    
    #Find the highest 
    score = max(
        map(lambda x:min(x),
            [smoothed_prediction[i:i+5] for i in range(0,len(smoothed_prediction)-4)]
            )
        )

    results["Score"] = score

    return results

def process_sequences(sequences:List[str],accept_short=False)->List[dict]:
    results = []
    if isinstance(sequences,str):
        sequences=[sequences]
    for seq in sequences:
        result = process_prediction(get_prediction(seq,accept_short=accept_short))
        for r in range(len(result["Strong domain indexes"])):
            result["Strong domain indexes"][r]=(result["Strong domain indexes"][r][0],min(result["Strong domain indexes"][r][1],len(seq)-1))
        for r in range(len(result["Medium domain indexes"])):
            result["Medium domain indexes"][r]=(result["Medium domain indexes"][r][0],min(result["Medium domain indexes"][r][1],len(seq)-1))
        
        result["AA in strong hits"]=min(result["AA in strong hits"],len(seq))
        result["AA in medium hits"]=min(result["AA in medium hits"],len(seq))
        result["AA in strong or medium hits"]=min(result["AA in strong or medium hits"],len(seq))
        
        results.append(result)
    return results
    
def _condense_windows(windows:List[Tuple[int]],overlap_threshold=26)->List[Tuple[int]]:
    """
    This helper function takes a list of windows from paddle and combines
    any which are close enough that the amino acids they cover would
    overlap by more than overlap_threshold, which defaults to 26, the
    overlap criteria for combination used by 
    """
    condensed = []
    if windows:
        condensed.append(windows[0])
        for window in windows[1:]:
            last_window = condensed[-1]
            if 53-(window[0]-last_window[1])>overlap_threshold:
                condensed[-1] = (last_window[0], window[1])
            else:
                condensed.append(window)
    return condensed

def _get_overlap(a:tuple,b:tuple)->float:
    """
    This helper function finds the overlap between two line segments a and b
    a and b are each a tuple of the form (start,end) of a line segment
    """
    return max((0,
        min((
            a[1]-a[0],
            b[1]-b[0],
            a[1]-b[0],
            b[1]-a[0]
            ))
        ))

def _count_in_windows(windows:List[Tuple[int]]):
    """
    Counts how many amino acids are in a list of windows, handling duplicates
    example: 
    [
        (0,10),
        (9,12),
    ]
    would return 12, not counting the duplicated 9 and 10 that are in both windows
    """
    if len(windows)==0:
        return 0
    upper_bound = max(map(lambda x:x[1],windows))
    count = 0
    for aa in range(0,upper_bound):
        for window in windows:
            if aa>=window[0] and aa<window[1]:
                count+=1
                break
    return count
        


def _consec_trues(arr:np.ndarray,min_len : int)->List[Tuple[int]]:
    """
    This helper function finds windows of consecutive "true" values 
    within an array and returns a list that consists of tuples 
    where each tuple correponds to (start,end) for a window
    of consecutive trues of at least min_len length
    """
    result = []
    start = None

    for i, value in enumerate(arr):
        if value:
            if start is None:
                start = i
        elif start is not None:
            end = i - 1
            if end - start + 1 >= min_len:
                result.append((start, end))
            start = None
    # Check for the last consecutive True sequence if it extends to the end of the array
    if start is not None and len(arr) - start >= min_len:
        result.append((start, len(arr) - 1))
    return result

