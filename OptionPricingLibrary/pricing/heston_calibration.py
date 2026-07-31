# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 17:43:14 2026

@author: ma6
"""

import numpy as np
from scipy.optimize import minimize

from pricing.products import EuropeanOption
from pricing.market import MarketData
from pricing.heston_params import HestonParams
from pricing.heston_closed_form import HestonClosedFormEngine

class HestonCalibrator:
    def __init__(
            self,
            pricing_engine = None
                 ):
        if pricing_engine is None:
            pricing_engine = HestonClosedFormEngine()
        
        self.pricing_engine = pricing_engine
    
    
    def _params_from_vector(self, x):
        return HestonParams(
            v0 = x[0],
            kappa = x[1],
            theta = x[2],
            xi = x[3],
            rho = x[4]
            )
    
    
    def _objective(self, x, quotes, spot, rate, dividend):
        if len(quotes) == 0:
            raise ValueError('quotes must not be empty.')
        params = self._params_from_vector(x)
        
        total_error = 0.0 
        
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
            
            model_price = self.pricing_engine.price(
                option = option,
                market = market,
                params = params
                )
            
            market_price = quote['market_price']
            
            error = model_price - market_price
            total_error += error**2
        
        return total_error / len(quotes)
    
    
    def calibrate(
            self,
            quotes,
            spot,
            rate,
            dividend,
            initial_guess = None,
            bounds = None
            ):
        if len(quotes) == 0:
            raise ValueError('quotes must not be empty.')
            
        if initial_guess is not None and len(initial_guess) != 5:
            raise ValueError('initial_guess must contain five parameters.')
            
        if initial_guess is None:
            initial_guess = np.array([
                0.25**2, #v0
                2.0, #kappa
                0.25**2, #theta
                0.4, #xi
                -0.7 #rho
                ])
        if bounds is None:
            bounds = [
                (1e-6, 2.0),
                (1e-4, 10.0),
                (1e-6, 2.0),
                (1e-6, 5.0),
                (-0.999, 0.999)
                ]
        result = minimize(
            fun = self._objective,
            x0 = initial_guess,
            args = (quotes, spot, rate, dividend),
            method = "L-BFGS-B",
            bounds = bounds
            )
        
        calibrated_params = self._params_from_vector(result.x)
        return calibrated_params, result
    






