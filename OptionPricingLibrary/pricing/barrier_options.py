# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 21:12:32 2026

@author: ma6
"""

import numpy as np
from pricing.products import BarrierOption
            
class BarrierMonteCarloEngine:
    def __init__(
            self,
            n_paths = 10**6,
            n_steps = 252,
            seed = 1,
            antithetic = True
            ):
        
        self.n_paths = n_paths
        self.n_steps = n_steps
        self.seed = seed
        self.antithetic = antithetic
        
        self._validate_inputs()
        
        
        
    def _validate_inputs(self):
        if not isinstance(self.n_paths, int):
            raise ValueError("n_paths must be an integer.")
        
        if not isinstance(self.n_steps, int):
            raise ValueError("n_steps must be an integer.")
        
        if self.n_paths <= 0:
            raise ValueError("n_paths must be positive.")
            
        if self.n_steps <= 0:
            raise ValueError("n_steps must be positive.")
        
    
    
    def price_error(self, option, market):
        '''
        Price a knock-out barrier option and return price and standard error.
        '''
        
        if not isinstance(option, BarrierOption):
            raise TypeError('option must be a BarrierOption.')
        
        S_paths = self._simulate_paths(option = option, market = market)
        
        knocked_out = self._check_knock_out(
            S_paths = S_paths,
            option = option
            )
        
        ST = S_paths[:, -1]
        
        vanilla_payoff = self._terminal_payoff(
            ST = ST,
            option = option
            )
        
        payoff = np.where(
            knocked_out,
            0.0,
            vanilla_payoff
            )
        
        discounted_payoff = np.exp(-market.rate * option.tau) * payoff
        
        price = np.mean(discounted_payoff)
        standard_error = (
            np.std(discounted_payoff, ddof = 1) / np.sqrt(len(discounted_payoff))
            )
        
        return price, standard_error
    
    
    
    def price(self, option, market):
        price, _ = self.price_error(
            option = option,
            market = market
            )
        return price
    
    
    
    def _simulate_paths(self, option, market):
        S0 = option.spot
        T = option.tau
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        if sigma < 0:
            raise ValueError("market.volatility must be positive.")
        
        dt = T / self.n_steps
        rng = np.random.default_rng(self.seed)
        
        if self.antithetic:
            n_half = self.n_paths // 2
            Z_half = rng.standard_normal(
                size = (n_half, self.n_steps)
                )
            
            Z = np.concatenate(
                [Z_half, -Z_half],
                axis = 0
                )
            
            if self.n_paths % 2 == 1:
                Z_extra = rng.standard_normal(
                    size = (1, self.n_steps)
                    )
                
                Z = np.concatenate(
                    [Z, Z_extra],
                    axis = 0
                    )
        else:
            Z = rng.standard_normal(
                size = (self.n_paths, self.n_steps)
                )
        actual_n_paths = Z.shape[0]
        
        S_paths = np.empty(
            shape=(actual_n_paths, self.n_steps + 1),
            dtype = float
            )
        
        S_paths[:, 0] = S0
        
        drift = (r - y - 0.5*sigma**2)*dt
        diffusion_scale = sigma*np.sqrt(dt)
        
        for step in range(1, self.n_steps+1):
            S_paths[:, step] = (
                S_paths[:, step - 1] * np.exp(drift + diffusion_scale * Z[:, step - 1])
                )
        
        return S_paths
    
    
    
    def _check_knock_out(self, S_paths, option):
        if option.barrier_type == 'Down':
            knocked_out = np.any(
                S_paths <= option.barrier,
                axis = 1
                )
        elif option.barrier_type == 'Up':
            knocked_out = np.any(
                S_paths >= option.barrier, axis = 1
                )
        else:
            raise ValueError("barrier_type must be 'Down' or 'Up'.")
        
        return knocked_out # knocked_out = np.array([False, True, False...])
    
    
    
    def _terminal_payoff(self, ST, option):
        '''
        compute vanila terminal payoff before applying barrier condition
        '''
        
        K = option.strike
        
        if option.option_type == 'Call':
            payoff = np.maximum(ST - K, 0.0)
        elif option.option_type == 'Put':
            payoff = np.maximum(K - ST, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
        
        return payoff
            
            
        
        
        
        
        
        
