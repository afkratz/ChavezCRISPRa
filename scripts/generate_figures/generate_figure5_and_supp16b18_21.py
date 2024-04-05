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
import pandas as pd
import numpy as np

def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"FigureSourceData")):
        os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"FigureSourceData"))

    writer = pd.ExcelWriter(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "FigureSourceData",
            "Figure 5 and Supplementary Figures 16b and 18-21.xlsx"
        ),
        engine='xlsxwriter')
     
    from fig5s16b18_21 import Main5a
    sheet_one = Main5a.main()
    sheet_one.to_excel(writer,sheet_name='Main 5a',index=False)
    
    from fig5s16b18_21 import Main5b_Supp20a
    sheet_two = Main5b_Supp20a.main()
    sheet_two.to_excel(writer,sheet_name='Main 5b; Supp20a',index=False)
    
    
    

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 5a'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 5b; Supp20a'].write(0, col_num, value, cell_format)
    
    
    
    
    writer._save()

if __name__=="__main__":
    main()