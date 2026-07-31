# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:45:00 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.local_volatility import (
    LocalVolatilitySurface,
    LocalVolatilityMonteCarloEngine
    )

def make_option():
    return EuropeanOption(
        spot = 100.0,
        strike = 100.0,
        tau = 1.0,
        option_type = 'Call'
        )

def make_market():
    return MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )

def test_get_vol_constant_surface():
    local_vol_surface = LocalVolatilitySurface(
        base_vol = 0.25,
        skew_strength = 0.0,
        term_strength = 0.0,
        reference_spot = 100.0
        )
    
    t = 0.5
    spot = np.array([80.0, 100.0, 120.0])
    
    sigma = local_vol_surface.get_vol(
        t = t,
        spot = spot
        )
    
    expected_sigma = np.array([0.25, 0.25, 0.25])
    
    assert np.allclose(sigma, expected_sigma)


def test_get_vol_skew_surface_higher_when_spot_lower():
    local_vol_surface = LocalVolatilitySurface(
        base_vol = 0.20,
        skew_strength = 0.30,
        term_strength = 0.05,
        reference_spot = 100.0
        )
    
    t = 0.0
    
    sigma_low_spot = local_vol_surface.get_vol(
        t = t,
        spot = 80.0
        )
    
    sigma_atm_spot = local_vol_surface.get_vol(
        t = t,
        spot = 100.0
        )
    
    sigma_high_spot = local_vol_surface.get_vol(
        t = t,
        spot = 120.0
        )
    
    assert sigma_low_spot > sigma_atm_spot
    assert np.allclose(sigma_atm_spot, sigma_high_spot)
    

def test_simulated_paths_have_correct_shape():
    option = make_option()
    market = make_market()
    
    local_vol_surface = LocalVolatilitySurface(
        base_vol = 0.25,
        skew_strength = 0.0,
        term_strength = 0.0,
        reference_spot = 100.0
        )
    
    lv_engine = LocalVolatilityMonteCarloEngine(
        n_paths = 10**3,
        n_steps = 252,
        seed = 1,
        antithetic = True
        )
    
    S_paths = lv_engine._simulate_paths(
        option = option,
        market = market,
        local_vol_surface = local_vol_surface
        )
    
    assert S_paths.shape == (10**3, 253)
    assert np.allclose(S_paths[:,0], option.spot)
    assert np.all(S_paths > 0.0)


def test_local_vol_mc_constant_vol_matches_bs():
    option = make_option()
    market = make_market()
    
    const_vol_surface = LocalVolatilitySurface(
        base_vol = 0.25,
        skew_strength = 0.0,
        term_strength = 0.0,
        reference_spot = 100.0
        )
    
    lv_engine = LocalVolatilityMonteCarloEngine(
        n_paths=10**5,
        n_steps=252,
        seed=1,
        antithetic=True
        )
    bs_engine = BlackScholesEngine()
    
    lv_price, lv_se = lv_engine.price_error(
        option = option, 
        market = market, 
        local_vol_surface = const_vol_surface
        )
    
    bs_price = bs_engine.price(option = option, market = market)
    
    assert abs(lv_price - bs_price) <= max(5.0 * lv_se, 0.1)



def test_price_error_returns_positive_price_and_se():
    option = make_option()
    market = make_market()
    
    local_vol_surface = LocalVolatilitySurface(
        base_vol = 0.25,
        skew_strength = 0.30,
        term_strength = 0.05,
        reference_spot = 100.0
        )
    
    lv_engine = LocalVolatilityMonteCarloEngine(
        n_paths = 10**5,
        n_steps = 252,
        seed = 1,
        antithetic = True
        )
    
    lv_price, lv_se = lv_engine.price_error(
        option = option, 
        market = market, 
        local_vol_surface = local_vol_surface
        )
    
    assert lv_price >= 0.0
    assert lv_se > 0.0
    assert np.isfinite(lv_price)
    assert np.isfinite(lv_se)
    

def test_invalid_engine_inputs_raise_error():
    try:
        lv_engine = LocalVolatilityMonteCarloEngine(
            n_paths = 0,
            n_steps = 252
            )
        raise AssertionError("Expected ValueError for n_paths = 0.")
    
    except ValueError:
        pass
    
    try:
        lv_engine = LocalVolatilityMonteCarloEngine(
            n_paths = 10**6,
            n_steps = 0
            )
        raise AssertionError("Expected ValueError for n_steps = 0.")
        
    except ValueError:
        pass
    
    try:
        lv_engine = LocalVolatilityMonteCarloEngine(
            n_paths = 1000.5,
            n_steps = 252
            )
        raise AssertionError("Expected ValueError for non-integer n_paths.")
    
    except ValueError:
        pass
    
    
def test_invalid_surface_inputs_raise_error():
    try:
        local_vol_surface = LocalVolatilitySurface(
            base_vol = 0.0,
            skew_strength = 0.30,
            term_strength = 0.05,
            reference_spot = 100.0
            )
        raise AssertionError("Expected ValueError for base_vol= 0.")
    except ValueError:
        pass
    
    try:
        local_vol_surface = LocalVolatilitySurface(
            base_vol = 0.25,
            skew_strength = -0.3,
            term_strength = 0.05,
            reference_spot = 100.0
            )
        raise AssertionError("Expected ValueError for negative skew_strength.")
    except ValueError:
        pass
    
    try:
        local_vol_surface = LocalVolatilitySurface(
            base_vol = 0.20,
            skew_strength = 0.30,
            term_strength = -0.05,
            reference_spot = 100.0
            )
        raise AssertionError("Expected ValueError for negative term_strength.")
    except ValueError:
        pass
    
    try:
        local_vol_surface = LocalVolatilitySurface(
            base_vol = 0.20,
            skew_strength = 0.30,
            term_strength = 0.05,
            reference_spot = 0.0
            )
        raise AssertionError("Expected ValueError for reference_spot = 0.")
    except ValueError:
        pass


def test_invalid_local_vol_surface_type_raises_erro():
    option = make_option()
    market = make_market()
    lv_engine = LocalVolatilityMonteCarloEngine(
        n_paths = 10**3,
        n_steps = 10,
        seed = 1
        )
    try:
        lv_engine.price_error(
            option = option,
            market = market,
            local_vol_surface = None
            )
        raise AssertionError("Expected TypeError for invalid local_vol_surface.")
    except TypeError:
        pass



if __name__ == "__main__":
    test_get_vol_constant_surface()
    test_get_vol_skew_surface_higher_when_spot_lower()
    test_simulated_paths_have_correct_shape()
    test_local_vol_mc_constant_vol_matches_bs()
    test_price_error_returns_positive_price_and_se()
    test_invalid_engine_inputs_raise_error()
    test_invalid_surface_inputs_raise_error()
    test_invalid_local_vol_surface_type_raises_erro()
    
    print("All local volatility tests passed.")
    
    
    
    
    
    












