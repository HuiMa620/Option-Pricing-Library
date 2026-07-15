# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 19:16:10 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
import csv
import tempfile 

from pricing.option_chain import load_option_chain_csv
from pricing.volatility_surface import VolatilitySurface

def _write_temp_csv(rows, fieldnames = None):
    
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    
    temp_file = tempfile.NamedTemporaryFile(
        mode = "w",
        newline = "",
        suffix = ".csv",
        delete = False
        )
    
    with temp_file as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames = fieldnames
            )
        writer.writeheader()
        writer.writerows(rows)
    
    return temp_file.name



def test_load_option_chain_csv_computes_mid_prices():
    rows = [
        {
            'tau': '0.5',
            'strike': '100',
            'option_type': 'Call',
            'bid': '5.0',
            'ask': '5.4'
            }
        ]
    file_path = _write_temp_csv(rows)
    quotes = load_option_chain_csv(file_path)
    
    assert len(quotes) ==1
    assert quotes[0]['tau'] == 0.5
    assert quotes[0]['strike'] == 100.0
    assert quotes[0]['option_type'] == 'Call'
    assert abs(quotes[0]['market_price'] - 5.2) < 1e-12
    
    
    
def test_load_option_chain_csv_multiple_rows():
    rows = [
        {
            'tau': '0.5',
            'strike': '90',
            'option_type': 'Put',
            'bid': '1.2',
            'ask': '1.4'
            },
        {
            'tau': '1.0',
            'strike': '110',
            'option_type': 'Call',
            'bid': '7.0',
            'ask': '7.2'
            }
        ]
    
    file_path = _write_temp_csv(rows)
    
    quotes = load_option_chain_csv(file_path)
    
    assert len(quotes) == 2
    assert quotes[0]['tau'] == 0.5
    assert quotes[0]['strike'] == 90.0
    assert quotes[0]['option_type'] == 'Put'
    assert abs(quotes[0]['market_price'] - 1.3) < 1e-12
    
    assert quotes[1]['tau'] == 1.0
    assert quotes[1]['strike'] == 110.0
    assert quotes[1]['option_type'] == 'Call'
    assert abs(quotes[1]['market_price'] - 7.1) < 1e-12
    
    
    
def test_load_option_chain_csv_missing_column_raises_error():
    rows = [
        {
            'tau': '0.5',
            'strike': '100',
            'option_type': 'Call',
            'bid': '5.0'
            #missing ask
            }
        ]
    
    fieldnames = [
        'tau',
        'strike',
        'option_type',
        'bid'
        ]
    
    file_path = _write_temp_csv(
        rows = rows,
        fieldnames = fieldnames
        )
    
    try:
        load_option_chain_csv(file_path)
    except ValueError:
        print('Passed: missing column raises ValueError.')
    else:
        raise AssertionError(
            'Expected ValueError for missing required column, '
            'but no error was raised.'
            )
    

def test_load_option_chain_csv_ask_below_bid_raises_error():
    rows = [
        {
            'tau': '0.5',
            'strike': '100',
            'option_type': 'Call',
            'bid': '5.4',
            'ask': '5.0'
            }
        ]
    
    file_path = _write_temp_csv(rows)
    
    try:
        load_option_chain_csv(file_path)
    except ValueError:
        print('Passed: ask below bid raises ValueError.')
    else:
        raise AssertionError(
            'Expected ValueError for ask below bid, '
            'but no error was raised.'
            )
        
        
def test_load_option_chain_csv_invalid_option_type_raises_error():
    rows = [
        {
            'tau': '0.5',
            'strike': '100',
            'option_type': 'InvalidType',
            'bid': '5.0',
            'ask': '5.4'
            }
        ]
    
    file_path = _write_temp_csv(rows)
    
    try:
        load_option_chain_csv(file_path)
    except ValueError:
        print('Passed: invalid option_type raises ValueError.')
    else:
        raise AssertionError(
            'Expected ValueError for invalid option_type, '
            'but no error was raised.'
            )
        

def test_load_option_chain_csv_negative_bid_raises_error():
    rows = [
        {
            'tau': '0.5',
            'strike': '100',
            'option_type': 'Call',
            'bid': '-1.0',
            'ask': '5.4'
            }
        ]
    
    file_path = _write_temp_csv(rows)
    
    try:
        load_option_chain_csv(file_path)
    except ValueError:
        print('Passed: negative bid raises ValueError.')
    else:
        raise AssertionError(
            'Expected ValueError for negative bid, '
            'but no error was raised.'
            )
    
    
def test_build_surface_from_synthetic_option_chain_csv():
    quotes = load_option_chain_csv(
        'data/synthetic_option_chain.csv'
        )
    
    surface = VolatilitySurface.from_option_quotes(
        quotes = quotes,
        spot = 100.0,
        rate = 0.04,
        dividend = 0.02,
        initial_vol_guess = 0.2
        )
    
    assert len(quotes) == 25
    assert len(surface.maturities) == 5
    assert len(surface.strikes) == 5
    assert surface.vol_matrix.shape == (5,5)
    
    assert np.all(surface.vol_matrix > 0)
    assert not np.any(np.isnan(surface.vol_matrix))
    
    
    
    


if __name__ == '__main__':
    test_load_option_chain_csv_computes_mid_prices()
    test_load_option_chain_csv_multiple_rows()
    test_load_option_chain_csv_missing_column_raises_error()
    test_load_option_chain_csv_ask_below_bid_raises_error()
    test_load_option_chain_csv_invalid_option_type_raises_error()
    test_load_option_chain_csv_negative_bid_raises_error()
    test_build_surface_from_synthetic_option_chain_csv()

