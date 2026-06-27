# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:16:41 2026

@author: ma6
"""

#import os
#os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.binomial_tree import BinomialTreeEngine
from pricing.finite_difference import AmericanPutImplicitFiniteDifferenceEngine

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
    volatility= 0.25
    )

bs_engine = BlackScholesEngine()

implicit_engine = AmericanPutImplicitFiniteDifferenceEngine(
    s_max = 300,
    n_s = 200,
    n_t = 500
    )

euro_tree_engine = BinomialTreeEngine(
    n_steps = 10**3,
    exercise = 'European'
    )

american_tree_engine = BinomialTreeEngine(
    n_steps = 10**3,
    exercise = 'American'
    )

for option in [call, put]:
    bs_price = bs_engine.price(option, market)
    euro_tree_price = euro_tree_engine.price(option, market)
    bs_euro_diff = abs(bs_price - euro_tree_price)
    print(option.option_type)
    print(f"BS price:                                   {bs_price:.10f}")
    print(f"European Tree Price:                        {euro_tree_price:.10f}")
    print(f"European price difference: BS vs Tree:      {bs_euro_diff:.10f}")
    print()
    



american_tree_price = american_tree_engine.price(option, market)
american_implicit_price = implicit_engine.price(option, market)
implicit_american_tree_diff = abs(american_implicit_price - american_tree_price)

print(put.option_type)
print(f"American implicit price:                    {american_implicit_price:.10f}")
print(f"American Tree Price:                        {american_tree_price:.10f}")
print(f"American price difference: Implicit vs Tree:{implicit_american_tree_diff:.10f}")


















