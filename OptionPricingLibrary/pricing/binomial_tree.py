# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 00:15:06 2026

@author: ma6
"""

import numpy as np

class BinomialTreeEngine():
    
    def __init__(self, n_steps = 500, exercise ='European'):
        self.n_steps = n_steps
        self.exercise = exercise
        
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        n = self.n_steps
        dt = T/n
        
        u = np.exp(sigma*np.sqrt(dt))
        d = 1.0/u
        
        discount = np.exp(-r*dt)
        p = (np.exp((r - y) * dt) - d) / (u - d)
        
        if p < 0 or p > 1.0:
            raise ValueError(
                "Risk-neutral probablity is outside [0, 1]"
                "Try increasing n_steps or checking input parameters"
                )
        
        #Stock prices at maturity
        j = np.arange(n+1)
        S_T = S0*(u**j) * (d**(n-j))
        
        #payoff at maturity
        if option_type == 'Call':
            V = np.maximum(S_T - K, 0.0)
        elif option_type == 'Put':
            V = np.maximum(K - S_T, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
        
        #Backward induction
        for step in range(n-1, -1, -1):
            V = discount * (p * V[1:] + (1.0 - p) * V[:-1])
            
            if self.exercise == 'American':
                j = np.arange(step + 1)
                S = S0*(u**j)*(d**(step-j))
                
                if option_type == 'Call':
                    exercise_value = np.maximum(S - K, 0.0)
                else:
                    exercise_value = np.maximum(K - S, 0.0)
                
                V = np.maximum(V, exercise_value)
            elif self.exercise == 'European':
                pass
            else:
                raise ValueError("exercise must be 'European' or 'American'.")
        
        return V[0]
        
        
        
        
    