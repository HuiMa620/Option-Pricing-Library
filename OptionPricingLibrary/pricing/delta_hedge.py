# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 18:20:35 2026

@author: ma6
"""

import numpy as np
from pricing.black_scholes import BlackScholesEngine
from dataclasses import replace
from scipy.stats import norm

class DeltaHedgingSimulator:
    def __init__(self, n_steps = 252, n_paths = 10**4, seed = 10):
        self.n_steps = n_steps
        self.n_paths = n_paths
        self.seed = seed
        
    def simulate_one_path(self, option, market, realized_volatility):
        if option.option_type != 'Call':
            raise ValueError("First version must be Call option.")
        
        rng = np.random.default_rng(self.seed)
        S0 = option.spot
        K = option.strike
        T = option.tau
        
        r = market.rate
        y = market.dividend
        
        dt = T / self.n_steps
        S = S0
        bs_engine = BlackScholesEngine()
        
        initial_price = bs_engine.price(option, market)
        initial_delta = bs_engine.Delta(option, market)
        
        stock_position = initial_delta
        cash_position = initial_price - initial_delta*S0
        
        for steps in range(1, self.n_steps + 1):
            cash_position = cash_position * np.exp(r*dt)
            cash_position += stock_position * S * (np.exp(y * dt) - 1.0)
            Z = rng.standard_normal()
            S = S * np.exp((r - y - 0.5*realized_volatility**2)*dt + realized_volatility * np.sqrt(dt)* Z)
            tau = T - steps*dt
            if tau > 0:
                updated_option = replace(
                    option,
                    spot=S,
                    tau=tau
                    )
                new_delta = bs_engine.Delta(updated_option, market)
                shares_to_buy = new_delta- stock_position
                cash_position -= shares_to_buy * S
                stock_position = new_delta
            
        payoff = np.maximum(S - K, 0)
        pnl = cash_position + stock_position*S - payoff
        
        return pnl
    
    
    
    
    def simulate(self, option, market, realized_volatility):
        if option.option_type not in ['Call', 'Put']:
            raise ValueError("option_type must be Call or Put option.")
            
        rng = np.random.default_rng(self.seed)
        S0 = option.spot
        K = option.strike
        T = option.tau
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dt = T / self.n_steps
        S = S0*np.ones(self.n_paths)
        bs_engine = BlackScholesEngine()
            
        initial_price = bs_engine.price(option, market)
        initial_delta = bs_engine.Delta(option, market)
        shares_to_buy = np.zeros(self.n_paths)
        
        stock_position = initial_delta
        cash_position = initial_price - initial_delta*S0
            
        for steps in range(1, self.n_steps + 1):
            cash_position = cash_position * np.exp(r*dt)
            cash_position += stock_position * S * (np.exp(y * dt) - 1.0)
            
            Z = rng.standard_normal(self.n_paths)
            S = S * np.exp((r - y - 0.5*realized_volatility**2)*dt + realized_volatility * np.sqrt(dt)* Z)
            
            tau = T - steps*dt
            if tau>0:
                d1 = (np.log(S/K) + (r - y + sigma**2/2)*tau)/(sigma * np.sqrt(tau))
                if option.option_type == 'Call':
                    new_delta = np.exp(-y*tau) * norm.cdf(d1)
                elif option.option_type == 'Put':
                    new_delta = np.exp(-y * tau) * (norm.cdf(d1) - 1.0)
                shares_to_buy = new_delta - stock_position
                cash_position -= shares_to_buy * S
                stock_position = new_delta
        
        if option.option_type == 'Call':
            payoff = np.maximum(S - K, 0.0)
        else:
            payoff = np.maximum(K - S, 0.0)
        pnl = cash_position + stock_position*S - payoff
        
        return pnl
            
                        
                        
                        
                
                
                
                
            
            
        
        
        
        