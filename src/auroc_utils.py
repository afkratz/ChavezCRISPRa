# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
import numpy as np
from sklearn.metrics import auc
def get_FPR_TPR(x:list,y:list):
    #In case someone passes in an np.ndarray we can listify it
    if not isinstance(x,list):
        x=list(x)
    if not isinstance(y,list):
        y=list(y)
    
    assert len(x)==len(y)
    positives = y.count(True)
    negatives = y.count(False)
    assert positives+negatives == len(y)

    x_values = sorted(x,reverse=True)
    true_positive_rates=[]
    false_positive_rates=[]
    
    for parameter in x_values:
        true_positive = 0
        false_positive = 0
        
        for i in range(len(x)):
            if x[i]>parameter and y[i]:
                true_positive+=1
            if x[i]>parameter and not y[i]:
                false_positive+=1
        true_positive_rate = true_positive/positives
        false_positive_rate = false_positive/negatives
        true_positive_rates.append(true_positive_rate)
        false_positive_rates.append(false_positive_rate)
    return false_positive_rates,true_positive_rates

def calculate_auc(fpr,tpr):
    return auc(fpr,tpr)