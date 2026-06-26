# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:35:11 2026

@author: ma6
"""



from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.finite_difference import (
    ImplicitFiniteDifferenceEngine,
    AmericanPutImplicitFiniteDifferenceEngine
    )

def test_american_put_greater_than_european_put():
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
    
    european_engine = ImplicitFiniteDifferenceEngine(
        s_max = 300,
        n_s = 200,
        n_t = 500
        )
    
    american_engine = AmericanPutImplicitFiniteDifferenceEngine(
        s_max = 300,
        n_s = 200,
        n_t = 500
        )
    
    european_put_price = european_engine.price(put, market)
    american_put_price = american_engine.price(put, market)
    
    assert american_put_price >= european_put_price
    

def test_american_put_price_above_intrinsic_value():
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
    
    american_engine = AmericanPutImplicitFiniteDifferenceEngine(
        s_max = 300,
        n_s = 200,
        n_t = 500
        )
    
    american_put_price = american_engine.price(put, market)
    intrinsic_value = max(put.strike - put.spot, 0.0)
    
    assert american_put_price >= intrinsic_value
    








