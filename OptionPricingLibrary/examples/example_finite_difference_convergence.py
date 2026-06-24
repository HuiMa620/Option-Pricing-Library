# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:38:47 2026

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

market = MarketData(
    rate = 0.04,
    dividend = 0.02,
    volatility = 0.25
    )

grid_test = [
    (50, 5000),
    (100, 10000),
    (200, 20000),
    (400, 40000),
    (800, 80000)
    ]

bs_engine = BlackScholesEngine()
bs_price = bs_engine.price(call, market)
print(f"Black Scholes Benchmark price:{bs_price:.10f}")
print()
print(
      f"{'n_s':>15}"
      f"{'n_t':>15}"
      f"{'FD price':>15}"
      f"{'abs error':>15}"
      )
print('-'*80)

for n_s, n_t in grid_test:
    fd_engine = ExplicitFiniteDifferenceEngine(
        s_max = 300,
        n_s = n_s,
        n_t = n_t
        )
    
    fd_price = fd_engine.price_loop(call, market)
    abs_error = abs(fd_price - bs_price)
    
    print(
        f"{n_s:15d}"
        f"{n_t:15d}"
        f"{fd_price:15.10f}"
        f"{abs_error:15.10f}"
        )















