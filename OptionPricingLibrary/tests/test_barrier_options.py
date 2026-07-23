# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 21:14:32 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np
from pricing.products import EuropeanOption, BarrierOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.barrier_options import BarrierMonteCarloEngine

def make_market():
    return MarketData(
        rate = 0.04,
        dividend = 0.02,
        volatility = 0.25
        )

def test_terminal_payoff_call():
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 80.0,
        tau = 1.0,
        option_type = 'Call',
        barrier_type = 'Down',
        knock_type = 'Out'
        )
    
    barrier_engine = BarrierMonteCarloEngine()
    ST = np.array([80, 100, 120])
    payoff = barrier_engine._terminal_payoff(ST, barrier_option)
    expected_payoff = np.array([0.0, 0.0, 20.0])
    assert np.allclose(payoff, expected_payoff)
    

def test_terminal_payoff_put():
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 80.0,
        tau = 1.0,
        option_type = 'Put',
        barrier_type = 'Down',
        knock_type = 'Out'
        )
    
    barrier_engine = BarrierMonteCarloEngine()
    ST = np.array([80, 100, 120])
    payoff = barrier_engine._terminal_payoff(ST, barrier_option)
    expected_payoff = np.array([20, 0, 0])
    assert np.allclose(payoff, expected_payoff)
    

def test_check_knock_out_down_barrier():
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 80.0,
        tau = 1.0,
        option_type = 'Call',
        barrier_type = 'Down',
        knock_type = 'Out'
        )
    
    S_paths = np.array([
        [100, 95, 90, 85],
        [100, 90, 79, 85],
        [100, 80, 90, 100]
        ])
    
    barrier_engine = BarrierMonteCarloEngine()
    knocked_out = barrier_engine._check_knock_out(S_paths, barrier_option)
    expected = np.array([False, True, True])
    
    assert np.array_equal(knocked_out, expected)


def test_check_knock_out_up_barrier():
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 120.0,
        tau = 1.0,
        option_type = 'Call',
        barrier_type = 'Up',
        knock_type = 'Out'
        )
    
    S_paths = np.array([
        [100, 95, 90, 85],
        [100, 120, 79, 85],
        [100, 110, 130, 100]
        ])
    
    barrier_engine = BarrierMonteCarloEngine()
    knocked_out = barrier_engine._check_knock_out(S_paths, barrier_option)
    expected = np.array([False, True, True])
    
    assert np.array_equal(knocked_out, expected)
    

def test_simulated_paths_have_correct_shape():
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 120.0,
        tau = 1.0,
        option_type = 'Call',
        barrier_type = 'Up',
        knock_type = 'Out'
        )
    
    market = make_market()
    
    barrier_engine = BarrierMonteCarloEngine(
        n_paths = 1000,
        n_steps = 252,
        seed = 1
        )
    
    S_paths = barrier_engine._simulate_paths(barrier_option, market)
    
    assert S_paths.shape == (1000, barrier_engine.n_steps + 1)
    assert np.all(S_paths[:,0] == barrier_option.spot)
    

def test_invalid_n_paths_raises_error():
    try:
        barrier_engine = BarrierMonteCarloEngine(n_paths = 0)
        raise AssertionError("Expected ValueError.")
    except ValueError:
        pass
    

def test_invalid_barrier_type_raises_error():
    try:
        barrier_option = BarrierOption(
            spot = 100.0,
            strike = 100.0,
            barrier = 80,
            tau = 1,
            option_type = 'Call',
            barrier_type = 'Sideways',
            knock_type = 'Out'
            )
        raise AssertionError("Expected ValueError.")
    except ValueError:
        pass
    

def test_down_and_out_call_price_less_than_vanilla_call():
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 80.0,
        tau = 1.0,
        option_type = 'Call',
        barrier_type = 'Down',
        knock_type = 'Out'
        )
    
    vanilla_option = EuropeanOption(
        spot = 100.0,
        strike = 100.0,
        tau = 1.0,
        option_type = 'Call'
        )
    
    market = make_market()
    
    barrier_engine = BarrierMonteCarloEngine(
        n_paths = 10**5,
        n_steps = 252,
        seed = 1,
        antithetic = True
        )
    
    bs_engine = BlackScholesEngine()
    
    barrier_price = barrier_engine.price(option = barrier_option, market = market)
    vanilla_price = bs_engine.price(option = vanilla_option, market = market)
    
    assert barrier_price <= vanilla_price
    
   
    

def test_down_and_out_call_zero_if_barrier_above_or_equal_spot():
    barrier_engine = BarrierMonteCarloEngine()
    
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 100.0,
        tau = 1,
        option_type = 'Call',
        barrier_type = 'Down',
        knock_type = 'Out'
        )
    
    market = make_market()
    
    price = barrier_engine.price(option = barrier_option, market = market)
    
    assert price == 0.0


def test_up_and_out_call_zero_if_barrier_below_or_equal_spot():
    barrier_engine = BarrierMonteCarloEngine()
    
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 100.0,
        tau = 1,
        option_type = 'Call',
        barrier_type = 'Up',
        knock_type = 'Out'
        )
    
    market = make_market()
    
    price = barrier_engine.price(option = barrier_option, market = market)
    
    assert price == 0.0
    

def test_down_and_out_call_approaches_vanilla_when_barrier_very_low():
    bs_engine = BlackScholesEngine()
    barrier_engine = BarrierMonteCarloEngine(
        n_paths = 2*10**5,
        n_steps = 252,
        seed = 1,
        antithetic = True
        )
    
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 1.0,
        tau = 1.0,
        option_type = 'Call',
        barrier_type = 'Down',
        knock_type = 'Out'
        )
    
    vanilla_option = EuropeanOption(
        spot = 100.0,
        strike = 100.0,
        tau = 1.0,
        option_type = 'Call'
        )
    
    market = make_market()
    
    barrier_price, barrier_se = barrier_engine.price_error(
        option = barrier_option, 
        market = market
        )
    
    vanilla_price = bs_engine.price(
        option = vanilla_option, 
        market = market
        )
    
    assert abs(barrier_price - vanilla_price) <= max(5.0 * barrier_se, 0.1)
    
    
def test_barrier_price_error_returns_positive_standard_error():
    barrier_engine = BarrierMonteCarloEngine()
    
    barrier_option = BarrierOption(
        spot = 100.0,
        strike = 100.0,
        barrier = 1.0,
        tau = 1.0,
        option_type = 'Call',
        barrier_type = 'Down',
        knock_type = 'Out'
        )
    
    market = make_market()
    
    barrier_price, barrier_se = barrier_engine.price_error(
        option = barrier_option, 
        market = market
        )
    
    assert barrier_price >= 0.0
    assert barrier_se >= 0.0
    


if __name__ == '__main__':
    test_terminal_payoff_call()
    test_terminal_payoff_put()
    test_check_knock_out_down_barrier()
    test_check_knock_out_up_barrier()
    test_simulated_paths_have_correct_shape()
    test_invalid_n_paths_raises_error()
    test_invalid_barrier_type_raises_error()
    test_down_and_out_call_price_less_than_vanilla_call()
    test_down_and_out_call_zero_if_barrier_above_or_equal_spot()
    test_up_and_out_call_zero_if_barrier_below_or_equal_spot()
    test_down_and_out_call_approaches_vanilla_when_barrier_very_low()
    
    print("All barrier option tests passed.")

    



