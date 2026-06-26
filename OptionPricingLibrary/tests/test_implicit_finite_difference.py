#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:27:29 2026

@author: huima
"""



from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.finite_difference import ImplicitFiniteDifferenceEngine


def test_implicit_fd_call_price_vs_bs_price():
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
    
    implicit_fd_engine = ImplicitFiniteDifferenceEngine(
        s_max = 300,
        n_s = 200,
        n_t = 500
        )
    implicit_fd_price = implicit_fd_engine.price(call, market)
    diff = abs(bs_price - implicit_fd_price)
    assert diff < 0.05



def test_implicit_fd_put_price_vs_bs_price():
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
    
    implicit_fd_engine = ImplicitFiniteDifferenceEngine(
        s_max = 300,
        n_s = 200,
        n_t = 500
        )
    implicit_fd_price = implicit_fd_engine.price(put, market)
    diff = abs(bs_price - implicit_fd_price)
    assert diff < 0.05
    
    

















