# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 12:56:20 2026

@author: ma6
"""

#import os
#os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import CrankNicolsonFiniteDifferenceEngine

test_settings = [
    (100, 100),
    (100, 500),
    (200, 500),
    (200, 1000),
    (400, 1000),
    (600, 2000)
]

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

print(f'Benchmark price: {bs_price:.10f}')
print()
print(
      f"{'n_s':>15}"
      f"{'n_t':>15}"
      f"{'CN price':>15}"
      f"{'abs error':>15}"
      )
print('-'*68)


for n_s, n_t in test_settings:
    cn_engine = CrankNicolsonFiniteDifferenceEngine(
        s_max = 300,
        n_s = n_s,
        n_t = n_t
        )
    
    cn_price = cn_engine.price(call, market)
    abs_error = abs(bs_price - cn_price)
    print(
        f"{n_s:15d}"
        f"{n_t:15d}"
        f"{cn_price:15.10f}"
        f"{abs_error:15.10f}"
        )
    
    
    
    


















