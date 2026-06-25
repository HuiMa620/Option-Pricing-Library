# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 12:32:35 2026

@author: ma6
"""

#pricing/finite_difference.py

import numpy as np

class ExplicitFiniteDifferenceEngine():
    
    def __init__(self, s_max = 300, n_s = 200, n_t = 2*10**4):
        self.s_max = s_max
        self.n_s= n_s
        self.n_t = n_t
        
    def price_loop(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Call':
            V = np.maximum(S_grid - K, 0.0)
        elif option_type == 'Put':
            V = np.maximum(K - S_grid, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        
        #reverse time stepping
        for step in range(self.n_t):
            tau = dt * (step + 1)
            
            V_old = V.copy()
            
            #boundary condition at two sides of S
            if option_type == 'Call':
                V[0] = 0.0
                V[-1] = self.s_max * np.exp(-y*tau) - K*np.exp(-r*tau)
            else:
                V[0] = K*np.exp(-r*tau)
                V[-1] = 0.0
                
            for i in range(1, self.n_s):
                delta = (V_old[i+1] - V_old[i-1])/ (2*dS)
                gamma = (V_old[i+1] - 2*V_old[i] + V_old[i-1]) / (dS**2)
                
                theta_forward = (
                    0.5*sigma**2 * S_grid[i]**2 * gamma
                    + (r - y) * S_grid[i] * delta
                    - r*V_old[i]
                    )
                
                V[i] = V_old[i] + dt * theta_forward
                
            
        price = np.interp(S0, S_grid, V)
            
        return price
    
    
    
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Call':
            V = np.maximum(S_grid - K, 0.0)
        elif option_type == 'Put':
            V = np.maximum(K - S_grid, 0.0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        #reverse time stepping
        i = np.arange(1, self.n_s)
        S_inner = S_grid[i]
        
        for step in range(self.n_t):
            tau = dt * (step + 1)
            V_old = V.copy()
            
            if option_type == 'Call':
                V[0] = 0.0
                V[-1] = self.s_max * np.exp(-y*tau) - K*np.exp(-r*tau)
            else:
                V[0] = K*np.exp(-r*tau)
                V[-1] = 0.0
                
            delta = (V_old[i+1] - V_old[i-1])/ (2*dS)
            gamma = (V_old[i+1] - 2*V_old[i] + V_old[i-1]) / (dS**2)
            theta_forward = (
                0.5*sigma**2 * S_inner**2 * gamma
                + (r - y) * S_grid[i] * delta
                - r*V_old[i]
                )
            V[i] = V_old[i] + dt * theta_forward
        
        
        price = np.interp(S0, S_grid, V)
        return price
        
        
        
        
class ImplicitFiniteDifferenceEngine:
    def __init__(self, s_max = 300.0, n_s= 200, n_t = 500):
        self.s_max = s_max
        self.n_s = n_s
        self.n_t = n_t
        
        
    def price(self, option, market):
        S0 = option.spot
        K = option.strike
        T = option.tau
        option_type = option.option_type
        
        r = market.rate
        y = market.dividend
        sigma = market.volatility
        
        dS = self.s_max / self.n_s
        dt = T / self.n_t
        
        S_grid = np.linspace(0.0, self.s_max, self.n_s + 1)
        
        #boundary condition at tau = 0
        if option_type == 'Call':
            V = np.maximum(S_grid - K, 0)
        elif option_type == 'Put':
            V = np.maximum(K - S_grid, 0)
        else:
            raise ValueError("option_type must be 'Call' or 'Put'.")
            
        #vectorize
        i = np.arange(1, self.n_s)
        S_inner = S_grid[i]
        
        A = 0.5*sigma**2 * S_inner**2
        B = (r - y)*S_inner
        
        lower = - dt*(A/dS **2 - B /(2*dS))
        diag = 1.0 + dt*(2*A/dS**2 + r)
        upper = -dt*(A/dS**2 + B/(2*dS))
        
        #tridiagonal matrix
        M = np.zeros((self.n_s - 1, self.n_s - 1))
        np.fill_diagonal(M, diag)
        np.fill_diagonal(M[1:], lower[1:])
        np.fill_diagonal(M[:,1:], upper[:-1])
        
        for step in range(self.n_t):
            tau = (step + 1) * dt
            
            #boundary condition at the to sides of S
            if option_type == 'Call':
                leftB = 0.0
                rightB = self.s_max * np.exp(-y*tau) - K*np.exp(-r*tau)
            else:
                leftB = K*np.exp(-r*tau)
                rightB = 0.0
                
            rhs = V[1:-1].copy()
            rhs[0] -= lower[0] * leftB
            rhs[-1] -= upper[-1] * rightB
            
            V_inner_new = np.linalg.solve(M, rhs)
            
            V[0] = leftB
            V[-1] = rightB
            V[1:-1] = V_inner_new
            
        price = np.interp(S0, S_grid, V)
        return price
                
        
        
        
        
        
        
        
        
        
        