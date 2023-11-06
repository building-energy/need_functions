# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:08:36 2023

@author: cvskf
"""

import unittest

import need_functions

import csvw_functions_extra

import datetime
import json
import os

metadata_document_location=r'https://raw.githubusercontent.com/building-energy/need_functions/main/need_tables-metadata.json' 
metadata_filename = 'need_tables-metadata.json'

class TestDataFolder(unittest.TestCase):
    ""
    
    def test_get_available_csv_file_names(self):
        ""
        result = need_functions.get_available_csv_file_names()
        #print(result)
        self.assertEqual(
            result,
            ['need_2021_anon_dataset_4million.csv']
            )
        
    
    def _test__download_table_group_LOCAL_METADATA(self):
        ""
        fp_table_group_metadata = \
            os.path.join(os.pardir,metadata_filename)
        
        csvw_functions_extra.download_table_group(
            metadata_document_location=fp_table_group_metadata,
            data_folder='_data',
            overwrite_existing_files=False,
            verbose=True
            )
        
        
    def _test__import_table_group_to_sqlite(self):
        ""
        need_functions._import_table_group_to_sqlite(
            verbose=True)
    
    
    def _test_download_and_import_data(self):
        ""
        need_functions.download_and_import_data(
            verbose=True,
            )
        
        
    def test_get_need_table_names_in_database(self):
        ""
        result = \
            need_functions.get_need_table_names_in_database()
        #print(result)
        self.assertEqual(
            result,
            ['need_2021_anon_dataset_4million']
            )

        
    def test_get_metadata_columns_codes(self):
        ""
        result=need_functions.get_metadata_columns_codes(
            column_names='PROP_AGE_BAND',
            sql_table_name='need_2021_anon_dataset_4million'
            )
        #print(result)
        self.assertEqual(
            result,
            {
                'PROP_AGE_BAND': {
                    1: 'before 1930', 
                    2: '1930-1972', 
                    3: '1973-1999', 
                    4: '2000 or later'
                    }
                }
            )
        
        

class TestMainFunctions(unittest.TestCase):
    ""
    
    def test_get_distribution(self):
        ""
        result=need_functions.get_distribution(
            'PROP_TYPE',
            'need_2021_anon_dataset_4million'
            )
        #print(result)
        self.assertEqual(
            result,
            [
                {'PROP_TYPE': 'Bungalow', 'COUNT': 359717}, 
                {'PROP_TYPE': 'Detached', 'COUNT': 622875}, 
                {'PROP_TYPE': 'End terrace', 'COUNT': 358170}, 
                {'PROP_TYPE': 'Flat', 'COUNT': 862623}, 
                {'PROP_TYPE': 'Mid terrace', 'COUNT': 773569}, 
                {'PROP_TYPE': 'Semi detached', 'COUNT': 1023046}
            ]
            )


    def test_get_distribution_with_codes(self):
        ""
        result=need_functions.get_distribution(
            'PROP_AGE_BAND',
            'need_2021_anon_dataset_4million'
            )
        #print(result)
        self.assertEqual(
            result,
            [
                {'PROP_AGE_BAND': 'before 1930', 'COUNT': 1008310}, 
                {'PROP_AGE_BAND': '1930-1972', 'COUNT': 1570567}, 
                {'PROP_AGE_BAND': '1973-1999', 'COUNT': 868532}, 
                {'PROP_AGE_BAND': '2000 or later', 'COUNT': 552591}
                ]
            )
        


    
if __name__=='__main__':
    
    unittest.main()