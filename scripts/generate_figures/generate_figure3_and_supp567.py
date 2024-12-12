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
            "Figure 3 and Supplementary Figures 5-7.xlsx"
        ),
        engine='xlsxwriter')
    
    from fig3s567 import Main3c
    sheet_one = Main3c.main()
    sheet_one.to_excel(writer,sheet_name='Main 3c',index=False)
    
    from fig3s567 import Main3cd_Supp6ab
    sheet_two = Main3cd_Supp6ab.main()
    sheet_two.to_excel(writer,sheet_name='Main 3c,d; Supp 6a,b',index=False)
    
    from fig3s567 import Main3e_Supp7
    sheet_three = Main3e_Supp7.main()
    sheet_three.to_excel(writer,sheet_name='Main 3e; Supp 7',index=False)
    
    from fig3s567 import Supp5c
    sheet_four = Supp5c.main()
    sheet_four.to_excel(writer,sheet_name='Supp 5c',index=False)

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 3c'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 3c,d; Supp 6a,b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Main 3e; Supp 7'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_four.columns.values):
        writer.sheets['Supp 5c'].write(0, col_num, value, cell_format)
    
    writer._save()

if __name__=="__main__":
    main()