# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:16:59 2023

@author: cvskf
"""

import urllib
import urllib.request
import json
import os
import sqlite3
import csvw_functions_extra
import matplotlib.pyplot as plt
from matplotlib import ticker


_default_data_folder='_data'  # the default
_default_database_name='need_data.sqlite'

urllib.request.urlcleanup()

metadata_document_location=r'https://raw.githubusercontent.com/building-energy/need_functions/main/need_tables-metadata.json' 
metadata_filename = 'need_tables-metadata.json'


#%% data folder

def get_available_csv_file_names(
        ):
    """Returns the CSV file names of all tables in the (remote) CSVW metadata file.
    
    """
    result = \
        csvw_functions_extra.get_available_csv_file_names(
            metadata_document_location = metadata_document_location
            )
    
    return result


def _download_table_group(
        data_folder = '_data',
        csv_file_names = None,  
        verbose = False
        ):
    """
    """
    csvw_functions_extra.download_table_group(
        metadata_document_location = metadata_document_location,
        csv_file_names = csv_file_names,
        data_folder = data_folder,
        overwrite_existing_files = True,
        verbose = verbose
        )
        
    
def _import_table_group_to_sqlite(
        data_folder = '_data',
        database_name = 'need_data.sqlite',
        csv_file_names = None, 
        verbose = False
        ):
    """
    """
    csvw_functions_extra.import_table_group_to_sqlite(
        metadata_filename = metadata_filename,
        csv_file_names = csv_file_names,
        data_folder = data_folder,
        database_name = database_name,
        overwrite_existing_tables = True,
        verbose = verbose
        )
        


def download_and_import_data(
        csv_file_names = None,
        data_folder = '_data',
        database_name = 'need_data.sqlite',
        verbose=False,
        ):
    """
    """
    _download_table_group(
            data_folder = data_folder,
            csv_file_names = csv_file_names,  
            verbose = verbose
            )
    
    _import_table_group_to_sqlite(
            data_folder = data_folder,
            database_name = database_name,
            csv_file_names = csv_file_names, 
            verbose = verbose
            )
    
    
def get_need_table_names_in_database(
        data_folder = '_data',
        database_name = 'need_data.sqlite',
        ):
    """
    """
    
    result = \
        csvw_functions_extra.get_sql_table_names_in_database(
            data_folder,
            database_name,
            metadata_filename
            )
    
    return result
    

       
def get_metadata_columns_codes(
        column_names,
        sql_table_name,
        data_folder = '_data',
        ):
    """
    """    

    metadata_filename = 'need_tables-metadata.json'

    result = \
        csvw_functions_extra.get_metadata_columns_codes(
            column_names,
            sql_table_name,
            data_folder = data_folder,
            metadata_filename = metadata_filename
            )

    return result


    
#%% main functions

def get_distribution(
        field,
        sql_table_name,
        data_folder = '_data',
        database_name = 'need_data.sqlite',
        verbose=False
        ):
    ""
   
    query=f"""
        SELECT "{field}", COUNT("{field}") AS COUNT
        FROM "{sql_table_name}" 
        GROUP BY "{field}" 
        ORDER BY "{field}"
        """
        
    result = csvw_functions_extra.run_sql(
        query,
        data_folder=data_folder,
        database_name=database_name,
        verbose=verbose
        )
    
    codes = \
        get_metadata_columns_codes(
            field,
            sql_table_name
            )
        
    codes = codes[field]
    
    if verbose:
        print('codes', codes)
        
    if len(codes)>0:
    
        result=[{k:codes.get(v,v) if k==field else v
                 for k,v in x.items()} 
                for x in result]
        
    return result


def plot_distribution(
    field,
    table_name='need_2021_anon_dataset_4million',
    data_folder=_default_data_folder,
    database_name=_default_database_name,
    verbose=False,
    y_label_max_size=50
    ):
    ""
    result = \
        get_distribution(
            field,
            table_name=table_name,
            data_folder=data_folder,
            database_name=database_name,
            verbose=verbose
            )
    result=result[::-1]
    x=[str(z[field])[:y_label_max_size] for z in result]
    y=[z['COUNT'] for z in result]
    fig, ax = plt.subplots(figsize=(16,6))
    bars=ax.barh(x,y)
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.bar_label(bars, labels=[format(z/sum(y), ".2%") for z in y])
    return fig,ax















    
