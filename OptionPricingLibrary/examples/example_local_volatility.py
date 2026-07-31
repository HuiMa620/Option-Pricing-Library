# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 19:15:17 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.black_scholes import BlackScholesEngine
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.local_volatility import (
    LocalVolatilityMonteCarloEngine,
    LocalVolatilitySurface
    )

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

local_vol_surface = LocalVolatilitySurface(
    base_vol = 0.20,
    skew_strength = 0.30,
    term_strength = 0.05,
    reference_spot = 100.0
    )

local_vol_const_surface = LocalVolatilitySurface(
    base_vol = 0.25,
    skew_strength = 0.0,
    term_strength = 0.0,
    reference_spot = 100.0
    )

lv_engine = LocalVolatilityMonteCarloEngine(
    n_paths = 2*10**5,
    n_steps = 252,
    seed = 1,
    antithetic = True
    )

bs_engine = BlackScholesEngine()

lv_price, lv_se = lv_engine.price_error(
    option = option, 
    market = market, 
    local_vol_surface = local_vol_surface
    )

bs_price = bs_engine.price(option, market)

lv_const_price = lv_engine.price(
    option = option,
    market = market,
    local_vol_surface = local_vol_const_surface
    )



print(f"Black Scholes price:                         {bs_price:.10f}")
print(f"Local Volatility Monte Carlo price:          {lv_price:.10f}")
print(f"Local Volatility Monte Carlo standard error: {lv_se:.10f}")
print(f"Constant Local Volatility Monte Carlo price: {lv_const_price:.10f}")
print(f"Local Volatility - Black Scholes difference: {lv_price - bs_price:.10f}")
print(f"Constant Local Vol - Black Scholes diff    : {lv_const_price - bs_price:.10f}")















