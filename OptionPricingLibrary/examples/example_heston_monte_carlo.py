# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 17:54:46 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.heston_monte_carlo import HestonMonteCarloEngine
from pricing.heston_params import HestonParams

option = EuropeanOption(
    spot = 100.0,
    strike = 100.0,
    tau = 1.0,
    option_type = 'Call'
    )

market = MarketData(
    rate = 0.04,
    dividend = 0.02,
    volatility = 0.25
    )

params = HestonParams(
    v0 = 0.25 **2,
    kappa = 2.0,
    theta = 0.25**2,
    xi = 0.4,
    rho = -0.7
    )

heston_engine = HestonMonteCarloEngine(
    n_paths = 10**5,
    n_steps = 252,
    seed = 1,
    antithetic = True
    )

heston_price, heston_se = heston_engine.price_error(
    option = option,
    market = market,
    params = params
    )

bs_engine = BlackScholesEngine()
bs_price = bs_engine.price(option = option, market = market)

print(f"Black-Scholes price:               {bs_price:.10f}")
print(f"Heston Monte Carlo price:          {heston_price:.10f}")
print(f"Heston Monte Carlo standard error: {heston_se:.10f}")
print(f"Heston - Black-Scholes difference: {heston_price - bs_price:.10f}")
print(f"Feller condition satisfied:        {params.satisfies_feller_condition()}")







