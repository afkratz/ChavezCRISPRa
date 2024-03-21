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
            "Figure 4 and Supplementary Figures 7-16a and 17.xlsx"
        ),
        engine='xlsxwriter')
    
    from fig4s7_16a17 import Main4bc_Supp78
    sheet_one = Main4bc_Supp78.main()
    sheet_one.to_excel(writer,sheet_name='Main 4b,c; Supp 7,8',index=False)

    from fig4s7_16a17 import Main4d
    sheet_two = Main4d.main()
    sheet_two.to_excel(writer,sheet_name='Main 4d',index=False)

    from fig4s7_16a17 import Main4e_Supp15b
    sheet_three = Main4e_Supp15b.main()
    sheet_three.to_excel(writer,sheet_name='Main 4e and Supp 15b',index=False)

    
    from fig4s7_16a17 import Main4f
    sheet_four = Main4f.main()
    sheet_four.to_excel(writer,sheet_name="Main 4f",index=False)

    from fig4s7_16a17 import Supp9
    sheet_five = Supp9.main()
    sheet_five.to_excel(writer,sheet_name="Supp 9,24",index=False)

    from fig4s7_16a17 import Supp10b
    sheet_six = Supp10b.main()
    sheet_six.to_excel(writer,sheet_name="Supp 10b",index=False)

    from fig4s7_16a17 import Supp10c
    sheet_seven  = Supp10c.main()
    sheet_seven.to_excel(writer,sheet_name="Supp 10c",index=False)

    from fig4s7_16a17 import Supp11
    sheet_eight  = Supp11.main()
    sheet_eight.to_excel(writer,sheet_name="Supp 11",index=False)

    from fig4s7_16a17 import Supp12
    sheet_nine = Supp12.main()
    sheet_nine.to_excel(writer,sheet_name="Supp 12",index=False)
    
    from fig4s7_16a17 import Supp14a
    sheet_ten = Supp14a.main()
    sheet_ten.to_excel(writer,sheet_name="Supp 14a",index=False)

    from fig4s7_16a17 import Supp14b
    sheet_eleven = Supp14b.main()
    sheet_eleven.to_excel(writer,sheet_name="Supp 14b",index=False)

    from fig4s7_16a17 import Supp15a
    sheet_twelve = Supp15a.main()
    sheet_twelve.to_excel(writer,sheet_name="Supp 15a",index=False)

    from fig4s7_16a17 import Supp16a
    sheet_thirteen = Supp16a.main()
    sheet_thirteen.to_excel(writer,sheet_name="Supp 16a",index=False)
    
    from fig4s7_16a17 import Supp17ab
    sheet_fourteen = Supp17ab.main()
    sheet_fourteen.to_excel(writer,sheet_name="Supp 17a,b",index=False)
    
    
    

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 4b,c; Supp 7,8'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 4d'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Main 4e and Supp 15b'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_four.columns.values):
        writer.sheets['Main 4f'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_five.columns.values):
        writer.sheets['Supp 9,24'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_six.columns.values):
        writer.sheets['Supp 10b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_seven.columns.values):
        writer.sheets['Supp 10c'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_eight.columns.values):
        writer.sheets['Supp 11'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_nine.columns.values):
        writer.sheets['Supp 12'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_ten.columns.values):
        writer.sheets['Supp 14a'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_eleven.columns.values):
        writer.sheets['Supp 14b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_twelve.columns.values):
        writer.sheets['Supp 15a'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_thirteen.columns.values):
        writer.sheets['Supp 16a'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_fourteen.columns.values):
        writer.sheets['Supp 17a,b'].write(0, col_num, value, cell_format)
    
    
    
    
    
    
    
    
    writer._save()

if __name__=="__main__":
    main()