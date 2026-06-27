# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 17:27:46 2026

@author: ma6
"""



from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.binomial_tree import BinomialTreeEngine
from pricing.black_scholes import BlackScholesEngine

def test_european_call():
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
    
    tree_engine = BinomialTreeEngine(
        n_steps = 10**3,
        exercise = 'European'
        )
    tree_price = tree_engine.price(call, market)
    
    assert abs(bs_price - tree_price) < 0.05




def test_european_put():
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
    bs_price = bs_engine.price(put, market)
    
    tree_engine = BinomialTreeEngine(
        n_steps = 10**3,
        exercise = 'European'
        )
    
    tree_price = tree_engine.price(put, market)
    assert abs(bs_price - tree_price) < 0.05
    
    
    
    
def test_american_put_greater_than_european_put():
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
    
    euro_put_engine = BinomialTreeEngine(
        n_steps = 10**3,
        exercise = 'European'
        )
    
    american_put_engine = BinomialTreeEngine(
        n_steps = 10**3,
        exercise = 'American'
        )
    
    euro_price = euro_put_engine.price(put, market)
    american_price = american_put_engine.price(put, market)
    
    assert american_price >= euro_price
    
    
    
    



