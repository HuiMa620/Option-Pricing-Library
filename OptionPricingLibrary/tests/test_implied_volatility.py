# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 22:53:11 2026

@author: ma6
"""


from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.implied_volatility import ImpliedVolatilitySolver
from pricing.black_scholes import BlackScholesEngine

def test_implied_volatility():
    true_vol = 0.25

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
        volatility = true_vol
        )

    bs_engine = BlackScholesEngine()
    call_market_price = bs_engine.price(call, market)
    put_market_price = bs_engine.price(put, market)

    implied_vol_engine = ImpliedVolatilitySolver()

    bisection_call = implied_vol_engine.bisection_solve(call, market, call_market_price)
    bisection_put = implied_vol_engine.bisection_solve(put, market, put_market_price)
    hybrid_call = implied_vol_engine.solve(call, market, call_market_price)
    hybrid_put = implied_vol_engine.solve(put, market, put_market_price)

    assert abs(bisection_call - true_vol) < 1e-6
    assert abs(bisection_put - true_vol) < 1e-6
    assert abs(hybrid_call - true_vol) < 1e-6
    assert abs(hybrid_put - true_vol) < 1e-6



