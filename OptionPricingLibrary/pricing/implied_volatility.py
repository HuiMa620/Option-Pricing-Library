# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 02:12:38 2026

@author: ma6
"""

from pricing.black_scholes import BlackScholesEngine
from dataclasses import replace

class ImpliedVolatilitySolver:
    
    def __init__(self, low_vol = 1e-6, high_vol = 5, tolerance = 1e-8, max_iterations = 200):
        self.low_vol = low_vol
        self.high_vol = high_vol
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        
    def bisection_solve(self, option, market, market_price):
        bs_engine = BlackScholesEngine()
        low_vol = self.low_vol
        high_vol = self.high_vol
        low_price = bs_engine.price(
            option,
            replace(
                market,
                volatility = low_vol)
            )
        high_price = bs_engine.price(
            option,
            replace(
                market,
                volatility = high_vol
                )
            )
        
        if market_price < low_price or market_price > high_price:
            raise ValueError("Market price is out of price range implied by the volatility bounds.")
        
        for i in range(self.max_iterations):
            mid_vol = 0.5*(low_vol + high_vol)
            
            model_price = bs_engine.price(
                option,
                replace(
                    market,
                    volatility = mid_vol
                    )
                )
            
            if abs(model_price - market_price) < self.tolerance:
                return mid_vol
            if model_price > market_price:
                high_vol = mid_vol
            else:
                low_vol = mid_vol
                
        return mid_vol
    
    
    def newton_solve(self, option, market, market_price, initial_guess = 0.2):
        sigma = initial_guess
        bs_engine= BlackScholesEngine()
        
        for _ in range(self.max_iterations):
            current_market = replace(
                market,
                volatility = sigma
                )
            model_price = bs_engine.price(option, current_market)
            vega = bs_engine.Vega(option, current_market)
            
            error = model_price - market_price
            if abs(error) < self.tolerance:
                return sigma
            
            if abs(vega) < 1e-10:
                raise ValueError("Vega is too small for Newton method.")
            
            sigma = sigma - error/vega
            
            if sigma <= 0:
                raise ValueError("Newton method produces non-positive volatility.")
                
        return sigma
        
        
    def solve(self, option, market, market_price, initial_guess = 0.2):
        if initial_guess < self.low_vol or initial_guess > self.high_vol:
            return self.bisection_solve(option, market, market_price)
        
        sigma = initial_guess
        bs_engine= BlackScholesEngine()
        
        for _ in range(self.max_iterations):
            current_market = replace(
                market,
                volatility = sigma
                )
            model_price = bs_engine.price(option, current_market)
            vega = bs_engine.Vega(option, current_market)
            
            error = model_price - market_price
            if abs(error) < self.tolerance:
                return sigma
            
            if abs(vega) < 1e-10:
                return self.bisection_solve(option, market, market_price)
            
            new_sigma = sigma - error/vega
            
            if new_sigma <= 0:
                return self.bisection_solve(option, market, market_price)
                
            if new_sigma < self.low_vol or new_sigma > self.high_vol:
                return self.bisection_solve(option, market, market_price)
            
            sigma = new_sigma
                
        return self.bisection_solve(option, market, market_price)
        
            
            
            
        
        
        
    
        