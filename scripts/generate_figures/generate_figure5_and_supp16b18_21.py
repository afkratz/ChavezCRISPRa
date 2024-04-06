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
    
    from fig5s16b18_21 import Main5c_Supp21a
    sheet_three = Main5c_Supp21a.main()
    sheet_three.to_excel(writer,sheet_name='Main 5c; Supp21a',index=False)

    from fig5s16b18_21 import Main5d_Supp21b
    sheet_four = Main5d_Supp21b.main()
    sheet_four.to_excel(writer,sheet_name='Main 5d; Supp21b',index=False)

    from fig5s16b18_21 import Supp16b
    sheet_five = Supp16b.main()
    sheet_five.to_excel(writer,sheet_name='Supp 16b',index=False)

    from fig5s16b18_21 import Supp18
    sheet_six = Supp18.main()
    sheet_six.to_excel(writer,sheet_name='Supp 18',index=False)

    from fig5s16b18_21 import Supp19a_cxcr4
    sheet_seven = Supp19a_cxcr4.main()
    sheet_seven.to_excel(writer,sheet_name='Supp 19a (CXCR4)',index=False)

    from fig5s16b18_21 import Supp19a_reporter
    sheet_eight = Supp19a_reporter.main()
    sheet_eight.to_excel(writer,sheet_name='Supp 19a (Reporter)',index=False)

    from fig5s16b18_21 import Supp19b_epcam
    sheet_nine = Supp19b_epcam.main()
    sheet_nine.to_excel(writer,sheet_name='Supp 19b (EPCAM)',index=False)

    from fig5s16b18_21 import Supp19b_cxcr4
    sheet_ten = Supp19b_cxcr4.main()
    sheet_ten.to_excel(writer,sheet_name='Supp 19b (CXCR4)',index=False)

    from fig5s16b18_21 import Supp19b_reporter
    sheet_eleven = Supp19b_reporter.main()
    sheet_eleven.to_excel(writer,sheet_name='Supp 19b (Reporter)',index=False)

    from fig5s16b18_21 import Supp20b
    sheet_twelve = Supp20b.main()
    sheet_twelve.to_excel(writer,sheet_name='Supp 20b',index=False)

    

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 5a'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 5b; Supp20a'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Main 5c; Supp21a'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_four.columns.values):
        writer.sheets['Main 5d; Supp21b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_five.columns.values):
        writer.sheets['Supp 16b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_six.columns.values):
        writer.sheets['Supp 18'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_seven.columns.values):
        writer.sheets['Supp 19a (CXCR4)'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_eight.columns.values):
        writer.sheets['Supp 19a (Reporter)'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_nine.columns.values):
        writer.sheets['Supp 19b (EPCAM)'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_ten.columns.values):
        writer.sheets['Supp 19b (CXCR4)'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_eleven.columns.values):
        writer.sheets['Supp 19b (Reporter)'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_twelve.columns.values):
        writer.sheets['Supp 20b'].write(0, col_num, value, cell_format)
    
    

    
    
    
    
    
    
    
    
    writer._save()

if __name__=="__main__":
    main()