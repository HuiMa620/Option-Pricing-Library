# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 01:26:53 2026

@author: ma6
"""

import numpy as np
from pricing.products import EuropeanOption
from pricing.heston_params import HestonParams

class HestonMonteCarloEngine:
    
    def __init__(
            self,
            n_paths = 10**5,
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
            
    
    
    def _correlated_normal_random_number_generator(self, params):
        rho = params.rho
        rng = np.random.default_rng(self.seed)
        
        if self.antithetic:
            n_half = self.n_paths // 2
            Z_v_half = rng.standard_normal(
                size = (n_half, self.n_steps)
                )
            Z_ind_half = rng.standard_normal(
                size = (n_half, self.n_steps)
                )
            
            Z_v = np.concatenate(
                [Z_v_half, -Z_v_half],
                axis = 0
                )
            Z_ind = np.concatenate(
                [Z_ind_half, -Z_ind_half],
                axis = 0
                )
            
            if self.n_paths % 2 == 1:
                Z_v_extra = rng.standard_normal(size=(1, self.n_steps))
                Z_ind_extra = rng.standard_normal(size=(1, self.n_steps))

                Z_v = np.concatenate([Z_v, Z_v_extra], axis=0)
                Z_ind = np.concatenate([Z_ind, Z_ind_extra], axis=0)
            
        else:
            Z_v = rng.standard_normal(
                size = (self.n_paths, self.n_steps)
                )
            Z_ind = rng.standard_normal(
                size = (self.n_paths, self.n_steps)
                )
            
        Z_s = rho * Z_v + np.sqrt(1 - rho **2) * Z_ind
        
        return Z_s, Z_v
    
    
    
    def _simulate_paths(self, option, market, params):
        S0 = option.spot
        T = option.tau
        r = market.rate
        y = market.dividend
        
        v0 = params.v0
        kappa = params.kappa
        theta = params.theta
        xi = params.xi
        
        dt = T / self.n_steps
        sqrt_dt = np.sqrt(dt)
        
        Z_s, Z_v = self._correlated_normal_random_number_generator(params)
        actual_n_paths = Z_s.shape[0]
        
        S_paths = np.empty((actual_n_paths, self.n_steps + 1))
        v_paths = np.empty((actual_n_paths, self.n_steps + 1))
        
        S_paths[:, 0] = S0
        v_paths[:, 0] = v0
        
        S = S_paths[:, 0]
        v = v_paths[:, 0]
        
        for step in range(1, self.n_steps + 1):
            v_positive = np.maximum(v, 0.0)
            
            S_next = S * np.exp(
                (r - y - 0.5*v_positive) * dt 
                + np.sqrt(v_positive) * sqrt_dt * Z_s[:, step - 1]
                )
            
            v_next = (
                v + kappa * (theta - v_positive) * dt
                + xi * np.sqrt(v_positive) * sqrt_dt * Z_v[:, step - 1]
                )
            
            S = S_next
            v = np.maximum(v_next, 0.0)
            
            S_paths[:, step] = S
            v_paths[:, step] = v
        
        return S_paths, v_paths
    
    
    
    def _terminal_payoff(self, ST, option):
        K = option.strike
        
        if option.option_type == 'Call':
            return np.maximum(ST - K, 0.0)
        elif option.option_type == 'Put':
            return np.maximum(K - ST, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
        
        
        
    def price_error(self, option, market, params):
        if not isinstance(option, EuropeanOption):
            raise TypeError("option must be a EuropeanOption.")
        
        if not isinstance(params, HestonParams):
            raise TypeError("params must be HestonParams.")
        
        S_paths, v_paths = self._simulate_paths(
            option = option,
            market = market,
            params = params
            )
        
        ST = S_paths[:, -1]
        payoff = self._terminal_payoff(ST = ST, option = option)
        
        discounted_payoff = np.exp(-market.rate * option.tau) * payoff
        price = np.mean(discounted_payoff)
        se = np.std(discounted_payoff, ddof = 1) / np.sqrt(len(discounted_payoff))
        
        return price, se
    
    
    
    def price(self, option, market, params):
        price, _ = self.price_error(
            option = option, 
            market = market, 
            params = params
            )
        return price
        


    
    
    
            
        
        
    