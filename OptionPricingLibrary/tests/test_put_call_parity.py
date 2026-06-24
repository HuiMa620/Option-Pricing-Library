# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 23:23:03 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.validation import check_put_call_parity

def test_put_call_parity():
    call = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 0.5,
        option_type = 'Call'
        )
    
    put = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 0.5,
        option_type = 'Put'
        )
    
    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )
    
    engine = BlackScholesEngine()
    call_price = engine.price(call, market)
    put_price = engine.price(put, market)
    
    left, right, error = check_put_call_parity(
        call_price,
        put_price,
        call,
        market
        )
    
    assert abs(error) < 1e-10

















