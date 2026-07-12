# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:28:58 2026

@author: ma6
"""

import os
os.chdir('..')

import numpy as np

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.black_scholes import BlackScholesEngine
from pricing.volatility_surface import VolatilitySurface



def synthetic_flat_vol_quotes(
        spot = 100.0,
        rate = 0.04,
        dividend = 0.02,
        true_vol = 0.25
        ):
    maturities = np.linspace(0.25, 2.0, 5)
    strikes = np.linspace(80, 120, 5)
    
    bs_engine = BlackScholesEngine()
    quotes = []
    
    for tau in maturities:
        for strike in strikes:
            
            if strike < spot:
                option_type = 'Put'
            else:
                option_type = 'Call'
            
            option = EuropeanOption(
                spot = spot,
                strike = strike,
                tau = float(tau),
                option_type = option_type
                )
            
            market = MarketData(
                rate = rate,
                dividend = dividend,
                volatility = true_vol
                )
            
            market_price = bs_engine.price(option, market)
            
            quotes.append({
                'tau': float(tau),
                'strike': float(strike),
                'option_type': option_type,
                'market_price': float(market_price)
                })
            
    return quotes, maturities, strikes, true_vol




def test_from_option_quotes_get_vol_surface():
    spot = 100.0
    rate = 0.04
    dividend = 0.02
    
    quotes, maturities, strikes, true_vol = synthetic_flat_vol_quotes(
        spot = spot,
        rate = rate,
        dividend = dividend,
        true_vol = 0.25
        )
    
    surface = VolatilitySurface.from_option_quotes(
        quotes = quotes,
        spot = spot,
        rate = rate,
        dividend = dividend,
        initial_vol_guess = 0.2
        )
    
    assert np.allclose(surface.maturities, maturities)
    assert np.allclose(surface.strikes, strikes)
    assert surface.vol_matrix.shape == (len(maturities), len(strikes))
    assert np.allclose(surface.vol_matrix, true_vol, atol = 1e-6)




def test_get_vol_at_grid_points():
    maturities = [0.5, 1.0]
    strikes = [90, 100, 110]
    
    vol_matrix = [
        [0.28, 0.25, 0.24],
        [0.27, 0.255, 0.245]
        ]
    
    surface = VolatilitySurface(
        maturities = maturities,
        strikes = strikes,
        vol_matrix = vol_matrix
        )
    
    vol = surface.get_vol(
        tau= 0.5,
        strike = 110
        )
    
    assert abs(vol - 0.24) < 1e-12
    
    
    

def test_vol_interpolation():
    maturities = [0.5, 1.0]
    strikes = [100, 120]
    
    vol_matrix = [
        [0.2, 0.3],
        [0.3, 0.4]
        ]
    
    surface = VolatilitySurface(
        maturities = maturities,
        strikes = strikes,
        vol_matrix = vol_matrix
        )
    
    vol = surface.get_vol(
        tau = 0.75,
        strike = 110
        )
    
    assert abs(vol - 0.3) < 1e-12
    



def test_from_option_quotes_missing_quote_raises_error():
    spot = 100.0
    rate = 0.04
    dividend = 0.02
    
    quotes, _, _, _ = synthetic_flat_vol_quotes(
        spot = spot,
        rate = rate,
        dividend = dividend,
        true_vol = 0.25
        )
    
    quotes = quotes[:-1]
    
    try:
        VolatilitySurface.from_option_quotes(
            quotes = quotes,
            spot = spot,
            rate = rate,
            dividend = dividend,
            initial_vol_guess = 0.2
            )
    except ValueError:
        print('Passed: missing quote raises ValueError')
    else:
        raise AssertionError('Expected ValueError for missing quote, but no error was raised.')
        



def test_duplicate_quote_raises_error():
    spot = 100.0
    rate = 0.04
    dividend = 0.02
    
    quotes, _, _, _ = synthetic_flat_vol_quotes(
        spot = spot,
        rate = rate,
        dividend = dividend,
        true_vol = 0.25
        )
    
    quotes.append(quotes[0].copy())
    
    try:
        VolatilitySurface.from_option_quotes(
            quotes = quotes,
            spot = spot,
            rate = rate,
            dividend = dividend,
            initial_vol_guess = 0.2
            )
    except ValueError:
        print('Passed: duplicate quote raises ValueError.')
    else:
        raise AssertionError('Expected ValueError for duplicate quote, but no error was raised.')
        
        
        
        
def test_invalid_surface_shape_raises_error():
    maturities = [0.5, 1.0]
    strikes = [90, 100, 110]
    
    wrong_shape_vol_matrix = [
        [0.25, 0.25],
        [0.25, 0.25]
        ]
    
    try:
        VolatilitySurface(
            maturities = maturities,
            strikes = strikes,
            vol_matrix = wrong_shape_vol_matrix
            )
    except ValueError:
        print('Passed: invalid vol_matrix shape raises ValueError.')
    else:
        raise AssertionError('Expected ValueError for invalid vol_matrix shape, but no error was raised.')
        


def local_true_vol_smile(tau, strike, spot):
    moneyness = strike/spot
    smile = 0.2 + 0.8* (moneyness - 1.0)**2
    term_structure = 0.05 * np.exp(-tau)
    return smile + term_structure

def synthetic_smile_vol_quotes(
        spot = 100.0,
        rate = 0.04,
        dividend = 0.02
        ):
    
    maturities = np.linspace(0.2, 2.1, 20)
    strikes = np.linspace(81, 120, 20)
    
    bs_engine = BlackScholesEngine()
    quotes = []
    true_vol_matrix = np.zeros(shape = (len(maturities), len(strikes)))
    
    for i, tau in enumerate(maturities):
        for j, strike in enumerate(strikes):
            
            if strike < spot:
                option_type = 'Put'
            else:
                option_type = 'Call'
            
            local_true_vol = local_true_vol_smile(
                tau = float(tau),
                strike = float(strike),
                spot = spot
                )
            
            true_vol_matrix[i, j] = local_true_vol
            
            option = EuropeanOption(
                spot = spot,
                strike = strike,
                tau = tau,
                option_type = option_type
                )
            
            market = MarketData(
                rate = rate,
                dividend = dividend,
                volatility = local_true_vol
                )
            
            market_price = bs_engine.price(option, market)
            
            quotes.append({
                'tau': float(tau),
                'strike': float(strike),
                'option_type': option_type,
                'market_price': float(market_price)
                })
            
    return quotes, maturities, strikes, true_vol_matrix


def test_volatility_smile():
    spot = 100
    rate = 0.04
    dividend = 0.02
    quotes, maturities, strikes, true_vol_matrix = synthetic_smile_vol_quotes(
        spot = spot,
        rate = rate,
        dividend = dividend
        )

    surface = VolatilitySurface.from_option_quotes(
        quotes = quotes,
        spot = spot,
        rate = rate,
        dividend = dividend,
        initial_vol_guess = 0.2
        )
    
    max_error = np.max(abs(surface.vol_matrix - true_vol_matrix))
    
    
    assert np.allclose(surface.maturities, maturities)
    assert np.allclose(surface.strikes, strikes)
    assert surface.vol_matrix.shape == true_vol_matrix.shape
    assert max_error < 1e-6



def test_get_vol_interp_smile_surface():
    spot = 100.0
    
    maturities = [0.5, 1.0]
    strikes = [90, 110]
    true_vol_matrix = np.zeros((len(maturities), len(strikes)))
    
    for i, tau in enumerate(maturities):
        for j, strike in enumerate(strikes):
            true_vol_matrix[i, j] = local_true_vol_smile(
                tau = tau,
                strike = strike,
                spot = spot
                )
    surface = VolatilitySurface(
        maturities = maturities,
        strikes = strikes,
        vol_matrix = true_vol_matrix
        )
    
    vol = surface.get_vol(
        tau = 0.75,
        strike = 100
        )
    
    row_vols = []
    for i in range(len(maturities)):
        row_vol = np.interp(
            100,
            strikes,
            true_vol_matrix[i,:]
            )
        row_vols.append(row_vol)
    
    expected_vol = np.interp(
        0.75,
        maturities,
        row_vols
        )
    
    assert abs(vol - expected_vol) < 1e-12
            

def test_vol_smile_has_atm_minimum():
    spot = 100.0
    tau = 1.0
    
    vol_atm = local_true_vol_smile(tau=tau, strike=100, spot=spot)
    vol_low_strike = local_true_vol_smile(tau = tau, strike = 80.0, spot = spot)
    vol_high_strike = local_true_vol_smile(tau=tau, strike = 120.0, spot = spot)
    
    assert vol_atm < vol_low_strike
    assert vol_atm < vol_high_strike
    assert abs(vol_low_strike - vol_high_strike) < 1e-12


def local_true_vol_skew(tau, strike, spot):
    moneyness = strike / spot
    skew = 0.25 - 0.3 * (moneyness - 1.0)
    term_structure = 0.1 * np.exp(-tau)
    return skew + term_structure


def synthetic_skew_vol_quotes(
        spot = 100.0,
        rate = 0.04,
        dividend = 0.02
        ):
    
    maturities = np.linspace(0.2, 2.1, 20)
    strikes = np.linspace(71, 130, 20)
    
    bs_engine = BlackScholesEngine()
    quotes = []
    true_vol_matrix = np.zeros(shape = (len(maturities), len(strikes)))
    
    for i, tau in enumerate(maturities):
        for j, strike in enumerate(strikes):
            
            if strike < spot:
                option_type = 'Put'
            else:
                option_type = 'Call'
            
            local_true_vol = local_true_vol_skew(
                tau = float(tau),
                strike = float(strike),
                spot = spot
                )
            
            true_vol_matrix[i, j] = local_true_vol
            
            option = EuropeanOption(
                spot = spot,
                strike = strike,
                tau = tau,
                option_type = option_type
                )
            
            market = MarketData(
                rate = rate,
                dividend = dividend,
                volatility = local_true_vol
                )
            
            market_price = bs_engine.price(option, market)
            
            quotes.append({
                'tau': float(tau),
                'strike': float(strike),
                'option_type': option_type,
                'market_price': float(market_price)
                })
            
    return quotes, maturities, strikes, true_vol_matrix




def test_volatility_skew():
    spot = 100
    rate = 0.04
    dividend = 0.02
    quotes, maturities, strikes, true_vol_matrix = synthetic_skew_vol_quotes(
        spot = spot,
        rate = rate,
        dividend = dividend
        )

    surface = VolatilitySurface.from_option_quotes(
        quotes = quotes,
        spot = spot,
        rate = rate,
        dividend = dividend,
        initial_vol_guess = 0.2
        )
    
    max_error = np.max(abs(surface.vol_matrix - true_vol_matrix))
    
    
    assert np.allclose(surface.maturities, maturities)
    assert np.allclose(surface.strikes, strikes)
    assert surface.vol_matrix.shape == true_vol_matrix.shape
    assert max_error < 1e-6



def test_get_vol_interp_skew_surface():
    spot = 100.0
    
    maturities = [0.5, 1.0]
    strikes = [90, 110]
    true_vol_matrix = np.zeros((len(maturities), len(strikes)))
    
    for i, tau in enumerate(maturities):
        for j, strike in enumerate(strikes):
            true_vol_matrix[i, j] = local_true_vol_skew(
                tau = tau,
                strike = strike,
                spot = spot
                )
    surface = VolatilitySurface(
        maturities = maturities,
        strikes = strikes,
        vol_matrix = true_vol_matrix
        )
    
    vol = surface.get_vol(
        tau = 0.75,
        strike = 100
        )
    
    row_vols = []
    for i in range(len(maturities)):
        row_vol = np.interp(
            100,
            strikes,
            true_vol_matrix[i,:]
            )
        row_vols.append(row_vol)
    
    expected_vol = np.interp(
        0.75,
        maturities,
        row_vols
        )
    
    assert abs(vol - expected_vol) < 1e-12
            

def test_vol_skew_has_downward_slope():
    spot = 100.0
    tau = 1.0
    
    vol_atm = local_true_vol_skew(tau=tau, strike=100, spot=spot)
    vol_low_strike = local_true_vol_skew(tau = tau, strike = 80.0, spot = spot)
    vol_high_strike = local_true_vol_skew(tau=tau, strike = 120.0, spot = spot)
    
    assert vol_atm < vol_low_strike
    assert vol_high_strike < vol_atm
    





if __name__ == "__main__":
    test_from_option_quotes_get_vol_surface()
    test_get_vol_at_grid_points()
    test_vol_interpolation()
    test_from_option_quotes_missing_quote_raises_error()
    test_duplicate_quote_raises_error()
    test_invalid_surface_shape_raises_error()
    test_volatility_smile()
    test_get_vol_interp_smile_surface()
    test_vol_smile_has_atm_minimum()
    test_volatility_skew()
    test_get_vol_interp_skew_surface()
    test_vol_skew_has_downward_slope()









