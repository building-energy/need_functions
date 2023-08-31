# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:08:36 2023

@author: cvskf
"""

import unittest

from need_functions import need_functions

import datetime
import json
import os


class TestDataFolder(unittest.TestCase):
    ""
    
    def test_set_data_folder(self):
        ""
        
        fp=os.path.join(os.pardir,'need_tables-metadata.json')
        
        need_functions.set_data_folder(
            metadata_document_location=fp,
            #verbose=True,
            #overwrite_existing_files=True,
            import_to_database=False,
            remove_existing_tables=True,
            )


    def test_get_metadata_table_group_dict(self):
        ""
        result=need_functions.get_metadata_table_group_dict()
        #print(list(result.keys()))
        self.assertEqual(
            list(result.keys()),
            ['@context', '@type', 'tables']
            )
        
        
    def test_get_metadata_table_dict(self):
        ""
        result=need_functions.get_metadata_table_dict(
            'need_2021_anon_dataset_4million'
            )
        #print(list(result.keys()))
        self.assertEqual(
            list(result.keys()),
            [
                '@type', 
                'url', 
                'https://purl.org/berg/csvw_functions/vocab/zip_download_url', 
                'https://purl.org/berg/csvw_functions/vocab/zip_file_name', 
                'https://purl.org/berg/csvw_functions/vocab/csv_zip_extract_path', 
                'https://purl.org/berg/csvw_functions/vocab/csv_file_name', 
                'https://purl.org/berg/csvw_functions/vocab/sql_table_name', 
                'rdfs:seeAlso', 
                'tableSchema'
                ]
            )
        
        
    def test_get_metadata_column_dict(self):
        ""
        result=need_functions.get_metadata_column_dict(
            column_name='PROP_AGE_BAND',
            table_name='need_2021_anon_dataset_4million'
            )
        #print(list(result.keys()))
        self.assertEqual(
            list(result.keys()),
            [
                'name', 
                'datatype', 
                'rdfs:comment', 
                'https://purl.org/berg/csvw_functions/vocab/column_notes', 
                'https://purl.org/berg/csvw_functions/vocab/codes'
                ]
            )
        
        
    def test_get_codes(self):
        ""
        result=need_functions.get_codes(
            column_name='PROP_AGE_BAND',
            table_name='need_2021_anon_dataset_4million'
            )
        #print(result)
        self.assertEqual(
            result,
            {
                1: 'before 1930', 
                2: '1930-1972', 
                3: '1973-1999', 
                4: '2000 or later'
                }
            )
        
    
    def test_run_sql(self):
        ""
        query="SELECT * FROM need_2021_anon_dataset_4million LIMIT 1"
        result=need_functions.run_sql(query)
        #print(result)
        self.assertEqual(
            len(result),
            1
            )
        
        
    def test_add_index(self):
        ""
        need_functions.add_index(
            'PROP_TYPE',
            'need_2021_anon_dataset_4million',
            #unique=True,
            #verbose=True
            )
        
        need_functions.add_index(
            'PROP_AGE_BAND',
            'need_2021_anon_dataset_4million'
            )


class TestMainFunctions(unittest.TestCase):
    ""
    
    def test_get_distribution(self):
        ""
        result=need_functions.get_distribution('PROP_TYPE')
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
        result=need_functions.get_distribution('PROP_AGE_BAND')
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