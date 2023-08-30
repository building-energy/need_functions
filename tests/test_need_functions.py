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
            verbose=True,
            #overwrite_existing_files=True,
            remove_existing_tables=True,
            )


    def test__read_metadata_table_group_dict(self):
        ""
        


class TestMainFunctions(unittest.TestCase):
    ""
    
    





    
if __name__=='__main__':
    
    unittest.main()