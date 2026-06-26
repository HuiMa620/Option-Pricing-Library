# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 22:14:09 2026

@author: ma6
"""

#import os
#os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import (
    ImplicitFiniteDifferenceEngine,
    AmericanPutImplicitFiniteDifferenceEngine
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

bs_engine = BlackScholesEngine()
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

bs_put = bs_engine.price(put, market)
european_put_price = european_engine.price(put, market)
american_put_price = american_engine.price(put, market)

print(f"European put BS price:   {bs_put:.10f}")
print(f"European put implicit FD:{european_put_price:.10f}")
print(f"American put implicit FD:{american_put_price:.10f}")
print(f"Early exercise premium:  {american_put_price - european_put_price:.10f}")



















