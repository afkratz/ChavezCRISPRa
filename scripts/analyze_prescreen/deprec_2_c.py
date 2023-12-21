# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""

import pandas as pd
import os
from pathlib import Path
import sys
os.chdir(Path(__file__).resolve().parent.parent.parent)
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from src import logistic_regression_utils as lru

df = pd.read_csv(
    os.path.join(
        "output",
        "prescreen_results",
        "03_manually_tested_biochem_charachterized.csv"
    ),
    index_col='Unnamed: 0'
)

only_centroids = df[df['Is centroid']==True]

independent_variables=[
            'NCPR',
            'Hydropathy',
            'Omega',
            'Disorder promoting fraction',
            'Kappa']

model = lru.fit_lr(
    df=only_centroids,
    independent_variables=independent_variables,
    dependent_variable='Hit on any',
)
df['Logistic regression predictions']=lru.apply_model(model,df,independent_variables)
df.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2c - lr preds.csv"
    )
)
summary = lru.get_summary(model)
summary.to_csv(
    os.path.join(
        "output",
        "figures",
        "fig2",
        "2c - hitVmiss Logistic Regression.csv"
    )
)