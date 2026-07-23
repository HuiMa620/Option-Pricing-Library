# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 00:36:24 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.barrier_options import BarrierMonteCarloEngine
from pricing.products import EuropeanOption, BarrierOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine

barrier_option = BarrierOption(
    spot = 100.0,
    strike = 100.0,
    barrier = 80.0,
    tau = 1.0,
    option_type = 'Call',
    barrier_type = 'Down',
    knock_type = 'Out'
    )

market = MarketData(
    rate = 0.04,
    dividend = 0.02,
    volatility = 0.25
    )

barrier_engine = BarrierMonteCarloEngine(
    n_paths = 10**6,
    n_steps = 252,
    seed = 1,
    antithetic = True
    )

barrier_price, barrier_se = barrier_engine.price_error(
    option = barrier_option,
    market = market
    )

vanilla_option = EuropeanOption(
    spot = 100.0,
    strike = 100.0,
    tau = 1.0,
    option_type = 'Call'
    )

bs_engine = BlackScholesEngine()

vanilla_price = bs_engine.price(option = vanilla_option, market = market)

label_width = 45
value_width = 15

print(f"{'Vanilla call price':<{label_width}}: {vanilla_price:>{value_width}.10f}")
print(f"{'Down-and-out call MC price':<{label_width}}: {barrier_price:>{value_width}.10f}")
print(f"{'Monte Carlo standard error':<{label_width}}: {barrier_se:>{value_width}.10f}")
print(f"{'Barrier price <= vanilla price':<{label_width}}: {barrier_price <= vanilla_price}")









