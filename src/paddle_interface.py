# -*- coding: utf-8 -*-


"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
"""
from pathlib import Path
import os
import sys
bundled_code_path = os.path.join(
    Path(__file__).resolve().parent.parent,
    "bundled_code"
)
current_working_dir = os.getcwd()
os.chdir(
    os.path.join(
        bundled_code_path,
        "paddle",
    )
)
sys.path.insert(0,os.getcwd())
import paddle
paddle_noSS_model = paddle.PADDLE_noSS()
os.chdir(current_working_dir)
