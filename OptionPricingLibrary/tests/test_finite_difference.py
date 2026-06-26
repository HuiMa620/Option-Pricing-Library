# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:03:29 2026

@author: ma6
"""



from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import ExplicitFiniteDifferenceEngine


def test_explicit_fd_call_against_black_scholes():
    call = EuropeanOption(
        spot = 100,
        strike =110,
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
    fd_engine = ExplicitFiniteDifferenceEngine()

    bs_call_price = bs_engine.price(call, market)
    fd_loop_call_price = fd_engine.price_loop(call, market)
    fd_call_price = fd_engine.price(call, market)

    bs_put_price = bs_engine.price(put, market)
    fd_loop_put_price = fd_engine.price_loop(put, market)
    fd_put_price = fd_engine.price(put, market)

    assert abs(bs_call_price - fd_loop_call_price) < 0.05
    assert abs(bs_put_price - fd_loop_put_price) < 0.05
    assert abs(bs_call_price - fd_call_price) < 0.05
    assert abs(bs_put_price - fd_put_price) < 0.05











