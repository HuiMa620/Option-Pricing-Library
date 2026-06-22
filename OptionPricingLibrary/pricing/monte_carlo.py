# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 00:18:44 2026

@author: ma6
"""

#pricing/monte_carlo.py

import numpy as np


class MonteCarloEngine():
    def __init__(self, n_paths = 5*10**6, seed = 1, antithetic=True):
        self.n_paths = n_paths
        self.seed = seed
        self.antithetic = antithetic
    
    
    
    def price_error(self, option, market):
        S = option.spot
        K = option.strike
        tau = option.tau
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        rng = np.random.default_rng(self.seed)
        
        if self.antithetic:
            n_half = self.n_paths //2
            Z_half = rng.standard_normal(n_half)
            Z = np.concatenate([Z_half, -Z_half])
        else:
            Z = rng.standard_normal(self.n_paths)
            
        ST = S * np.exp(
            (r - y - 0.5*sigma**2) * tau + sigma * np.sqrt(tau)*Z
            )
        
        if option.option_type == 'Call':
            payoff = np.maximum(ST-K, 0)
        elif option.option_type == 'Put':
            payoff = np.maximum(K-ST, 0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'")
        
        discounted_payoff = np.exp(-r*tau) * payoff
        
        price = np.mean(discounted_payoff)
        standard_error = np.std(discounted_payoff, ddof=1) / np.sqrt(len(discounted_payoff))
        
        return price, standard_error
    
    
    def price(self, option, market):
        price, _ = self.price_error(option, market)
        return price
        




