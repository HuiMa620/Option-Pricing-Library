# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 18:34:54 2026

@author: ma6
"""

#examples/example_black_scholes.py
import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.validation import check_put_call_parity

market = MarketData(
    rate = 0.04, 
    dividend = 0.02, 
    volatility = 0.25
    )

call = EuropeanOption(
    spot = 100, 
    strike = 110, 
    tau = 0.1, 
    option_type = 'Call'
    )

put = EuropeanOption(
    spot = 100, 
    strike = 110, 
    tau = 0.1, 
    option_type = 'Put'
    )

engine = BlackScholesEngine()

call_price = engine.price(call, market)
put_price = engine.price(put, market)

print('European Call')
print(f'Price:{call_price:.6f}')
print(f'Delta:{engine.Delta(call, market):.6f}')
print(f'Gamma:{engine.Gamma(call, market):.6f}')
print(f'Vega:{engine.Vega(call, market):.6f}')
print(f'Theta:{engine.Theta(call, market):.6f}')

print()
print('European Put')
print(f'Price:{put_price:.6f}')
print(f'Delta:{engine.Delta(put, market):.6f}')
print(f'Gamma:{engine.Gamma(put, market):.6f}')
print(f'Vega:{engine.Vega(put, market):.6f}')
print(f'Theta:{engine.Theta(put, market):.6f}')

print()
print('Put-Call Parity Check')
left, right, error = check_put_call_parity(call_price, put_price, call, market)

print(f'Call - Put:                  {left:.6f}')
print(f'S*exp(-q tau)-K*exp(-r tau): {right:.6f}')
print(f'Error:                       {error:10f}')








