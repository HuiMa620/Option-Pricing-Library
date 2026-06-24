# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 21:43:26 2026

@author: ma6
"""

#OptionPricingLibrary/example_numerical_greeks
import os
os.chdir('..')

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.numerical_greeks import numerical_delta, numerical_gamma, numerical_theta, numerical_vega



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

print('Numerical Greeks validation')
print()

print('European Call')
print(f'Analytical delta:{engine.Delta(call, market):.10f}')
print(f'Numerical delta: {numerical_delta(engine, call, market):.10f}')
print(f"Delta error:     {engine.Delta(call, market) - numerical_delta(engine, call, market):.10f}")
print()

print(f'Analytical gamma:{engine.Gamma(call, market):.10f}')
print(f'Numerical gamma: {numerical_gamma(engine, call, market):.10f}')
print(f"Gamma error:     {engine.Gamma(call, market) - numerical_gamma(engine, call, market):.10f}")
print()

print(f'Analytical theta:{engine.Theta(call, market):.10f}')
print(f'Numerical theta: {numerical_theta(engine, call, market):.10f}')
print(f"Theta error:     {engine.Theta(call, market) - numerical_theta(engine, call, market):.10f}")
print()

print(f'Analytical vega:{engine.Vega(call, market):.10f}')
print(f'Numerical vega: {numerical_vega(engine, call, market):.10f}')
print(f"Vega error:     {engine.Vega(call, market) - numerical_vega(engine, call, market):.10f}")
print()



print('European Put')
print(f'Analytical delta:{engine.Delta(put, market):.10f}')
print(f'Numerical delta: {numerical_delta(engine, put, market):.10f}')
print(f"Delta error:     {engine.Delta(put, market) - numerical_delta(engine, put, market):.10f}")
print()

print(f'Analytical gamma:{engine.Gamma(put, market):.10f}')
print(f'Numerical gamma: {numerical_gamma(engine, put, market):.10f}')
print(f"Gamma error:     {engine.Gamma(put, market) - numerical_gamma(engine, put, market):.10f}")
print()

print(f'Analytical theta:{engine.Theta(put, market):.10f}')
print(f'Numerical theta: {numerical_theta(engine, put, market):.10f}')
print(f"Theta error:     {engine.Theta(put, market) - numerical_theta(engine, put, market):.10f}")
print()

print(f'Analytical vega:{engine.Vega(put, market):.10f}')
print(f'Numerical vega: {numerical_vega(engine, put, market):.10f}')
print(f"Vega error:     {engine.Vega(put, market) - numerical_vega(engine, put, market):.10f}")
print()









