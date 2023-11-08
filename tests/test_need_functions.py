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
            sql_table_name='need_2021_anon_dataset_4million',
            column_names='PROP_AGE_BAND'
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
    
    
    def test_get_rows(self):
        ""
        result = \
            need_functions.get_rows(
                limit = 1
                )
        #print(result)
        self.assertEqual(
            result,
            [
                {
                    'PROP_TYPE': 'Semi detached', 
                    'PROP_AGE_BAND': 3, 
                    'FLOOR_AREA_BAND': 2, 
                    'CONSERVATORY_FLAG': '', 
                    'COUNCIL_TAX_BAND': 'B', 
                    'IMD_BAND_ENG': 2, 
                    'IMD_BAND_WALES': '', 
                    'REGION': 'E12000005', 
                    'LI_FLAG': 0, 
                    'LI_DATE': '', 
                    'CWI_FLAG': 1, 
                    'CWI_DATE': 2012, 
                    'PV_FLAG': 0, 
                    'PV_DATE': '', 
                    'MAIN_HEAT_FUEL': 1, 
                    'Gcons2005': 5000, 
                    'Gcons2006': 7300, 
                    'Gcons2007': 7900, 
                    'Gcons2008': 7400, 
                    'Gcons2009': 6400, 
                    'Gcons2010': 7700, 
                    'Gcons2011': 7000, 
                    'Gcons2012': 5800, 
                    'Gcons2013': 6400, 
                    'Gcons2014': 6800, 
                    'Gcons2015': 6800, 
                    'Gcons2016': 7200, 
                    'Gcons2017': 7200, 
                    'Gcons2018': 7700, 
                    'Gcons2019': 8000, 
                    'GasValFlag2005': 'V', 
                    'GasValFlag2006': 'V', 
                    'GasValFlag2007': 'V', 
                    'GasValFlag2008': 'V', 
                    'GasValFlag2009': 'V', 
                    'GasValFlag2010': 'V', 
                    'GasValFlag2011': 'V', 
                    'GasValFlag2012': 'V', 
                    'GasValFlag2013': 'V', 
                    'GasValFlag2014': 'V', 
                    'GasValFlag2015': 'V', 
                    'GasValFlag2016': 'V', 
                    'GasValFlag2017': 'V', 
                    'GasValFlag2018': 'V', 
                    'GasValFlag2019': 'V', 
                    'Econs2005': 1300, 
                    'Econs2006': 1400, 
                    'Econs2007': 1400, 
                    'Econs2008': 1400, 
                    'Econs2009': 1400, 
                    'Econs2010': 1500, 
                    'Econs2011': 1500, 
                    'Econs2012': 1300, 
                    'Econs2013': 1300, 
                    'Econs2014': 800, 
                    'Econs2015': 1200, 
                    'Econs2016': 1300, 
                    'Econs2017': 1300, 
                    'Econs2018': 1300, 
                    'Econs2019': 1100, 
                    'ElecValFlag2005': 'V', 
                    'ElecValFlag2006': 'V', 
                    'ElecValFlag2007': 'V', 
                    'ElecValFlag2008': 'V', 
                    'ElecValFlag2009': 'V', 
                    'ElecValFlag2010': 'V', 
                    'ElecValFlag2011': 'V', 
                    'ElecValFlag2012': 'V', 
                    'ElecValFlag2013': 'V', 
                    'ElecValFlag2014': 'V', 
                    'ElecValFlag2015': 'V', 
                    'ElecValFlag2016': 'V', 
                    'ElecValFlag2017': 'V', 
                    'ElecValFlag2018': 'V', 
                    'ElecValFlag2019': 'V'
                    }
                ]
            )
    
        
        result = \
            need_functions.get_rows(
                limit = 1,
                replace_codes = True
                )
        #print(result)
        self.assertEqual(
            result,
            [
                {
                    'PROP_TYPE': 'Semi detached', 
                    'PROP_AGE_BAND': '1973-1999', 
                    'FLOOR_AREA_BAND': '51 - 100 (square meters)', 
                    'CONSERVATORY_FLAG': 'unknown', 
                    'COUNCIL_TAX_BAND': 'B', 
                    'IMD_BAND_ENG': '2', 
                    'IMD_BAND_WALES': '', 
                    'REGION': 'E12000005', 
                    'LI_FLAG': 'not installed', 
                    'LI_DATE': '', 
                    'CWI_FLAG': 'installed', 
                    'CWI_DATE': 2012, 
                    'PV_FLAG': 'not installed', 
                    'PV_DATE': '', 
                    'MAIN_HEAT_FUEL': 'gas is the main heating fuel', 
                    'Gcons2005': 5000, 
                    'Gcons2006': 7300, 
                    'Gcons2007': 7900, 
                    'Gcons2008': 7400, 
                    'Gcons2009': 6400, 
                    'Gcons2010': 7700, 
                    'Gcons2011': 7000, 
                    'Gcons2012': 5800, 
                    'Gcons2013': 6400, 
                    'Gcons2014': 6800, 
                    'Gcons2015': 6800, 
                    'Gcons2016': 7200, 
                    'Gcons2017': 7200, 
                    'Gcons2018': 7700, 
                    'Gcons2019': 8000, 
                    'GasValFlag2005': 'valid', 
                    'GasValFlag2006': 'valid', 
                    'GasValFlag2007': 'valid', 
                    'GasValFlag2008': 'valid', 
                    'GasValFlag2009': 'valid', 
                    'GasValFlag2010': 'valid', 
                    'GasValFlag2011': 'valid', 
                    'GasValFlag2012': 'valid', 
                    'GasValFlag2013': 'valid', 
                    'GasValFlag2014': 'valid', 
                    'GasValFlag2015': 'valid', 
                    'GasValFlag2016': 'valid', 
                    'GasValFlag2017': 'valid', 
                    'GasValFlag2018': 'valid', 
                    'GasValFlag2019': 'valid', 
                    'Econs2005': 1300, 
                    'Econs2006': 1400, 
                    'Econs2007': 1400, 
                    'Econs2008': 1400, 
                    'Econs2009': 1400, 
                    'Econs2010': 1500, 
                    'Econs2011': 1500, 
                    'Econs2012': 1300, 
                    'Econs2013': 1300, 
                    'Econs2014': 800, 
                    'Econs2015': 1200, 
                    'Econs2016': 1300, 
                    'Econs2017': 1300, 
                    'Econs2018': 1300, 
                    'Econs2019': 1100, 
                    'ElecValFlag2005': 'valid', 
                    'ElecValFlag2006': 'valid', 
                    'ElecValFlag2007': 'valid', 
                    'ElecValFlag2008': 'valid', 
                    'ElecValFlag2009': 'valid', 
                    'ElecValFlag2010': 'valid', 
                    'ElecValFlag2011': 'valid', 
                    'ElecValFlag2012': 'valid', 
                    'ElecValFlag2013': 'valid', 
                    'ElecValFlag2014': 'valid', 
                    'ElecValFlag2015': 'valid', 
                    'ElecValFlag2016': 'valid', 
                    'ElecValFlag2017': 'valid', 
                    'ElecValFlag2018': 'valid', 
                    'ElecValFlag2019': 'valid'
                    }
                ]
            )
        
        # pandas
        result = \
            need_functions.get_rows(
                limit = 1,
                pandas = True,
                replace_codes=True
                )
        #print(result)
        
        
    
    
    
    # def test_get_distribution(self):
    #     ""
    #     result=need_functions.get_distribution(
    #         'PROP_TYPE',
    #         'need_2021_anon_dataset_4million'
    #         )
    #     #print(result)
    #     self.assertEqual(
    #         result,
    #         [
    #             {'PROP_TYPE': 'Bungalow', 'COUNT': 359717}, 
    #             {'PROP_TYPE': 'Detached', 'COUNT': 622875}, 
    #             {'PROP_TYPE': 'End terrace', 'COUNT': 358170}, 
    #             {'PROP_TYPE': 'Flat', 'COUNT': 862623}, 
    #             {'PROP_TYPE': 'Mid terrace', 'COUNT': 773569}, 
    #             {'PROP_TYPE': 'Semi detached', 'COUNT': 1023046}
    #         ]
    #         )


    # def test_get_distribution_with_codes(self):
    #     ""
    #     result=need_functions.get_distribution(
    #         'PROP_AGE_BAND',
    #         'need_2021_anon_dataset_4million'
    #         )
    #     #print(result)
    #     self.assertEqual(
    #         result,
    #         [
    #             {'PROP_AGE_BAND': 'before 1930', 'COUNT': 1008310}, 
    #             {'PROP_AGE_BAND': '1930-1972', 'COUNT': 1570567}, 
    #             {'PROP_AGE_BAND': '1973-1999', 'COUNT': 868532}, 
    #             {'PROP_AGE_BAND': '2000 or later', 'COUNT': 552591}
    #             ]
    #         )
        


    
if __name__=='__main__':
    
    unittest.main()