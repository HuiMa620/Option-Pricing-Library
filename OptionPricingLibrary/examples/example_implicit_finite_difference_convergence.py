#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:42:20 2026

@author: huima
"""

import os
os.chdir('..')
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import ImplicitFiniteDifferenceEngine


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


test_settings = [
    (100, 100),
    (100, 500),
    (200, 500),
    (200, 1000),
    (400, 1000),
]

bs_engine = BlackScholesEngine()
bs_price = bs_engine.price(call, market)
print(call.option_type)
print(f"Benchmark price: {bs_price:.10f}")
print()
print(
      f"{'n_s':>15}"
      f"{'n_t':>15}"
      f"{'Implicit FD price':>15}"
      f"{'abs error':>15}"
      )
print('-'*86)

for n_s, n_t in test_settings:
    implicit_engine = ImplicitFiniteDifferenceEngine(
        s_max = 300,
        n_s = n_s,
        n_t = n_t
        )
    
    implicit_price = implicit_engine.price(call, market)
    abs_error = abs(bs_price - implicit_price)
    print(
        f"{n_s:15d}"
        f"{n_t:15d}"
        f"{implicit_price:15.10f}"
        f"{abs_error:15.10f}"
        )
    print()
    
    
    




