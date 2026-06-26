#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:14:13 2026

@author: huima
"""
#import os
#os.chdir('..')
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import ExplicitFiniteDifferenceEngine
from pricing.finite_difference import ImplicitFiniteDifferenceEngine


call = EuropeanOption(
    spot = 100,
    strike = 110,
    tau = 0.5,
    option_type = 'Call'
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
explicit_engine = ExplicitFiniteDifferenceEngine(
    s_max = 300,
    n_s = 200,
    n_t = 20000
    )

implicit_engine = ImplicitFiniteDifferenceEngine(
    s_max = 300,
    n_s = 200,
    n_t = 500
    )


for option in [call, put]:
    bs_price = bs_engine.price(option, market)
    explicit_price = explicit_engine.price(option, market)
    implicit_price = implicit_engine.price(option, market)
    explicit_diff = abs(bs_price - explicit_price)
    implicit_diff = abs(bs_price - implicit_price)
    
    print(option.option_type)
    print(f"BS price:                   {bs_price:10f}")
    print(f"Explicit FD price:          {explicit_price:.10f}")
    print(f"Implicit FD price:          {implicit_price:.10f}")
    print(f"Explicit FD price abs error:{explicit_diff:.10f}")
    print(f"Implicit FD price abs error:{implicit_diff:.10f}")
    print()
    







