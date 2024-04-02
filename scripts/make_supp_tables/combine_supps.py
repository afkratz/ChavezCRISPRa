# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
Copyright 2023 Alexander Kratz, Alejandro Chavez lab
All Rights Reserved
MIT license
--------------------------------------------------------------------------------
Combines csv's within the SuppTables folder to a single excel sheet with
all nine supplements as sheets

"""
import os
from pathlib import Path
import pandas as pd

def main():
    ChavezCIRSPRa_root_dir  = Path(__file__).resolve().parent.parent.parent

    writer = pd.ExcelWriter(
        os.path.join(
            ChavezCIRSPRa_root_dir,
            "SuppTables",
            "Supplementary Tables 1-9.xlsx"
        ),
        engine='xlsxwriter')

    headers = [
        'Domain origins and sequences',
        'PADDLE efficacy on dCas9 fusion activation data',
        'A-IDs of combinatorially assembled domains',
        'High-throughput screen activation scores',
        'High-throughput screen toxicity scores',
        'Guide RNA sequences used in this study',
        'Filtering parameters used for NGS analyses',
        'DNA sequences of select plasmids used in this study',
        'qPCR primer sequences used in this study',
    ]
    workbook = writer.book
    bold_format = workbook.add_format({'bold': True})
    
    for sheet_n,header in zip([1,2,3,4,5,6,7,8,9],headers):
        supp_table = pd.read_csv(os.path.join(ChavezCIRSPRa_root_dir,'SuppTables','Supplementary Table {}.csv'.format(sheet_n)))

        supp_table.to_excel(writer,sheet_name='Supplementary Table {}'.format(sheet_n),index=False,startrow=2)
    
        worksheet = writer.sheets['Supplementary Table {}'.format(sheet_n)]
    
        worksheet.write_rich_string('A1',bold_format,'Supplementary Table {}. '.format(sheet_n),header)

    writer._save()

if __name__=='__main__':
    main()