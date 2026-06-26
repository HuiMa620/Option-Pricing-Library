# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 13:16:40 2026

@author: ma6
"""



from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import CrankNicolsonFiniteDifferenceEngine

def test_crank_nicolson_vs_black_scholes_call():
    call = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 0.5,
        option_type = 'Call'
        )
    
    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )
    
    bs_engine = BlackScholesEngine()
    bs_price = bs_engine.price(call, market)
    
    cn_engine = CrankNicolsonFiniteDifferenceEngine()
    cn_price = cn_engine.price(call, market)
    
    assert abs(cn_price - bs_price) < 0.05


def test_crank_nicolson_vs_black_scholes_put():
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
    
    bs_engine = BlackScholesEngine()
    bs_price = bs_engine.price(put, market)
    
    cn_engine = CrankNicolsonFiniteDifferenceEngine()
    cn_price = cn_engine.price(put, market)
    
    assert abs(cn_price - bs_price) < 0.05











