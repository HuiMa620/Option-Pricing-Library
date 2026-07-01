# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 22:48:36 2026

@author: ma6
"""


from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.monte_carlo import MonteCarloEngine


def test_control_variate_mc_vs_plain_mc():
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

    mc_engine = MonteCarloEngine(antithetic = False)

    mc_plain_price, mc_plain_error = mc_engine.price_error(call, market)
    mc_cv_price, mc_cv_error = mc_engine.price_control_variate_error(call, market)

    assert mc_cv_error < mc_plain_error
    assert  abs(bs_price - mc_cv_price) < 5*mc_cv_error
    

    

