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
            "Figure 4 and Supplementary Figures 8-18a and 19.xlsx"
        ),
        engine='xlsxwriter')
    
    from fig4s8_18a19 import Main4bc_Supp89
    sheet_one = Main4bc_Supp89.main()
    sheet_one.to_excel(writer,sheet_name='Main 4b,c; Supp 8,9',index=False)

    from fig4s8_18a19 import Main4d
    sheet_two = Main4d.main()
    sheet_two.to_excel(writer,sheet_name='Main 4d',index=False)

    from fig4s8_18a19 import Main4e_Supp17b
    sheet_three = Main4e_Supp17b.main()
    sheet_three.to_excel(writer,sheet_name='Main 4e and Supp 17b',index=False)

    from fig4s8_18a19 import Main4f
    sheet_four = Main4f.main()
    sheet_four.to_excel(writer,sheet_name="Main 4f",index=False)

    from fig4s8_18a19 import Supp10
    sheet_five = Supp10.main()
    sheet_five.to_excel(writer,sheet_name="Supp 10",index=False)

    from fig4s8_18a19 import Supp11b
    sheet_six = Supp11b.main()
    sheet_six.to_excel(writer,sheet_name="Supp 11b",index=False)

    from fig4s8_18a19 import Supp11c
    sheet_seven  = Supp11c.main()
    sheet_seven.to_excel(writer,sheet_name="Supp 11c",index=False)

    from fig4s8_18a19 import Supp12
    sheet_eight  = Supp12.main()
    sheet_eight.to_excel(writer,sheet_name="Supp 12",index=False)

    from fig4s8_18a19 import Supp13
    sheet_nine = Supp13.main()
    sheet_nine.to_excel(writer,sheet_name='Supp 13',index=False)

    from fig4s8_18a19 import Supp14
    sheet_ten = Supp14.main()
    sheet_ten.to_excel(writer,sheet_name="Supp 14",index=False)
    
    from fig4s8_18a19 import Supp16a
    sheet_eleven = Supp16a.main()
    sheet_eleven.to_excel(writer,sheet_name="Supp 16a",index=False)

    from fig4s8_18a19 import Supp16b
    sheet_twelve = Supp16b.main()
    sheet_twelve.to_excel(writer,sheet_name="Supp 16b",index=False)

    from fig4s8_18a19 import Supp17a
    sheet_thirteen = Supp17a.main()
    sheet_thirteen.to_excel(writer,sheet_name="Supp 17a",index=False)

    from fig4s8_18a19 import Supp18a
    sheet_fourteen = Supp18a.main()
    sheet_fourteen.to_excel(writer,sheet_name="Supp 18a",index=False)
    
    from fig4s8_18a19 import Supp19ab
    sheet_fifteen = Supp19ab.main()
    sheet_fifteen.to_excel(writer,sheet_name="Supp 19a,b",index=False)
    
    
    

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 4b,c; Supp 8,9'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 4d'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Main 4e and Supp 17b'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_four.columns.values):
        writer.sheets['Main 4f'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_five.columns.values):
        writer.sheets['Supp 10'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_six.columns.values):
        writer.sheets['Supp 11b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_seven.columns.values):
        writer.sheets['Supp 11c'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_eight.columns.values):
        writer.sheets['Supp 12'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_nine.columns.values):
        writer.sheets['Supp 13'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_ten.columns.values):
        writer.sheets['Supp 14'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_eleven.columns.values):
        writer.sheets['Supp 16a'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_twelve.columns.values):
        writer.sheets['Supp 16b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_thirteen.columns.values):
        writer.sheets['Supp 17a'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_fourteen.columns.values):
        writer.sheets['Supp 18a'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_fifteen.columns.values):
        writer.sheets['Supp 19a,b'].write(0, col_num, value, cell_format)
    
    
    
    
    
    
    
    
    writer._save()

if __name__=="__main__":
    main()