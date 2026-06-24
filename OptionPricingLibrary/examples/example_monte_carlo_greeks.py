# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 23:47:31 2026

@author: ma6
"""

#OptionPricingLibrary/example_monte_carlo_greeks.py
import os
os.chdir('..')


from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.monte_carlo import MonteCarloEngine
from pricing.numerical_greeks import (
    numerical_delta, 
    numerical_gamma, 
    numerical_theta, 
    numerical_vega
    )

if __name__ == '__main__':
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
    bs_delta = bs_engine.Delta(call, market)
    bs_gamma = bs_engine.Gamma(call, market)
    bs_theta = bs_engine.Theta(call, market)
    bs_vega = bs_engine.Vega(call, market)
    
    mc_engine = MonteCarloEngine(
        n_paths = 10**6,
        seed = 42,
        antithetic = True
        )
    
    mc_delta = numerical_delta(mc_engine, call, market, bump = 1e-2)
    mc_gamma = numerical_gamma(mc_engine, call, market, bump = 1e-1)
    mc_theta = numerical_theta(mc_engine, call, market, bump = 1e-4)
    mc_vega = numerical_vega(mc_engine, call, market, bump = 1e-3)
    
    print('Monte Carlo Numerical Greeks validation')
    print(f"BS delta:  {bs_delta:.10f}")
    print(f"MC delta:  {mc_delta:.10f}")
    print(f"Difference:{bs_delta - mc_delta:.10f}")
    print()
    
    print(f"BS gamma:  {bs_gamma:.10f}")
    print(f"MC gamma:  {mc_gamma:.10f}")
    print(f"Difference:{bs_gamma - mc_gamma:.10f}")
    print()
    
    print(f"BS theta:  {bs_theta:.10f}")
    print(f"MC theta:  {mc_theta:.10f}")
    print(f"Difference:{bs_theta - mc_theta:.10f}")
    print()
    
    print(f"BS vega:   {bs_vega:.10f}")
    print(f"MC vega:   {mc_vega:.10f}")
    print(f"Difference:{bs_vega - mc_vega:.10f}")
    print()
    
    
    

















