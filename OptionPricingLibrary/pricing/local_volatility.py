# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:34:46 2026

@author: ma6
"""

import numpy as np
from pricing.products import EuropeanOption

class LocalVolatilitySurface:
    def __init__(
            self, 
            base_vol = 0.2,
            skew_strength = 0.3, 
            term_strength = 0.05, 
            reference_spot = 100.0
            ):
        
        self.base_vol = base_vol
        self.skew_strength = skew_strength
        self.term_strength = term_strength
        self.reference_spot = reference_spot
        
        self._validate_inputs()
        
    def _validate_inputs(self):
        if self.base_vol <= 0:
            raise ValueError("base_vol must be positive.")
        
        if self.skew_strength < 0:
            raise ValueError("skew_strength must be non-negative.")
        
        if self.term_strength < 0:
            raise ValueError("term_strength must be non-negative.")
            
        if self.reference_spot <= 0:
            raise ValueError("reference_spot must be positive.")
            
            
        

    
    def local_vol_function(self, t, spot):
        spot = np.asarray(spot, dtype = float)
        
        moneyness = spot / self.reference_spot
        
        skew_component = self.skew_strength * np.maximum(1.0 - moneyness, 0.0)
        term_component = self.term_strength * np.exp(-t)
        
        sigma = self.base_vol + skew_component + term_component
        
        sigma = np.clip(sigma, 0.05, 1.00)
        
        return sigma
    

    
    
    def get_vol(self, t, spot):
        sigma = self.local_vol_function(t, spot)
        
        sigma = np.asarray(sigma, dtype = float)
        
        if np.any(sigma <= 0):
            raise ValueError("sigma must be positive.")
            
        return sigma
    
    
    
    
    
class LocalVolatilityMonteCarloEngine:
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
    
    
    def _simulate_paths(self, option, market, local_vol_surface):
        S0 = option.spot
        T = option.tau
        r = market.rate
        y = market.dividend
        
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
        
        for step in range(1, self.n_steps+1):
            current_time = (step - 1) * dt
            current_spot = S_paths[:, step - 1]
            
            local_sigma = local_vol_surface.get_vol(
                t = current_time,
                spot = current_spot
                )
            
            drift = (r - y - 0.5*local_sigma**2)*dt
            diffusion = local_sigma * np.sqrt(dt) * Z[:, step - 1]
            
            S_paths[:, step] = current_spot * np.exp(drift + diffusion)
        
        return S_paths
    
    
    def _terminal_payoff(self, ST, option):
        K = option.strike
        
        if option.option_type == 'Call':
            payoff = np.maximum(ST - K, 0.0)
        elif option.option_type == 'Put':
            payoff = np.maximum(K - ST, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
        
        return payoff
    
    
    def price_error(self, option, market, local_vol_surface):
        if not isinstance(option, EuropeanOption):
            raise TypeError('option must be a EuropeanOption.')
            
        if not isinstance(local_vol_surface, LocalVolatilitySurface):
            raise TypeError("local_vol_surface must be a LocalVolatilitySurface.")
        
        S_paths = self._simulate_paths(
            option = option,
            market = market,
            local_vol_surface = local_vol_surface
            )
        
        ST = S_paths[:, -1]
        
        payoff = self._terminal_payoff(
            ST = ST,
            option = option
            )
        
        discounted_payoff = np.exp(-market.rate * option.tau) * payoff
        
        price = np.mean(discounted_payoff)
        
        standard_error = (
            np.std(discounted_payoff, ddof = 1) / np.sqrt(len(discounted_payoff))
            )
        
        return price, standard_error
    
    
    def price(self, option, market, local_vol_surface):
        price, _ = self.price_error(
            option = option,
            market = market,
            local_vol_surface = local_vol_surface
            )
        return price
        
        
            
    


