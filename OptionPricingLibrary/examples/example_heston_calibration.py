# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:13:44 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.heston_params import HestonParams
from pricing.heston_calibration import HestonCalibrator
from pricing.heston_closed_form import HestonClosedFormEngine

spot = 100.0
rate = 0.04
dividend = 0.02

market = MarketData(
    rate = rate,
    dividend = dividend,
    volatility = 0.25
    )

true_params = HestonParams(
    v0 = 0.25**2,
    kappa = 2.0,
    theta = 0.25**2,
    xi = 0.4,
    rho = -0.7
    )

pricing_engine = HestonClosedFormEngine(
    integration_limit = 100.0
    )

strikes = [80.0, 90.0, 100.0, 110.0, 120.0]
maturities = [0.5, 1.0, 2.0]

quotes = []

for tau in maturities:
    for strike in strikes:
        option = EuropeanOption(
            spot = spot,
            strike = strike,
            tau = tau,
            option_type = 'Call'
            )
        
        synthetic_market_price = pricing_engine.price(
            option = option,
            market = market,
            params = true_params
            )
        
        quotes.append({
            'tau': tau,
            'strike': strike,
            'option_type': 'Call',
            'market_price': synthetic_market_price
            })
        

initial_guess = np.array([
    0.20**2, #v0
    1.0, #kappa
    0.20**2, #theta
    0.3, #xi
    -0.3 #rho
    ])

initial_params = HestonParams(
    v0 = initial_guess[0],
    kappa = initial_guess[1],
    theta = initial_guess[2],
    xi = initial_guess[3],
    rho = initial_guess[4]
    )

calibrator = HestonCalibrator(
    pricing_engine = pricing_engine
    )

calibrated_params, result = calibrator.calibrate(
    quotes = quotes,
    spot = spot,
    rate = rate,
    dividend = dividend,
    initial_guess = initial_guess
    )

def compute_rmse(params):
    squared_errors = []
    
    for quote in quotes:
        option = EuropeanOption(
            spot = spot,
            strike = quote['strike'],
            tau = quote['tau'],
            option_type = quote['option_type']
            )
        
        model_price = pricing_engine.price(
            option = option,
            market = market,
            params = params
            )
        
        error = model_price - quote['market_price']
        squared_errors.append(error**2)
        
    return np.sqrt(np.mean(squared_errors))

initial_rmse = compute_rmse(initial_params)
calibrated_rmse = compute_rmse(calibrated_params)

print()
print('Heston calibration example')
print('-' * 60)

print('Optimization success:', result.success)
print('Optimization message:', result.message)
print('Final objective value:', result.fun)

print()
print('True parameters:')
print(true_params)

print()
print('Initial parameters:')
print(initial_params)

print()
print('Calibrated parameters:')
print(calibrated_params)

print()
print(f"Initial RMSE:    {initial_rmse:.10f}")
print(f"Calibrated RMSE: {calibrated_rmse:.10f}")

print()
print('Calibrated volatility interpretation:')
print(f"sqrt(v0): {np.sqrt(calibrated_params.v0):.10f}")
print(f"sqrt(theta): {np.sqrt(calibrated_params.theta):.10f}")

print()
print("Quote comparison:")
print(
      f"{'tau':>15}"
      f"{'strike':>15}"
      f"{'market_price':>15}"
      f"{'calibrated_price':>20}"
      f"{'error':>15}"
      )
print('-' * 80)

for quote in quotes:
    option = EuropeanOption(
        spot = spot,
        strike = quote['strike'],
        tau = quote['tau'],
        option_type = quote['option_type']
        )
    
    calibrated_price = pricing_engine.price(
        option = option,
        market = market,
        params = calibrated_params
        )
    
    error = calibrated_price - quote['market_price']
    
    print(
        f"{quote['tau']:>15.2f}"
        f"{quote['strike']:>15.2f}"
        f"{quote['market_price']:>15.10f}"
        f"{calibrated_price:>20.10f}"
        f"{error:>15.10f}"
        )







