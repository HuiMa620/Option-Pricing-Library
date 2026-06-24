# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 14:06:51 2026

@author: ma6
"""
import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import ExplicitFiniteDifferenceEngine

call = EuropeanOption(
    spot = 100,
    strike = 110,
    tau = 0.5,
    option_type = 'Call'
    )

put = EuropeanOption(
    spot = 100,
    strike = 110,
    tau =0.5,
    option_type = 'Put'
    )

market = MarketData(
    rate = 0.04,
    dividend = 0.02,
    volatility = 0.25
    )

bs_engine = BlackScholesEngine()
fd_engine = ExplicitFiniteDifferenceEngine()


for option in [call, put]:
    bs_price = bs_engine.price(option, market)
    fd_price = fd_engine.fast_price(option, market)
    fd_fast_price = fd_engine.fast_price(option, market)
    fd_diff = abs(bs_price - fd_price)
    fd_fast_diff = abs(bs_price - fd_fast_price)
    
    print(option.option_type)
    print(f"BS price:                    {bs_price:.10f}")
    print(f"FD price:                    {fd_price:.10f}")
    print(f"Difference of BS and FD:     {fd_diff:.10f}")
    print(f"Difference of BS and fast FD:{fd_fast_diff:.10f}")
    print()
    














