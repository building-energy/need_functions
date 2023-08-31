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
from csvw_functions import csvw_functions_extra


_default_data_folder='_data'  # the default
_default_database_name='need_data.sqlite'

urllib.request.urlcleanup()


#%% data folder

def set_data_folder(
        metadata_document_location=r'https://raw.githubusercontent.com/building-energy/need_functions/main/need_tables-metadata.json', 
        data_folder=_default_data_folder,
        overwrite_existing_files=False,
        database_name=_default_database_name,
        remove_existing_tables=False,
        verbose=False,
        ):
    ""
    
    # download all tables to data_folder
    fp_metadata=\
        csvw_functions_extra.download_table_group(
            metadata_document_location,
            data_folder=data_folder,
            overwrite_existing_files=overwrite_existing_files,
            verbose=verbose
            )

    return
        
    # import all tables to sqlite
    csvw_functions_extra.import_table_group_to_sqlite(
        metadata_document_location=fp_metadata,
        data_folder=data_folder,
        database_name=database_name,
        remove_existing_tables=remove_existing_tables,
        verbose=verbose
        )


def _read_metadata_table_group_dict(
        data_folder,
        ):
    ""
    fp=os.path.join(
        data_folder,
        'snecs_tables-metadata.json'
        )
    with open(fp) as f:
        metadata_table_group_dic=json.load(f)
        
    return metadata_table_group_dic
        

    
#%% main functions

def _convert_to_iterator(
        x
        ):
    ""
    if x is None:
        return []
    elif isinstance(x,str):
        return [x]
    else:
        try:   
            _ = iter(x)
            return x
        except TypeError:
            return [x]
            

def _get_where_clause_list(
        d
        ):
    ""
    conditions=[]
    
    for k,v in d.items():
        
        if not v is None:
            
            x=_convert_to_iterator(v)
            x=[f'"{x}"' if isinstance(x,str) else f'{x}' for x in x] 
            if len(x)==1:
                x=f'("{k}" = {x[0]})'
            elif len(x)>1:
                x=','.join(x)
                x=f'("{k}" IN ({x}))'
            conditions.append(x)
            
    result=''
            
    if len(conditions)>0:
        
        x=' AND '.join(conditions)
        result=f'WHERE {x}'
        
    return result


def get_government_office_region_elec(
        year=None,
        region_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='elec_GOR_stacked_2005_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'year':year, 'gor':region_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result


def get_government_office_region_gas(
        year=None,
        region_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='gas_GOR_stacked_2005_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'year':year, 'region.code':region_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
    

def get_local_authority_elec(
        year=None,
        la_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='elec_LA_stacked_2005_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'year':year, 'la_code':la_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result


def get_local_authority_gas(
        year=None,
        la_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='gas_LA_stacked_2005_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'year':year, 'la.code':la_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result


def get_LSOA_elec_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        lsoa_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='elec_domestic_LSOA_stacked_2010_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'YEAR':year, 'LACode':la_code, 'MSOACode':msoa_code,'LSOACode':lsoa_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
    

def get_LSOA_gas_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        lsoa_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='gas_domestic_LSOA_stacked_2010_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'year':year, 'la.code':la_code, 'msoa.code':msoa_code,'lsoa.code':lsoa_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
    

def get_MSOA_elec_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='elec_domestic_MSOA_stacked_2010_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'YEAR':year, 'LACode':la_code, 'MSOAcode':msoa_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
    

def get_MSOA_gas_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='gas_domestic_MSOA_stacked_2010_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'year':year, 'la.code':la_code, 'msoa.code':msoa_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
    

def get_MSOA_elec_non_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='elec_non_domestic_MSOA_stacked_2010_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'YEAR':year, 'LACode':la_code, 'MSOAcode':msoa_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
     

def get_MSOA_gas_non_domestic(
        year=None,
        la_code=None,
        msoa_code=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name='gas_non_domestic_MSOA_stacked_2010_21'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        {'year':year, 'la.code':la_code, 'msoa.code':msoa_code}
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
    

def get_postcode_elec_all_meters(
        year,
        postcode=None,
        outcode=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name=f'Postcode_level_all_meters_electricity_{year}'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        dict(Postcode=postcode, Outcode=outcode)
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result


def get_postcode_elec_economy_7(
        year,
        postcode=None,
        outcode=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name=f'Postcode_level_economy_7_electricity_{year}'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        dict(Postcode=postcode, Outcode=outcode)
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
        

def get_postcode_elec_standard(
        year,
        postcode=None,
        outcode=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name=f'Postcode_level_standard_electricity_{year}'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        dict(Postcode=postcode, Outcode=outcode)
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result


def get_postcode_gas(
        year,
        postcode=None,
        outcode=None,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    table_name=f'Postcode_level_gas_{year}'
    
    fp_database=os.path.join(data_folder,database_name)
    
    where_clause=_get_where_clause_list(
        dict(Postcode=postcode, Outcode=outcode)
        )
        
    query=f"SELECT * FROM {table_name} {where_clause};"
    if verbose:
        print(query)
    
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(query).fetchall()]
        
    return result
    
    
