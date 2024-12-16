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
    if not os.path.exists(os.path.join(ChavezCIRSPRa_root_dir,"Figure Source Data")):
        os.mkdir(os.path.join(ChavezCIRSPRa_root_dir,"Figure Source Data"))

    writer = pd.ExcelWriter(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "Figure Source Data",
            "Soruce Data Figure 5 and Supplementary Figures 19b and 20-23.xlsx"
        ),
        engine='xlsxwriter')
     
    from fig5s18b20_23 import Main5a
    sheet_one = Main5a.main()
    sheet_one.to_excel(writer,sheet_name='Main 5a',index=False)
    

    from fig5s18b20_23 import Main5b_Supp22a
    sheet_two = Main5b_Supp22a.main()
    sheet_two.to_excel(writer,sheet_name='Main 5b; Supp22a',index=False)

    from fig5s18b20_23 import Main5c_Supp22b
    sheet_three = Main5c_Supp22b.main()
    sheet_three.to_excel(writer,sheet_name='Main 5c; Supp22b',index=False)
    
    from fig5s18b20_23 import Main5d_Supp23b
    sheet_four = Main5d_Supp23b.main()
    sheet_four.to_excel(writer,sheet_name='Main 5d; Supp23b',index=False)

    from fig5s18b20_23 import Supp18b
    sheet_five = Supp18b.main()
    sheet_five.to_excel(writer,sheet_name='Supp 18b',index=False)

    from fig5s18b20_23 import Supp20
    sheet_six = Supp20.main()
    sheet_six.to_excel(writer,sheet_name='Supp 20',index=False)

    from fig5s18b20_23 import Supp21a_cxcr4
    sheet_seven = Supp21a_cxcr4.main()
    sheet_seven.to_excel(writer,sheet_name='Supp 21a (CXCR4)',index=False)

    from fig5s18b20_23 import Supp21a_reporter
    sheet_eight = Supp21a_reporter.main()
    sheet_eight.to_excel(writer,sheet_name='Supp 21a (Reporter)',index=False)

    from fig5s18b20_23 import Supp21b_epcam
    sheet_nine = Supp21b_epcam.main()
    sheet_nine.to_excel(writer,sheet_name='Supp 21b (EPCAM)',index=False)

    from fig5s18b20_23 import Supp21b_cxcr4
    sheet_ten = Supp21b_cxcr4.main()
    sheet_ten.to_excel(writer,sheet_name='Supp 21b (CXCR4)',index=False)

    from fig5s18b20_23 import Supp21b_reporter
    sheet_eleven = Supp21b_reporter.main()
    sheet_eleven.to_excel(writer,sheet_name='Supp 21b (Reporter)',index=False)

    from fig5s18b20_23 import Supp23a
    sheet_twelve = Supp23a.main()
    sheet_twelve.to_excel(writer,sheet_name='Supp 23a',index=False)

    

    workbook=writer.book
    cell_format = workbook.add_format({'bold': False})
    for col_num, value in enumerate(sheet_one.columns.values):
        writer.sheets['Main 5a'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_two.columns.values):
        writer.sheets['Main 5b; Supp22a'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_three.columns.values):
        writer.sheets['Main 5c; Supp22b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_four.columns.values):
        writer.sheets['Main 5d; Supp23b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_five.columns.values):
        writer.sheets['Supp 18b'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_six.columns.values):
        writer.sheets['Supp 20'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_seven.columns.values):
        writer.sheets['Supp 21a (CXCR4)'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_eight.columns.values):
        writer.sheets['Supp 21a (Reporter)'].write(0, col_num, value, cell_format)

    for col_num, value in enumerate(sheet_nine.columns.values):
        writer.sheets['Supp 21b (EPCAM)'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_ten.columns.values):
        writer.sheets['Supp 21b (CXCR4)'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_eleven.columns.values):
        writer.sheets['Supp 21b (Reporter)'].write(0, col_num, value, cell_format)
    
    for col_num, value in enumerate(sheet_twelve.columns.values):
        writer.sheets['Supp 23a'].write(0, col_num, value, cell_format)
    
    

    
    
    
    
    
    
    
    
    writer._save()

if __name__=="__main__":
    main()