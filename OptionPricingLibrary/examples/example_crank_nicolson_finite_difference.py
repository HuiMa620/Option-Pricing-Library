# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 23:37:33 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import (
    ExplicitFiniteDifferenceEngine,
    ImplicitFiniteDifferenceEngine,
    CrankNicolsonFiniteDifferenceEngine
    )


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
    n_t = 2*10**4
    )

implicit_engine = ImplicitFiniteDifferenceEngine(
    s_max = 300,
    n_s = 200,
    n_t = 500
    )

cn_engine = CrankNicolsonFiniteDifferenceEngine(
    s_max = 300,
    n_s = 200,
    n_t = 500
    )

for option in [call, put]:
    bs_price = bs_engine.price(option, market)
    explicit_price = explicit_engine.price(option, market)
    implicit_price = implicit_engine.price(option, market)
    cn_price = cn_engine.price(option, market)
    cn_diff = abs(cn_price - bs_price)
    print(option.option_type)
    print(f"BS price:                         {bs_price:.10f}")
    print(f"Explicit FD price:                {explicit_price:.10f}")
    print(f"Implicit FD price:                {implicit_price:.10f}")
    print(f"Crank-Nicolson FD price:          {cn_price:.10f}")
    print(f"Crank-Nicolson FD price abs error:{cn_diff:.10f}")
    print()
    
 




