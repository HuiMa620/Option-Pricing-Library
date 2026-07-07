# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 01:18:24 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.finite_difference import (
    AmericanPutCrankNicolsonFiniteDifferenceEngine,
    AmericanPutImplicitFiniteDifferenceEngine,
    )
from pricing.binomial_tree import BinomialTreeEngine

def test_anerican_put_crank_nicolson():
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

    nc_engine = AmericanPutCrankNicolsonFiniteDifferenceEngine()
    implicit_engine = AmericanPutImplicitFiniteDifferenceEngine()
    tree_engine = BinomialTreeEngine(
        exercise = 'American'
        )

    nc_price = nc_engine.price(put, market)
    implicit_price = implicit_engine.price(put, market)
    tree_price = tree_engine.price(put, market)
    intrinsic = max(put.strike - put.spot, 0)

    assert nc_price >= intrinsic
    assert abs(nc_price - implicit_price) < 0.05
    assert abs(nc_price - tree_price) < 0.05















