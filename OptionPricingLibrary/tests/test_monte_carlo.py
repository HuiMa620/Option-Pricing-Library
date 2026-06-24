# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 23:44:36 2026

@author: ma6
"""

#tet/test_monte_carlo.py
import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.monte_carlo import MonteCarloEngine


def test_monte_carlo():
    call = EuropeanOption(
        spot = 100,
        strike =110,
        tau = 0.5,
        option_type = 'Call'
        )
    
    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )
    
    bs_engine = BlackScholesEngine()
    mc_engine = MonteCarloEngine(
        n_paths = 10**6,
        seed = 42,
        antithetic = True
        )
    
    bs_price = bs_engine.price(call, market)
    mc_price, mc_error = mc_engine.price_error(call, market)
    z_score = abs(bs_price - mc_price)/mc_error
    
    assert z_score < 3.0
    
    
    



















