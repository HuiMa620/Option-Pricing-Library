# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:00:19 2026

@author: ma6
"""
import os
os.chdir('..')

import numpy as np
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.heston_closed_form import HestonClosedFormEngine
from pricing.heston_params import HestonParams
from pricing.black_scholes import BlackScholesEngine
from pricing.heston_monte_carlo import HestonMonteCarloEngine


def test_closed_form_xi_zero_matches_black_scholes():
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
        v0 = sigma**2,
        kappa = 2.0,
        theta = sigma**2,
        xi = 0.0,
        rho = -0.7
        )
    
    heston_price = HestonClosedFormEngine().price(
        option = option,
        market = market,
        params = params
        )
    
    bs_price = BlackScholesEngine().price(
        option = option,
        market = market
        )
    
    assert abs(heston_price - bs_price) < 1e-10
    

def test_heston_closed_form_put_call_parity():
    S0 = 100.0
    K = 100.0
    T = 1.0
    r = 0.04
    y = 0.02
    
    call_option = EuropeanOption(
        spot = S0,
        strike = K,
        tau = T,
        option_type = 'Call'
        )
    
    put_option = EuropeanOption(
        spot = S0,
        strike = K,
        tau = T,
        option_type = 'Put'
        )
    
    market = MarketData(
        rate = r,
        dividend = y,
        volatility = 0.25
        )
    
    params = HestonParams(
        v0 = 0.25**2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    heston_engine = HestonClosedFormEngine()
    
    call_price = heston_engine.price(
        option = call_option,
        market = market,
        params = params
        )
    
    put_price = heston_engine.price(
        option = put_option,
        market = market,
        params = params
        )
    
    lhs = call_price - put_price
    rhs = S0 * np.exp(-y*T) - K*np.exp(-r*T)
    
    assert abs(lhs - rhs) < 1e-8
    
    
def test_heston_closed_form_price_is_positive_and_finite():
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
        v0 = 0.25**2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    price = HestonClosedFormEngine().price(
        option = option,
        market = market,
        params = params
        )
    
    assert price > 0.0
    assert np.isfinite(price)
    

def test_heston_closed_form_matches_monte_carlo_sanity_check():
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
        v0 = 0.25**2,
        kappa = 2.0,
        theta = 0.25**2,
        xi = 0.4,
        rho = -0.7
        )
    
    closed_form_engine = HestonClosedFormEngine(
        integration_limit = 100.0
        )
    
    mc_engine = HestonMonteCarloEngine(
        n_paths = 2*10**5,
        n_steps = 252,
        seed = 1,
        antithetic = True
        )
    
    cf_price = closed_form_engine.price(
        option = option,
        market = market,
        params = params
        )
    
    mc_price, mc_se = mc_engine.price_error(
        option = option,
        market = market,
        params = params
        )
    
    assert abs(cf_price - mc_price) <= max(5.0*mc_se, 0.3)


def test_characteristic_function_xi_zero_v0_not_equal_theta_is_finite():
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
        v0 = 0.3**2,
        kappa = 2.0,
        theta = 0.2**2,
        xi = 0.0,
        rho = -0.7
        )
    
    heston_engine = HestonClosedFormEngine()
    
    phi = heston_engine._characteristic_function(
        u = 1.0,
        option = option,
        market = market,
        params = params
        )
    
    assert np.isfinite(np.real(phi))
    assert np.isfinite(np.imag(phi))




    
if __name__ == '__main__':
    test_closed_form_xi_zero_matches_black_scholes()
    test_heston_closed_form_put_call_parity()
    test_heston_closed_form_price_is_positive_and_finite()
    test_heston_closed_form_matches_monte_carlo_sanity_check()
    test_characteristic_function_xi_zero_v0_not_equal_theta_is_finite()
    
    print("All Heston closed-form tests passed.")
    
    
    
    
    
    