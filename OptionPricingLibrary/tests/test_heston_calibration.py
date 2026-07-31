# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 18:33:30 2026

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


def test_heston_calibration_fits_synthetic_prices():
    spot = 100.0
    rate = 0.04
    dividend = 0.02
    
    true_params = HestonParams(
        v0 = 0.25**2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    pricing_engine = HestonClosedFormEngine()
    
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
            
            market = MarketData(
                rate = rate,
                dividend = dividend,
                volatility = 0.25
                )
            
            market_price = pricing_engine.price(
                option = option,
                market = market,
                params = true_params
                )
            
            quotes.append({
                'tau': tau,
                'strike': strike,
                'option_type': 'Call',
                'market_price': market_price
                })
            
    calibrator = HestonCalibrator(
        pricing_engine = pricing_engine
        )
    
    initial_guess = np.array([
        0.2**2,
        1.0,
        0.2**2,
        0.3,
        -0.3
        ])
    
    calibrated_params, result = calibrator.calibrate(
        quotes = quotes,
        spot = spot,
        rate = rate,
        dividend = dividend,
        initial_guess = initial_guess
        )
    
    assert result.success
    
    for quote in quotes:
        option = EuropeanOption(
            spot = spot,
            strike = quote['strike'],
            tau = quote['tau'],
            option_type = quote['option_type']
            )
        
        market = MarketData(
            rate = rate,
            dividend = dividend,
            volatility = 0.25
            )
        
        calibrated_price = pricing_engine.price(
            option = option,
            market = market,
            params = calibrated_params
            )
        
        assert abs(calibrated_price - quote['market_price']) < 0.1
    
    initial_loss = calibrator._objective(
        x = initial_guess,
        quotes = quotes,
        spot = spot,
        rate = rate,
        dividend = dividend
        )
    
    calibrated_vector = np.array([
        calibrated_params.v0,
        calibrated_params.kappa,
        calibrated_params.theta,
        calibrated_params.xi,
        calibrated_params.rho
        ])
    
    calibrated_loss = calibrator._objective(
        x = calibrated_vector,
        quotes = quotes,
        spot = spot,
        rate = rate,
        dividend = dividend
        )
    
    assert calibrated_loss < initial_loss
        


def test_params_from_vector():
    calibrator = HestonCalibrator()
    
    x = np.array([
        0.04,
        2.0,
        0.05,
        0.3,
        -0.6
        ])
    
    params = calibrator._params_from_vector(x)
    
    assert isinstance(params, HestonParams)
    assert params.v0 == 0.04
    assert params.kappa == 2.0
    assert params.theta == 0.05
    assert params.xi == 0.3
    assert params.rho == -0.6


def test_objective_empty_quotes_raises_error():
    calibrator = HestonCalibrator()
    
    x = np.array([
        0.25**2,
        2.0,
        0.25**2,
        0.4,
        -0.7
        ])
    
    try:
        calibrator._objective(
            x = x,
            quotes = [],
            spot = 100.0,
            rate = 0.04,
            dividend = 0.02
            )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError for empty quotes.")



def test_calibration_runs_with_default_initial_guess_and_bounds():
    spot = 100.0
    rate = 0.04
    dividend = 0.02
    
    true_params = HestonParams(
        v0 = 0.25**2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    pricing_engine = HestonClosedFormEngine()
    market = MarketData(
        rate = rate,
        dividend = dividend,
        volatility = 0.25
        )
    
    quotes = []
    
    for strike in [90.0, 100.0, 110.0]:
        option = EuropeanOption(
            spot = spot,
            strike = strike,
            tau = 1.0,
            option_type = 'Call'
            )
        
        market_price = pricing_engine.price(
            option = option,
            market = market,
            params = true_params
            )
        
        quotes.append({
            'tau': 1.0,
            'strike': strike,
            'option_type': 'Call',
            'market_price': market_price
            })
        
    calibrator = HestonCalibrator(pricing_engine = pricing_engine)
        
    calibrated_params, result = calibrator.calibrate(
        quotes = quotes,
        spot = spot,
        rate = rate,
        dividend = dividend
        )
        
    assert isinstance(calibrated_params, HestonParams)
    assert np.isfinite(result.fun)





if __name__ == '__main__':
    test_heston_calibration_fits_synthetic_prices()
    test_params_from_vector()
    test_objective_empty_quotes_raises_error()
    test_calibration_runs_with_default_initial_guess_and_bounds()
    print("All Heston calibration tests passed.")








