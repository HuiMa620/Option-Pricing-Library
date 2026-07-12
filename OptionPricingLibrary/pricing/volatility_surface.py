# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 23:37:56 2026

@author: ma6
"""

import numpy as np
from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.implied_volatility import ImpliedVolatilitySolver

class VolatilitySurface:
    '''
    build volatility surface from market option data
    option data -> volatility
    
    rows -> maturities
    columns -> strikes
    vol_matrix[i,j] = implied volatility at
                      maturity = maturities[i]
                      strike = strikes[j]
    
    '''
    
    def __init__(self, maturities, strikes, vol_matrix):
        self.maturities = np.asarray(maturities, dtype = float)
        self.strikes = np.asarray(strikes, dtype = float)
        self.vol_matrix = np.asarray(vol_matrix, dtype = float)
        
        self._validate_surface()
        
    def _validate_surface(self):
        #validate maturities, strikes, and volatility matrix
        
        if self.maturities.ndim != 1:
            raise ValueError("maturities must be a one-dimensional array.")
        
        if self.strikes.ndim != 1:
            raise ValueError("strikes must be a one-dimensioanl array.")
            
        if np.any(self.maturities <= 0):
            raise ValueError("All maturities must be positive.")
            
        if np.any(self.strikes <= 0):
            raise ValueError("All strikes must be positive.")
            
        if not np.all(np.diff(self.maturities) > 0):
            raise ValueError("maturities must be strictly increasing.")
            
        if not np.all(np.diff(self.strikes) > 0):
            raise ValueError("strikes must be strictly increasing.")
            
        expected_shape = (len(self.maturities), len(self.strikes))
        
        if self.vol_matrix.shape != expected_shape:
            raise ValueError(
                "vol_matrix must be "
                f"{expected_shape}, but got {self.vol_matrix.shape}"
                )
        
        if np.any(np.isnan(self.vol_matrix)):
            raise ValueError("vol_matrix contains missing values.")
            
        if np.any(self.vol_matrix <= 0):
            raise ValueError("All implied volatilities must be positive.")
            
  
    
    @classmethod
    def from_option_quotes(
            cls,
            quotes,
            spot,
            rate,
            dividend,
            initial_vol_guess = 0.2,
            iv_solver = None
            ):
        
        '''
        build volatility surface form market option quotes
        
        quotes:
            {
                'tau': 0.5.
                'strike': 100
                'option_type': 'Call',
                'market_price': 7.0
                }
        '''
        
        if len(quotes) == 0:
            raise ValueError("quotes cannot be empty.")
            
        if spot <= 0:
            raise ValueError('spot must be positive.')
            
        maturities = sorted(set(float(q['tau']) for q in quotes))
        strikes = sorted(set(float(q['strike']) for q in quotes))
        
        n_maturities = len(maturities)
        n_strikes = len(strikes)
        
        vol_matrix = np.full(
            shape=(n_maturities, n_strikes),
            fill_value = np.nan,
            dtype = float
            )
        
        maturity_to_index = {
            maturity: i
            for i, maturity in enumerate(maturities)
            }
        
        strike_to_index = {
            strike: j
            for j, strike in enumerate(strikes)
            }
        
        if iv_solver is None:
            iv_solver = ImpliedVolatilitySolver()
            
        for quote in quotes:
            tau = float(quote['tau'])
            strike = float(quote['strike'])
            option_type = quote['option_type']
            market_price = float(quote['market_price'])
            
            if tau <= 0:
                raise ValueError('Quote maturity must be positive.')
            
            if strike <= 0:
                raise ValueError('Quote strike must be positive.')
                
            if market_price <= 0:
                raise ValueError("Quote market_price must be positive.")
                
            if option_type not in ['Call', 'Put']:
                raise ValueError("option_type must be 'Call' or 'Put'")
                
            option = EuropeanOption(
                spot = spot,
                strike = strike,
                tau = tau,
                option_type = option_type
                )
            
            market = MarketData(
                rate = rate,
                dividend = dividend,
                volatility = initial_vol_guess
                )
            
            implied_vol = iv_solver.solve(
                option = option,
                market = market,
                market_price = market_price,
                initial_guess = initial_vol_guess
                )
            
            i = maturity_to_index[tau]
            j = strike_to_index[strike]
            
            if not np.isnan(vol_matrix[i, j]):
                raise ValueError(
                    "Duplicate quote found for"
                    f"tau={tau}, strike={strike}"
                    )
                
            vol_matrix[i, j] = implied_vol
            
        if np.any(np.isnan(vol_matrix)):
            raise ValueError(
                "Missing quote detected."
                "First version requires a complete rectangular grid."
                )
        
        return cls(
            maturities = maturities,
            strikes = strikes,
            vol_matrix = vol_matrix
            )
    
    
    
    def get_vol(self, tau, strike):
        '''
        Get implied volatility for a given maturity and strike.
        Check the volatility surface or interp.
        '''
        
        tau = float(tau)
        strike = float(strike)
        
        if tau <= 0:
            raise ValueError("tau must be positive.")
            
        if strike <= 0:
            raise ValueError("strike must be positive.")
            
        vols_at_each_maturity = np.array([
            np.interp(strike, self.strikes, self.vol_matrix[i,:])
            for i in range(len(self.maturities))
            ])
        
        interpolated_vol = np.interp(
            tau,
            self.maturities,
            vols_at_each_maturity
            )
        return float(interpolated_vol)

            
            
        
        
        
        
        
