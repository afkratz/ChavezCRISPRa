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

def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent
    if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"FigureSourceData")):
        os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"FigureSourceData"))

    writer = pd.ExcelWriter(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "FigureSourceData",
            "Figure 2 and Supplementary Figure 4.xlsx"
        ),
        engine='xlsxwriter')
    
    from fig2s4 import Main2bcde_Supp4a
    sheet_one = Main2bcde_Supp4a.main()
    sheet_one.to_excel(writer,sheet_name='Main 2b,c,d,e; Supp 4a',index=False)

    from fig2s4 import Main2f
    sheet_two = Main2f.main()
    sheet_two.to_excel(writer,sheet_name='Main 2f',index=False)

    from fig2s4 import Supp4b
    sheet_three = Supp4b.main()
    sheet_three.to_excel(writer,sheet_name='Supp 4b',index=False)

    

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 2b,c,d,e; Supp 4a'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 2f'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Supp 4b'].write(0, col_num, value, cell_format)

    
    writer._save()

if __name__=="__main__":
    main()