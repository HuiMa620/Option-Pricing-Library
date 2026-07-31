# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:41:53 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.heston_params import HestonParams
from pricing.heston_closed_form import HestonClosedFormEngine

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
    v0 = 0.25**2,
    kappa = 2.0,
    theta = 0.25**2,
    xi = 0.4,
    rho = -0.7
    )

heston_engine = HestonClosedFormEngine(
    integration_limit = 100.0
    )

heston_price = heston_engine.price(
    option = option,
    market = market,
    params = params
    )

bs_price = BlackScholesEngine().price(
    option = option,
    market = market
    )

print(f"Black-Scholes price:         {bs_price:.10f}")
print(f"Heston closed-form price:    {heston_price:.10f}")
print(f"Heston - Black-Scholes diff: {heston_price - bs_price:.10f}")
print(f"Feller condition satisfied: {params.satisfies_feller_condition()}")









