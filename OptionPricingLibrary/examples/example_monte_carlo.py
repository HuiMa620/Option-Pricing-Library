# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 12:49:40 2026

@author: ma6
"""

#OptionPricingLibrary/example_monte_carlo.py
#import os
#os.chdir('..')


from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.monte_carlo import MonteCarloEngine


if __name__ == '__main__':
    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25                
        )

    call = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 0.5,
        option_type ='Call'
        )

    put = EuropeanOption(
        spot = 100,
        strike = 110,
        tau = 0.5,
        option_type = 'Put'
        )


    bs_engine = BlackScholesEngine()
    mc_engine = MonteCarloEngine()

    bs_call_price = bs_engine.price(call, market)
    mc_call_price, mc_call_error = mc_engine.price_error(call, market)
    call_price_diff = bs_call_price - mc_call_price

    bs_put_price = bs_engine.price(put, market)
    mc_put_price, mc_put_error = mc_engine.price_error(put, market)
    put_price_diff = bs_put_price - mc_put_price

    print('European Call Option')
    print(f"Black Scholes call price:  {bs_call_price:.10f}")
    print(f"Monte Carlo call price:    {mc_call_price:.10f}")
    print(f"Standard Error of MC price:{mc_call_error:.10f}")
    print(f"Difference:                {call_price_diff:.10f}")
    print()
    
    
    print('European Put Option')
    print(f"Black Scholes put price:  {bs_put_price:.10f}")
    print(f"Monte Carlo put price:    {mc_put_price:.10f}")
    print(f"Standard Error of MC price:{mc_put_error:.10f}")
    print(f"Difference:                {put_price_diff:.10f}")
    print()
    
    
    call_z_score = abs(call_price_diff)/mc_call_error
    if call_z_score < 3:
        print('Monte Carlo call option price validation passed.')
    else:
        print('Monte Carlo call option price validation failed.')
        
    put_z_score = abs(put_price_diff)/mc_put_error
    if put_z_score < 3:
        print('Monte Carlo put option price validation passed.')
    else:
        print('Monte Carlo put option price validation failed.')











