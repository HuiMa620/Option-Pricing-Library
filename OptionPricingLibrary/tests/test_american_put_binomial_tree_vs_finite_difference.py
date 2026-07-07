# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 00:36:24 2026

@author: ma6
"""

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.finite_difference import AmericanPutImplicitFiniteDifferenceEngine
from pricing.binomial_tree import BinomialTreeEngine

def test_american_put_fd_vs_binomial_tree():
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

    fd_engine = AmericanPutImplicitFiniteDifferenceEngine()
    tree_engine = BinomialTreeEngine(
        n_steps = 5000,
        exercise = 'American'
        )

    fd_price = fd_engine.price(put, market)
    tree_price = tree_engine.price(put, market)

    assert abs(fd_price - tree_price) < 0.05





