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
import matplotlib.pyplot as plt
from matplotlib import ticker


_default_data_folder='_data'  # the default
_default_database_name='need_data.sqlite'

urllib.request.urlcleanup()


#%% data folder

def set_data_folder(
        metadata_document_location=r'https://raw.githubusercontent.com/building-energy/need_functions/main/need_tables-metadata.json', 
        data_folder=_default_data_folder,
        overwrite_existing_files=False,
        import_to_database=True,
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

    if import_to_database:
        
        # import all tables to sqlite
        csvw_functions_extra.import_table_group_to_sqlite(
            metadata_document_location=fp_metadata,
            data_folder=data_folder,
            database_name=database_name,
            remove_existing_tables=remove_existing_tables,
            verbose=verbose
            )


def get_metadata_table_group_dict(
        data_folder=_default_data_folder,
        ):
    ""
    fp=os.path.join(
        data_folder,
        'need_tables-metadata.json'
        )
    with open(fp) as f:
        metadata_table_group_dict=json.load(f)
        
    return metadata_table_group_dict


def get_metadata_table_dict(
        table_name,
        metadata_table_group_dict=None,
        data_folder=_default_data_folder
        ):
    ""
    if metadata_table_group_dict is None:
        
        metadata_table_group_dict=\
            get_metadata_table_group_dict(
                data_folder=data_folder,
                )
    
    for metadata_table_dict in metadata_table_group_dict['tables']:
        
        if metadata_table_dict['https://purl.org/berg/csvw_functions/vocab/sql_table_name']['@value']==table_name:
            
            break
        
    else:
        
        raise Exception
    
    return metadata_table_dict
    
       

def get_metadata_column_dict(
        column_name,
        table_name,
        metadata_table_group_dict=None,
        data_folder=_default_data_folder
        ):
    ""
    if metadata_table_group_dict is None:
        
        metadata_table_group_dict = \
            get_metadata_table_group_dict(
                data_folder=data_folder,
                )
            
    metadata_table_dict = \
        get_metadata_table_dict(
               table_name,
               metadata_table_group_dict
               )
    
    for metadata_column_dict in metadata_table_dict['tableSchema']['columns']:
        
        if metadata_column_dict['name']==column_name:
            
            break
        
    else:
        
        raise Exception
    
    return metadata_column_dict
    

def get_codes(
        column_name,
        table_name,
        metadata_table_group_dict=None,
        data_folder=_default_data_folder
        ):
    ""
    metadata_column_dict = \
        get_metadata_column_dict(
                column_name,
                table_name,
                metadata_table_group_dict=metadata_table_group_dict,
                data_folder=data_folder
                )
        
    datatype_base = metadata_column_dict['datatype']['base']
        
    codes = metadata_column_dict.get(
        'https://purl.org/berg/csvw_functions/vocab/codes',
        {}
        )
    
    if datatype_base == 'integer':
        x=lambda y:int(y) if y!='' else y
    elif datatype_base in ['decimal','number']:
        x=lambda y:float(y) if y!='' else y
    elif datatype_base == 'string':
        x=lambda y:y
    else:
        raise Exception
    
    codes = {x(k):v['@value'] for k,v in codes.items()}
    
    return codes


def run_sql(
        sql_query,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    fp_database=os.path.join(data_folder,database_name)
    
    if verbose:
        print('fp_database',fp_database)
        print(sql_query)
        
    with sqlite3.connect(fp_database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        result=[dict(x) for x in c.execute(sql_query).fetchall()]
        
    return result


def add_index(
        fields,
        table_name,
        unique=False,
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
    fields=_convert_to_iterator(fields)
    fields_string='__'.join(fields)
    
    if unique:
        unique_string='UNIQUE'
    else:
        unique_string=''
    
    index_name=f'index__{table_name}__{fields_string}'
    if unique:
        index_name=f'{index_name}__UNIQUE'
    
    if verbose:
        print('index_name',index_name)
        
    column_list='","'.join(fields)
    column_list=f'"{column_list}"'
        
    fp_database=os.path.join(data_folder,database_name)
    
    query=f"""
        CREATE {unique_string} INDEX "{index_name}" 
        ON "{table_name}"({column_list});
    """
    if verbose:
        print('fp_database',fp_database)
        print(query)
        
    try:
        
        with sqlite3.connect(fp_database) as conn:
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            
    except sqlite3.OperationalError:
        
        if verbose:
            print('Index not created - already exists in table')

    
#%% main functions

def get_distribution(
        field,
        table_name='need_2021_anon_dataset_4million',
        data_folder=_default_data_folder,
        database_name=_default_database_name,
        verbose=False
        ):
    ""
   
    query=f"""
        SELECT "{field}", COUNT("{field}") AS COUNT
        FROM "{table_name}" 
        GROUP BY "{field}" 
        ORDER BY "{field}"
        """
        
    result = run_sql(
        query,
        data_folder=data_folder,
        database_name=database_name,
        verbose=verbose
        )
    
    codes = \
        get_codes(
            field,
            table_name
            )
    
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
    verbose=False
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
    x=[z[field] for z in result]
    y=[z['COUNT'] for z in result]
    fig, ax = plt.subplots(figsize=(16,6))
    bars=ax.barh(x,y)
    ax.get_xaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.bar_label(bars, labels=[format(z/sum(y), ".2%") for z in y])
    return fig,ax
















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
    
    
