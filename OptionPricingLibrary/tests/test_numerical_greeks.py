# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 23:33:03 2026

@author: ma6
"""

#test/test_numerical_greeks.py


from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.numerical_greeks import (
    numerical_delta,
    numerical_gamma, 
    numerical_theta,
    numerical_vega
    )



def test_numerical_greeks_vs_analytical_greeks():
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
    
    engine = BlackScholesEngine()
    
    analytic_delta = engine.Delta(call, market)
    analytic_gamma = engine.Gamma(call, market)
    analytic_theta = engine.Theta(call, market)
    analytic_vega = engine.Vega(call, market)
    
    numeric_delta = numerical_delta(engine, call, market, bump = 1e-4)
    numeric_gamma = numerical_gamma(engine, call, market, bump = 1e-3)
    numeric_theta = numerical_theta(engine, call, market, bump = 1e-4)
    numeric_vega = numerical_vega(engine, call, market, bump = 1e-5)
    
    assert abs(analytic_delta - numeric_delta) < 1e-5
    assert abs(analytic_gamma - numeric_gamma) < 1e-5
    assert abs(analytic_theta - numeric_theta) < 1e-5
    assert abs(analytic_vega - numeric_vega) < 1e-4
    
































