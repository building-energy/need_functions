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

```python
need_functions.get_available_csv_file_names()
```

### download_and_import_data

```python
need_functions.download_and_import_all_data(
        csv_file_names = None,
        data_folder='_data',
        database_name='need_data.sqlite',
        verbose=False,
        )
```

### get_need_table_names_in_database

```python
get_need_table_names_in_database(
        data_folder = '_data',
        database_name = 'need_data.sqlite',
        )
```

### get_metadata_columns_codes

```python
need_functions.get_metadata_columns_codes(
        column_names,
        table_name,
        data_folder = '_data',
        )
```


