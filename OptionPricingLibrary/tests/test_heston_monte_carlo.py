# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 18:57:02 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.heston_monte_carlo import HestonMonteCarloEngine
from pricing.heston_params import HestonParams
from pricing.black_scholes import BlackScholesEngine


def test_invalid_heston_params_raises_error():
    
    try:
        params = HestonParams(
            v0 = -0.01,
            kappa = 2.0,
            theta = 0.25**2,
            xi = 0.4,
            rho = -0.7
            )
        raise AssertionError("Expected value error for v0 < 0.")
    except ValueError:
        pass
    
    try:
        params = HestonParams(
            v0 = 0.25**2,
            kappa = -2.0,
            theta = 0.25**2,
            xi = 0.4,
            rho = -0.7
            )
        raise AssertionError("Expected value error for kappa <= 0.")
    except ValueError:
        pass
    
    try:
        params = HestonParams(
            v0 = 0.25 **2,
            kappa = 2.0,
            theta = -0.25**2,
            xi = 0.4,
            rho = -0.7
            )
        raise AssertionError("Expected value error for theta <= 0.")
    except ValueError:
        pass
    
    try:
        params = HestonParams(
            v0 = 0.25 **2,
            kappa = 2.0,
            theta = 0.25**2,
            xi = -0.4,
            rho = -0.7
            )
        raise AssertionError("Expected value error for xi < 0.")
    except ValueError:
        pass
    
    try:
        params = HestonParams(
            v0 = 0.25 **2,
            kappa = 2.0,
            theta = 0.25**2,
            xi = 0.4,
            rho = -1.7
            )
        raise AssertionError("Expected value for rho outside of [-1, 1].")
    except ValueError:
        pass


def test_feller_condition():
    params = HestonParams(
        v0 = 0.25 **2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    assert params.satisfies_feller_condition()


def test_correlated_normal_shape():
    params = HestonParams(
        v0 = 0.25 **2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    heston_engine = HestonMonteCarloEngine(
        n_paths = 1000,
        n_steps = 252,
        seed = 1
        )
    
    Z_s, Z_v = heston_engine._correlated_normal_random_number_generator(params)
    
    assert Z_s.shape == (1000, 252)
    assert Z_v.shape == (1000, 252)
    
    
def test_correlated_normal_have_target_correlation():
    rho = -0.7
    params = HestonParams(
        v0 = 0.25 **2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = rho
        )
    
    heston_engine = HestonMonteCarloEngine(
        n_paths = 10**5,
        n_steps = 252,
        seed = 1
        )
    
    Z_s, Z_v = heston_engine._correlated_normal_random_number_generator(params)
    
    numerical_rho = np.corrcoef(Z_s.flatten(), Z_v.flatten())[0, 1]
    
    assert np.all(abs(numerical_rho - rho) < 0.03)
    

def test_heston_simulated_paths_shape_and_positivity():
    option = EuropeanOption(
        spot = 100.0,
        strike = 100.0,
        tau = 1.0,
        option_type = 'Call'
        )
    
    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )
    
    params = HestonParams(
        v0 = 0.25 **2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    heston_engine = HestonMonteCarloEngine(
        n_paths = 10**4,
        n_steps = 252,
        seed = 1
        )
    
    S_paths, v_paths = heston_engine._simulate_paths(
        option = option,
        market = market,
        params = params
        )
    
    assert S_paths.shape == (10**4, 253)
    assert v_paths.shape == (10**4, 253)
    assert np.all(S_paths > 0)
    assert np.all(v_paths >= 0)


def test_heston_xi_zero_matches_black_scholes():
    
    sigma = 0.25
    
    option = EuropeanOption(
        spot = 100.0,
        strike = 100.0,
        tau = 1.0,
        option_type = 'Call'
        )
    
    market = MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = sigma
        )
    
    params = HestonParams(
        v0 = sigma **2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.0,
        rho = -0.7
        )
    
    heston_engine = HestonMonteCarloEngine(
        n_paths = 10**5,
        n_steps = 252,
        seed = 1
        )
    
    heston_price, heston_se = heston_engine.price_error(
        option = option,
        market = market,
        params = params
        )
    
    bs_engine = BlackScholesEngine()
    bs_price = bs_engine.price(option = option, market = market)
    
    assert abs(heston_price - bs_price) <= max(5.0*heston_se, 0.1)
    


if __name__ == '__main__':
    test_invalid_heston_params_raises_error()
    test_feller_condition()
    test_correlated_normal_shape()
    test_correlated_normal_have_target_correlation()
    test_heston_simulated_paths_shape_and_positivity()
    test_heston_xi_zero_matches_black_scholes()
    
    print("All Heston Monte Carlo tests passed.")
    
    
    
    
    
        
