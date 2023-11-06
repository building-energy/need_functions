# need_functions
Python package for working with the National Energy Efficiency Data-Framework (NEED) dataset

## Overview

The National Energy Efficiency Data-Framework (NEED) dataset is published by the UK Government here: https://www.gov.uk/government/collections/national-energy-efficiency-data-need-framework

This Python package contains a series of Python functions which can be used to:
- Download the CSV files which make up the NEED dataset.
- Import the data into a SQLite database.
- Access the data in the database, for data analysis and visualisation.

A description of the CSV files in the NEED dataset, along with instructions for downloading and importing in SQLite, has been created using the format of a [CSVW metadata Table Group object](https://www.w3.org/TR/2015/REC-tabular-metadata-20151217/#table-groups) (saved as a JSON file), which is available here: https://github.com/building-energy/need_functions/blob/main/need_tables-metadata.json

## Installation

`pip install git+https://github.com/building-energy/need_functions`

The python package [`csvw_functions_extra`](https://github.com/stevenkfirth/csvw_functions_extra) will also need to be installed.

## Quick Start




## API

### get_available_csv_file_names

Description: Returns the CSV file names of all tables in the [CSVW metadata file](https://raw.githubusercontent.com/building-energy/snecs_functions/main/snecs_tables-metadata.json).

```python
need_functions.get_available_csv_file_names()
```

Returns: A list of the `https://purl.org/berg/csvw_functions_extra/vocab/csv_file_name` value in each table.


### download_and_import_data

Description: Downloads all the NEED data and imports all data into a SQLite database.

```python
need_functions.download_and_import_all_data(
        csv_file_names = None,
        data_folder='_data',
        database_name='need_data.sqlite',
        verbose=False,
        )
```

The data to be downloaded is described in the CSVW metadata file here: https://raw.githubusercontent.com/building-energy/snecs_functions/main/snecs_tables-metadata.json

Running this function will:
- create the `data_folder` if it does not already exist.
- download the CSV files to the data folder.
- download the CSVW metadata file to the data folder. This is named 'need_tables-metadata.json'.
- create a SQLite database named `database_name` in the data folder if it does not already exist.
- import the CSV data into the SQLite database.

Arguments:
- **csv_file_names** *(str, list or None)*: The CSV file name(s) to download and import (see [`get_available_csv_file_names`](#get_available_csv_file_names)). `None` will download the entire dataset.
- **data_folder** *(str)*: The filepath of a local folder where the downloaded CSV data is saved to and the SQLite database is stored.
- **database_name** *(str)*: The name of the SQLite database, relative to the data_folder.
- **verbose (bool)**: If True, then this function prints intermediate variables and other useful information.

Returns: None


### get_need_table_names_in_database

Description: Returns the table names of all NEED tables in the SQLite database.

```python
get_need_table_names_in_database(
        data_folder = '_data',
        database_name = 'need_data.sqlite',
        )
```

- **data_folder** *(str)*: The filepath of a local folder where the SQLite database is stored.
- **database_name** *(str)*: The name of the SQLite database, relative to the data_folder.

Returns: A list of table names.

### get_metadata_columns_codes

Description: Returns lookup dictionaries for the NEED lookup codes for one or more columns.

```python
need_functions.get_metadata_columns_codes(
        column_names,
        sql_table_name,
        data_folder = '_data',
        )
```

Arguments:
- **column_name** *(str)*: The `name` value of a column in a CSVW TableSchema object.
- **sql_table_name** *(str)*: The `https://purl.org/berg/csvw_functions_extra/vocab/sql_table_name` value of the table.
- **data_folder** *(str)*: The filepath of a local folder where the normalized CSVW metadata file is saved.

Returns *(dict of dicts)*: A dictionary with:
- keys: the names of the column(s)
- values: a dictionary with keys as lookup codes and values as code descriptions.


