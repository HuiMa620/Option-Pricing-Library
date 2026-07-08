# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 00:30:46 2026

@author: ma6
"""


from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.binomial_tree import BinomialTreeEngine
from pricing.finite_difference import AmericanPutCrankNicolsonFiniteDifferenceEngine

def test_american_put_crank_nicolson_vs_binomial_tree():
    tree_engine = BinomialTreeEngine(
        exercise = 'American'
        )

    cn_engine = AmericanPutCrankNicolsonFiniteDifferenceEngine()

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

    tree_price = tree_engine.price(put, market)
    cn_price = cn_engine.price(put, market)

    assert abs(tree_price - cn_price) <= 0.05



def test_american_put_implicit_vs_binomial_tree():
    tree_engine = BinomialTreeEngine(
        exercise = 'American'
        )

    implicit_engine = AmericanPutCrankNicolsonFiniteDifferenceEngine()

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

    tree_price = tree_engine.price(put, market)
    implicit_price = implicit_engine.price(put, market)

    assert abs(tree_price - implicit_price) <= 0.05







