# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 22:57:13 2026

@author: ma6
"""
#test/test_black_scholes.py
import os
os.chdir('..')
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine

def test_black_scholes_call_price():
    call = EuropeanOption(
        spot = 100,
        strike = 100,
        tau = 1.0,
        option_type = 'Call'
        )
    
    market = MarketData(
        rate = 0.05,
        dividend = 0.00,
        volatility = 0.2       
        )
    
    expected_price = 10.4505835722
    
    engine = BlackScholesEngine()
    price = engine.price(call, market)
    
    diff = abs(price - expected_price)
    assert diff < 1e-8



def test_black_scholes_put_price():
    put = EuropeanOption(
        spot = 100,
        strike = 100,
        tau = 1.0,
        option_type = 'Put'
        )
    
    market = MarketData(
        rate = 0.05,
        dividend = 0.0,
        volatility = 0.2
        )
    
    expected_price = 5.5735260223
    
    engine = BlackScholesEngine()
    price = engine.price(put, market)
    
    diff = abs(price - expected_price)
    assert diff < 1e-8

















