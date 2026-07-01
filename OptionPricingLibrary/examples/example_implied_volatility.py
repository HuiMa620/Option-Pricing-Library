#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:08:59 2026

@author: huima
"""
import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.implied_volatility import ImpliedVolatilitySolver

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
    volatility = 0.25
    )

bs_engine = BlackScholesEngine()
bs_call_price = bs_engine.price(call, market)
bs_put_price = bs_engine.price(put, market)

implied_vol_engine = ImpliedVolatilitySolver()

bisection_call = implied_vol_engine.bisection_solve(call, market, bs_call_price)
bisection_put = implied_vol_engine.bisection_solve(put, market, bs_put_price)

newton_call = implied_vol_engine.newton_solve(call, market, bs_call_price)
newton_put = implied_vol_engine.newton_solve(put, market, bs_put_price)

bad_initial_guess = 100
hybrid_call = implied_vol_engine.solve(call, market, bs_call_price, bad_initial_guess)
hybrid_put = implied_vol_engine.solve(put, market, bs_put_price, bad_initial_guess)

print("The true volatility is 0.25.")
print()
print("Bisection solver")
print(f"Implied volatility by bisection method for call:{bisection_call:.10f}")
print(f"Implied volatility by bisection method for put:  {bisection_put:.10f}")
print()
print("Newton method")
print(f"Implied volatility by Newton method for call:   {newton_call:.10f}")
print(f"Implied volatility by Newton method for put:    {newton_put:.10f}")
print()
print("Hybrid method")
print(f"Implied volatility by hybrid method for call:   {hybrid_call:.10f}")
print(f"Implied volatility by hybrid method for put:    {hybrid_put:.10f}")

















