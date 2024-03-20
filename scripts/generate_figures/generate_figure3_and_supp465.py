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
    if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"output","figures_and_tables")):
        os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"output","figures_and_tables"))

    writer = pd.ExcelWriter(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "output",
            "figures_and_tables",
            "Figure 3 and Supplementary Figures 4-6.xlsx"
        ),
        engine='xlsxwriter')
    
    from fig3s456 import Main3c
    sheet_one = Main3c.main()
    sheet_one.to_excel(writer,sheet_name='Main 3c',index=False)
    
    from fig3s456 import Main3cd_Supp5ab
    sheet_two = Main3cd_Supp5ab.main()
    sheet_two.to_excel(writer,sheet_name='Main 3c,d; Supp 5a,b',index=False)
    
    from fig3s456 import Main3e_Supp6
    sheet_three = Main3e_Supp6.main()
    sheet_three.to_excel(writer,sheet_name='Main 3e; Supp 6',index=False)
    
    from fig3s456 import Supp4c
    sheet_four = Supp4c.main()
    sheet_four.to_excel(writer,sheet_name='Supp 4c',index=False)

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 3c'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 3c,d; Supp 5a,b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Main 3e; Supp 6'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_four.columns.values):
        writer.sheets['Supp 4c'].write(0, col_num, value, cell_format)
    
    writer._save()

if __name__=="__main__":
    main()