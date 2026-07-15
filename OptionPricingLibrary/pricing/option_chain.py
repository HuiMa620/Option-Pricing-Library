# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:11:35 2026

@author: ma6
"""

import csv

Required_Columns = [
    'tau',
    'strike',
    'option_type',
    'bid',
    'ask'
    ]


def load_option_chain_csv(file_path):
    '''
    Load option data from a csv file
    
    Expected csv columns:
        tau strike option_type bid ask
        
    Example csv:
        tau   strike   option_type   bid   ask
        0.5     90       Put         1.20  1.30
        0.5     100      Call        5.10  5.30
        1.0     110      Call        7.00  7.25
    '''
    quotes = []
    
    with open(file_path, mode = 'r', newline = '') as csv_file:
        reader = csv.DictReader(csv_file)
        
        _validate_required_columns(reader.fieldnames)
        
        for row_number, row in enumerate(reader, start = 2):
            quote = _parse_option_chain_row(
                row = row,
                row_number = row_number
                )
            
            quotes.append(quote)
            
        if len(quotes) == 0:
            raise ValueError('Option chain csv contains no data rows.')
        return quotes
    
    

def _validate_required_columns(fieldnames):
    
    if fieldnames is None:
        raise ValueError('CSV file appears to be empty or missing a header row.')
        
    missing_columns = [
        column
        for column in Required_Columns
        if column not in fieldnames
        ]
    
    if len(missing_columns) > 0:
        raise ValueError(
            'csv file is missing required columns: '
            f'{missing_columns}. '
            f'Required columns are: {Required_Columns}'            
            )
        
        
def _parse_option_chain_row(row, row_number):
    '''
    Parse and validate one row from an option chain csv file
    '''
    
    tau = _parse_positive_float(
        value = row['tau'],
        field_name = 'tau',
        row_number = row_number
        )
    
    strike = _parse_positive_float(
        value = row['strike'],
        field_name = 'strike',
        row_number = row_number
        )
    
    bid = _parse_non_negative_float(
        value = row['bid'],
        field_name = 'bid',
        row_number = row_number
        )
    
    ask = _parse_positive_float(
        value = row['ask'],
        field_name = 'ask',
        row_number = row_number
        )
    
    option_type = row['option_type'].strip()
    
    if option_type not in ['Call', 'Put']:
        raise ValueError(
            f"Row {row_number}: option_type must be 'Call' or 'Put', "
            f"but got {option_type!r}."
            )
    
    if ask < bid:
        raise ValueError(
            f"Row {row_number}: ask must be greater than or equal to bid. "
            f"Got bid = {bid}, ask = {ask}."
            )
        
    mid_price = 0.5 *(bid + ask)
    
    if mid_price <= 0:
        raise ValueError(
            f"Row {row_number}: mid price must be positive. "
            f"Got mid_price = {mid_price}."
            )
        
    quote = {
        'tau': tau,
        'strike': strike,
        'option_type': option_type,
        'market_price': mid_price
        }
    
    return quote



def _parse_positive_float(value, field_name, row_number):
    #parse a strictly a positive float from a csv file
    try:
        parsed_value = float(value)
    except ValueError:
        raise ValueError(
            f"Row {row_number}: {field_name} must be a number, "
            f"but got {value!r}."
            )
    
    if parsed_value <= 0:
        raise ValueError(
            f"Row {row_number}: {field_name} must be positive, "
            f"but got {parsed_value}."
            )
        
    return parsed_value


def _parse_non_negative_float(value, field_name, row_number):
    #parse a non-negative float from a csv field
    
    try:
        parsed_value = float(value)
    except ValueError:
        raise ValueError(
            f"Row {row_number}: {field_name} must be a number, "
            f"but got {value!r}."
            )
        
    if parsed_value < 0:
        raise ValueError(
            f"Row {row_number}: {field_name} must be a non_negative, "
            f"but got {parsed_value}."
            )
        
    return parsed_value








