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
            "Figure 2 and Supplementary Figure 3.xlsx"
        ),
        engine='xlsxwriter')
    
    import Main2bcde_Supp3a
    sheet_one = Main2bcde_Supp3a.main()
    sheet_one.to_excel(writer,sheet_name='Main 2b,c,d,e; Supp 3a',index=False)

    import Main2f
    sheet_two = Main2f.main()
    sheet_two.to_excel(writer,sheet_name='Main 2f',index=False)

    import Supp3b
    sheet_three = Supp3b.main()
    sheet_three.to_excel(writer,sheet_name='Supp 3b',index=False)

    

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 2b,c,d,e; Supp 3a'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 2f'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Supp 3b'].write(0, col_num, value, cell_format)

    
    writer._save()

if __name__=="__main__":
    main()