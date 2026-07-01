# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 22:31:35 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.monte_carlo import MonteCarloEngine

if __name__ == '__main__':
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
    mc_plain_engine = MonteCarloEngine(antithetic = False)
    mc_antithetic_engine = MonteCarloEngine()
    
    bs_price = bs_engine.price(call, market)
    mc_plain_price, mc_plain_error = mc_plain_engine.price_error(call, market)
    mc_antithetic_price, mc_antithetic_error = mc_antithetic_engine.price_error(call, market)
    mc_cv_price, mc_cv_error = mc_antithetic_engine.price_control_variate_error(call, market)
    
    print(f"BS price:                 {bs_price:.10f}")
    print(f"Plain MC price:           {mc_plain_price:.10f}")
    print(f"Plain MC error:           {mc_plain_error:.10f}")
    print(f"Antithetic MC price:      {mc_antithetic_price:.10f}")
    print(f"Antithetic MC error:      {mc_antithetic_error:.10f}")
    print(f"Control variate MC price: {mc_cv_price:.10f}")
    print(f"Control variate MC error: {mc_cv_error:.10f}")
















