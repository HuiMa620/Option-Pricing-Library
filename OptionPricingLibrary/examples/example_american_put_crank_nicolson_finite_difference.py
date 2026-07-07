# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 01:07:59 2026

@author: ma6
"""

import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.finite_difference import (
    AmericanPutImplicitFiniteDifferenceEngine,
    AmericanPutCrankNicolsonFiniteDifferenceEngine
    )
from pricing.binomial_tree import BinomialTreeEngine


if __name__ == '__main__':
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

    implicit_engine = AmericanPutImplicitFiniteDifferenceEngine()
    nc_engine = AmericanPutCrankNicolsonFiniteDifferenceEngine()
    tree_engine = BinomialTreeEngine(
        exercise = 'American'
        )

    implicit_price = implicit_engine.price(put, market)
    nc_price = nc_engine.price(put, market)
    tree_price = tree_engine.price(put, market)

    print(f"American put implicit FD price:   {implicit_price:.10f}")
    print(f"American put NC FD price:         {nc_price:.10f}")
    print(f"American put binomial tree price: {tree_price:.10f}")









