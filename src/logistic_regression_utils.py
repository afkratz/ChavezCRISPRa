# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

import pandas as pd
from typing import List

def get_lr(df:pd.DataFrame,independent_variables:List[str],dependent_variable:str):
    df=df.copy()
    for iv in independent_variables:
        assert iv in df.columns
    assert dependent_variable in df.columns
    assert 'intercept' not in df.columns
    
    df["intercept"]=1
    scaler = StandardScaler()
    df[independent_variables] = scaler.fit_transform(df[independent_variables])
    X = df[independent_variables+['intercept']]
    
    y = df[dependent_variable]

    for item in y:
        if not isinstance(item,bool):
            raise TypeError("LR requires dependent variable to be type bool")
    
    
    logit_model = sm.Logit(y,X)

    result = logit_model.fit()

    return pd.DataFrame({
        'coef':result.params,
        'std err':result.bse,
        'z':result.tvalues,
        'P>|z|':result.pvalues,
        '[0.025':result.conf_int()[0],
        '0.975]':result.conf_int()[1],
    })

